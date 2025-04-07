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

    useEffect(() => {
        const fetchMessages = async () => {
            // Mocked data for now
            const response = [
                { sender: "doc", text: "Hello, how can I help you today?" },
                { sender: "user", text: "My baby has a fever." },
                { sender: "doc", text: "How high is the temperature?" }
            ];
            setMessages(response);

            // To use real backend, uncomment below and replace with your endpoint
            // const result = await axios.get("https://your-backend.com/api/messages");
            // setMessages(result.data);
        };
        fetchMessages();
    }, []);

    const handleSend = async () => {
        if (!input.trim()) return;
        const newMessage = { text: input, sender: "user" };
        setMessages([...messages, newMessage]);
        setInput("");

        // Optionally send to backend
        // await axios.post("https://your-backend.com/api/messages", newMessage);
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
