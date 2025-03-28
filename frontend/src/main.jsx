import { GoogleOAuthProvider } from '@react-oauth/google'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { store } from './redux/store'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import './index.scss'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store} >
      <GoogleOAuthProvider clientId={import.meta.env.VITE_CLIENT_ID} >
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </GoogleOAuthProvider>
    </Provider>
  </React.StrictMode>,
)


// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import { Provider } from 'react-redux';
// import { store } from './redux/store';
// import { BrowserRouter, Link } from 'react-router-dom';
// import './index.scss';

// const HomePage = () => {
//   return (
//     <div className="home-page">
//       <header>
//         <img src="frontend/src/assets/dialologo.png" alt="Welcome Logo" className="logo" />
//         <h1>Welcome to Dialo</h1>
//       </header>
//       <section className="bots-section">
//         <h2>Different Bots:</h2>
//         <div className="bot-boxes">
//           <Link to="/bot1" className="box">
//             <h3>Bot 1</h3>
//             <p>Go to Bot 1</p>
//           </Link>
//           <Link to="/bot2" className="box">
//             <h3>Bot 2</h3>
//             <p>Go to Bot 2</p>
//           </Link>
//           <Link to="/bot3" className="box">
//             <h3>Bot 3</h3>
//             <p>Go to Bot 3</p>
//           </Link>
//         </div>
//       </section>
//       <footer className="footer">
//         <div className="team-info">
//           <h3>Team Members:</h3>
//           <ul>
//             <li>Abhay Kumar</li>
//             <li>Rakshith</li>
//             <li>Shresth Bhakta</li>
//           </ul>
//         </div>
//         <div className="team-name">
//           <h3>Team Name:</h3>
//           <p>Dialo </p>
//         </div>
//         <div className="contact-us">
//           <h3>Contact Us:</h3>
//           <p>Email: [info@dialo.com](mailto:info@dialo.com)</p>
//           <p>Phone: +1-123-456-7890</p>
//         </div>
//         <div className="copyright">
//           <p>&copy; 2024 Dialo Team. All rights reserved.</p>
//         </div>
//       </footer>
//     </div>
//   );
// };

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <Provider store={store}>
//       <BrowserRouter>
//         <HomePage />
//       </BrowserRouter>
//     </Provider>
//   </React.StrictMode>,
// );
