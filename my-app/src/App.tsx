import React from 'react';
import './App.css';
import Home from "./page/home"
import { AppBar, Container, Toolbar, Typography } from '@mui/material';
import logo from './logo.png';

function App() {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", width: "100vw"}}>
      <div style={{ backgroundColor:"#D9DFEF"}}>
        {/* <Typography align="center" variant='h3'>eMosh</Typography> */}
        <img src={logo} style={{ height: "150px", display: "block", margin: "auto"}}></img>
      </div>
      <Home />

      <div style={{ width: "100%", backgroundColor:"#D9DFEF", alignSelf:"flex-end"}}>
        <Typography style={{ color: "#99AAB5", margin: "1.5% 0"}} fontWeight="400" align="center">Developed by John Chan, Kodai Hiraishi,Tanishk Sharma, and Sam Su Zhou💻</Typography>
      </div>
    </div>
  );
}

export default App;
