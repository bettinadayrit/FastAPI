import React from 'react';
import {render} from 'react-dom';
import App from './App.jsx';

function Test (){
  return(
    <App/>
  )
}

const rootElement = document.getElementById ("root")
render(<App/>, rootElement)