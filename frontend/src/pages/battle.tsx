import { useCallback, useEffect, useState } from "react";
import { motion } from "motion/react";
import { Lightbulb } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import GameCard, { type Topic } from "../components/GameCard";
import type { AppOutletContext } from "../appOutlet";

const MOCK_TOPICS: Topic[] = [
  {
    id: "1",
    name: "Neymar goals",
    subtext: "MONTHLY PULSE HIGH",
    imageUrl: "https://picsum.photos/seed/neymar/800/1000",
    searchVolume: 1_250_000,
    icon: "trending",
  },
  {
    id: "2",
    name: "Cristiano Ronaldo last game",
    subtext: "GLOBAL HOT TOPIC",
    imageUrl: "https://picsum.photos/seed/ronaldo/800/1000",
    searchVolume: 2_800_000,
    icon: "history",
  },
];

function pickPair(topics: Topic[]): [Topic, Topic] {
  const shuffled = [...topics].sort(() => Math.random() - 0.5);
  return [shuffled[0], shuffled[1]];
}

export default function Battle() {
  const { setScore, setBest } = useOutletContext<AppOutletContext>();

  const [leftTopic, setLeftTopic] = useState<Topic | null>(null);
  const [rightTopic, setRightTopic] = useState<Topic | null>(null);
  const [isRevealing, setIsRevealing] = useState(false);

  const startRound = useCallback(() => {
    const [a, b] = pickPair(MOCK_TOPICS);
    setLeftTopic(a);
    setRightTopic(b);
    setIsRevealing(false);
  }, []);

  useEffect(() => {
    startRound();
  }, [startRound]);

  const handleGuess = (picked: Topic | null) => {
    if (!picked || !leftTopic || !rightTopic || isRevealing) return;

    const winner =
      leftTopic.searchVolume >= rightTopic.searchVolume ? leftTopic : rightTopic;
    const correct = picked.id === winner.id;

    setIsRevealing(true);
    if (correct) {
      setScore((s: number) => {
        const next = s + 1;
        setBest((b: number) => Math.max(b, next));
        return next;
      });
    }

    window.setTimeout(() => {
      startRound();
    }, 2200);
  };

  return (
    <main className="flex-grow flex flex-col items-center justify-center relative px-6 py-12 md:py-16">
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-primary-container/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-secondary-container/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-6xl relative z-10">
        <div className="text-center mb-12">
          <motion.span
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-tertiary-container text-on-tertiary-container px-4 py-1 rounded-full text-xs font-black uppercase tracking-widest mb-4 inline-block"
          >
            Football Pulse
          </motion.span>
          <motion.h1
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-4xl md:text-6xl font-headline font-extrabold tracking-tighter text-on-surface mt-2"
          >
            Which was searched <span className="italic text-primary">more?</span>
          </motion.h1>
        </div>

        <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-0 relative">
          <GameCard
            topic={leftTopic}
            onClick={() => handleGuess(leftTopic)}
            isRevealing={isRevealing}
            side="left"
          />

          <div className="lg:absolute lg:left-1/2 lg:top-1/2 lg:-translate-x-1/2 lg:-translate-y-1/2 z-30 pointer-events-none">
            <motion.div
              animate={isRevealing ? { scale: [1, 1.2, 1] } : {}}
              className="w-24 h-24 md:w-32 md:h-32 bg-white rounded-full flex items-center justify-center shadow-2xl border-4 border-surface-container-high"
            >
              <span className="font-headline text-4xl md:text-6xl font-black italic tracking-tighter bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">
                VS
              </span>
            </motion.div>
          </div>

          <GameCard
            topic={rightTopic}
            onClick={() => handleGuess(rightTopic)}
            isRevealing={isRevealing}
            side="right"
          />
        </div>

        <div className="mt-12 text-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="inline-flex items-center gap-3 bg-surface-container/80 backdrop-blur-md px-6 py-3 rounded-full border border-on-surface/10"
          >
            <Lightbulb className="text-primary fill-primary/20" size={18} />
            <p className="font-body text-sm font-medium text-on-surface-variant">
              Tap the card you think has the higher search volume globally!
            </p>
          </motion.div>
        </div>
      </div>
    </main>
  );
}
