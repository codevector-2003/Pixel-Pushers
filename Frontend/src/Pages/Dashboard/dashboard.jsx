import React, { useEffect, useState } from "react";
import './dashboard.css';
import { useNavigate } from "react-router-dom";
import Navbar from "../../Components/Navbar.jsx";
import bgimage from './Dashboardimg/Rectangle3467956.png';
import searchimg from './Dashboardimg/search1.png';
import sendimg from './Dashboardimg/send-horizontal1.png';
import bellimg from './Dashboardimg/bell1.png';
import calenderimg from './Dashboardimg/calendar1.png';
import babyimg from './Dashboardimg/baby1.png';
import childimg from './Dashboardimg/freepik--group--inject-86.png';
import { CgAdd } from "react-icons/cg";
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

const fetchIllnessData = async () => {
    return [
        { month: 1, sickDays: 3 },
        { month: 6, sickDays: 4 },
        { month: 12, sickDays: 8, unusuallySick: true },
        { month: 18, sickDays: 6 },
        { month: 24, sickDays: 7 },
        { month: 30, sickDays: 5 },
        { month: 36, sickDays: 2 },
        { month: 42, sickDays: 3, unusuallySick: true },
        { month: 48, sickDays: 4 },
        { month: 54, sickDays: 5 },
        { month: 60, sickDays: 2 },
        { month: 66, sickDays: 1 },
        { month: 72, sickDays: 0 },
    ];
};

const fetchDietData = async () => {
    return {
        totalCalories: 180,
        breakdown: {
            milk: 60,
            cereal: 70,
            biscuit: 50,
            Fruits: 30
        }
    };
};

const fetchHeightData = async () => {
    return {
        heightCm: 47
    };
};

const fetchVaccineData = async () => {
    return {
        nextVaccineIn: 17,
        nextVaccineName: "Rota-1",
        vaccines: [
            { name: "BCG", age: "24 hours", taken: true },
            { name: "OPV-0", age: "2 weeks", taken: true },
            { name: "Pentavalent 1", age: "6 weeks", taken: true },
            { name: "Rota-1", age: "2 month", taken: false },
            { name: "cCine 2", age: "3 months", taken: false }
        ]
    };
};

const fetchMilestones = async () => {
    return {
        status: "Late bloomer",
        items: [
            { title: "Smiles", age: "2 months" },
            { title: "Said “Momma”", age: "3 months" },
            { title: "Said “Pappa”", age: "3 months" },
            { title: "Hehe lol", age: "1 month" },
            { title: "Hi-Fi", age: "3 months" },
            { title: "Yawns", age: "2 months" }
        ]
    };
};


const Dashboard = () => {

    const [weightData, setWeightData] = useState([]);
    const [illnessData, setIllnessData] = useState([]);
    const [dietData, setDietData] = useState(null);
    const [heightData, setHeightData] = useState(null);
    const [vaccineData, setVaccineData] = useState(null);
    const [milestoneData, setMilestoneData] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();


    useEffect(() => {
        const loadData = async () => {
            const weight = await fetchWeightData();
            const illness = await fetchIllnessData();
            const diet = await fetchDietData();
            const height = await fetchHeightData();
            const vaccine = await fetchVaccineData();
            const milestones = await fetchMilestones();
            setWeightData(weight);
            setIllnessData(illness);
            setDietData(diet);
            setHeightData(height);
            setVaccineData(vaccine);
            setMilestoneData(milestones);

        };
        loadData();
    }, []);

    const lowerQuery = searchQuery.toLowerCase();

    const filteredWeight = weightData.filter(
        (item) => item.age.toString().includes(lowerQuery) || item.weight.toString().includes(lowerQuery)
    );
    const filteredIllness = illnessData.filter(
        (item) => item.month.toString().includes(lowerQuery) || item.sickDays.toString().includes(lowerQuery)
    );
    const filteredVaccines = vaccineData?.vaccines.filter(
        (item) => item.name.toLowerCase().includes(lowerQuery) || item.age.toLowerCase().includes(lowerQuery)
    );
    const filteredMilestones = milestoneData?.items.filter(
        (item) => item.title.toLowerCase().includes(lowerQuery) || item.age.toLowerCase().includes(lowerQuery)
    );
    const filteredDiet = dietData && (
        dietData.totalCalories.toString().includes(lowerQuery) ||
        Object.entries(dietData.breakdown).some(
            ([key, val]) => key.toLowerCase().includes(lowerQuery) || val.toString().includes(lowerQuery)
        )
    );
    const filteredHeight = heightData && heightData.heightCm.toString().includes(lowerQuery);

    return (
        <div className="dashboard" style={{ '--bg-image': `url(${bgimage})` }}>
            <title>Dashboard</title>
            <div className="navbar">
                <Navbar />
            </div>

            <div className="container">


                <div className="weight-chart" onClick={() => navigate('/growthpage')}>
                    <p style={{ fontFamily: 'Poppins', fontSize: '20px', marginLeft: '20px', marginTop: '10px' }}>
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
                                    stroke="#DB88C5"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="lower"
                                    stroke="#DB88C5"
                                    strokeDasharray="4 4"
                                    dot={false}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="weight"
                                    stroke="#F67EAD"
                                    strokeWidth={3}
                                    dot={{ stroke: '#F67EAD', strokeWidth: 2, r: 5 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>


                <div className="illnes-tracker">
                    <p style={{ fontFamily: 'Poppins', fontSize: '20px', marginLeft: '20px', marginTop: '10px' }}>Illness Timeline</p>
                    <div style={{ position: 'absolute', top: '30px', left: '0px', right: '20px', bottom: '0px' }}>
                        <ResponsiveContainer width="100%" height="90%">
                            <BarChart data={illnessData} margin={{ top: 50, right: 20, bottom: 0, left: 0 }}>
                                <CartesianGrid stroke="#f2d8e7" strokeDasharray="3 3" />
                                <XAxis
                                    dataKey="month"
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
                                <Bar
                                    dataKey="sickDays"
                                    radius={[8, 8, 0, 0]}
                                    label={({ x, y, index }) =>
                                        illnessData[index].unusuallySick ? (
                                            <text
                                                x={x}
                                                y={y - 10}
                                                fill="#F67EAD"
                                                fontSize={12}
                                                fontWeight="bold"
                                                fontFamily="Poppins"
                                            >
                                                Unusually sick
                                            </text>
                                        ) : null
                                    }
                                >
                                    {illnessData.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={entry.unusuallySick ? "#F67EAD" : "#E6E6E6"}
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                </div>


                <div className="diet-chart">
                    <p style={{ fontFamily: 'Poppins', fontSize: '18px', margin: '10px 0 0 20px' }}>Diet Chart</p>
                    {dietData && (
                        <div style={{ width: '100%', height: 150, position: 'relative' }}>
                            <ResponsiveContainer>
                                <PieChart>
                                    <Pie
                                        data={[
                                            { name: 'Milk', value: dietData.breakdown.milk },
                                            { name: 'Cereal', value: dietData.breakdown.cereal },
                                            { name: 'Biscuit', value: dietData.breakdown.biscuit }
                                        ]}
                                        dataKey="value"
                                        innerRadius={50}
                                        outerRadius={70}
                                        paddingAngle={5}
                                        fill="#8884d8"
                                    >
                                        <Cell fill="#DB5E9D" />
                                        <Cell fill="#E4A0D7" />
                                        <Cell fill="#B9A0E4" />
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                            <div style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                textAlign: 'center',
                                fontFamily: 'Poppins'
                            }}>
                                <div style={{ fontSize: 14 }}>Total</div>
                                <div style={{ fontWeight: 'bold' }}>{dietData.totalCalories} kCal</div>
                            </div>
                        </div>
                    )}
                </div>


                ‍<div className="vaccine-tracker" onClick={() => navigate('/vaccine')}>
                    <p style={{ fontFamily: 'Poppins', fontSize: '18px', margin: '7px 0 0 20px' }}>Vaccine tracker</p>
                    {vaccineData && (
                        <div style={{ padding: '10px 20px' }}>
                            <div style={{ fontSize: '23px', fontWeight: '600', fontFamily: 'Poppins', marginLeft: '205px' }}>
                                {vaccineData.nextVaccineIn} days
                            </div>
                            <div style={{ fontFamily: 'Poppins', fontSize: '16px', marginBottom: '15px', fontWeight: 'bold' }}>
                                {vaccineData.nextVaccineName}
                                <span style={{ color: '#888', marginLeft: '135px' }}>Next vaccine</span>
                            </div>

                            {vaccineData.vaccines.map((vac, index) => (
                                <div key={index} style={{

                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '10px',
                                    marginBottom: '8px'
                                }}>
                                    {vac.missed ? (
                                        <span style={{
                                            color: '#F67EAD',
                                            fontWeight: 'bold',
                                            fontSize: '18px'
                                        }}>❗</span>
                                    ) : (
                                        <input type="checkbox" checked={vac.taken} readOnly />
                                    )}
                                    <span style={{
                                        textDecoration: vac.missed ? 'none' : '',
                                        color: vac.missed ? '#F67EAD' : '#000',
                                        fontWeight: vac.missed ? 'bold' : 'normal',
                                        fontFamily: 'Poppins'
                                    }}>
                                        {vac.name}
                                    </span>
                                    <span style={{ marginLeft: 'auto', fontSize: '13px', color: '#888' }}>
                                        {vac.age}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>


                <div className="baby-growth-tracker" onClick={() => navigate('/milestones')}>
                    <p style={{ fontFamily: 'Poppins', fontSize: '18px', margin: '10px 0 0 20px' }}>Milestones</p>
                    {milestoneData && (
                        <div style={{ padding: '10px 20px' }}>
                            <div style={{ fontSize: '18px', fontWeight: '600', marginBottom: '10px', fontFamily: 'Poppins' }}>
                                {milestoneData.status}
                            </div>
                            {milestoneData.items.map((item, index) => (
                                <div key={index} style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    fontFamily: 'Poppins',
                                    marginBottom: '10px',
                                    gap: '5px',
                                }}>
                                    <span>{item.title}</span>
                                    <span style={{ color: '#888', fontSize: '13px' }}>{item.age}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>


                <div className="topbar">
                    <div className="search-bar">
                        <div className="search-icon">
                            <img src={searchimg} alt="search" />
                        </div>
                        <input type="text" placeholder="Search..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                    </div>

                    <div className="notification-icon">
                        <button className="notification-button"></button>
                        <img src={bellimg} className="bellimage" alt="bell" />
                    </div>

                    <div className="profile">
                        <div className="profile-icon">
                            <img src={babyimg} alt="profile" />
                        </div>
                        <p>Jhone Doe</p>

                    </div>

                    <div className="add">
                        <button></button>
                        <CgAdd className="add-icon" style={{ color: '#B2BEB5', height: '40px', width: '40px' }} />
                    </div>

                </div>
                <div className="chat-box">
                    <p style={{ fontFamily: 'Poppins', fontSize: '16px', margin: '10px 0 0 20px' }}>Chat</p>
                    <div style={{ fontSize: '20px', fontWeight: '600', fontFamily: 'Poppins', margin: '0px 20px' }}>
                        Talk to <br /> your doctor
                    </div>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        margin: '20px',
                        padding: '10px 15px',
                        borderRadius: '12px',
                        backgroundColor: '#F4EFF1'
                    }}>
                        <input
                            type="text"
                            placeholder="Type your message"
                            style={{
                                flex: 1,
                                border: 'none',
                                outline: 'none',
                                backgroundColor: 'transparent',
                                fontFamily: 'Poppins',
                                fontSize: '14px',
                                color: '#000'
                            }}
                        />
                        <button style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            paddingLeft: '10px'
                        }}>
                            <img src={sendimg} alt="send" style={{ width: '20px', height: '20px' }} onClick={() => navigate('/chatbot')} />
                        </button>
                    </div>
                </div>



                <div className="height-tracker" onClick={() => navigate('/growthpage')}>
                    <p style={{ fontFamily: 'Poppins', fontSize: '18px', margin: '10px 0 0 20px' }}>Height</p>
                    {heightData && (
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            padding: '20px'
                        }}>
                            <div style={{ fontSize: '30px', fontWeight: 'bold', fontFamily: 'Poppins' }}>
                                {heightData.heightCm} <span style={{ fontSize: '18px', color: '#888' }}>cm</span>
                            </div>
                            <div style={{ height: 100, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                                {[43, 40, 33].map(label => (
                                    <div key={label} style={{ fontSize: '14px', color: '#888' }}>{label} cm</div>
                                ))}
                            </div>
                            <div>
                                <img src={childimg} alt="child" style={{ height: '100px' }} />
                            </div>
                        </div>
                    )}
                </div>

            </div>
        </div>
    )

}
export default Dashboard;