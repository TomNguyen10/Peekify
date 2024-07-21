import React, { useEffect, useState } from "react";
import axios from "axios";

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

  return (
    <div>
      {isLoggedIn ? (
        <div>
          <h1>Welcome, {userInfo.display_name}</h1>
        </div>
      ) : (
        <div className="center-login">
          <h2>Welcome to Peekify</h2>
          <p className="subtitle">Your weekly Spotify Analysis</p>
          <button onClick={handleLogin}>Log in with Spotify</button>
        </div>
      )}
    </div>
  );
};

export default App;
