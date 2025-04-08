// Chatbot.jsx
import React, { useEffect, useState } from "react";
import Navbar from "../../Components/Navbar.jsx";
import "./chatbot.css";
import bgimg from "./chatbotimg/Rectangle3467956.png";
import { FaBell, FaSearch } from "react-icons/fa";
import axios from "axios";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const token = localStorage.getItem("token");

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get("http://52.140.41.112:8080/doctor/chat/", {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });
                setMessages(response.data);
            } catch (error) {
                console.error("Error fetching messages:", error);
                setMessages([]);
            }
        };
        fetchMessages();
    }, [token]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { text: input, sender: "user" };
        setMessages(prev => [...prev, userMessage]);
        setInput("");

        try {
            const response = await axios.post(
                "http://52.140.41.112:8080/doctor/chat/",
                { text: input },
                {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );


            const doctorMessage = {
                text: response.data.doctor_reply,
                sender: "doctor"
            };
            setMessages(prev => [...prev, doctorMessage]);

        } catch (error) {
            console.error("Error sending message:", error);

        }
    };



    return (
        <div className="chatbot-container" style={{ '--bg-image': `url(${bgimg})` }}>
            <div className="navbar">
                <Navbar />
            </div>
            <div className="chatbot-content">
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

                <div className="chatbot-window">
                    <div className="chat-area">
                        <div className="chat-header">
                            <p><strong>Chat With Doc</strong><br />
                                Dr. Steven Appleseed,<br />
                                Consultant Gynecologist.
                            </p>
                        </div>

                        <div className="messages-section">
                            {messages.map((msg, index) => (
                                <div
                                    key={index}
                                    className={`chat-message ${msg.sender === "user" ? "user-message" : "doc-message"}`}
                                >
                                    {msg.text}
                                </div>
                            ))}
                        </div>

                        <div className="chat-input">
                            <input
                                type="text"
                                placeholder="Your message..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            />
                            <button onClick={handleSend}>➤</button>
                        </div>
                    </div>

                    <div className="chat-history">
                        <p className="history-title">History</p>
                        <div className="empty-history">
                            <p>No chats here yet</p>
                        </div>
                        <button className="new-chat-btn">New Chat</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
