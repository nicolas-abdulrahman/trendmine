import React from "react";
import { Check, type LucideIcon } from "lucide-react";

interface TopicCardProps {
  name: string;
  Icon: React.ElementType;
  isActive?: boolean;
  onClick?: () => void;
}

const TopicCard: React.FC<TopicCardProps> = ({
  name,
  Icon,
  isActive,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      type="button"
      className={`group relative flex items-center gap-3 px-6 py-4 rounded-lg transition-all duration-300 ${
        isActive
          ? "bg-primary text-white shadow-xl shadow-primary/20 scale-105"
          : "bg-surface-container-lowest border-2 border-transparent hover:border-secondary-container hover:shadow-md"
      }`}
    >
      <Icon
        size={24}
        isActive={isActive}
        className={`${isActive ? "text-white" : "text-primary"}`}
      />

      <span className="font-headline font-bold text-lg">{name}</span>

      {/* This only shows if isActive={true} is passed from the parent */}
      {isActive && (
        <div className="absolute -top-2 -right-2 bg-tertiary-container rounded-full p-1 shadow-md border border-white/20">
          <Check
            size={14}
            strokeWidth={4}
            className="text-on-tertiary-container"
          />
        </div>
      )}
    </button>
  );
};

export default TopicCard;
