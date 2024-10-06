import { Link } from "react-router-dom";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { ArrowUpRight, Menu } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface DashboardProps {
  handleLogout: () => Promise<void>;
  userInfo: any;
}

const API_BASE_URL = "http://localhost:8000";

export const Dashboard: React.FC<DashboardProps> = ({
  handleLogout,
  userInfo,
}) => {
  const [songsPerDay, setSongsPerDay] = useState<any>(null);
  const [topSongs, setTopSongs] = useState<any>(null);
  const [topArtists, setTopArtists] = useState<any>(null);

  // Fetch songs per day, top songs, and top artists data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // const songsPerDayResponse = await axios.get(
        //   `${API_BASE_URL}/top_items/songs-per-day`,
        //   {
        //     params: { user_spotify_id: userInfo.spotify_id },
        //   }
        // );
        // setSongsPerDay(songsPerDayResponse.data.songs_per_day);

        const topSongsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-songs-this-week`,
          {
            params: { user_spotify_id: userInfo.id, limit: 10 },
          }
        );
        setTopSongs(topSongsResponse.data.top_songs);

        const topArtistsResponse = await axios.get(
          `${API_BASE_URL}/top_items/top-artists-this-week`,
          {
            params: { user_spotify_id: userInfo.id },
          }
        );
        setTopArtists(topArtistsResponse.data.top_artists);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    if (userInfo) {
      fetchData();
    }
  }, [userInfo]);

  return (
    <div className="flex min-h-screen w-full flex-col">
      <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Songs per Day
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {songsPerDay ? songsPerDay : "Loading..."}
              </div>
              {/* <p className="text-xs text-muted-foreground">
                +100% from last week
              </p> */}
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Listening Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Hello</div>
              {/* <p className="text-xs text-muted-foreground">+180.1% from week</p> */}
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Songs Listened
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold"></div>
              {/* <p className="text-xs text-muted-foreground">
                +19% from last week
              </p> */}
            </CardContent>
          </Card>
          {/* <Card x-chunk="dashboard-01-chunk-3">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Now</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">+573</div>
              <p className="text-xs text-muted-foreground">
                +201 since last hour
              </p>
            </CardContent>
          </Card> */}
        </div>
        <div className="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-3">
          <Card className="xl:col-span-2" x-chunk="dashboard-01-chunk-4 ">
            <CardHeader className="flex flex-row items-center">
              <div className="grid gap-2">
                <CardTitle>Top Songs from Last Week</CardTitle>
              </div>
              <Button asChild size="sm" className="ml-auto gap-1">
                <Link to="#top-songs">
                  View All
                  <ArrowUpRight className="h-4 w-4" />
                </Link>
              </Button>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Track Name</TableHead>
                    <TableHead>Artist Name</TableHead>
                    <TableHead className="text-right">Play Count</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {topSongs
                    ? topSongs.map((song: any, index: number) => (
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
                    : "Loading..."}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          <Card x-chunk="dashboard-01-chunk-5">
            <CardHeader className="flex flex-row items-center">
              <div className="grid gap-2">
                <CardTitle>Top Artists from Last Week</CardTitle>
              </div>
              <Button asChild size="sm" className="ml-auto gap-1">
                <Link to="#top-artists">
                  View All
                  <ArrowUpRight className="h-4 w-4" />
                </Link>
              </Button>
            </CardHeader>
            <CardContent className="grid gap-8">
              {topArtists
                ? topArtists.map((artist: any, index: number) => (
                    <div className="flex items-center gap-4">
                      <Avatar className="hidden h-9 w-9 sm:flex">
                        <AvatarImage src="/avatars/01.png" alt="Avatar" />
                        <AvatarFallback></AvatarFallback>
                      </Avatar>
                      <div className="grid gap-1">
                        <p
                          className="text-sm font-medium leading-none"
                          key={index}
                        >
                          {artist.artist_name}
                        </p>
                      </div>
                      <div className="ml-auto font-medium">
                        {artist.play_count} plays
                      </div>
                    </div>
                  ))
                : "Loading..."}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};
