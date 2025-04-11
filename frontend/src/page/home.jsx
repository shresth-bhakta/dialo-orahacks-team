import React from 'react';
import { BrowserRouter, Link } from 'react-router-dom';
import './style.scss';

const HomePage = () => {
  return (
    
    <div className="home-page">
      <header>
        <img src="../src/assets/dialo.png" alt="Welcome Logo" className="logo" />
        <h1>Welcome to Dialo</h1>
      </header>
      <section className="bots-section">
        <h2>Different Bots:</h2>
        <div className="bot-boxes">
          <Link to="/bot1" className="box">
            {/* <h3>Bot 1</h3> */}
            <p>Order Management BOT</p>
          </Link>
          <Link to="/bot2" className="box">
            {/* <h3>Bot 2</h3> */}
            <p>Marketing BOT</p>
          </Link>
          {/* <Link to="/bot3" className="box">
            <h3>Bot 3</h3>
            <p>Go to Bot 3</p>
          </Link> */}
        </div>
      </section>
      <footer className="footer">
        <div className="team-info">
          <h3>Team Members:</h3>
          <ul>
            <div>Abhay Kumar</div>
            <div>Rakshith</div>
            <div>Shresth Bhakta</div>
            <div>Gaurav Kumawat</div>
          </ul>
        </div>
        <div className="team-name">
          <h3>Team Name:</h3>
          <p>Dialo </p>
        </div>
        <div className="contact-us">
          <h3>Contact Us:</h3>
          <p>Email: [info@dialo.com](mailto:info@dialo.com)</p>
          <p>Phone: +91 7990377120</p>
        </div>
        <div className="copyright">
          <p>&copy; 2024 Dialo Team. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;