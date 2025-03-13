import React from 'react'
import './ContactUs.css'
import Swal from 'sweetalert2'

const Contact = () => {

  const onSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    formData.append("access_key", "99c02115-99bf-48f4-95da-101f5e7a4f0c");

    const object = Object.fromEntries(formData);
    const json = JSON.stringify(object);

    const res = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: json
    }).then((res) => res.json());

    if (res.success) {
      Swal.fire({
        title: "Success!",
        text: "Message sent succsessfully!",
        icon: "success"
      });
    }
  };

  return (
    <section className='contact'> 
      <form onSubmit={onSubmit}>
         <h2>Contact Form</h2>
         <div className="input-box">
            <label>Full Name of Baby</label>
            <input type="text" className="field" placeholder='Enter  name' name='name' required />
         </div>
         <div className="input-box">
            <label>Age</label>
            <input type="text" className="field" placeholder='Enter age' name='email' required />
         </div>
         <div className="input-box">
            <label>Gender</label>
            <select name="gender" className="field" required >
              <option value="" disabled selected placeholder="Select Gender"></option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
         </div>
         <div className="input-box">
            <label>Your Message</label>
            <textarea name="message" id="" className='field mess'placeholder='Enter your message' required></textarea>
         </div>
         <button type="submit">Send Message</button>
      </form>
    </section>
  )
}

export default Contact