import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Loginpage.css"; 
import image2 from './assets/image2.png'

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!username || !password) {
      setError("Please enter both username and password.");
      return;
    }

    if (username === "admin" && password === "1234") {
      alert("Login successful!");
      navigate("/dashboard");
    } else {
      setError("Invalid username or password.");
    }
  };

  return (
    <div>
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
  );
};

export default Login;
