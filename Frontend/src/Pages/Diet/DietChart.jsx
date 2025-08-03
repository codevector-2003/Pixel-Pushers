import React, { useState, useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import {
  FaClipboard,
  FaPlus,
  FaSearch,
  FaBell,
  FaEdit,
} from "react-icons/fa";
import Navbar from "../../Components/Navbar.jsx";
import "./DietChart.css";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];

function DietChart() {
  const baby_id = localStorage.getItem("baby_id");

  const [dietData, setDietData] = useState([]);
  const [kcal, setKcal] = useState(0);
  const [note, setNote] = useState('');
  const [foodTags, setFoodTags] = useState([]);
  const [allergies, setAllergies] = useState([]);
  const [tableRows, setTableRows] = useState([]);

  useEffect(() => {
    // Fetch diet data
    fetch(`https://your-api.com/api/diet/${baby_id}`)
      .then(res => res.json())
      .then(data => {
        setDietData(data.macros);
        setKcal(data.kcal);
        setNote(data.note);
        setFoodTags(data.foods);
        setAllergies(data.allergies);
        setTableRows(data.table); // assuming server returns full table
      })
      .catch(err => console.error("Failed to fetch diet data:", err));
  }, [baby_id]);

  return (
    <div className="page-wrapper">
      <div className="navbar">
        <Navbar />
      </div>

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

      <div className="diet-chart-container">
        <div className="left-panel">
          <h2>Diet Chart</h2>

          <div className="dietchart-header-icons">
            <button className="icon-button" title="Add">
              <FaPlus />
            </button>
            <button className="icon-button" title="Edit">
              <FaEdit />
            </button>
          </div>

          <h3 className="kcal-title-left">{kcal} Kcal</h3>

          <div className="paragraph-chart-row">
            <p className="kcal-note">{note}</p>

            <div className="pie-chart-wrapper">
              <PieChart width={250} height={250}>
                <Pie
                  data={dietData}
                  dataKey="value"
                  outerRadius={80}
                  label
                  fill="#8884d8"
                >
                  {dietData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>
          </div>

          <table className="diet-table">
            <thead>
              <tr>
                <th></th>
                <th>Food</th>
                <th>Amount</th>
                <th>Nutrient</th>
                <th>Calories</th>
              </tr>
            </thead>
            <tbody>
              {tableRows.map((item, i) => (
                <tr key={i}>
                  <td>
                    <span
                      style={{
                        display: "inline-block",
                        width: "12px",
                        height: "12px",
                        borderRadius: "50%",
                        backgroundColor: COLORS[i % COLORS.length],
                        marginRight: "8px",
                      }}
                    ></span>
                  </td>
                  <td>{item.food}</td>
                  <td>{item.amount}</td>
                  <td>{item.nutrient}</td>
                  <td>{item.calories} Kcal</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="right-panel">
          <div className="new-diet-section">
            <h2>Create New Diet</h2>
            <p>
              Add a new diet chart setup to create a new healthy diet based on foods you have access to, and design your body’s eating trace.
            </p>

            <div className="tags-section">
              <label>Foods</label>
              <div className="tags-row">
                {foodTags.map((food, idx) => (
                  <span key={idx}>{food}</span>
                ))}
              </div>
              <button className="add-button"><FaPlus /> Add</button>
            </div>

            <div className="tags-section">
              <label>Allergies</label>
              <div className="tags-row">
                {allergies.map((allergy, idx) => (
                  <span key={idx}>{allergy}</span>
                ))}
              </div>
              <button className="add-button"><FaPlus /> Add</button>
            </div>
          </div>

          <div className="doctors-note-section">
            <h3><FaClipboard /> Doctor’s Notes</h3>
            <blockquote>“Add more sugar!”</blockquote>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DietChart;
