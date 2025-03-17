import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./loginpage.css";
import { FaUser, FaLock } from "react-icons/fa";

const LoginRegister = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [passwordStrength, setPasswordStrength] = useState("");
    const [authError, setAuthError] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const [error, setError] = useState("");
    const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup

    // Validate username
    const validateUsername = (username) => {
        if (username.length < 8) return "Username must be at least 8 characters long";
        return "";
    };

    // Validate password and set password strength
    const validatePassword = (password) => {
        let strength = "Weak";
        if (password.length >= 8) {
            if (/[a-z]/.test(password) && /[A-Z]/.test(password) && /[^a-zA-Z0-9]/.test(password)) {
                strength = "Strong";
            } else if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
                strength = "Medium";
            }
        }

        setPasswordStrength(strength);

        if (password.length < 8) return "Password must be at least 8 characters long";
        if (!/[a-z]/.test(password)) return "Password must contain at least one lowercase letter";
        if (!/[A-Z]/.test(password)) return "Password must contain at least one uppercase letter";
        if (!/[^a-zA-Z0-9]/.test(password)) return "Password must contain at least one special character";
        return "";
    };

    // Validate confirm password
    const validateConfirmPassword = (confirmPassword) => {
        if (confirmPassword !== password) return "Passwords do not match";
        return "";
    };

    // Handle login form submission
    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const response = await axios.post(
                "http://127.0.0.1:8078/login",
                { username, password },
                { headers: { "Content-Type": "application/json" } }
            );

            if (response.status === 200) {
                if (rememberMe) {
                    localStorage.setItem("user", JSON.stringify({ username }));
                }
                navigate("/dashboard"); // Redirect to dashboard
            }
        } catch (error) {
            setError(error.response?.data?.message || "Login failed. Please try again.");
        }
    };

    // Handle signup form submission
    const handleSignup = async (e) => {
        e.preventDefault();
        setAuthError("");

        const newErrors = {
            username: validateUsername(username),
            password: validatePassword(password),
            confirm_password: validateConfirmPassword(confirmPassword),
        };

        setErrors(newErrors);

        if (!newErrors.username && !newErrors.password && !newErrors.confirm_password) {
            try {
                const response = await axios.post(
                    "http://127.0.0.1:8078/signup",
                    { username, password },
                    { headers: { "Content-Type": "application/json" } }
                );

                setAuthError(response.data.message);
                setTimeout(() => setIsLogin(true), 2000); // Switch to login form after successful signup
            } catch (error) {
                setAuthError(error.response?.data?.detail || "Signup failed. Please try again.");
            }
        } else {
            setAuthError("Please fix the errors before proceeding.");
        }
    };

    return (
        <div className="wrapper">
            <div className={`form-box ${isLogin ? "login" : "signup"}`}>
                <form onSubmit={isLogin ? handleLogin : handleSignup}>
                    <h1>{isLogin ? "Login" : "Sign Up"}</h1>

                    {/* Display error messages */}
                    {error && <p className="error-message">{error}</p>}
                    {authError && <p className="error-message">{authError}</p>}

                    {/* Username Input */}
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

                    {/* Password Input */}
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

                    {/* Confirm Password Input (Only for Signup) */}
                    {!isLogin && (
                        <div className="input-box">
                            <input
                                type="password"
                                placeholder="Confirm Password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                            />
                            <FaLock className="icon" />
                        </div>
                    )}

                    {/* Remember Me (Only for Login) */}
                    {isLogin && (
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
                    )}

                    {/* Submit Button */}
                    <button type="submit">{isLogin ? "Login" : "Sign Up"}</button>

                    {/* Toggle between Login and Signup */}
                    <div className="register-link">
                        <p>
                            {isLogin ? "Don't have an account? " : "Already have an account? "}
                            <span onClick={() => setIsLogin(!isLogin)}>
                                {isLogin ? "Register" : "Login"}
                            </span>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginRegister;