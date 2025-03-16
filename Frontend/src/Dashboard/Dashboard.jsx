import React,{useState} from "react";
import Navbar from "../Navbar/Navbar.jsx"
import './Dashboard.css'


const Dashboard=()=>{

    const [Theme,setTheme]=useState('light');
    return(
        <>
        <div className={`container ${Theme}`}>
        <Navbar Theme={Theme} setTheme={setTheme}></Navbar>
        </div>
        
        </>
    );
}
export default Dashboard;