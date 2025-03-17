import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./Navbar.css";
import logo_dark from "./images/logo-white.png";
import logo_light from "./images/logo-black.png";
import search_icon_light from "./images/search-w.png";
import search_icon_dark from "./images/search-b.png";
import toggle_light from "./images/night.png";
import toggle_dark from "./images/day.png";

const Navbar = ({ Theme, setTheme }) => {
    const navigate = useNavigate(); // Initialize useNavigate

    const toggle_mode = () => {
        setTheme(Theme === "light" ? "dark" : "light");
    };

    return (
        <div className="navbar">
            <img src={Theme === "light" ? logo_light : logo_dark} alt="Logo" className="logo" />
            <ul>
                <li onClick={() => navigate("/")}>Home</li>
                <li onClick={() => navigate("/products")}>Products</li>
                <li onClick={() => navigate("/forum")}>Forum</li>
                <li onClick={() => navigate("/nutrition")}>Nutrition</li>
                <li onClick={() => navigate("/vaccination")}>Vaccination</li>
                <li onClick={() => navigate("/Milestones")}>Milestones</li>
            </ul>

            <div className="search-box">
                <input type="text" placeholder="Search Here" />
                <img src={Theme === "light" ? search_icon_light : search_icon_dark} alt="Search Icon" />
            </div>

            {/* Toggle Icon Changes Based on Theme */}
            <img
                onClick={toggle_mode}
                src={Theme === "light" ? toggle_light : toggle_dark}
                alt="Toggle Mode"
                className="toggle-icon"
            />
        </div>
    );
};

export default Navbar;
