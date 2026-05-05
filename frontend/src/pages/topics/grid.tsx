import React from "react";
import { BadgeCheck, type LucideIcon } from "lucide-react";

interface TopicGridButtonProps {
  name: string;
  Icon: LucideIcon;
  isActive?: boolean;
  onClick?: () => void;
}

const TopicGridButton: React.FC<TopicGridButtonProps> = ({
  name,
  Icon,
  isActive,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center justify-center gap-4 p-8 rounded-lg border-2 transition-all duration-300 group relative ${
        isActive
          ? "bg-secondary-container border-secondary scale-105 shadow-xl shadow-secondary/20"
          : "bg-surface-container-lowest border-transparent hover:border-primary"
      }`}
    >
      <div
        className={`w-16 h-16 rounded-full flex items-center justify-center transition-colors ${
          isActive
            ? "bg-white/40"
            : "bg-surface-container group-hover:bg-primary-container"
        }`}
      >
        <Icon
          size={32}
          className={
            isActive ? "text-on-secondary-container" : "text-on-surface"
          }
        />
      </div>
      <span
        className={`font-headline font-bold ${isActive ? "text-on-secondary-container" : ""}`}
      >
        {name}
      </span>

      {isActive && (
        <div className="absolute top-4 right-4 text-on-secondary-container">
          <BadgeCheck size={24} fill="currentColor" />
        </div>
      )}
    </button>
  );
};

export default TopicGridButton;
