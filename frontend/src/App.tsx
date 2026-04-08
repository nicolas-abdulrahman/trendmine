import "./index.css";
import { useState, ReactNode } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Trophy,
  BookOpen,
  PartyPopper,
  Settings,
  BarChart3,
  Globe,
  Share2,
  ChevronRight,
} from "lucide-react";

interface ThemeCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  colorClass: string;
  iconBgClass: string;
  iconColorClass: string;
  lineColorClass: string;
  delay: number;
}

const ThemeCard = ({
  title,
  description,
  icon,
  colorClass,
  iconBgClass,
  iconColorClass,
  lineColorClass,
  delay,
}: ThemeCardProps) => {
  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }}
      whileHover={{ y: -16, scale: 1.02 }}
      className={`group relative flex flex-col items-center p-10 rounded-xl ${colorClass} transition-all duration-500 overflow-hidden cursor-pointer w-full`}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

      <motion.div
        whileHover={{ scale: 1.1 }}
        className={`w-32 h-32 rounded-full ${iconBgClass} flex items-center justify-center mb-8 relative z-10 transition-transform duration-500`}
      >
        <div className={iconColorClass}>{icon}</div>
      </motion.div>

      <h2 className="font-headline text-3xl font-bold text-on-surface relative z-10">
        {title}
      </h2>
      <p className="font-body text-on-surface-variant mt-3 text-sm opacity-80 relative z-10">
        {description}
      </p>

      <div
        className={`mt-8 w-12 h-1 ${lineColorClass} rounded-full group-hover:w-24 transition-all duration-500`}
      />
    </motion.button>
  );
};

export default function App() {
  const [score] = useState(0);
  const [best] = useState(12);

  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-primary/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-black italic tracking-tighter text-primary">
              PULSE DUEL
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
          <div className="h-screen bg-red-500 flex items-center justify-center">
            <h1 className="text-5xl text-white font-bold">
              Tailwind is Active
            </h1>
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

      <main className="flex-grow flex flex-col items-center justify-center px-6 py-12 relative overflow-hidden">
        {/* Ambient Background Glows */}
        <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] bg-primary-container/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] bg-secondary-container/10 rounded-full blur-[120px] pointer-events-none" />

        <div className="w-full max-w-6xl z-10">
          <header className="text-center mb-16">
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="font-headline text-5xl md:text-7xl font-extrabold tracking-tighter text-on-surface mb-4 text-shadow-glow"
            >
              Which is more{" "}
              <span className="text-primary italic">searched?</span>
            </motion.h1>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="font-body text-on-surface-variant text-lg md:text-xl max-w-2xl mx-auto"
            >
              Test your intuition against global trends. Pick a theme to start
              the duel.
            </motion.p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10">
            <ThemeCard
              title="Football"
              description="Clubs, Players, Leagues"
              icon={<Trophy size={48} strokeWidth={1.5} />}
              colorClass="bg-surface-container-low hover:bg-surface-container"
              iconBgClass="bg-primary-container"
              iconColorClass="text-on-primary-container"
              lineColorClass="bg-primary"
              delay={0.3}
            />
            <ThemeCard
              title="Books"
              description="Literature, Authors, Genres"
              icon={<BookOpen size={48} strokeWidth={1.5} />}
              colorClass="bg-surface-container-high hover:bg-surface-container-highest"
              iconBgClass="bg-tertiary-container"
              iconColorClass="text-on-tertiary-container"
              lineColorClass="bg-tertiary-container"
              delay={0.4}
            />
            <ThemeCard
              title="Events"
              description="History, Holidays, Festivals"
              icon={<PartyPopper size={48} strokeWidth={1.5} />}
              colorClass="bg-secondary-container/20 hover:bg-secondary-container/40"
              iconBgClass="bg-secondary-container"
              iconColorClass="text-on-secondary-container"
              lineColorClass="bg-secondary"
              delay={0.5}
            />
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7 }}
            className="mt-20 flex justify-center"
          >
            <button className="group relative bg-gradient-to-r from-primary to-primary-container text-on-primary font-headline font-bold py-5 px-12 rounded-full text-xl shadow-xl shadow-primary/20 hover:scale-105 hover:brightness-110 transition-all duration-300 active:scale-95 flex items-center gap-3">
              Surprise Me
              <ChevronRight className="group-hover:translate-x-1 transition-transform" />
            </button>
          </motion.div>
        </div>

        {/* Side Bento Cards (Desktop Only) */}
        <aside className="hidden xl:flex flex-col gap-6 absolute right-12 top-1/2 -translate-y-1/2 w-72">
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 }}
            className="p-6 rounded-2xl bg-surface-container-low border-l-4 border-primary shadow-sm"
          >
            <p className="text-[10px] font-bold uppercase tracking-widest text-primary mb-2">
              Trend Report
            </p>
            <h4 className="font-headline font-bold text-on-surface leading-tight">
              "Super Bowl" is peaking right now.
            </h4>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9 }}
            className="p-6 rounded-2xl bg-surface-container-low border-l-4 border-secondary shadow-sm"
          >
            <p className="text-[10px] font-bold uppercase tracking-widest text-secondary mb-2">
              Did you know?
            </p>
            <h4 className="font-headline font-bold text-on-surface leading-tight">
              Football is searched 4x more than Baseball globally.
            </h4>
          </motion.div>
        </aside>
      </main>

      <footer className="bg-surface-container-low/50 border-t border-primary/5">
        <div className="max-w-7xl mx-auto px-12 py-10 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex flex-col items-center md:items-start gap-1">
            <span className="text-lg font-black text-primary italic">
              PULSE DUEL
            </span>
            <span className="text-[10px] font-medium tracking-widest uppercase opacity-40">
              © 2024 THE ELECTRIC PLAYGROUND
            </span>
          </div>

          <div className="flex gap-8">
            {["Privacy", "Terms", "Support"].map((link) => (
              <a
                key={link}
                href="#"
                className="text-xs font-bold uppercase tracking-widest text-on-surface/40 hover:text-primary transition-colors"
              >
                {link}
              </a>
            ))}
          </div>

          <div className="flex gap-4">
            <button className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center hover:scale-110 hover:bg-primary/10 text-primary transition-all">
              <Globe size={18} />
            </button>
            <button className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center hover:scale-110 hover:bg-primary/10 text-primary transition-all">
              <Share2 size={18} />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

