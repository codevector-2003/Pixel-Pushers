import React, { useEffect, useState } from "react";
import "./vaccine.css";
import bgimg from '../../Pages/Vaccine/Vaccineimg/Rectangle3467956.png';
import Navbar from '../../Components/Navbar.jsx';
import searchimg from '../growthpage/growthpageimg/search.png';
import bellimg from '../growthpage/growthpageimg/bell1.png';
import axios from "axios";
import { useParams } from "react-router-dom";


const Vaccine = () => {
  const [vaccines, setVaccines] = useState([]);
  const { baby_id } = useParams(); 
  
  const token = localStorage.getItem("token");
        if (!token) {
          console.error("Access Token not found. Please try again.");
          return;
        }

  useEffect(() => {
    const fetchVaccines = async () => {
      try {

        const response = await axios.get(`http://127.0.0.1:8078/babies/${baby_id}/vaccines/`, {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
        });
        setVaccines(response.data);
      } catch (err) {
        console.error("Error fetching vaccines:", err);
      }
    };

    fetchVaccines();
  }, [baby_id]);

  const handleCheckboxChange = async (vaccineId, currentStatus) => {
    if (currentStatus) return; // Already given, do nothing

    const today = new Date().toISOString().split("T")[0];

    try {
      const response = await axios.put(
        `/babies/${baby_id}/vaccines/${vaccineId}/mark?given_date=${today}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log("Vaccine response:", response.data);
      // Update state with newly marked vaccine
      setVaccines((prev) =>
        prev.map((v) =>
          v.id === vaccineId ? { ...v, given: true, given_date: today } : v
        )
      );
    } catch (err) {
      console.error("Error marking vaccine:", err);
    }
  };

  return (
    <div className="vaccine-container" style={{ '--bg-image': `url(${bgimg})` }}>
      <title>Vaccine</title>
      <div className="navbar">
        <Navbar />
      </div>

      <div className="content">
        <div className="growthpage__header">
          <div className="search-bar">
            <div className="search-icon">
              <img src={searchimg} alt="search" />
            </div>
            <input type="text" placeholder="Search..." />
          </div>
          <div className="notification-icon">
            <button className="notification-button"></button>
            <img src={bellimg} className="bellimage" alt="bell" />
          </div>
        </div>

        <div className="table-container">
          <table className="vaccine-table">
            <thead>
              <tr>
                <th>STATUS</th>
                <th>VACCINE NAME</th>
                <th>GIVEN DATE</th>
                <th>NOTES</th>
              </tr>
            </thead>
            <tbody>
              {vaccines.map((vaccine) => (
                <tr
                  key={vaccine.id}
                  className={!vaccine.given && new Date(vaccine.standard_date) < new Date() ? "overdue" : ""}
                >
                  <td>
                    {vaccine.given ? (
                      <input type="checkbox" checked readOnly />
                    ) : (
                      <input
                        type="checkbox"
                        onChange={() => handleCheckboxChange(vaccine.id, vaccine.given)}
                      />
                    )}
                  </td>
                  <td className={!vaccine.given ? "red-text" : ""}>{vaccine.name}</td>
                  <td className={!vaccine.given ? "red-text" : ""}>
                    {vaccine.given ? vaccine.given_date : "Pending"}
                  </td>
                  <td>{vaccine.notes || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Vaccine;
