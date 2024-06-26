import cv2
import dlib
import math
import secrets
import time
import os
from deepface import DeepFace

# --- thresholds, set based on obsereved values from calculations
BLINK_RATIO_THRESHOLD = 5 
HEAD_TURN_ANGLE_THRESHOLD = 10
HEAD_TILT_ANGLE_THRESHOLD_up = 17
HEAD_TILT_ANGLE_THRESHOLD_down = 25

class ActionConstants:
    BLINK = "Blink"
    TURN_RIGHT = "Turn right"
    TURN_LEFT = "Turn left"
    LOOK_UP = "Look up"
    LOOK_DOWN = "Look down"
    actions = [BLINK, TURN_RIGHT, TURN_LEFT, LOOK_UP, LOOK_DOWN]

verification_result_storage = {"result": "Pending"} # initial value of verification result

def midpoint(point1 ,point2): # formula
    return (point1.x + point2.x)/2,(point1.y + point2.y)/2

def euclidean_distance(point1 , point2): # formula
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_blink_ratio(eye_points, facial_landmarks): # projects eye landmarks points to live feed -> then gets its values
    corner_left  = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y) 
    corner_right = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4])) 
    
    horizontal_length = euclidean_distance(corner_left,corner_right) # expected to not change 
    vertical_length = euclidean_distance(center_top,center_bottom) # changes accordingly when blinking (decreases in value)
    ratio = horizontal_length / vertical_length # higher ratio = blink, ave 3-4 (value) = not blinking 
    return ratio 

def get_head_turn_angle(facial_landmarks):
    nose_tip = (facial_landmarks.part(30).x, facial_landmarks.part(30).y)
    left_cheek = (facial_landmarks.part(1).x, facial_landmarks.part(1).y)
    right_cheek = (facial_landmarks.part(15).x, facial_landmarks.part(15).y)

    delta_x = right_cheek[0] - left_cheek[0] # horizontal distance, constant -> according to the user's face
    horizontal_midpoint = midpoint(facial_landmarks.part(1), facial_landmarks.part(15)) # decreases when head is turned right, increases when head is turned left
    nose_midpoint_delta_x = nose_tip[0] - horizontal_midpoint[0] # decreases when head is turned right (by a lot, negative val), increases when head is turned left
    angle = math.degrees(math.atan2(nose_midpoint_delta_x, delta_x)) 
    return angle

def get_head_tilt_angle(facial_landmarks):
    nose_tip = (facial_landmarks.part(30).x, facial_landmarks.part(30).y)
    nose_bridge = (facial_landmarks.part(27).x, facial_landmarks.part(27).y)
    delta_y = nose_tip[1] - nose_bridge[1]  # Vertical distance between nose bridge and nose tip
    
    left_eye = (facial_landmarks.part(36).x, facial_landmarks.part(36).y)
    right_eye = (facial_landmarks.part(45).x, facial_landmarks.part(45).y)
    eye_distance = euclidean_distance(left_eye, right_eye)
    normalized_delta_y = delta_y / eye_distance # decreases when head is titled upwards, increases when head is titled down
    angle = math.degrees(math.atan2(normalized_delta_y, 1))
    return angle

def get_random_action():
    return secrets.choice(ActionConstants.actions)

def check_action(action, blink_ratio, head_turn_angle, head_tilt_angle):
    if action == ActionConstants.BLINK and blink_ratio > BLINK_RATIO_THRESHOLD:
        return True
    elif action == ActionConstants.TURN_RIGHT and head_turn_angle < -HEAD_TURN_ANGLE_THRESHOLD:
        return True
    elif action == ActionConstants.TURN_LEFT and head_turn_angle > HEAD_TURN_ANGLE_THRESHOLD:
        return True
    elif action == ActionConstants.LOOK_UP and head_tilt_angle < HEAD_TILT_ANGLE_THRESHOLD_up:
        return True
    elif action == ActionConstants.LOOK_DOWN and head_tilt_angle > HEAD_TILT_ANGLE_THRESHOLD_down:
        return True
    return False

def liveness_check(user_input):
    cap = cv2.VideoCapture(0)
    global verification_result_storage

    detector = dlib.get_frontal_face_detector() 
    predictor = dlib.shape_predictor("/Users/bettinadayrit/FastAPI/shape_predictor_68_face_landmarks.dat") # loads a pre-trained facial landmarks predictor model
    left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
    right_eye_landmarks = [42, 43, 44, 45, 46, 47]

    current_action = get_random_action()
    actions_completed = 0
    total_actions_required = 5

    os.makedirs("./Autocaptures/", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
             break 

        faces = detector(image = frame)
        for face in faces:
            landmarks = predictor(frame, face) # gets the facial landmarks for the face in the live stream

            left_eye_ratio  = get_blink_ratio(left_eye_landmarks, landmarks) 
            right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
            blink_ratio = (left_eye_ratio + right_eye_ratio)/2
            head_turn_angle = get_head_turn_angle(landmarks)
            head_tilt_angle = get_head_tilt_angle(landmarks)

            if actions_completed < total_actions_required:
                cv2.putText(frame, f"Please perform the action: {current_action}", (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
                if check_action(current_action, blink_ratio, head_turn_angle, head_tilt_angle):
                    actions_completed += 1
                    if actions_completed <= total_actions_required:
                        current_action = get_random_action()
            else:
                cv2.putText(frame, "Face detected.", (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                faces = DeepFace.extract_faces(img_path = frame, detector_backend='yolov8', enforce_detection=False)
                x = []
                y = []
                w = []
                h = []
                for face in faces:
                    x.append(face['facial_area']['x'])
                    y.append(face['facial_area']['y'])
                    w.append(face['facial_area']['w'])
                    h.append(face['facial_area']['h'])
                for i in range(len(faces)):
                    cv2.rectangle(frame, (x[i], y[i]), (x[i] + w[i], y[i] + h[i]) , (0,255,0), 2)

                    if blink_ratio < BLINK_RATIO_THRESHOLD and 0 < head_turn_angle < 3 and 19 < head_tilt_angle < 23: #ensures that the face is facing the camera directly 
                        timestamp = int(time.time())
                        detected_face = f"./Autocaptures/detectedface-{timestamp}.jpg"
                        success = cv2.imwrite(detected_face, frame)
                        if success:
                            cap.release()
                            result = DeepFace.verify(
                                img1_path=detected_face,
                                img2_path=f"/Users/bettinadayrit/FastAPI/Backend/src/Database/{user_input}",
                                enforce_detection=False
                            )
                            verification_result_storage["result"] = "Success, Face verified: match!" if result['verified'] else "Failure, Face not verified: not a match!"
                    else:
                        pass

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') 
    cap.release()
    cv2.destroyAllWindows()