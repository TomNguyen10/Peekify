import React from "react";
import "./Button.css";

const LogoutButton: React.FC = () => {
  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8000/logout", {
        method: "GET",
        credentials: "include",
      });
      if (response.redirected) {
        window.location.href = response.url;
      }
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <button className="spotify-button" onClick={handleLogout}>
      Log Out of Spotify
    </button>
  );
};

export default LogoutButton;
