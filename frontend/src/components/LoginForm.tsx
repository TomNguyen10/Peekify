import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface LoginFormProps {
  handleLogin: () => void;
}

export function LoginForm({ handleLogin }: LoginFormProps) {
  return (
    <Card className="mx-auto w-full max-w-sm bg-black border-black">
      <CardContent>
        <Button
          type="button"
          className="w-64 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded text-black"
          onClick={handleLogin}
        >
          Login with Spotify
        </Button>
      </CardContent>
    </Card>
  );
}
