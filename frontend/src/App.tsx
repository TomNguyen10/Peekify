import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import { Button } from "./components/ui/button";
import { LoginForm } from "./components/LoginForm";

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
        <div>
          <h1>Welcome, {userInfo.display_name}</h1>
          <Button onClick={handleLogout}>Log Out</Button>
        </div>
      ) : (
        <>
          <div className="flex flex-col items-center justify-center w-1/2 h-full text-white text-3xl">
            <h1 className="text-5xl font-bold text-green-400">
              Welcome to Peekify
            </h1>
            <p className="text-sm p-5">Your Weekly Spotify Analysis</p>
          </div>
          <div className="flex justify-center items-center w-1/2 h-full">
            <LoginForm handleLogin={handleLogin} />
          </div>
        </>
      )}
    </div>
  );
};

export default App;
