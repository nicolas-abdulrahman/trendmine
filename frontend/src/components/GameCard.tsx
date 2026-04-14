import { motion } from "motion/react";
import { TrendingUp, History, ChevronRight } from "lucide-react";
import { getTopicImage } from "../utils/getTopicImage";

export interface Topic {
  id: string;
  name: string;
  imageUrl: string;
  searchVolume: number;
  icon: "trending" | "history";
}

export interface GameCardProps {
  topic: Topic | null;
  onClick: () => void;
  isRevealing: boolean;
  side: "left" | "right";
}
export default function GameCard({
  topic,
  onClick,
  isRevealing,
  side,
}: GameCardProps) {
  const gradientClass =
    side === "left"
      ? "from-primary/80 via-transparent to-transparent"
      : "from-secondary/80 via-transparent to-transparent";
  if (!topic) {
    return (
      <div
        className={`w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden rounded-2xl bg-surface-container-high animate-pulse ${
          side === "left"
            ? "rounded-t-2xl lg:rounded-l-2xl lg:rounded-tr-none"
            : "rounded-b-2xl lg:rounded-r-2xl lg:rounded-bl-none"
        }`}
      />
    );
  }

  return (
    <motion.button
      type="button"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      disabled={isRevealing}
      className={`group w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden transition-all duration-500 bg-surface-container-high ${
        side === "left"
          ? "rounded-t-2xl lg:rounded-l-2xl lg:rounded-tr-none"
          : "rounded-b-2xl lg:rounded-r-2xl lg:rounded-bl-none"
      }`}
    >
      <img
        src={topic.imageUrl}
        alt={topic.name}
        referrerPolicy="no-referrer"
        className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 brightness-75 group-hover:brightness-100"
      />
      <div
        className={`absolute inset-0 bg-gradient-to-t ${gradientClass} opacity-60`}
      />

      <div className="absolute bottom-0 left-0 right-0 p-10 text-left">
        <motion.div
          layout
          className="font-headline text-3xl md:text-5xl font-black text-white leading-none tracking-tighter"
        >
          {topic.name.split(" ").map((word, i) => (
            <span key={i}>
              {word}
              <br />
            </span>
          ))}
        </motion.div>

        {isRevealing && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 text-white"
          >
            <div className="text-sm font-bold opacity-70 uppercase tracking-widest">
              Search Volume
            </div>
            <div className="text-3xl md:text-4xl font-black font-headline">
              {topic.searchVolume.toLocaleString()}
            </div>
          </motion.div>
        )}
      </div>

      <div className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white">
          <ChevronRight size={24} />
        </div>
      </div>
    </motion.button>
  );
}
