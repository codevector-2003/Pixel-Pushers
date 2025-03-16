import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Intro from "./Homepage/Intro.jsx";
import Login from "./pages/Loginpage.jsx";
import Signup from "./pages/Signuppage.jsx";
import Dashboard from "./Dashboard/dashboard.jsx"

const App = () => {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/login" element={<Login />} />
        <Route path="/Signup" element={<Signup/>}/>
        <Route path="/Dashboard" element={<Dashboard/>}/>
      </Routes>
    </Router>
  );Route
};

export default App;