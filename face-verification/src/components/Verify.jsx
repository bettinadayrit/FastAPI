import React, { useState, useRef, useEffect } from 'react';
import { Heading, Button, Text, Box, Spinner, Alert, AlertIcon } from "@chakra-ui/react";

function useInterval(callback, delay) { // function for delays and to allow continuous checking for verficiation results. 
    const savedCallback = useRef();
    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);

    useEffect(() => {
        function tick() {
            savedCallback.current();
        }

        if (delay !== null) {
            const id = setInterval(tick, delay);
            return () => clearInterval(id);
        }
    }, [delay]);
}

function MyForm() {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [showStream, setShowStream] = useState(false);
    const [streamUrl, setStreamUrl] = useState('');
    const [verificationResult, setVerificationResult] = useState('Pending');
    const [isProcessing, setIsProcessing] = useState(false);

    const handleFileInputChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!file) { // if no file selected, return error 
            setUploadStatus('error');
            return;
        }

        const filename = file.name;
        setIsProcessing(true);
        setUploadStatus('');
        
        try {
            const endpoint = `http://localhost:8000/face-verification/?user_input=${encodeURIComponent(filename)}`;
            const response = await fetch(endpoint, {
                method: "GET",
            });

            if (response.ok) {
                setStreamUrl(endpoint);
                setShowStream(true);
                setUploadStatus('success');
                fetchVerificationResult();
            } else {
                setUploadStatus('error');
            }
        } catch (error) {
            setUploadStatus('error');
        } finally {
            setIsProcessing(false);
        }
    };

    const fetchVerificationResult = async () => {
        try {
            const response = await fetch("http://localhost:8000/verification-result");
            if (response.ok) {
                const result = await response.json();
                setVerificationResult(result.result);
            } else {
                console.error("Failed to fetch verification result");
            }
        } catch (error) {
            console.error("Error fetching verification result:", error);
        }
    };

    useInterval(() => {
        if (showStream) {
            fetchVerificationResult();
        }
    }, 5000);

    return (
        <> 
            <Box 
            borderWidth="2px" 
            m={4} 
            p={4} 
            rounded='md' 
            alignSelf="center">

                <div align="center">
                    <Heading as="h2" size="md" fontWeight="bold" m={1}>
                        Face Verification and Liveness Check
                    </Heading>
                    <Heading as="h3" size="sm" fontStyle="italic" fontWeight="normal" m={1}>
                        Select File from Database for Verification
                    </Heading>
                    <input type="file" onChange={handleFileInputChange} accept="image/jpeg, image/png" />
                    <form onSubmit={handleSubmit}>
                        <Button 
                            type="submit" 
                            colorScheme="pink" 
                            variant="solid" 
                            m={3}
                            isDisabled={isProcessing}>
                            Start Verification
                        </Button>
                    </form>

                    {isProcessing && <Spinner size="lg" />}

                    {uploadStatus === 'success' && (
                        <Alert status="success" mt={3} justifyContent='center' display='flex' borderRadius="md">
                            <AlertIcon />
                            File selected successfully. Please follow instructions on live stream.
                        </Alert>
                    )}

                    {uploadStatus === 'error' && (
                        <Alert status="error" mt={3} justifyContent='center' display='flex' borderRadius="md">
                            <AlertIcon />
                            Failed to start live stream.
                        </Alert>
                    )}
                    
                    <br></br>
                    {showStream && (
                    <div align="center">
                    <img
                        src= {streamUrl}
                        alt="Live Stream"
                        style={{ width: 1280, height: 720 }}
                        borderRadius="md" />
                     </div>
                    )}  

                </div>   
            </Box>

            <Box 
            borderWidth="2px" 
            m={4} 
            p={4} r
            ounded='md'>
                <div align="center">
                    {verificationResult && (
                        <div>
                            <Heading as="h3" size="sm" fontWeight="normal" fontStyle='italic'>
                                Verification result:
                            </Heading>
                            <Text fontSize={24} fontWeight="bold">
                                {verificationResult}
                            </Text>
                        </div>
                    )}
                </div>
            </Box>
        </>
    );
}

export default MyForm;