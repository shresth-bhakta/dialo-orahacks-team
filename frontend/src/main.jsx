// import { GoogleOAuthProvider } from '@react-oauth/google'
// import React from 'react'
// import ReactDOM from 'react-dom/client'
// import { Provider } from 'react-redux'
// import { store } from './redux/store'
// import App from './App'
// import { BrowserRouter } from 'react-router-dom'
// import './index.scss'

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <Provider store={store} >
//       <GoogleOAuthProvider clientId={import.meta.env.VITE_CLIENT_ID} >
//         <BrowserRouter>
//           <App />
//         </BrowserRouter>
//       </GoogleOAuthProvider>
//     </Provider>
//   </React.StrictMode>,
// )


import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import { BrowserRouter, Link } from 'react-router-dom';
import './index.scss';

const HomePage = () => {
  return (
    <div className="home-page">
      <h1>Welcome to Dialo</h1>
      <div className="page-boxes">
        <Link to="/about" className="box">
          <h2>About Us</h2>
          <p>Learn more about our company</p>
        </Link>
        <Link to="/services" className="box">
          <h2>Our Services</h2>
          <p>Discover what we offer</p>
        </Link>
        <Link to="/contact" className="box">
          <h2>Contact Us</h2>
          <p>Get in touch with us</p>
        </Link>
        <Link to="/blog" className="box">
          <h2>Blog</h2>
          <p>Read our latest articles</p>
        </Link>
        <Link to="/faq" className="box">
          <h2>Frequently Asked Questions</h2>
          <p>Find answers to common questions</p>
        </Link>
      </div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
);
