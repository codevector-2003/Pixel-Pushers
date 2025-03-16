import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom"; // Import Link here
import "./loginpage.css";
import { FaUser, FaLock } from "react-icons/fa";

const LoginRegister = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = (e) => {
        e.preventDefault();

        // Dummy authentication logic (Replace with API call later)
        if (username === "admin" && password === "password123") {
            console.log("Login Successful!");
            if (rememberMe) {
                localStorage.setItem("user", JSON.stringify({ username }));
            }
            navigate("/dashboard"); // Redirect to dashboard
        } else {
            setError("Invalid username or password!");
        }
    };

    return (
        <div className="wrapper">
            <div className="form-box login">
                <form onSubmit={handleLogin}>
                    <h1>Login</h1>

                    {error && <p className="error-message">{error}</p>}

                    <div className="input-box">
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                        <FaUser className="icon" />
                    </div>

                    <div className="input-box">
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <FaLock className="icon" />
                    </div>

                    <div className="remember-forgot">
                        <label>
                            <input
                                type="checkbox"
                                checked={rememberMe}
                                onChange={() => setRememberMe(!rememberMe)}
                            />
                            Remember Me
                        </label>
                        <a href="#">Forgot password?</a>
                    </div>

                    <button type="submit">Login</button>

                    <div className="register-link">
                        <p>
                            Don't have an account?
                            <Link to='/signup'>Register</Link> {/* Updated Link path */}
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginRegister;
