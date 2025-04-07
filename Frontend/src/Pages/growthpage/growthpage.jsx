import react, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './growthpage.css';
import bgimage from './growthpageimg/Rectangle3467956.png';
import searchimg from './growthpageimg/search.png';
import bellimg from './growthpageimg/bell1.png';
import Navbar from '../../Components/Navbar.jsx';
import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    BarChart,
    Bar,
    Cell,
    PieChart,
    Pie
} from "recharts";

const fetchWeightData = async () => {
    return [
        { age: 1, weight: 4, lower: 3, upper: 5 },
        { age: 6, weight: 7, lower: 6, upper: 9 },
        { age: 12, weight: 11, lower: 9, upper: 13 },
        { age: 18, weight: 14, lower: 12, upper: 16 },
        { age: 24, weight: 16, lower: 14, upper: 18 },
        { age: 30, weight: 18, lower: 16, upper: 21 },
    ];
};

const fetchHeightData = async () => {
    return [
        { age: 1, height: 50, lower: 48, upper: 52 },
        { age: 6, height: 70, lower: 68, upper: 72 },
        { age: 12, height: 130, lower: 120, upper: 132 },
        { age: 18, height: 160, lower: 158, upper: 162 },
        { age: 24, height: 170, lower: 168, upper: 172 },
        { age: 30, height: 175, lower: 173, upper: 177 },
    ];
}

const fetchWeightRecords = async () => {
    return [
        { id: 1, weight: '5.5 KG', date: '88/88/8888', notes: 'Chubby babe' },
        { id: 2, weight: '5.2 KG', date: '88/88/8888', notes: 'Chubby babe' },
        { id: 3, weight: '5.3 KG', date: '88/88/8888', notes: 'Chubby babe' },

    ];
};

const fetchHeightRecords = async () => {
    return [
        { id: 1, height: '41 cm', date: '88/88/8888', notes: 'Tall boi damn' },
        { id: 2, height: '39 cm', date: '88/88/8888', notes: 'Tall boi damn' },
        { id: 3, height: '37 cm', date: '88/88/8888', notes: 'Tall boi damn' },
    ];
};


const Growthpage = () => {


    const [weightData, setWeightData] = useState([]);
    const [heightData, setHeightData] = useState([]);
    const [weightRecords, setWeightRecords] = useState([]);
    const [heightRecords, setHeightRecords] = useState([]);


    useEffect(() => {
        const loadData = async () => {
            const weight = await fetchWeightData();
            const height = await fetchHeightData();
            const weightRecs = await fetchWeightRecords();
            const heightRecs = await fetchHeightRecords();
            setWeightData(weight);
            setHeightData(height);
            setWeightRecords(weightRecs);
            setHeightRecords(heightRecs);
        };
        loadData();
    }, []);

    return (
        <div className="growthpage" style={{ '--bg-image': `url(${bgimage})` }} >
            <title>Growth Tracker</title>
            <div className='navbar'>
                <Navbar />
            </div>
            <div className="growthpage__container">

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
                <div className="height">
                    <div className="record-section">
                        <h3 style={{ marginLeft: '20px', fontFamily: 'Poppins' }}>Height Records</h3>
                        <button onClick={() => {
                            setHeightRecords([...heightRecords, {
                                id: Date.now(),
                                date: '',
                                height: '',
                                notes: ''
                            }]);
                        }} className='addrecordbtn'>➕</button>
                        <table className="record-table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Height</th>
                                    <th>Notes</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {heightRecords.map((record, index) => (
                                    <tr key={record.id}>
                                        <td><input value={record.date} onChange={(e) => {
                                            const updated = [...heightRecords];
                                            updated[index].date = e.target.value;
                                            setHeightRecords(updated);
                                        }} /></td>
                                        <td><input value={record.height} onChange={(e) => {
                                            const updated = [...heightRecords];
                                            updated[index].height = e.target.value;
                                            setHeightRecords(updated);
                                        }} /></td>
                                        <td><input value={record.notes} onChange={(e) => {
                                            const updated = [...heightRecords];
                                            updated[index].notes = e.target.value;
                                            setHeightRecords(updated);
                                        }} /></td>
                                        <td><button onClick={() => {
                                            const updated = heightRecords.filter((_, i) => i !== index);
                                            setHeightRecords(updated);
                                        }}>Delete</button></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                    </div>

                </div>


                <div className="weight">
                    <div className="record-section">
                        <h3 style={{ marginLeft: '20px', fontFamily: 'Poppins' }}>Weight Records</h3>
                        <button onClick={() => {
                            setWeightRecords([...weightRecords, {
                                id: Date.now(),
                                date: '',
                                weight: '',
                                notes: ''
                            }]);
                        }} className='addrecordbtn'>➕</button>
                        <table className="record-table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Weight</th>
                                    <th>Notes</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {weightRecords.map((record, index) => (
                                    <tr key={record.id}>
                                        <td><input value={record.date} onChange={(e) => {
                                            const updated = [...weightRecords];
                                            updated[index].date = e.target.value;
                                            setWeightRecords(updated);
                                        }} /></td>
                                        <td><input value={record.weight} onChange={(e) => {
                                            const updated = [...weightRecords];
                                            updated[index].weight = e.target.value;
                                            setWeightRecords(updated);
                                        }} /></td>
                                        <td><input value={record.notes} onChange={(e) => {
                                            const updated = [...weightRecords];
                                            updated[index].notes = e.target.value;
                                            setWeightRecords(updated);
                                        }} /></td>
                                        <td><button onClick={() => {
                                            const updated = weightRecords.filter((_, i) => i !== index);
                                            setWeightRecords(updated);
                                        }}>Delete</button></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                    </div>

                </div>



                <div className="heightchart">
                    <p style={{ fontFamily: 'Poppins', fontSize: '20px', marginLeft: '20px', marginTop: '10px', align: 'center' }}>
                        Height<span style={{ fontSize: '20px', color: '#888' }}>(cm)</span> / Month
                    </p>
                    <div style={{ position: 'absolute', top: '10px', left: '0px', right: '20px', bottom: '10px' }}>
                        <ResponsiveContainer width="100%" height="90%">
                            <LineChart data={heightData} margin={{ top: 50, right: 20, bottom: 0, left: 0 }}>
                                <CartesianGrid stroke="#f2d8e7" strokeDasharray="3 3" />
                                <XAxis
                                    dataKey="age"
                                    tick={{ fill: '#555', fontFamily: 'Poppins', fontSize: 12 }}

                                />
                                <YAxis
                                    tick={{ fill: '#555', fontFamily: 'Poppins', fontSize: 12 }}

                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: '#FFF4F9',
                                        border: '1px solidrgb(108, 123, 172)',
                                        fontFamily: 'Poppins',
                                        fontSize: 12
                                    }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="upper"
                                    stroke="#457eff"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="lower"
                                    stroke="#457eff"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="height"
                                    stroke="#f4a444"
                                    strokeWidth={3}
                                    dot={{ stroke: '#F67EAD', strokeWidth: 2, r: 5 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>


                <div className="weightchart">
                    <p style={{ fontFamily: 'Poppins', fontSize: '20px', marginLeft: '20px', marginTop: '10px', align: 'center' }}>
                        Weight <span style={{ fontSize: '20px', color: '#888' }}>(kg)</span> / Month
                    </p>
                    <div style={{ position: 'absolute', top: '10px', left: '0px', right: '20px', bottom: '10px' }}>
                        <ResponsiveContainer width="100%" height="90%">
                            <LineChart data={weightData} margin={{ top: 50, right: 20, bottom: 0, left: 0 }}>
                                <CartesianGrid stroke="#f2d8e7" strokeDasharray="3 3" />
                                <XAxis
                                    dataKey="age"
                                    tick={{ fill: '#555', fontFamily: 'Poppins', fontSize: 12 }}

                                />
                                <YAxis
                                    tick={{ fill: '#555', fontFamily: 'Poppins', fontSize: 12 }}

                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: '#FFF4F9',
                                        border: '1px solid #F67EAD',
                                        fontFamily: 'Poppins',
                                        fontSize: 12
                                    }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="upper"
                                    stroke="#f4a444"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="lower"
                                    stroke="#f4a444"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="weight"
                                    stroke="#457eff"
                                    strokeWidth={3}
                                    dot={{ stroke: '#F67EAD', strokeWidth: 2, r: 5 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

            </div>
        </div>
    );
}
export default Growthpage;