import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Login.css';
import axios from 'axios';
import login_img from '../../assets/sysadmin_03.jpg';
// import logo from '../images/logo_black.png';


const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const[Result,setResult] = useState('');
  const [error, setError] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate(); 


  const handleSubmit = async(event) => {
    event.preventDefault();

    const validUsername = 'admin';
    const validPassword = '12345';
    const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        try {
            const response = await axios.post(
              "http://127.0.0.1:5000/login",
              formData
            );
            console.log("Response:", response.data);
      if (response.data.error) {
        setError("⚠️ " + response.data.error);
        return;
      }
      setResult(response.data);
      navigate('/home',{state:response.data});
      console.log("Query submitted successfully:", response.data);

    
        }
            catch (error) {
                console.error("Error while submitting details:", error);
              }
              
  };

  return (
    <div className="main-container">
      <div className="container">
        <div className="left-container">
          <img src = {login_img} alt = "login"/>
        </div>

        <div className="right-container">
          <form className="login-form" onSubmit={handleSubmit}>
            {/* <img src = {logo}/> */}
            {/* <h2>Login</h2> */}

            <label htmlFor="userID">User ID</label>
            <input
              type="text"
              id="userID"
              name="userID"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {error && <div className="error-message">{error}</div>}

            <button type="submit">Login</button>
          </form>

          {loggedIn && (
            <Link to="/home">Go to Home</Link>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;
