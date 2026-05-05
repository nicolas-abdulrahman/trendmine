import { motion } from "motion/react";
import { Trophy, Cpu, Dna, ChevronRight, Gamepad } from "lucide-react";
import { useNavigate } from "react-router-dom";
import ThemeCard from "../components/ThemeCard";

export default function Home() {
  const navigate = useNavigate();

  return (
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
            Oque é mais buscado
            <span className="text-primary italic"> buscado?</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="font-body text-on-surface-variant text-lg md:text-xl max-w-2xl mx-auto"
          >
            Teste seu conhecimento com o que é mais buscado no Wikipedia.
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
            seed="football"
          />
          <ThemeCard
            title="Technology"
            description="Languages, Software, Companies & Concepts"
            icon={<Cpu size={48} strokeWidth={1.5} />}
            colorClass="bg-surface-container-high hover:bg-surface-container-highest"
            iconBgClass="bg-tertiary-container"
            iconColorClass="text-on-tertiary-container"
            lineColorClass="bg-tertiary-container"
            delay={0.4}
            seed="tech"
          />
          <ThemeCard
            title="Games"
            description="Strategy, Adventure, RPG & Simulation"
            icon={<Gamepad size={48} strokeWidth={1.5} />}
            colorClass="bg-secondary-container/20 hover:bg-secondary-container/40"
            iconBgClass="bg-secondary-container"
            iconColorClass="text-on-secondary-container"
            lineColorClass="bg-secondary"
            delay={0.5}
            seed="games"
          />
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-20 flex justify-center"
        >
          <button
            type="button"
            onClick={() => navigate("/battle")}
            className="group relative bg-gradient-to-r from-primary to-primary-container text-on-primary font-headline font-bold py-5 px-12 rounded-full text-xl shadow-xl shadow-primary/20 hover:scale-105 hover:brightness-110 transition-all duration-300 active:scale-95 flex items-center gap-3"
          >
            Surprise Me
            <ChevronRight className="group-hover:translate-x-1 transition-transform" />
          </button>
        </motion.div>
      </div>
    </main>
  );
}
