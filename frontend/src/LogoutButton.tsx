import React from "react";
import "./Button.css";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const LogoutButton: React.FC = () => {
  const handleLogout = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/logout-session`,
        {},
        { withCredentials: true }
      );
      localStorage.clear();
      sessionStorage.clear();

      window.location.href = "/login";
    } catch (error) {
      console.error("Failed to logout:", error);
    }
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
