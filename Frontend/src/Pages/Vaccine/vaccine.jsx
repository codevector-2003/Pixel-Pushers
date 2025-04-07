import React from "react";
import "./vaccine.css";
import bgimg from '../../Pages/Vaccine/Vaccineimg/Rectangle3467956.png';
import Navbar from '../../Components/Navbar.jsx';
import searchimg from '../growthpage/growthpageimg/search.png';
import bellimg from '../growthpage/growthpageimg/bell1.png';

const Vaccine = () => {
  
  name
  standard_date
  notes
  given: bool
  given_date
  
  
  
  
  
  
  
  
  return (
    <div className="vaccine-container" style={{ '--bg-image': `url(${bgimg})` }} >
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
                <th>DATE</th>
                <th>BATCH NUMBER</th>
                <th>NOTES</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><input type="checkbox" /></td>
                <td>Hepatitis B</td>
                <td>Pending</td>
                <td>123456</td>
                <td>-</td>
              </tr>
              <tr>
                <td><input type="checkbox" /></td>
                <td>Rotavirus</td>
                <td>Pending</td>
                <td>123456</td>
                <td>-</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>COVID-19 Vaccine</td>
                <td>2023-01-15</td>
                <td>123456</td>
                <td>First dose</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>Influenza Vaccine</td>
                <td>2023-10-05</td>
                <td>123456</td>
                <td>Annual flu shot</td>
              </tr>
              <tr className="overdue">
                <td><span className="icon">!</span></td>
                <td className="red-text">Tetanus Booster</td>
                <td className="red-text">Overdue</td>
                <td>-</td>
                <td>Every 10 years</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>MMR Vaccine</td>
                <td>2023-05-12</td>
                <td>123456</td>
                <td>Measles, mumps, rubella</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>Hepatitis B Vaccine</td>
                <td>2023-07-30</td>
                <td>123456</td>
                <td>Series of three doses</td>
              </tr>
              <tr className="overdue">
                <td><span className="icon">!</span></td>
                <td className="red-text">Varicella Vaccine</td>
                <td className="red-text">Overdue</td>
                <td>123456</td>
                <td>Chickenpox vaccine</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>HPV Vaccine</td>
                <td>2023-04-25</td>
                <td>-</td>
                <td>Series of two doses</td>
              </tr>
              <tr>
                <td><input type="checkbox" defaultChecked /></td>
                <td>Pertussis</td>
                <td>2023-08-15</td>
                <td>123456</td>
                <td>Recommended for adults 50+</td>
              </tr>
            </tbody>
          </table>
        </div>



      </div>
    </div>
  );
};

export default Vaccine;
