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

          // Remove the code from the URL before making the request to prevent multiple requests
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
    const clientId = "afbb70c2c3f1418ab00bdfc52ab754f7";
    const redirectUri = "http://localhost:5173/callback";
    const scope = "user-read-email user-read-private";
    const authUrl = `https://accounts.spotify.com/authorize?response_type=code&client_id=${clientId}&scope=${encodeURIComponent(
      scope
    )}&redirect_uri=${encodeURIComponent(redirectUri)}`;

    window.location.href = authUrl;
  };

  return (
    <div>
      {isLoggedIn ? (
        <div>
          <h1>Welcome, {userInfo.display_name}</h1>
          {/* Display other user info as needed */}
        </div>
      ) : (
        <div>
          <h1>Please log in</h1>
          <button onClick={handleLogin}>Log in with Spotify</button>
        </div>
      )}
    </div>
  );
};

export default App;
