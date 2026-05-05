import { useCallback, useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lightbulb, Loader2 } from "lucide-react";
import { useSearchParams } from "react-router-dom";
import GameCard, { type Topic, type GameCardHandle } from "./GameCard";
import { getTopicImage } from "../../utils/getTopicImage";

// --- Interfaces ---
interface Competitor {
  name: string;
  page: string;
  score: number;
}

interface BattleResponse {
  battle_id: string;
  a: Competitor;
  b: Competitor;
}

// --- Helpers ---
async function competitorToTopic(
  id: string,
  competitor: Competitor,
): Promise<Topic> {
  const imageUrl = await getTopicImage(competitor.page);
  return {
    id,
    name: competitor.name,
    imageUrl: imageUrl,
    searchVolume: competitor.score,
  };
}

export default function Battle() {
  const [searchParams] = useSearchParams();
  const seed = searchParams.get("seed") ?? "football";

  const leftCardRef = useRef<GameCardHandle>(null);
  const rightCardRef = useRef<GameCardHandle>(null);

  const [battleId, setBattleId] = useState<string | null>(null);
  const [leftTopic, setLeftTopic] = useState<Topic | null>(null);
  const [rightTopic, setRightTopic] = useState<Topic | null>(null);

  const [isRevealing, setIsRevealing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(0);

  const [resultStatus, setResultStatus] = useState<{
    left: "idle" | "winner" | "loser";
    right: "idle" | "winner" | "loser";
  }>({ left: "idle", right: "idle" });

  const prepareBattleData = useCallback(async (data: BattleResponse) => {
    const [left, right] = await Promise.all([
      competitorToTopic("a", data.a),
      competitorToTopic("b", data.b),
    ]);
    return { id: data.battle_id, left, right };
  }, []);

  useEffect(() => {
    let ignore = false;
    const init = async () => {
      if (ignore) return;
      setLoading(true);
      try {
        const res = await fetch(`/api/battle?seed=${encodeURIComponent(seed)}`);
        const data = await res.json();
        const prepared = await prepareBattleData(data);
        setBattleId(prepared.id);
        setLeftTopic(prepared.left);
        setRightTopic(prepared.right);
      } catch (e) {
        console.error("Failed to start game:", e);
      } finally {
        setLoading(false);
      }
    };
    init();
    return () => {
      ignore = true;
    };
  }, [seed, prepareBattleData]);

  const handleGuess = async (pickedId: string) => {
    if (
      !battleId ||
      isRevealing ||
      loading ||
      isTransitioning ||
      !leftTopic ||
      !rightTopic
    )
      return;

    // 1. LÓGICA LOCAL INSTANTÂNEA
    const winnerId =
      leftTopic.searchVolume! >= rightTopic.searchVolume! ? "a" : "b";
    const isCorrect = pickedId === winnerId;

    setResultStatus({
      left: winnerId === "a" ? "winner" : "loser",
      right: winnerId === "b" ? "winner" : "loser",
    });

    setIsRevealing(true);
    setIsTransitioning(true);

    if (isCorrect) {
      setScore((s) => {
        const next = s + 1;
        if (next > best) setBest(next);
        return next;
      });
      if (pickedId === "a") leftCardRef.current?.triggerConfetti();
      else rightCardRef.current?.triggerConfetti();
    } else {
      setScore(0);
    }

    // 2. SINCRONIZAÇÃO COM A API
    try {
      const response = await fetch("/api/battle/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          battle_id: battleId,
          guess: isCorrect, // Envia o booleano conforme a nova API
        }),
      });

      // O retorno agora é diretamente a estrutura da próxima batalha (BattleResponse)
      const data: BattleResponse = await response.json();

      // Pré-carrega as imagens da próxima rodada em background
      const nextBattle = await prepareBattleData(data);

      // 3. TRANSIÇÃO SUAVE
      setTimeout(() => {
        setBattleId(nextBattle.id);
        setLeftTopic(nextBattle.left);
        setRightTopic(nextBattle.right);

        setIsRevealing(false);
        setResultStatus({ left: "idle", right: "idle" });
        setIsTransitioning(false);
      }, 3000);
    } catch (err) {
      console.error("Transition Error:", err);
      setTimeout(() => {
        setIsRevealing(false);
        setIsTransitioning(false);
      }, 3000);
    }
  };

  return (
    <main className="flex-grow flex flex-col items-center justify-center relative px-6 py-12 md:py-16 overflow-hidden">
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-secondary/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-6xl relative z-10">
        <div className="text-center mb-10">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center gap-2"
          >
            <span className="bg-primary/10 text-primary px-4 py-1 rounded-full text-xs font-black uppercase tracking-[0.2em]">
              Arena: {seed}
            </span>
            <h1 className="text-4xl md:text-6xl font-headline font-extrabold tracking-tighter text-on-surface mt-2">
              O que é mais <span className="text-primary italic">buscado?</span>
            </h1>
          </motion.div>

          <div className="mt-6 flex items-center justify-center gap-12">
            <div className="flex flex-col items-center">
              <span className="text-[10px] uppercase tracking-widest font-bold opacity-50">
                Score
              </span>
              <span className="text-4xl font-headline font-black text-primary">
                {score}
              </span>
            </div>
            <div className="h-10 w-[1px] bg-on-surface/10" />
            <div className="flex flex-col items-center">
              <span className="text-[10px] uppercase tracking-widest font-bold opacity-50">
                Best
              </span>
              <span className="text-4xl font-headline font-black text-secondary">
                {best}
              </span>
            </div>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row items-center justify-center relative gap-4 lg:gap-0">
          <GameCard
            ref={leftCardRef}
            topic={leftTopic}
            onClick={() => handleGuess("a")}
            isRevealing={isRevealing}
            isLoading={loading && !leftTopic}
            status={resultStatus.left}
            side="left"
          />

          <div className="lg:absolute lg:left-1/2 lg:top-1/2 lg:-translate-x-1/2 lg:-translate-y-1/2 z-30 pointer-events-none">
            <motion.div
              animate={
                isRevealing
                  ? { rotate: 360, scale: 0.8 }
                  : { rotate: 0, scale: 1 }
              }
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
              className="w-20 h-20 md:w-28 md:h-28 bg-white rounded-full flex items-center justify-center shadow-2xl border-4 border-surface-container-high relative"
            >
              <span className="font-headline text-3xl md:text-5xl font-black italic tracking-tighter bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">
                VS
              </span>
            </motion.div>
          </div>

          <GameCard
            ref={rightCardRef}
            topic={rightTopic}
            onClick={() => handleGuess("b")}
            isRevealing={isRevealing}
            isLoading={loading && !rightTopic}
            status={resultStatus.right}
            side="right"
          />
        </div>

        <div className="mt-12 text-center">
          <AnimatePresence mode="wait">
            {!isRevealing ? (
              <motion.div
                key="hint"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="inline-flex items-center gap-3 bg-surface-container-low/80 backdrop-blur-md px-6 py-3 rounded-full border border-on-surface/5"
              >
                <Lightbulb className="text-primary animate-pulse" size={18} />
                <p className="font-body text-sm font-medium text-on-surface-variant">
                  Escolha o tópico com maior volume de buscas global.
                </p>
              </motion.div>
            ) : (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="font-headline font-black text-xl italic uppercase tracking-widest text-primary/40"
              >
                {resultStatus.left === "winner"
                  ? `${leftTopic?.name} Wins!`
                  : `${rightTopic?.name} Wins!`}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </main>
  );
}
