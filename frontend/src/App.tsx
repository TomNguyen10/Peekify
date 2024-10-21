import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; // Import Router and Routes
import { TopArtists } from "./pages/TopArtists";
import { TopSongs } from "./pages/TopSongs";
import { Dashboard } from "./pages/Dashboard";
import SongsPerDay from "./pages/SongsPerDay";
import axios from "axios";
import "./App.css";

import { LoginPage } from "./pages/LoginPage";
import { HomePage } from "./pages/HomePage";
import { Navbar } from "./components/Navbar";

const API_BASE_URL = "http://localhost:8000";

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkForAuthorizationCode = async () => {
      const queryParams = new URLSearchParams(window.location.search);
      const code = queryParams.get("code");

      if (code) {
        try {
          console.log("Authorization code found:", code);

          queryParams.delete("code");
          const response = await axios.get(
            `${API_BASE_URL}/callback?code=${code}`
          );
          console.log("User info response:", response.data);
          localStorage.setItem("login", "true");
          const jsonString = JSON.stringify(response.data);
          localStorage.setItem("userInfo", jsonString);
          window.location.href = "/home";
        } catch (error: any) {
          console.error(
            "Failed to login:",
            error.response ? error.response.data : error.message
          );
        }
      }
    };

    checkForAuthorizationCode();
  }, []);

  const handleLogin = () => {
    window.location.href = `${API_BASE_URL}/login/spotify`;
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${API_BASE_URL}/logout`);
      localStorage.clear();
      window.location.href = "/";
    } catch (error) {
      console.error("Failed to log out:", error);
    }
  };

  useEffect(() => {
    const storedLogin = localStorage.getItem("login");
    if (storedLogin === "true") {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  return (
    <Router>
      {isLoggedIn && <Navbar handleLogout={handleLogout} />}
      <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/top-songs" element={<TopSongs />} />
        <Route path="/top-artists" element={<TopArtists />} />
        <Route path="/songs-per-day" element={<SongsPerDay />} />
        <Route path="/" element={<LoginPage handleLogin={handleLogin} />} />
      </Routes>
    </Router>
  );
};

export default App;
