// src/App.js
import React from 'react';
import './App.css';
import {ChakraProvider} from '@chakra-ui/react';
import Header from './components/Header';
import Verify from './components/Verify';
import Upload from './components/Upload';

function App() {
    return (
    <ChakraProvider>
      <Header/>
      <Upload/>
      <Verify/>
    </ChakraProvider>
    );
}
export default App;
