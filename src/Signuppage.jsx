import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signuppage.css"; 
import image2 from './assets/image2.png'

const Signup=()=>{
    const [Mothername,setMothername]=useState("");
    const [MotherDOB,setMotherDOB]=useState("");
    const [Age,setAge]=useState("");
    const [Email,setEmail]=useState("");
    const [phonenumber,setPhonenumber]=useState("");
    const [Bloodgroup,SetBloodgroup]=useState("");
    //const [userName,setuserName]=useState("");
    const [password,setPassword]= useState("");
    const [confirmpassword,setConfirmpassword]=useState("");
   // const [SOSname,setSOSname]=useState("");
    //const [SOSmobileno,setSOSmobileno]=useState("");
    const [error,Seterror]=useState("");
    const navigate = useNavigate();

    const handleSignup=()=>{
        if (!Mothername || !MotherDOB || !Age || !Email || !phonenumber || !Bloodgroup){
            Seterror("All the feilds are required")
            return;
        }

        if (password!==confirmpassword){
            Seterror("Password do not match");
            return;
        }
        alert("Sign up succesfull")

        navigate("/login")

    }




    return(
        <div>
            <div className="backImage" style={{ backgroundImage: `url(${image2})` }}></div>
            <div className="signup-container">
                <h1>Sign up</h1>
                <h6>Sign up to continue</h6>

                <input
                type="text"
                placeholder="Mother's Name"
                value={Mothername}
                onChange={(e)=>setMothername(e.target.value)}
                className="Signup-input"
                ></input>

                
                <input
                type="Date"
                placeholder="Mother's D.O.B"
                value={MotherDOB}
                onChange={(e)=>setMotherDOB(e.target.value)}
                className="Signup-input"
                ></input>


                <input
                type="text"
                placeholder="Age"
                value={Age}
                onChange={(e)=>setAge(e.target.value)}
                className="Signup-input"
                ></input>

                <input
                type="tel"
                placeholder="Phone Number"
                value={phonenumber}
                maxlength="10"
                onChange={(e) => setPhonenumber(e.target.value)}
                className="Signup-input"
                />

                <input
                type="email"
                placeholder="Email"
                value={Email}
                onChange={(e) => setEmail(e.target.value)}
                className="Signup-input"
                />

                 {/* Blood Group Dropdown */}
                <select
                value={Bloodgroup}
                onChange={(e) => SetBloodgroup(e.target.value)}
                className="Signup-input"
                >
                <option value="">Select Blood Group</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                </select>

                <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="Signup-input"
                />

                <input
                type="password"
                placeholder="Confirm Password"
                value={confirmpassword}
                onChange={(e) => setConfirmpassword(e.target.value)}
                className="Signup-input"
                />
            <button className="Signup-button" onClick={handleSignup}>Sign Up</button>
            {error && <p className="error-message">{error}</p>}
            </div>
        </div>
    )

}

export default Signup;