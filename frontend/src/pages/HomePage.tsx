import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";


export const HomePage: React.FC = () => {
  const jsonString = localStorage.getItem("userInfo");
  let userInfo;
  if (jsonString) {
    userInfo = JSON.parse(jsonString);
  }
  return (
    <>
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
    </>
  );
};
