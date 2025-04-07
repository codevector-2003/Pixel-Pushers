import React, { useState, useRef } from "react";
import "./Signupnext.css";
import { FaCalendarAlt } from "react-icons/fa";
import bgImage from '../../Pages/Signupnext/Signupnextimg/backgroundimg.png';
import babyimg from '../../Pages/Signupnext/Signupnextimg/baby1.png';
import axios from 'axios'; //  npm install axios
import { useNavigate } from "react-router-dom";

const Signupnext = () => {
  const [Gurdian_name, setGurdianName] = useState("");
  const [gender, setSex] = useState(null);
  const [preterm, setPreterm] = useState(null);
  const [blood_Type, setBloodType] = useState("");
  const [birth_date, setBirthday] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const birthdayRef = useRef(null);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!Gurdian_name || !gender || !birth_date || !blood_Type || !preterm) {
      setErrorMsg("Please fill out all fields.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setErrorMsg("Access Token not found. Please try again.");
        return;
      }

      const response = await axios.post("http://127.0.0.1:8078/babies", {
        Gurdian_name,
        birth_date,
        gender,
        blood_Type,
        preterm
      }, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
      });

      console.log("Backend response:", response.data);

      if (response.status === 200 || response.status === 201) {
        navigate("/");
      } else {
        setErrorMsg(response.data.message || "Submission failed. Try again.");
      }
    } catch (error) {
      console.error("Error submitting baby info:", error);
      setErrorMsg("Something went wrong. Try again.");
    }

  };

  return (
    <div className="signup-container updated-container" style={{ '--bg-image': `url(${bgImage})` }}>
      <div className="signup-content">
        {/* Left Section */}
        <div className="left-section">
          <div className="icon">
            <img src={babyimg} alt="baby" />
          </div>
          <h1 className="black-text">
            Sign up for <br />
            <span className="bold">smartBaby</span>
            <sup>LK</sup>
          </h1>
          <p className="description">
            Tell us more about your precious baby. Your baby book will be ready in an instant!
          </p>
        </div>

        {/* Right Section */}
        <div className="right-section new-box-style">
          <div className="signup-box">
            <h2 className="label">Guardian's Full Name</h2>
            <input
              type="text"
              placeholder="Guardian's Full Name"
              className="input-field"
              value={Gurdian_name}
              onChange={(e) => setGurdianName(e.target.value)}
            />

            <h2 className="label">Gender</h2>
            <div className="toggle-buttons">
              <button className={`toggle-button ${gender === "male" ? "active" : ""}`} onClick={() => setSex("male")}>Male</button>
              <button className={`toggle-button ${gender === "female" ? "active" : ""}`} onClick={() => setSex("female")}>Female</button>
            </div>

            <h2 className="label">Birthday</h2>
            <div className="date-picker-wrapper">
              <input
                type="date"
                ref={birthdayRef}
                value={birth_date}
                onChange={(e) => setBirthday(e.target.value)}
                className="input-field date-input"
              />
            </div>

            <h2 className="label">Blood Type</h2>
            <select
              className="drop-down"
              value={blood_Type}
              onChange={(e) => setBloodType(e.target.value)}
            >
              <option value="" disabled>Select Blood Type</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
            </select>

            <h2 className="label">Preterm?</h2>
            <div className="toggle-buttons">
              <button className={`toggle-button ${preterm === "true" ? "active" : ""}`} onClick={() => setPreterm("true")}>Yes</button>
              <button className={`toggle-button ${preterm === "false" ? "active" : ""}`} onClick={() => setPreterm("false")}>No</button>
            </div>

            {errorMsg && <p className="error-text">{errorMsg}</p>}
            <button className="next-button" onClick={handleSubmit}>Finish</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signupnext;
