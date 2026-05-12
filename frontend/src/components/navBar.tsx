import "../index.css";
import { LogIn } from "lucide-react";
import UserStats from "./userStats";
import { useLocation, useNavigate } from "react-router-dom";
import { User } from "../utils/user";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface NavBarProps {
  score: number;
}

export default function TrendmineNavBar({ score }: NavBarProps) {
  const navItems = [
    { label: "Home", href: "/" },
    { label: "Topics", href: "/topics" },
  ];
  const [user, setUser] = useState<User | null>(null);

  const location = useLocation();
  const navigate = useNavigate();
  useEffect(() => {
    setUser(User.current());
  }, [location.pathname]);

  return (
    <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-primary/5">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-black italic tracking-tighter text-primary">
              TRENDMINE
            </span>
          </Link>
        </div>

        <div className="hidden md:flex items-center gap-8">
          {navItems.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <button
                key={item.label}
                className={`font-headline font-bold text-sm transition-all hover:scale-105 ${
                  isActive
                    ? "text-primary border-b-2 border-primary"
                    : "text-on-surface/60 hover:text-on-surface"
                }`}
                onClick={() => navigate(item.href)}
              >
                {item.label}
              </button>
            );
          })}
        </div>
        {user ? (
          <UserStats
            score={score}
            name={user.name}
            best={user.score}
            setUser={setUser}
          />
        ) : (
          <div className="flex items-center gap-3">
            <button
              className="flex items-center gap-2 bg-gradient-to-br from-primary to-primary-container text-on-primary px-6 py-2.5 rounded-full font-display font-bold text-sm shadow-lg shadow-primary/20 hover:scale-105 transition-all"
              onClick={() => navigate("/log_in")}
            >
              <LogIn size={16} strokeWidth={3} />
              Login/Sign In
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
