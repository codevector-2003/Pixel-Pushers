import React, { useState } from "react";
import "./Record.css";
import Navbar from "../../Components/Navbar.jsx";
import bgimg from '../Milestones/Milestoneimg/Frame26080346.png';
import searchimg from '../growthpage/growthpageimg/search.png';
import bellimg from '../growthpage/growthpageimg/bell1.png';
import {
  FaSmile,
  FaLanguage,
  FaBrain,
  FaRunning,
  FaBell,
  FaSearch,
  FaClipboard,
  FaPaperPlane,
  FaTimes
} from "react-icons/fa";

const Record = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [date, setDate] = useState('');
  const [description, setDescription] = useState('');

  const openModal = (category) => {
    setSelectedCategory(category);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setDate('');
    setDescription('');
  };

  const handleSubmit = () => {
    const payload = {
      category: selectedCategory,
      date,
      description,
    };
    console.log("Submitting:", payload);
    // TODO: POST to backend
    closeModal();
  };

  return (
    <div className="record-container" style={{ '--bg-image': `url(${bgimg})` }}>
      <div className="navbar">
        <Navbar />
      </div>

      <div className="record-content">
        <div className="growthpage__header">
          <div className="search-bar">
            <div className="search-icon">
              <FaSearch />
            </div>
            <input type="text" placeholder="Search..." />
          </div>
          <div className="notification-icon">
            <button className="notification-button">
              <FaBell />
            </button>
          </div>
        </div>

        <div className="left-content">
          <div className="table-container">
            <table className="records-table">
              <thead>
                <tr>
                  <th>MILESTONES</th>
                  <th>DATE</th>
                  <th>CATEGORY</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>Lifts head briefly</td><td>88/88/8888</td><td>Emotional</td></tr>
                <tr><td>Smiles socially</td><td>88/88/8888</td><td>Cognitive</td></tr>
                <tr><td>Crawls</td><td>88/88/8888</td><td>Movement</td></tr>
                <tr><td>Babbles sounds</td><td>88/88/8888</td><td>Language</td></tr>
                <tr><td>Sits unsupported</td><td>88/88/8888</td><td>Language</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="right-content">
          <div className="add-new-section">
            <h3>Add New</h3>
            <p>Select a milestone category to add a new record.</p>
            <div className="milestone-cards">
              <div className="milestone-card" onClick={() => openModal('Emotional')}>
                <FaSmile size={28} />
                <span>Emotional</span>
              </div>
              <div className="milestone-card" onClick={() => openModal('Language')}>
                <FaLanguage size={28} />
                <span>Language</span>
              </div>
              <div className="milestone-card" onClick={() => openModal('Cognitive')}>
                <FaBrain size={28} />
                <span>Cognitive</span>
              </div>
              <div className="milestone-card" onClick={() => openModal('Movement')}>
                <FaRunning size={28} />
                <span>Movement</span>
              </div>
            </div>
          </div>

          <div className="doctors-note-section">
            <div className="note-header">
              <h3><FaClipboard style={{ marginRight: "8px" }} />Doctor’s Notes</h3>
            </div>
            <blockquote>
              <strong>“Might have ADHD”</strong><br />
              Since child consistently shows delayed attention span, impulsivity,
              hyperactivity, speech delays, difficulty following instructions, and
              trouble with emotional regulation, he may be at risk for ADHD.
            </blockquote>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-box">
            <h3><FaClipboard /> {selectedCategory} Milestone</h3>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              placeholder="Enter date"
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter milestone description"
              rows="4"
            />
            <div className="modal-actions">
              <button onClick={handleSubmit}>
                <FaPaperPlane /> Submit
              </button>
              <button onClick={closeModal}>
                <FaTimes /> Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Record;
