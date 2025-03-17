import React, { useState, useEffect } from "react";
import Navbar from "../Navbar/Navbar.jsx";
import "./Dashboard.css";

const Dashboard = () => {
    const [theme, setTheme] = useState("light");
    const [username, setUsername] = useState("");
    const [currentDate, setCurrentDate] = useState("");

    // Fetch the username from localStorage and set the current date
    useEffect(() => {
        const storedUsername = localStorage.getItem("username");
        if (storedUsername) {
            setUsername(storedUsername);
        }

        // Format the current date in the desired format: "Day, Date Month Year"
        const date = new Date();
        const formattedDate = date.toLocaleString('en-US', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
        setCurrentDate(formattedDate);
    }, []);

    return (
        <>
            <div className={`container ${theme}`}>
                <Navbar theme={theme} setTheme={setTheme} username={username} />
                <h1>Welcome, {username ? username : "Guest"} 👋</h1>
                <p>Today is {currentDate}</p>
            </div>
        </>
    );
};

export default Dashboard;