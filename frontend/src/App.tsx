import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [userInfo, setUserInfo] = useState<any>(null);

  const handleSpotifyLogin = async () => {
    try {
      const response = await axios.get<{ redirect_url: string }>(
        `${API_BASE_URL}/login/spotify`
      );
      window.location.href = response.data.redirect_url;
    } catch (error) {
      console.error("Failed to initiate Spotify login:", error);
    }
  };

  useEffect(() => {
    const checkForAuthorizationCode = async () => {
      const queryParams = new URLSearchParams(window.location.search);
      const code = queryParams.get("code");

      if (code) {
        try {
          const response = await axios.get(
            `${API_BASE_URL}/callback?code=${code}`
          );
          setUserInfo(response.data.user_info);
          setIsLoggedIn(true);
          window.history.replaceState({}, document.title, "/");
        } catch (error) {
          console.error("Failed to login:", error);
        }
      }
    };

    checkForAuthorizationCode();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Spotify Integration</h1>
      </header>
      <main>
        {isLoggedIn ? (
          <div>
            <p>Welcome, {userInfo?.display_name}!</p>
          </div>
        ) : (
          <div>
            <p>Welcome to the React Spotify Integration App!</p>
            <button onClick={handleSpotifyLogin}>Login with Spotify</button>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
