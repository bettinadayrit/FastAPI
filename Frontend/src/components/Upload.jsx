import React from "react";
import {Heading, Button, Text, Box, SimpleGrid} from "@chakra-ui/react";
import { useState } from 'react';
import { CheckIcon, WarningTwoIcon } from "@chakra-ui/icons";

function FileForm(){
    const [file, setFile] = useState(null); // for chosen file to upload
    const [uploadStatus, setUploadStatus] = useState(''); // for the upload status

    const handleFileInputChange = (event) => {
        setFile(event.target.files[0]) // when the file input changes, it sets the variable 'file' to the current file loaded in the UI
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!file) {
            setUploadStatus('error'); // if walang file then the user submits, it will return an error
          }

        const formData= new FormData(); // used to handle data from forms and allows you to send data thru fetch requests 
        formData.append('files', file); // adds the file to the 'files' variable declared in the endpoint (fastapi)

         try { // attempts to send the formData to the specified endpoint using a POST request
            const endpoint= "http://localhost:8000/upload-image/"
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData,
            });

            if (response.ok) { // if successful, 
              setUploadStatus('success');
          } else {
              setUploadStatus('error');
          }

         } catch(error){
            setUploadStatus('error'); // if not successful, the upload status is set to error
         }
    }

    return (
      <>
      <SimpleGrid
      m={2}
      p={4}
      rounded='md'
      columns={{ sm: 2, md: 2 }}>

      <Box 
      m={4} 
      p={4} 
      rounded='md'>
        <Heading
          as="h1"
          size="lg"
          fontWeight="bold"
          m={2}
          color= "pink.200">
          Welcome ･ᴗ･
        </Heading>
        <Text mt={1} fontSizesize={32} textAlign='justify'>
          This web application is a simple face recognition and liveness check. In here, there are three sections to navigate to: upload, verification, and results. 
          Uploading the image to be used is a prerequisite to the verification process, however, if the image to be used for verification is already uploaded to the database,
          one may skip uploading the file. 

          <br></br><br></br> ౨ৎ ˙⋆.˚ ᡣ𐭩  
        </Text>
      </Box>

      <Box
      borderWidth="2px"
      m={8}
      p={3}
      rounded='lg'
      alignItems='center'
      display= 'flex'
      justifyContent='center'>
      <div align="center">
        <Heading 
        as="h3" 
        size= "md"
        fontWeight='bold'
        m={1}>
        Upload File to the Database (.jpg/.jpeg/.png)
        </Heading>
            <form onSubmit={handleSubmit}> 
                <input type= "file" onChange={handleFileInputChange} accept="image/jpeg, image/png"/>
                <Button
                type ="submit"
                color="#B57294"
                title ="Upload Picture"
                variant="solid">
                Upload Picture
                </Button>

              {uploadStatus === 'success' && (
              <Text color="green.500" mt={2}>
                <CheckIcon m={2} />
                File uploaded successfully
              </Text>
              )}

              {uploadStatus === 'error' && (
              <Text color="red.500" mt={2} >
                <WarningTwoIcon m={2} />
                Failed to upload file
              </Text>
              )}
            </form>
      </div>
      </Box>
      
      </SimpleGrid>
      </>
    )
}
export default FileForm