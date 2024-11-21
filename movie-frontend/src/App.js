import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Home from './components/Home';
import DataAnalysis from './components/DataAnalysis';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Tracks login status

  const handleLogout = async () => {
    try {
      // Call the logout API
      await axios.post('http://127.0.0.1:5001/logout', {}, { withCredentials: true });
      setIsLoggedIn(false); // Update the state to logged out
    } catch (error) {
      console.error('Error logging out:', error.response?.data || error.message);
    }
  };

  return (
    <Router>
      <div>
        <nav>
          {!isLoggedIn ? (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Sign Up</Link>
            </>
          ) : (
            <>
              <Link to="/home">Home</Link>
              <Link to="/data-analysis">Data Analysis</Link>
              <button onClick={handleLogout} style={{ marginLeft: '10px' }}>
                Log Out
              </button>
            </>
          )}
        </nav>

        <Routes>
          {!isLoggedIn ? (
            <>
              <Route
                path="/login"
                element={<Login onLogin={() => setIsLoggedIn(true)} />}
              />
              <Route
                path="/signup"
                element={<Signup onSignup={() => setIsLoggedIn(true)} />}
              />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </>
          ) : (
            <>
              <Route path="/home" element={<Home />} />
              <Route path="/data-analysis" element={<DataAnalysis />} />
              <Route path="*" element={<Navigate to="/home" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
