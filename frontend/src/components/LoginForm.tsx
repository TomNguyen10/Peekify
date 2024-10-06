import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface LoginFormProps {
  handleLogin: () => void;
}

export function LoginForm({ handleLogin }: LoginFormProps) {
  return (
    <Card className="mx-auto w-full max-w-sm bg-black border-black">
      <CardContent>
        <Button
          type="button"
          className="w-full sm:w-auto bg-green-500 hover:bg-green-600 font-bold py-2 px-4 rounded text-black"
          onClick={handleLogin}
        >
          Login with Spotify
        </Button>
      </CardContent>
    </Card>
  );
}
