import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { TopArtists } from "./pages/TopArtists";
import { TopSongs } from "./pages/TopSongs";
import { Dashboard } from "./pages/Dashboard";
import SongsPerDay from "./pages/SongsPerDay";
import axios from "axios";
import "./App.css";

import { LoginPage } from "./pages/LoginPage";
import { HomePage } from "./pages/HomePage";
import { Navbar } from "./components/Navbar";

const LOCAL_BASE_URL = import.meta.env.VITE_LOCAL_BASE_URL;
const AWS_BASE_URL = import.meta.env.VITE_AWS_BASE_URL;

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
            `${AWS_BASE_URL}/callback?code=${code}`
          );
          console.log("User info response:", response.data);
          sessionStorage.setItem("login", "true");
          const jsonString = JSON.stringify(response.data);
          sessionStorage.setItem("userInfo", jsonString);
          window.location.href = "/home";
        } catch (error: unknown) {
          console.error(
            "Failed to login:",
            error instanceof Error ? error.message : String(error)
          );
        }
      }
    };

    checkForAuthorizationCode();
  }, []);

  const handleLogin = () => {
    window.location.href = `${AWS_BASE_URL}/login/spotify`;
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${AWS_BASE_URL}/logout`);
      sessionStorage.clear();
      window.location.href = "/";
    } catch (error) {
      console.error("Failed to log out:", error);
    }
  };

  useEffect(() => {
    const storedLogin = sessionStorage.getItem("login");
    if (storedLogin === "true") {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  return (
    <BrowserRouter>
      <div className="App">
        {isLoggedIn && <Navbar handleLogout={handleLogout} />}
        <Routes>
          <Route path="/" element={<LoginPage handleLogin={handleLogin} />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/top-artists" element={<TopArtists />} />
          <Route path="/top-songs" element={<TopSongs />} />
          <Route path="/songs-per-day" element={<SongsPerDay />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
