import { useCallback, useEffect, useState } from "react";
import { motion } from "motion/react";
import { Lightbulb, AlertTriangle, Loader2 } from "lucide-react";
import { useSearchParams } from "react-router-dom";
import GameCard, { type Topic } from "../components/GameCard";
import { getTopicImage } from "../utils/getTopicImage";

interface CompetitorStats {
  mean: number;
  std: number;
  cv: number;
}

interface Competitor {
  name: string;
  stats: CompetitorStats;
}

interface BattleResponse {
  seed: string;
  theme: string;
  competitor_a: Competitor;
  competitor_b: Competitor;
  all_candidates_scored: number;
}

async function competitorToTopic(
  id: string,
  competitor: Competitor,
): Promise<Topic> {
  const imageUrl = await getTopicImage(competitor.name);
  return {
    id,
    name: competitor.name,
    imageUrl: imageUrl,
    searchVolume: competitor.stats.mean,
    icon: "trending",
  };
}

export default function Battle() {
  const [searchParams] = useSearchParams();
  const seed = searchParams.get("seed") ?? "football";

  const [battleData, setBattleData] = useState<BattleResponse | null>(null);
  const [leftTopic, setLeftTopic] = useState<Topic | null>(null);
  const [rightTopic, setRightTopic] = useState<Topic | null>(null);
  const [isRevealing, setIsRevealing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(0);

  const loadBattle = useCallback(async () => {
    setLoading(true);
    setError(null);
    setIsRevealing(false);

    try {
      const res = await fetch(
        `http://localhost:8000/battle?seed=${encodeURIComponent(seed)}`,
      );
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data: BattleResponse = await res.json();
      setBattleData(data);
      const [left, right] = await Promise.all([
        competitorToTopic("a", data.competitor_a),
        competitorToTopic("b", data.competitor_b),
      ]);
      setLeftTopic(left);
      setRightTopic(right);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load battle");
    } finally {
      setLoading(false);
    }
  }, [seed]);

  useEffect(() => {
    loadBattle();
  }, [loadBattle]);

  const handleGuess = (picked: Topic | null) => {
    if (!picked || !leftTopic || !rightTopic || isRevealing || loading) return;

    const winner =
      leftTopic.searchVolume >= rightTopic.searchVolume
        ? leftTopic
        : rightTopic;
    const correct = picked.id === winner.id;

    setIsRevealing(true);

    if (correct) {
      setScore((s) => {
        const next = s + 1;
        setBest((b) => Math.max(b, next));
        return next;
      });
    }

    window.setTimeout(() => {
      loadBattle();
    }, 2200);
  };

  return (
    <main className="flex-grow flex flex-col items-center justify-center relative px-6 py-12 md:py-16">
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-primary-container/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-secondary-container/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-6xl relative z-10">
        <div className="text-center mb-12">
          <motion.span
            key={battleData?.theme ?? seed}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-tertiary-container text-on-tertiary-container px-4 py-1 rounded-full text-xs font-black uppercase tracking-widest mb-4 inline-block"
          >
            {battleData?.theme ?? seed} Pulse
          </motion.span>
          <motion.h1
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-4xl md:text-6xl font-headline font-extrabold tracking-tighter text-on-surface mt-2"
          >
            Which was searched{" "}
            <span className="italic text-primary">more?</span>
          </motion.h1>

          <div className="mt-4 flex items-center justify-center gap-6 text-sm font-headline font-bold">
            <span className="text-on-surface-variant">
              Score: <span className="text-primary text-lg">{score}</span>
            </span>
            <span className="text-on-surface-variant">
              Best: <span className="text-secondary text-lg">{best}</span>
            </span>
          </div>
        </div>

        {error ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center gap-4 py-20 text-center"
          >
            <AlertTriangle size={48} className="text-error" />
            <p className="font-headline font-bold text-on-surface text-xl">
              {error}
            </p>
            <button
              type="button"
              onClick={loadBattle}
              className="mt-2 px-8 py-3 rounded-full bg-primary text-on-primary font-headline font-bold hover:brightness-110 transition-all"
            >
              Retry
            </button>
          </motion.div>
        ) : loading ? (
          <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-0 relative">
            <div className="w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden rounded-t-2xl lg:rounded-l-2xl lg:rounded-tr-none bg-surface-container-high animate-pulse" />
            <div className="lg:absolute lg:left-1/2 lg:top-1/2 lg:-translate-x-1/2 lg:-translate-y-1/2 z-30 pointer-events-none">
              <div className="w-24 h-24 md:w-32 md:h-32 bg-white rounded-full flex items-center justify-center shadow-2xl border-4 border-surface-container-high">
                <Loader2 size={40} className="animate-spin text-primary" />
              </div>
            </div>
            <div className="w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden rounded-b-2xl lg:rounded-r-2xl lg:rounded-bl-none bg-surface-container-high animate-pulse" />
          </div>
        ) : (
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
        )}

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
