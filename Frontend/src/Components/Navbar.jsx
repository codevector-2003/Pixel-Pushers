import React from "react";
import './Navbar.css';
import { useNavigate } from "react-router-dom";
import chaticon from './Navbarimg/chaticon.png';
import docicon from './Navbarimg/docicon.png';
import homeicon from './Navbarimg/Homeicon.png';
import settingsicon from './Navbarimg/settingsicon.png';
import logo from './Navbarimg/unknown.png';

const Navbar = () => {
    const navigate = useNavigate();
    return (
        <div className="navbox">
            <div className="profile2" onClick={() => navigate('/')}>
                <img src={logo} alt="Logo" className="logo" />
            </div>

            <div className="chat-button" onClick={() => navigate('/chatbot')}>
                <img src={chaticon} alt="Chat Icon" className="chat-icon" />
            </div>
            <div className="doc-button" onClick={() => navigate('/vaccine')} >
                <img src={docicon} alt="Document Icon" className="doc-icon" />
            </div>
            <div className="home-button" onClick={() => navigate('/dashboard')}>
                <img src={homeicon} alt="Home Icon" className="home-icon" />
            </div>
            <div className="settings-button">
                <img src={settingsicon} alt="Settings Icon" className="settings-icon" />
            </div>
        </div>
    );
}
export default Navbar;