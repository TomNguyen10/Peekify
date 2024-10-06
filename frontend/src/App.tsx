import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom"; // Import Router and Routes

import axios from "axios";
import "./App.css";

import { Dashboard } from "./components/Dashboard";
import { LoginPage } from "./pages/LoginPage";
import { Navbar } from "./components/Navbar";
import { HomePage } from "./pages/HomePage";

const API_BASE_URL = "http://localhost:8000";

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState<any>(null);

  useEffect(() => {
    const checkForAuthorizationCode = async () => {
      const queryParams = new URLSearchParams(window.location.search);
      const code = queryParams.get("code");

      if (code) {
        try {
          console.log("Authorization code found:", code);

          queryParams.delete("code");
          window.history.replaceState(
            {},
            document.title,
            `${window.location.pathname}`
          );

          const response = await axios.get(
            `${API_BASE_URL}/callback?code=${code}`
          );
          console.log("User info response:", response.data);
          setUserInfo(response.data);
          setIsLoggedIn(true);

          // Redirect to the main page after login
          window.history.replaceState({}, document.title, "/");
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

  // Logout function to call backend and reset state
  const handleLogout = async () => {
    try {
      await axios.post(`${API_BASE_URL}/logout`);
      setIsLoggedIn(false);
      setUserInfo(null);
      window.location.href = "/";
    } catch (error) {
      console.error("Failed to log out:", error);
    }
  };

  return (
    <Router>
      <div>
        {isLoggedIn ? (
          // <Dashboard handleLogout={handleLogout} userInfo={userInfo} />
          // <>
          //   <Navbar handleLogout={handleLogout} />
          //   <Routes>
          //     <Route path="/" element={<Navigate to="/dashboard" />} />
          //     <Route
          //       path="/dashboard"
          //       element={
          //         <Dashboard handleLogout={handleLogout} userInfo={userInfo} />
          //       }
          //     />
          //     {/* <Route path="/top-artists" element={<TopArtists />} /> */}
          //   </Routes>
          // </>
          <HomePage handleLogout={handleLogout} userInfo={userInfo} />
        ) : (
          <LoginPage handleLogin={handleLogin} />
        )}
      </div>
    </Router>
    // <div className="min-h-screen relative w-full bg-black flex flex-col md:flex-row justify-center items-center">
    //   {isLoggedIn ? (
    //     <Dashboard handleLogout={handleLogout} userInfo={userInfo} />
    //   ) : (
    //     <LoginPage handleLogin={handleLogin} />
    //   )}
    // </div>
  );
};

export default App;
