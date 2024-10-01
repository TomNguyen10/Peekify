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
    <div className="mx-auto w-full max-w-sm">
      <Card className="mx-auto w-full max-w-sm bg-white">
        <CardHeader>
          <CardTitle className="text-2xl text-center">Login</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <Button
              type="button"
              className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
              onClick={handleLogin}
            >
              Login with Spotify
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
