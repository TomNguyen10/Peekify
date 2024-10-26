import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import React, { useEffect, useState } from "react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { url } from "inspector";
import { Car } from "lucide-react";

const jsonString = sessionStorage.getItem("userInfo");
const userInfo = jsonString ? JSON.parse(jsonString) : null;

export const HomePage: React.FC = () => {
  const [topTracks, setTopTracks] = useState<any>(null);
  const [topArtists, setTopArtists] = useState<any>(null);

  useEffect(() => {
    if (userInfo) {
      setTopArtists({
        long_term: userInfo.top_items.long_term.top_artists,
        medium_term: userInfo.top_items.medium_term.top_artists,
        short_term: userInfo.top_items.short_term.top_artists,
      });
      setTopTracks({
        long_term: userInfo.top_items.long_term.top_tracks,
        medium_term: userInfo.top_items.medium_term.top_tracks,
        short_term: userInfo.top_items.short_term.top_tracks,
      });
    }
  }, []);

  const renderArtists = (artists: any) =>
    artists && artists.length > 0 ? (
      artists.map((artist: any, index: number) => (
        <div
          key={index}
          className="p-4 flex flex-col items-center justify-center text-center align-center"
        >
          <img
            src={artist.images[1]?.url}
            alt={`${artist.name}'s image`}
            className="w-48 h-48 object-cover"
          />
          <p className="text-lg font-medium leading-none mt-2">
            {index + 1}. {artist.name}
          </p>
        </div>
      ))
    ) : (
      <div>No top artists found.</div>
    );

  const renderTracks = (tracks: any) =>
    tracks && tracks.length > 0 ? (
      tracks.map((track: any, index: number) => (
        <div key={index} className="flex items-center gap-4">
          {index + 1}
          <Avatar className="hidden h-9 w-9 sm:flex">
            <AvatarImage src={track.album.images[1]?.url} alt={track.name} />
            <AvatarFallback />
          </Avatar>
          <div className="grid gap-1">
            <p className="text-sm font-medium leading-none">{track.name}</p>
          </div>
          <div className="ml-auto text-sm">{track.album.name}</div>
        </div>
      ))
    ) : (
      <div>No top tracks found.</div>
    );

  const termLabels: {
    long_term: string;
    medium_term: string;
    short_term: string;
  } = {
    long_term: "This Year",
    medium_term: "This Past 4 Months",
    short_term: "This Month",
  };

  // Explicitly define the type for term as a union type
  const terms: Array<"long_term" | "medium_term" | "short_term"> = [
    "short_term",
    "medium_term",
    "long_term",
  ];

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

      {terms.map((term) => (
        <div className="grid gap-8 m-8 mb-12 px-20">
          <h1 className="text-4xl font-bold mb-8 text-center text-white">
            {termLabels[term]}
          </h1>
          <div key={term}>
            <Card>
              <CardHeader>
                <CardTitle className="align-center justify-center">
                  Top Artist
                </CardTitle>
              </CardHeader>
              <CardContent className="flex flex-wrap gap-3">
                {renderArtists(topArtists?.[term])}
              </CardContent>

              <CardHeader className="flex flex-row items-center mt-4">
                <CardTitle>Top Tracks and their Album</CardTitle>
              </CardHeader>
              <CardContent className="grid gap-8">
                {renderTracks(topTracks?.[term])}
              </CardContent>
            </Card>

          </div>
        </div>
      ))}
    </>
  );
};
