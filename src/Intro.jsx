import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./Intro.css";
import image0 from "./assets/image0.png";
import image1 from "./assets/image1.png";

const images = [image0, image1];

const Intro = () => {
  const [index, setIndex] = useState(0);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="intro-container">
      {/* Sliding Images */}
      <div
        className="intro-slider"
        style={{ transform: `translateX(-${index * 100}%)` }}
      >
        {images.map((img, i) => (
          <img key={i} src={img} alt={`Slide ${i}`} className="intro-slide" />
        ))}
      </div>

      {/* Signup & Login Buttons */}
      <div className="introButtons">
        <button onClick={()=>navigate("/Signup")}>Sign Up</button>
        <button onClick={() => navigate("/login")}>Login</button>
      </div>
    </div>
  );
};

export default Intro;
