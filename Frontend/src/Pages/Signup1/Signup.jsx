import React, { useState } from "react";
import "./Signup.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import axios from "axios"; // Don't forget: npm install axios
import { useNavigate } from "react-router-dom";
import bgImage from "../../Pages/Signup1/Signupimg/Rectangle3467956.png"; // Adjust the path as necessary
import babyIcon from "../../Pages/Signup1/Signupimg/baby1.png"; // Adjust the path as necessary

const Signup = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [full_name, setFullName] = useState("");
  const [guardian_name, setGuardianName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    
    try {
      const response = await axios.post("http://127.0.0.1:8078/signup", {
        email,
        full_name,
        guardian_name,
        username,
        password,
      });

      // If we get here, the request was successful
      console.log("Signup successful:", response.data);
      navigate("/signupnext"); // Change to your desired route
      
    } catch (error) {
      console.error("Signup error:", error);
      
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setErrorMsg(error.response.data.detail || "Signup failed. Try again.");
      } else if (error.request) {
        // The request was made but no response was received
        setErrorMsg("No response from server. Please try again.");
      } else {
        // Something happened in setting up the request that triggered an Error
        setErrorMsg("Something went wrong. Please try again.");
      }
    }
  };


  return (
    <div className="signup-container" style={{ '--bg-image': `url(${bgImage})` }}>
      <div className="signup-content">
        {/* Left Section */}
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

        {/* Right Section */}
        <div className="right-section">
          <div className="signup-box">
            <h2 className="label">Guardian’s Name</h2>
            <p className="info-text">
              The name of whoever will be taking care of the baby, ideally the mother. This is YOUR name, not your baby’s.
            </p>
            <input
              type="text"
              placeholder="First Last"
              className="input-field"
              value={guardianName}
              onChange={(e) => setGuardianName(e.target.value)}
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
