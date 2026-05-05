import React, { useState } from "react";
import { BarChart3, Settings } from "lucide-react";
import SettingsMenu from "./settingsMenu";
import { User } from "../utils/user";

interface UserStatsProps {
  name: string;
  score: number;
  best: number;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const UserStats: React.FC<UserStatsProps> = ({
  score,
  best,
  name,
  setUser,
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="flex items-center gap-6">
      {/* Score Labels */}
      <div className="flex flex-col items-end">
        <span className="text-primary font-headline font-bold tracking-tight">
          Score: {score}
        </span>
        <span className="text-[10px] uppercase tracking-wider opacity-60 font-bold text-on-surface">
          Best: {best}
        </span>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2">
        <span className="text-primary font-headline font-bold tracking-tight">
          {name}
        </span>
        <button
          title="Statistics"
          className="p-2 rounded-full hover:bg-primary/10 text-primary transition-all active:scale-90"
        >
          <BarChart3 size={20} />
        </button>

        <div className="relative">
          <button
            title="Settings"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className={`p-2 rounded-full transition-all active:scale-90 ${
              isMenuOpen
                ? "bg-primary text-white"
                : "hover:bg-primary/10 text-primary"
            }`}
          >
            <Settings size={20} />
          </button>

          {/* The Menu will now appear right under the button, aligned to the right */}
          <SettingsMenu
            isOpen={isMenuOpen}
            onLogout={() => {
              setIsMenuOpen(false);
              User.logout();
              setUser(User.current);
              console.log("Logout triggered");
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default UserStats;
