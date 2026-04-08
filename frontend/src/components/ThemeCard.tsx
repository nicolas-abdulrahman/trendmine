import type { ReactNode } from "react";
import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";

export interface ThemeCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  colorClass: string;
  iconBgClass: string;
  iconColorClass: string;
  lineColorClass: string;
  delay: number;
  /** Client route to open when the card is clicked (default `/battle`). */
  to?: string;
}

export default function ThemeCard({
  title,
  description,
  icon,
  colorClass,
  iconBgClass,
  iconColorClass,
  lineColorClass,
  delay,
  to = "/battle",
}: ThemeCardProps) {
  const navigate = useNavigate();

  return (
    <motion.button
      type="button"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }}
      whileHover={{ y: -16, scale: 1.02 }}
      onClick={() => navigate(to)}
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
}
