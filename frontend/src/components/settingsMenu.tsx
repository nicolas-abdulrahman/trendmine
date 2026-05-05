import React from "react";
import { User, Languages, LogOut } from "lucide-react";

interface SettingsMenuProps {
  isOpen: boolean;
  onLogout: () => void;
}

const SettingsMenu: React.FC<SettingsMenuProps> = ({ isOpen, onLogout }) => {
  if (!isOpen) return null;

  return (
    /* top-full pins it to the bottom of the button, right-0 pins it to the right edge */
    <div className="absolute top-full right-0 mt-2 w-48 z-50 bg-surface-container-lowest/97 backdrop-blur-xl border border-white/20 rounded-2xl shadow-[0_10px_30px_rgba(56,39,76,0.15)] overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
      <div className="p-1.5 flex flex-col gap-1">
        <button className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-primary/10 text-on-surface transition-colors">
          <User size={16} className="text-primary" />
          <span className="font-label font-bold text-xs">Profile</span>
        </button>

        <button className="flex items-center justify-between p-2.5 rounded-xl hover:bg-primary/10 text-on-surface transition-colors">
          <div className="flex items-center gap-3">
            <Languages size={16} className="text-secondary" />
            <span className="font-label font-bold text-xs">Language</span>
          </div>
          <span className="text-[9px] font-black opacity-50">PT</span>
        </button>

        <div className="h-px bg-outline-variant/10 mx-2" />

        <button
          onClick={onLogout}
          className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-error-container/10 text-error-container transition-colors"
        >
          <LogOut size={16} />
          <span className="font-label font-bold text-xs">Logout</span>
        </button>
      </div>
    </div>
  );
};

export default SettingsMenu;
