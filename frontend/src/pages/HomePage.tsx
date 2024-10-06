import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import { Navbar } from "../components/Navbar";
import { TopArtists } from "../pages/TopArtists";
import { Dashboard } from "@/components/Dashboard";
import { TopSongs } from "./TopSongs";
import { SongsPerDay } from "./SongsPerDay";

interface HomePageProps {
  handleLogout: () => Promise<void>;
  userInfo: any;
}

export const HomePage: React.FC<HomePageProps> = ({
  handleLogout,
  userInfo,
}) => {
  return (
    <>
      <Navbar handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Navigate to="/" />} />
        <Route
          path="/dashboard"
          element={
            <Dashboard handleLogout={handleLogout} userInfo={userInfo} />
          }
        />
        <Route path="/top-songs" element={<TopSongs />} />
        <Route path="/top-artists" element={<TopArtists />} />
        <Route path="/songs-per-day" element={<SongsPerDay />} />
      </Routes>
    </>
  );
};
