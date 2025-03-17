import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Loginpage.css";
import image2 from '../assets/image2.png';

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Please enter both username and password.");
      return;
    }

    try {
      // Send a POST request to the backend
      const response = await fetch("http://127.0.0.1:8078/login", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      // Check if the response is OK (status code 200-299)
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Login failed!");
      }

      // If login is successful
      const data = await response.json();
      alert(data.message); // Show success message
      navigate("/dashboard"); // Redirect to the dashboard
    } catch (error) {
      setError(error.message); // Show error message
    }
  };

  return (
    <div>
      <div className="login">
        <div className="backImage" style={{ backgroundImage: `url(${image2})` }}>
        </div>
        <div className="login-container">
          <h1>Login</h1>
          <p>Welcome back! Please enter your details to log in.</p>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="login-input"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />

          {error && <p className="error-message">{error}</p>}

          <button onClick={handleLogin} className="login-button">
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;