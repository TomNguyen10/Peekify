import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import axios from "axios";

interface NavbarProps {
  handleLogout: () => Promise<void>;
}

export const Navbar: React.FC<NavbarProps> = ({ handleLogout }) => {
  return (
    <header className="sticky top-0 flex h-16 items-center gap-4 bg-background px-4 md:px-6 rounded-sm w-full z-50">
      <nav className="hidden flex-grow flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
        <Link
          to="/home"
          className="text-foreground transition-colors hover:text-foreground "
        >
          <img
            src="../../src/assets/Peekify-logo-3.png"
            alt="peekify logo"
            className="w-auto h-7 object-contain"
          />
        </Link>
        <Link
          to="/home"
          className="text-foreground transition-colors hover:text-foreground "
        >
          Home
        </Link>
        <Link
          to="/dashboard"
          className="text-foreground transition-colors hover:text-foreground "
        >
          Dashboard
        </Link>
        <Link
          to="/top-songs"
          className="text-foreground transition-colors hover:text-foreground "
        >
          Top Songs
        </Link>
        <Link
          to="/top-artists"
          className="text-foreground transition-colors hover:text-foreground "
        >
          Top Artists
        </Link>
        <Link
          to="/songs-per-day"
          className="text-foreground transition-colors hover:text-foreground "
        >
          Songs per Day
        </Link>
        <Button onClick={handleLogout} className="hover:bg-green-600 ml-auto">
          Log Out
        </Button>
      </nav>
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="shrink-0 md:hidden">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="grid gap-6 text-lg font-medium">
            <Link to="/home">
              <img
                src="../../src/assets/Peekify-logo-2.png"
                alt="peekify logo"
              />
            </Link>
            <Link to="/home" className="hover:text-foreground">
              Home
            </Link>
            <Link to="/dashboard" className="hover:text-foreground">
              Dashboard
            </Link>
            <Link to="/top-songs" className="hover:text-foreground">
              Top Songs
            </Link>
            <Link to="/top-artists" className="hover:text-foreground">
              Top Artists
            </Link>
            <Link to="/songs-per-day" className="hover:text-foreground">
              Songs per Day
            </Link>
            <Button
              onClick={handleLogout}
              className="hover:bg-green-600 ml-auto"
            >
              Log Out
            </Button>
          </nav>
        </SheetContent>
      </Sheet>
    </header>
  );
};
