import { Link } from "react-router-dom";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { ArrowUpRight, Menu } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// import {
//   DropdownMenu,
//   DropdownMenuContent,
//   DropdownMenuItem,
//   DropdownMenuLabel,
//   DropdownMenuSeparator,
//   DropdownMenuTrigger,
// } from "@frontend/src/components/ui/dropdown-menu.tsx";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import SongsPerDay from "@/pages/SongsPerDay";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface DashboardProps {
  userInfo: any;
}

const API_BASE_URL = "http://localhost:8000";

export const Dashboard: React.FC<DashboardProps> = ({ userInfo }) => {
  const [topSongs, setTopSongs] = useState<any>(null);
  const [topArtists, setTopArtists] = useState<any>(null);

  // Fetch songs per day, top songs, and top artists data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const topSongsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-songs-this-week`,
          {
            params: { user_spotify_id: userInfo.id, limit: 8 },
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

        const topArtistsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-artists-this-week`,
          {
            params: { user_spotify_id: userInfo.id },
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
    <div className="min-h-screen w-full ">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8 text-center text-white">
          Your Music Dashboard
        </h1>
        <div className="mt-8">
          <SongsPerDay userInfo={userInfo} />
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          <Card>
            <CardHeader className="flex flex-row items-center">
              <div className="grid gap-2">
                <CardTitle>Top Songs from Last Week</CardTitle>
              </div>
              <Button asChild size="sm" className="ml-auto gap-1">
                <Link to="/top-songs">
                  View All <ArrowUpRight className="h-4 w-4" />{" "}
                </Link>
              </Button>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Track Name</TableHead>
                    <TableHead>Artist Name</TableHead>
                    <TableHead>Play Count</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {topSongs && topSongs.length > 0 ? (
                    topSongs.map((song: any, index: number) => (
                      <TableRow key={index}>
                        <TableCell>
                          <div className="font-medium">{song.track_name}</div>
                        </TableCell>
                        <TableCell>{song.artist_name}</TableCell>
                        <TableCell className="text-right">
                          {song.play_count}
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={3} className="text-center">
                        No top songs found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center">
              <div className="grid gap-2">
                <CardTitle>Top Artists from Last Week</CardTitle>
              </div>
              <Button asChild size="sm" className="ml-auto gap-1">
                <Link to="/top-artists">
                  View All
                  <ArrowUpRight className="h-4 w-4" />
                </Link>
              </Button>
            </CardHeader>
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
                <div>No top artists found.</div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};
