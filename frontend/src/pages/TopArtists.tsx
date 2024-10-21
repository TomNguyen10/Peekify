// TopArtists.tsx
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";


const API_BASE_URL = "http://localhost:8000";

export const TopArtists: React.FC = () => {
  const [topArtists, setTopArtists] = useState<any>(null);
  const [userInfo, setUserInfo] = useState<any>(null);

  useEffect(() => {
    const storedUserInfo = sessionStorage.getItem("userInfo");
    if (storedUserInfo) {
      setUserInfo(JSON.parse(storedUserInfo)); 
    }
  }, []);

  // Fetch songs per day, top songs, and top artists data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const topArtistsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-artists-this-week`,
          {
            params: { user_spotify_id: userInfo.id, limit: 10 },
          }
        );
        if (Array.isArray(topArtistsResponse.data)) {
          setTopArtists(topArtistsResponse.data);
        } else {
          console.error(
            "Unexpected format for top artists:",
            topArtistsResponse.data
          );
          setTopArtists([]); // Set to an empty array or handle as needed
        }
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    if (userInfo) {
      fetchData();
    }
  }, [userInfo]);
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8 text-center text-white">
        Your Top Artists From Last Week
      </h1>
      <div className="max-w-3xl mx-auto">
        <Card>
          <CardHeader></CardHeader>
          <CardContent className="grid gap-8">
            {topArtists && topArtists.length > 0 ? (
              topArtists.map((artist: any, index: number) => (
                <div className="flex items-center gap-4" key={index}>
                  <Avatar className="hidden h-9 w-9 sm:flex">
                    <AvatarImage
                      src={artist.image_160x160}
                      alt={artist.artist_name}
                    />
                    <AvatarFallback />
                  </Avatar>
                  <div className="grid gap-1">
                    <p className="text-sm font-medium leading-none">
                      {artist.artist_name}
                    </p>
                  </div>
                  <div className="ml-auto font-medium">
                    {artist.play_count} plays
                  </div>
                </div>
              ))
            ) : (
              <div>Loading...</div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
