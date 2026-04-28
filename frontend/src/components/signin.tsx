import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";

interface SignInButtonProps {
  onClick?: () => void;
  loading?: boolean;
}

export default function SignInButton({ onClick, loading = false }: SignInButtonProps) {
  const [hovered, setHovered] = useState(false);

  return (
    <motion.button
      type="button"
      onClick={onClick}
      disabled={loading}
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      whileTap={{ scale: 0.97 }}
      className="relative group flex items-center justify-center gap-3 overflow-hidden
                 h-14 px-10 rounded-2xl
                 bg-zinc-950 dark:bg-white
                 text-white dark:text-zinc-950
                 font-semibold text-[15px] tracking-wide
                 border border-white/10 dark:border-zinc-950/10
                 select-none cursor-pointer disabled:cursor-not-allowed disabled:opacity-60
                 transition-colors duration-300"
    >
      {/* Shimmer sweep */}
      <motion.span
        aria-hidden
        initial={{ x: "-110%", skewX: "-18deg" }}
        animate={{ x: hovered ? "220%" : "-110%" }}
        transition={{ duration: 0.55, ease: "easeInOut" }}
        className="absolute inset-0 w-1/3 bg-white/10 dark:bg-black/10 blur-sm pointer-events-none"
      />

      {/* Lock icon */}
      <span className="relative z-10 flex items-center justify-center w-5 h-5">
        <AnimatePresence mode="wait" initial={false}>
          {!hovered ? (
            <motion.svg
              key="locked"
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.2 }}
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M10 2a4 4 0 00-4 4v2H5a2 2 0 00-2 2v7a2 2 0 002 2h10a2 2 0 002-2v-7a2 2 0 00-2-2h-1V6a4 4 0 00-4-4zm-2 6V6a2 2 0 114 0v2H8zm2 3a1 1 0 100 2 1 1 0 000-2z"
              />
            </motion.svg>
          ) : (
            <motion.svg
              key="unlocked"
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.2 }}
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M14.5 2A3.5 3.5 0 0111 5.5V8H5a2 2 0 00-2 2v7a2 2 0 002 2h10a2 2 0 002-2v-7a2 2 0 00-2-2h-1V5.5a1.5 1.5 0 013 0V7h2V5.5A3.5 3.5 0 0014.5 2zM10 13a1 1 0 100 2 1 1 0 000-2z"
              />
            </motion.svg>
          )}
        </AnimatePresence>
      </span>

      {/* Label */}
      <motion.span
        className="relative z-10"
        animate={{ x: hovered ? 2 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      >
        {loading ? "Signing in…" : "Sign in"}
      </motion.span>

      {/* Arrow */}
      <motion.span
        aria-hidden
        className="relative z-10"
        initial={{ opacity: 0, x: -6 }}
        animate={{ opacity: hovered ? 1 : 0, x: hovered ? 0 : -6 }}
        transition={{ duration: 0.2 }}
      >
        →
      </motion.span>

      {/* Loading spinner overlay */}
      <AnimatePresence>
        {loading && (
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 flex items-center justify-center bg-zinc-950 dark:bg-white rounded-2xl z-20"
          >
            <svg
              className="animate-spin w-5 h-5 text-white dark:text-zinc-950"
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                className="opacity-25"
                cx="12" cy="12" r="10"
                stroke="currentColor" strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 100 16v-4l-3 3 3 3v-4a8 8 0 01-8-8z"
              />
            </svg>
          </motion.span>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
