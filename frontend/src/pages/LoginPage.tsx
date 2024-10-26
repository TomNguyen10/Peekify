import React from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface LoginPageProps {
  handleLogin: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ handleLogin }) => {
  return (
    <div className="min-h-screen relative w-full bg-black flex flex-col md:flex-row justify-center items-center">
      <div className="flex flex-col items-center justify-center w-full h-full md:w-1/2 text-white text-3xl sm:flex">
        <img
          src="/Peekify-logo.png"
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

        <Card className="mx-auto w-full max-w-sm bg-black border-black">
          <CardContent>
            <Button
              type="button"
              className="w-full sm:w-auto bg-green-500 hover:bg-green-600 font-bold py-2 px-4 rounded text-black"
              onClick={handleLogin}>
              Login with Spotify
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
