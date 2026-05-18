import { motion, AnimatePresence } from "motion/react";
import { Loader2, Trophy } from "lucide-react";
import { forwardRef, useImperativeHandle, useRef, useCallback } from "react";

export interface Topic {
  id: string;
  name: string;
  imageUrl: string;
  searchVolume: number | null;
}

export interface GameCardProps {
  topic: Topic | null;
  onClick: () => void;
  isRevealing: boolean;
  isLoading: boolean; // Sync loading state
  status: "idle" | "winner" | "loser"; // Win/Loss state
  side: "left" | "right";
}

export interface GameCardHandle {
  triggerConfetti: () => void;
}

// ... (createParticles and drawStar functions stay the same as provided) ...
const COLORS = [
  "#FF6B6B",
  "#FFD93D",
  "#6BCB77",
  "#4D96FF",
  "#FF6FC8",
  "#C77DFF",
  "#00CFFF",
  "#FF9A3C",
];
function randomBetween(a: number, b: number) {
  return a + Math.random() * (b - a);
}

function createParticles(cx: number, cy: number, count = 120): any[] {
  return Array.from({ length: count }, () => {
    const angle = randomBetween(0, Math.PI * 2);
    const speed = randomBetween(4, 14);
    return {
      x: cx,
      y: cy,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - randomBetween(2, 6),
      rotation: randomBetween(0, Math.PI * 2),
      rotationSpeed: randomBetween(-0.3, 0.3),
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      width: randomBetween(6, 14),
      height: randomBetween(4, 8),
      opacity: 1,
      shape: (["rect", "rect", "circle", "star"] as const)[
        Math.floor(Math.random() * 4)
      ],
    };
  });
}

function drawStar(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
) {
  const spikes = 5;
  const inner = r * 0.4;
  ctx.beginPath();
  for (let i = 0; i < spikes * 2; i++) {
    const ang = (i * Math.PI) / spikes - Math.PI / 2;
    const radius = i % 2 === 0 ? r : inner;
    ctx.lineTo(cx + Math.cos(ang) * radius, cy + Math.sin(ang) * radius);
  }
  ctx.closePath();
  ctx.fill();
}

const GameCard = forwardRef<GameCardHandle, GameCardProps>(function GameCard(
  { topic, onClick, isRevealing, isLoading, status, side },
  ref,
) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animFrameRef = useRef<number | null>(null);

  const triggerConfetti = useCallback(() => {
    const canvasEl = canvasRef.current;
    if (!canvasEl) return;
    if (animFrameRef.current !== null)
      cancelAnimationFrame(animFrameRef.current);
    const ctx = canvasEl.getContext("2d");
    if (!ctx) return;
    const canvas: HTMLCanvasElement = canvasEl;
    const context: CanvasRenderingContext2D = ctx;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    const particles = createParticles(rect.width / 2, rect.height / 2, 140);
    const gravity = 0.45;
    const drag = 0.985;

    function animate() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      let alive = false;
      for (const p of particles) {
        if (p.opacity <= 0) continue;
        alive = true;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += gravity;
        p.vx *= drag;
        p.vy *= drag;
        p.rotation += p.rotationSpeed;
        if (p.y > canvas.height + 20) {
          p.opacity = 0;
          continue;
        }
        if (p.y > canvas.height * 0.75) p.opacity -= 0.02;
        context.save();
        context.globalAlpha = Math.max(0, p.opacity);
        context.translate(p.x, p.y);
        context.rotate(p.rotation);
        context.fillStyle = p.color;
        if (p.shape === "circle") {
          context.beginPath();
          context.arc(0, 0, p.width / 2, 0, Math.PI * 2);
          context.fill();
        } else if (p.shape === "star") {
          drawStar(context, 0, 0, p.width / 2);
        } else {
          context.fillRect(-p.width / 2, -p.height / 2, p.width, p.height);
        }
        context.restore();
      }
      if (alive) animFrameRef.current = requestAnimationFrame(animate);
    }
    animFrameRef.current = requestAnimationFrame(animate);
  }, []);

  useImperativeHandle(ref, () => ({ triggerConfetti }), [triggerConfetti]);

  const roundingClass =
    side === "left"
      ? "rounded-t-2xl lg:rounded-l-2xl lg:rounded-tr-none"
      : "rounded-b-2xl lg:rounded-r-2xl lg:rounded-bl-none";

  // Visual State Logic
  const isLoser = isRevealing && status === "loser";
  const isWinner = isRevealing && status === "winner";

  return (
    <motion.button
      type="button"
      whileHover={!isRevealing && !isLoading ? { scale: 1.02 } : {}}
      whileTap={!isRevealing && !isLoading ? { scale: 0.98 } : {}}
      onClick={onClick}
      disabled={isRevealing || isLoading}
      className={`group w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden transition-all duration-700 bg-surface-container-lowest border-4 ${
        isWinner
          ? "border-primary shadow-[0_0_40px_rgba(106,28,246,0.4)] z-20"
          : "border-transparent"
      } ${roundingClass}`}
    >
      <AnimatePresence>
        {(isLoading || !topic) && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-50 bg-surface-container-high/60 backdrop-blur-md flex items-center justify-center"
          >
            <Loader2 className="animate-spin text-primary" size={48} />
          </motion.div>
        )}
      </AnimatePresence>

      {topic && (
        <>
          <img
            src={topic.imageUrl}
            className={`w-full h-full object-contain  ${
              isLoser
                ? "grayscale opacity-30 scale-95"
                : isRevealing
                  ? "grayscale-0 brightness-110"
                  : "grayscale group-hover:grayscale-0 brightness-75 group-hover:brightness-100"
            }`}
          />

          <div
            className={`absolute inset-0 transition-opacity duration-700 ${
              side === "left"
                ? "bg-gradient-to-t from-primary/40"
                : "bg-gradient-to-t from-secondary/40"
            } ${isLoser ? "opacity-0" : "opacity-60"}`}
          />

          <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full pointer-events-none z-30"
          />

          <div className="absolute bottom-0 left-0 right-0 p-10 text-left z-10">
            <motion.div
              layout
              className={`font-headline text-3xl md:text-5xl font-black leading-none tracking-tighter transition-colors duration-700 ${isLoser ? "text-on-surface/40" : "text-white"}`}
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
                className="mt-6"
              >
                <div
                  className={`text-sm font-bold uppercase tracking-widest ${isLoser ? "text-on-surface/30" : "text-white/70"}`}
                >
                  Search Volume
                </div>
                <div
                  className={`text-white text-4xl md:text-4xl font-headline [-webkit-text-stroke:1px_black]`}
                >
                  {topic.searchVolume?.toLocaleString() ?? "???"}
                </div>
              </motion.div>
            )}
          </div>

          {isWinner && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="absolute top-6 left-6 bg-primary text-white p-3 rounded-full shadow-xl z-40"
            >
              <Trophy size={24} />
            </motion.div>
          )}
        </>
      )}
    </motion.button>
  );
});

export default GameCard;
