import "../index.css";
import { BarChart3, Settings } from "lucide-react";

interface NavBarProps {
  score: number;
  best: number;
}

export default function TrendmineNavBar({ score, best }: NavBarProps) {
  return (
    <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-primary/5">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-black italic tracking-tighter text-primary">
            TRENDMINE
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          {["Play", "Themes", "Leaderboard"].map((item) => (
            <button
              key={item}
              className={`font-headline font-bold text-sm transition-all hover:scale-105 ${
                item === "Themes"
                  ? "text-primary border-b-2 border-primary"
                  : "text-on-surface/60 hover:text-on-surface"
              }`}
            >
              {item}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-6">
          <div className="flex flex-col items-end">
            <span className="text-primary font-headline font-bold tracking-tight">
              Score: {score}
            </span>
            <span className="text-[10px] uppercase tracking-wider opacity-60 font-bold">
              Best: {best}
            </span>
          </div>
          <div className="flex gap-2">
            <button className="p-2 rounded-full hover:bg-primary/10 text-primary transition-colors">
              <BarChart3 size={20} />
            </button>
            <button className="p-2 rounded-full hover:bg-primary/10 text-primary transition-colors">
              <Settings size={20} />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
