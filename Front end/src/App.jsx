import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Intro from "./Intro.jsx";
import Login from "./Loginpage.jsx";
import Signup from "./Signuppage.jsx";

const App = () => {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/login" element={<Login />} />
        <Route path="/Signup" element={<Signup/>}/>
      </Routes>
    </Router>
  );
};

export default App;