import React from 'react';
import {render} from 'react-dom';
import {ChakraProvider} from '@chakra-ui/react';

import Header from './components/Header';
import Verify from './components/Verify';
import Upload from './components/Upload';

function App(){
  return(
    <ChakraProvider>
      <Header/>
      <Upload/>
      <Verify/>
    </ChakraProvider>
  )
}

const rootElement = document.getElementById ("root")
render(<App/>, rootElement)