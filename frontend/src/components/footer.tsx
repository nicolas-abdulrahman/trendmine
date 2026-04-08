import { Globe, Share2 } from "lucide-react";

export default function TrendMineFooter() {
  return (
    <footer className="bg-surface-container-low/50 border-t border-primary/5">
      <div className="max-w-7xl mx-auto px-12 py-10 flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex flex-col items-center md:items-start gap-1">
          <span className="text-lg font-black text-primary italic">
            TRENDMINE
          </span>
          <span className="text-[10px] font-medium tracking-widest uppercase opacity-40">
            © 2024 THE ELECTRIC PLAYGROUND
          </span>
        </div>

        <div className="flex gap-8">
          {["Privacy", "Terms", "Support"].map((link) => (
            <a
              key={link}
              href="#"
              className="text-xs font-bold uppercase tracking-widest text-on-surface/40 hover:text-primary transition-colors"
            >
              {link}
            </a>
          ))}
        </div>

        <div className="flex gap-4">
          <button className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center hover:scale-110 hover:bg-primary/10 text-primary transition-all">
            <Globe size={18} />
          </button>
          <button className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center hover:scale-110 hover:bg-primary/10 text-primary transition-all">
            <Share2 size={18} />
          </button>
        </div>
      </div>
    </footer>
  );
}
