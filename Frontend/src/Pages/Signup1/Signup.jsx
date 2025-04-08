import React, { useState } from "react";
import "./Signup.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import bgImage from "../../Pages/Signup1/Signupimg/Rectangle3467956.png";
import babyIcon from "../../Pages/Signup1/Signupimg/baby1.png";

const Signup = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [full_name, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://52.140.41.112:8080/signup", {
        email,
        full_name,
        username,
        password,
      },
        {
          headers: {
            "Content-Type": "application/json",
          },
        });
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);

      }



      console.log("Signup successful:", response.data);
      navigate("/signupnext");

    } catch (error) {
      console.error("Signup error:", error);

      if (error.response) {
        setErrorMsg(error.response.data.detail || "Signup failed. Try again.");
      } else if (error.request) {
        setErrorMsg("No response from server. Please try again.");
      } else {
        setErrorMsg("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div className="signup-container" style={{ '--bg-image': `url(${bgImage})` }}>
      <div className="signup-content">
        <div className="left-section">
          <div className="icon">
            <img src={babyIcon} alt="baby icon" />
          </div>
          <h1 className="black-text">
            Sign up for <br />
            <span className="bold">smartBaby</span>
            <sup>LK</sup>
          </h1>
          <p className="description">
            You're one step closer to your child's very own smart baby-book!
          </p>
        </div>

        <div className="right-section">
          <div className="signup-box">
            <h2 className="label">Full Name</h2>
            <p className="info-text">
              The name of the baby
            </p>
            <input
              type="text"
              placeholder="First Last"
              className="input-field"
              value={full_name}
              onChange={(e) => setFullName(e.target.value)}
            />

            <h2 className="label">Email</h2>
            <input
              type="email"
              placeholder="you@mail.com"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <h2 className="label">Username</h2>
            <input
              type="text"
              placeholder="first_last"
              className="input-field"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

            <h2 className="label">Password</h2>
            <p className="info-text">
              Must include an uppercase letter and a number. Don’t forget your password!
            </p>
            <div className="password-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                className="password-input"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>

            {errorMsg && <p className="error-text">{errorMsg}</p>}
            <button className="next-button" onClick={handleSignup}>Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
