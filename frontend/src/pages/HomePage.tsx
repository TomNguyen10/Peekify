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
const Home: React.FC<{ userInfo: any }> = ({ userInfo }) => {
  return (
    <div className="welcome-container flex flex-col items-center justify-center text-white h-screen bg-gradient-to-b from-black-600 to-green-600">
      <div className="text-center p-6 rounded-lg shadow-lg bg-opacity-80 bg-green-900">
        <h1 className="text-4xl font-bold mb-4">
          Welcome, {userInfo.display_name}!
        </h1>
        <p className="text-lg">We're excited to have you on Peekify!</p>
        <p className="text-sm mt-2 text-gray-400">
          Enjoy exploring your favorite songs and artists.
        </p>
      </div>
    </div>
  );
};

export const HomePage: React.FC<HomePageProps> = ({
  handleLogout,
  userInfo,
}) => {
  return (
    <>
      <Navbar handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Home userInfo={userInfo} />} />
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
