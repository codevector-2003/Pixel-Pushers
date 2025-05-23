import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './Pages/landing page/landingpg.jsx'
import Dashboard from './Pages/Dashboard/dashboard.jsx';
import Growthpage from './Pages/growthpage/growthpage.jsx';
import Signup from './Pages/Signup1/Signup.jsx';
import Signupnext from './Pages/Signupnext/Signupnext.jsx';
import Vaccine from './Pages/Vaccine/vaccine.jsx';
import Milestones from './Pages/Milestones/Record.jsx';
import Chatbot from './Pages/chatbot/chatbot.jsx';

import './App.css'

function App() {


  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/growthpage" element={<Growthpage />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/signupnext" element={<Signupnext />} />
        <Route path="/vaccine" element={<Vaccine />} />
        <Route path="/milestones" element={<Milestones />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </Router>
  )
}

export default App
