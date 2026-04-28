import { motion } from "motion/react";
import { ChevronRight } from "lucide-react";
import { forwardRef, useImperativeHandle, useRef, useCallback } from "react";

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

export interface GameCardHandle {
  triggerConfetti: () => void;
}

// ---------------------------------------------------------------------------
// Confetti particle helpers
// ---------------------------------------------------------------------------
interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  rotation: number;
  rotationSpeed: number;
  color: string;
  width: number;
  height: number;
  opacity: number;
  shape: "rect" | "circle" | "star";
}

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

function createParticles(cx: number, cy: number, count = 120): Particle[] {
  return Array.from({ length: count }, () => {
    const angle = randomBetween(0, Math.PI * 2);
    const speed = randomBetween(4, 14);
    return {
      x: cx,
      y: cy,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - randomBetween(2, 6), // slight upward bias
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

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
const GameCard = forwardRef<GameCardHandle, GameCardProps>(function GameCard(
  { topic, onClick, isRevealing, side },
  ref,
) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animFrameRef = useRef<number | null>(null);

  const triggerConfetti = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Cancel any running animation
    if (animFrameRef.current !== null) {
      cancelAnimationFrame(animFrameRef.current);
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Size canvas to card
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    const particles = createParticles(rect.width / 2, rect.height / 2, 140);
    const gravity = 0.45;
    const drag = 0.985;

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

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

        // Fade out once below canvas or after some travel
        if (p.y > canvas.height + 20) {
          p.opacity = 0;
          continue;
        }
        // Gentle opacity decay near edges
        if (p.y > canvas.height * 0.75) {
          p.opacity -= 0.02;
        }

        ctx.save();
        ctx.globalAlpha = Math.max(0, p.opacity);
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.fillStyle = p.color;

        if (p.shape === "circle") {
          ctx.beginPath();
          ctx.arc(0, 0, p.width / 2, 0, Math.PI * 2);
          ctx.fill();
        } else if (p.shape === "star") {
          drawStar(ctx, 0, 0, p.width / 2);
        } else {
          ctx.fillRect(-p.width / 2, -p.height / 2, p.width, p.height);
        }

        ctx.restore();
      }

      if (alive) {
        animFrameRef.current = requestAnimationFrame(animate);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        animFrameRef.current = null;
      }
    }

    animFrameRef.current = requestAnimationFrame(animate);
  }, []);

  // Expose triggerConfetti to parent via ref
  useImperativeHandle(ref, () => ({ triggerConfetti }), [triggerConfetti]);

  const gradientClass =
    side === "left"
      ? "from-primary/80 via-transparent to-transparent"
      : "from-secondary/80 via-transparent to-transparent";

  const roundingClass =
    side === "left"
      ? "rounded-t-2xl lg:rounded-l-2xl lg:rounded-tr-none"
      : "rounded-b-2xl lg:rounded-r-2xl lg:rounded-bl-none";

  if (!topic) {
    return (
      <div
        className={`w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden rounded-2xl bg-surface-container-high animate-pulse ${roundingClass}`}
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
      className={`group w-full lg:w-1/2 relative h-[450px] md:h-[550px] overflow-hidden transition-all duration-500 bg-surface-container-high ${roundingClass}`}
    >
      {/* Background image */}
      <img
        src={topic.imageUrl}
        alt={topic.name}
        referrerPolicy="no-referrer"
        className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 brightness-75 group-hover:brightness-100"
      />

      {/* Gradient overlay */}
      <div
        className={`absolute inset-0 bg-gradient-to-t ${gradientClass} opacity-60`}
      />

      {/* Confetti canvas — sits above everything, pointer-events-none so clicks pass through */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none"
        style={{ zIndex: 20 }}
      />

      {/* Topic name */}
      <div
        className="absolute bottom-0 left-0 right-0 p-10 text-left"
        style={{ zIndex: 10 }}
      >
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

      {/* Hover chevron */}
      <div
        className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity"
        style={{ zIndex: 10 }}
      >
        <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white">
          <ChevronRight size={24} />
        </div>
      </div>
    </motion.button>
  );
});

export default GameCard;
