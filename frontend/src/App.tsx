import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import { Button } from "./components/ui/button";
import { LoginForm } from "./components/LoginForm";
import { Dashboard } from "./components/Dashboard";

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
    <div className="h-screen w-full bg-black flex justify-center items-center overflow-x: hidden;">
      {isLoggedIn ? (
        <Dashboard handleLogout={handleLogout} userInfo={userInfo} />
      ) : (
        <>
          <div className="flex flex-col items-end justify-center w-full md:w-1/2 h-full text-white text-3xl hidden sm:flex">
            <img
              src="../src/assets/Peekify-logo.png"
              className="animate-spin-slow max-w-[150px] md:max-w-[200px] lg:max-w-[250px]"
              alt="Rotating Image"
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full sm:w-3/4 md:w-1/2 h-full p-5">
            <div className="items-start text-center md:text-left">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-green-400 gradient-text text-transparent bg-clip-text">
                Welcome to
              </h1>
              <h1 className="text-6xl sm:text-7xl md:text-8xl font-bold text-green-400">
                Peekify
              </h1>
              <p className="text-xs sm:text-sm md:text-base pt-5 pb-5 text-white">
                Your Weekly Spotify Analysis
              </p>
            </div>
            <LoginForm handleLogin={handleLogin} />
          </div>
        </>
      )}
    </div>
  );
};

export default App;
