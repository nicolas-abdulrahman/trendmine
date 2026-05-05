import React from "react";
import { PlusCircle, CheckCircle2, type LucideIcon } from "lucide-react";

interface TopicListItemProps {
  name: string;
  Icon: LucideIcon;
  isActive?: boolean;
  onClick?: () => void;
}

const TopicListItem: React.FC<TopicListItemProps> = ({
  name,
  Icon,
  isActive,
  onClick,
}) => (
  <div
    onClick={onClick}
    className={`flex items-center justify-between p-4 rounded-lg transition-all cursor-pointer group ${
      isActive
        ? "bg-primary text-white shadow-md"
        : "bg-surface-container-lowest hover:bg-tertiary-container text-on-surface"
    }`}
  >
    <div className="flex items-center gap-3">
      <Icon size={20} className={isActive ? "text-white" : "text-primary"} />
      <span className="font-body font-semibold">{name}</span>
    </div>
    {isActive ? (
      <CheckCircle2 size={20} className="text-white" />
    ) : (
      <PlusCircle
        size={20}
        className="text-primary opacity-0 group-hover:opacity-100 transition-opacity"
      />
    )}
  </div>
);

export default TopicListItem;
