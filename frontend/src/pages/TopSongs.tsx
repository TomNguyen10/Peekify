// TopArtists.tsx
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const TopSongs: React.FC = () => {
  const [topSongs, setTopSongs] = useState<any>(null);
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
        const topSongsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-songs-this-week`,
          {
            params: { user_spotify_id: userInfo.id, limit: 20 },
          }
        );
        if (Array.isArray(topSongsResponse.data)) {
          setTopSongs(topSongsResponse.data);
        } else {
          console.error(
            "Unexpected format for top songs:",
            topSongsResponse.data
          );
          setTopSongs([]); // Set to an empty array or handle as needed
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
        Your Top Songs From Last Week
      </h1>
      <div className="max-w-3xl mx-auto">
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-right">No.</TableHead>
                  <TableHead>Track Name</TableHead>
                  <TableHead>Artist Name</TableHead>
                  <TableHead>Play Count</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {topSongs && topSongs.length > 0 ? (
                  topSongs.map((song: any, index: number) => (
                    <TableRow key={index}>
                      <TableCell className="text-right">{index + 1}</TableCell>
                      <TableCell>
                        <div className="font-medium">{song.track_name}</div>
                      </TableCell>
                      <TableCell>{song.artist_name}</TableCell>
                      <TableCell className="text-center">
                        {song.play_count}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center">
                      Loading... or please come back later
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
