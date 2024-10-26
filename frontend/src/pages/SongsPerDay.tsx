"use client";

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import { useEffect, useState } from "react";
import axios from "axios";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "../components/ui/chart";
import { Avatar, AvatarImage, AvatarFallback } from "@radix-ui/react-avatar";

export const description = "A multiple bar chart";

const chartConfig = {
  song_count: {
    label: "Song Counts",
    color: "hsl(var(--chart-1))",
  },
  time_count: {
    label: "Total Time",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const SongsPerDay: React.FC = () => {
  const [chartData, setChartData] = useState<any[]>([]);
  const [weekRange, setWeekRange] = useState<string>("");
  const [totalSongs, setTotalSongs] = useState<number>(0); // State for total songs
  const [totalListeningTime, setTotalListeningTime] = useState<number>(0); // State for total listening time
  const [topAlbum, setTopAlbum] = useState<any>(null);
  const [userInfo, setUserInfo] = useState<any>(null);

  useEffect(() => {
    const storedUserInfo = sessionStorage.getItem("userInfo");
    if (storedUserInfo) {
      setUserInfo(JSON.parse(storedUserInfo)); // Parse the JSON string
    }
  }, []);

  // Calculate the week range from Monday to Sunday
  useEffect(() => {
    const today = new Date();
    const currentDay = today.getDay(); // Sunday - Saturday : 0 - 6
    const monday = new Date(today);
    const sunday = new Date(today);

    // Calculate Monday's date
    monday.setDate(today.getDate() - ((currentDay + 6) % 7));
    // Calculate Sunday's date
    sunday.setDate(today.getDate() + ((7 - currentDay) % 7));

    // Format dates to YYYY-MM-DD
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    };

    const mondayFormatted = monday.toLocaleDateString("en-CA", options); // ISO format
    const sundayFormatted = sunday.toLocaleDateString("en-CA", options); // ISO format

    setWeekRange(`From ${mondayFormatted} to ${sundayFormatted}`);
  }, []);

  // Fetch the songs per day data
  useEffect(() => {
    const fetchSongsPerDayData = async () => {
      if (userInfo && userInfo.id) {
        try {
          const songsPerDayResponse = await axios.get(
            `${API_BASE_URL}/top_items/songs-per-day`,
            {
              params: { user_spotify_id: userInfo.id },
            }
          );
          const data = songsPerDayResponse.data;

          // Transform the response to match the chartData structure
          const transformedData = data.map((item: any) => ({
            day: item.day,
            song_count: item.song_count,
            total_duration_seconds: item.total_duration_seconds, // Include total duration
          }));

          setChartData(transformedData);

          // Calculate the total songs listened in the week
          const total = transformedData.reduce(
            (acc: number, item: { song_count: number }) =>
              acc + item.song_count,
            0
          );
          setTotalSongs(total);

          // Calculate the total listening time in hours
          const totalTime = transformedData.reduce(
            (acc: number, item: { total_duration_seconds: number }) =>
              acc + item.total_duration_seconds,
            0
          );
          setTotalListeningTime(totalTime / 3600000); // Convert seconds to hours

          const albumResponse = await axios.get(
            `${API_BASE_URL}/top_items/top-albums-this-week`,
            {
              params: { user_spotify_id: userInfo.id, limit: 4 },
            }
          );
          const albumData = albumResponse.data;
          setTopAlbum(albumData);
        } catch (error) {
          console.error("Failed to fetch songs per day data:", error);
        }
      }
    };

    // Fetch only if userInfo is available
    if (userInfo) {
      fetchSongsPerDayData();
    }
  }, [userInfo]);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Songs Per Day</CardTitle>
            <CardDescription>{weekRange}</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px] md:h-[400px] lg:h-[500px] items-center">
            <ChartContainer config={chartConfig}>
              <BarChart data={chartData}>
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="day"
                  tickLine={false}
                  tickMargin={10}
                  axisLine={false}
                  tickFormatter={(value) => value.slice(0, 3)}
                />
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent indicator="dashed" />}
                />
                <Bar
                  dataKey="song_count"
                  fill="var(--color-desktop)"
                  radius={4}
                />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>
        <div className="md:col-span-1">
          <Card className="mb-5">
            <CardHeader>
              <CardTitle className="text-sm font-medium">
                Total Listening Time
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalListeningTime.toFixed(2)} hours
              </div>
            </CardContent>
          </Card>

          <Card className="mb-5">
            <CardHeader>
              <CardTitle className="text-sm font-medium">
                Total Songs Listened
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalSongs}</div>
            </CardContent>
          </Card>

          <Card className="mb-5">
            <CardHeader>
              <CardTitle className="text-sm font-medium">
                Average Songs Per Day
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(totalSongs / 7).toFixed(2)}
              </div>
            </CardContent>
          </Card>

          <Card className="mb-5">
            <CardHeader>
              <CardTitle className="text-sm font-medium">
                Your Top Album
              </CardTitle>
            </CardHeader>
            <CardContent>
              {topAlbum && topAlbum.length > 0 ? (
                topAlbum.map((album: any, index: number) => (
                  <div
                    className="flex items-center gap-4 pt-3 pb-3"
                    key={index}>
                    <Avatar className="hidden h-9 w-9 sm:flex">
                      <AvatarImage
                        src={album.album_image_64x64}
                        alt={album.name}
                      />
                      <AvatarFallback />
                    </Avatar>
                    <div className="grid gap-1">
                      <p className="text-md font-medium leading-none">
                        {album.name}
                      </p>
                    </div>
                    <div className="ml-auto font-medium">
                      {album.play_count} plays
                    </div>
                  </div>
                ))
              ) : (
                <div>No top album found. Or please come back later</div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SongsPerDay;
