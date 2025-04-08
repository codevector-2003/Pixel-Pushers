import React, { useState } from "react";
import "./landingpg.css";
import babyimg from "./landingpgimg/Group 2610411.png";
import { FaGoogle, FaApple } from "react-icons/fa";
import bgImage from './landingpgimg/Frame26080345.png';
import { useNavigate } from "react-router-dom";
import axios from "axios"; // Make sure to install this via `npm install axios`

const LoginPage = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async () => {
        try {
            const response = await axios.post(
                "http://52.140.41.112:8080/token",
                new URLSearchParams({
                    username: username,
                    password: password,
                }),
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );

            const token = response.data.access_token;
            localStorage.setItem("token", token);

            if (response.data.baby_id) {
                localStorage.setItem("baby_id", response.data.baby_id);
            }

            navigate("/dashboard"); // Redirect on success
        } catch (err) {
            setError("Invalid username or password");
            console.error(err);
        }
    };

    return (
        <div className="landing-page" style={{ '--bg-image': `url(${bgImage})` }}>
            <title>Login</title>
            <div className="container">
                <div className="left-section">
                    <h2 className="title">Sign in to use</h2>
                    <h3 className="subtitle">smartbaby<span className="small-text">LK</span></h3>
                    <p className="info-text">Don't have an account? <span className="link" onClick={() => navigate('/signup')}>create an account</span></p>
                    <p className="info-subtext">It takes less than a minute!</p>

                    <div className="form-container">
                        <input
                            type='str'
                            placeholder="Username"
                            className="Input-field"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type='password'
                            placeholder="Password"
                            className="Input-field"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <a href="#" className="forgot-password">Forgot password?</a>
                        {error && <p className="error-text">{error}</p>}
                        <button className="sign-in-btn" onClick={handleLogin}>Sign in</button>
                        <button className="social-btn google-btn"><FaGoogle /> Sign in with Google</button>
                        <button className="social-btn apple-btn"><FaApple /> Sign in with Apple ID</button>
                    </div>
                </div>
                <div className="right-section">
                    <img src={babyimg} alt="baby illustration" className="illustration" />
                </div>
            </div>
        </div>
    );
}

export default LoginPage;
