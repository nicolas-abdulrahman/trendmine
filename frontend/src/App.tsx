
import React, { useState, useEffect } from 'react';
import { Trophy, TrendingUp, RefreshCw, Activity } from 'lucide-react';

// 1. Define the Shape of our Mined Data
interface BattleData {
  theme: string;
  competitor_a: string;
  competitor_b: string;
  avg_a: number;
  avg_b: number;
}

// 2. Define the possible Game States
type GameStatus = 'loading' | 'playing' | 'revealed' | 'error';

const TrendMineGame: React.FC = () => {
  const [battle, setBattle] = useState<BattleData | null>(null);
  const [gameState, setGameState] = useState<GameStatus>('loading');
  const [userSelection, setUserSelection] = useState<'a' | 'b' | null>(null);
  const [streak, setStreak] = useState<number>(0);

  const startNewBattle = async () => {
    setGameState('loading');
    setUserSelection(null);
    try {
      // Connects to your Flask Stochastic Miner
      const response = await fetch('http://127.0.0.1:8000/api/get-battle');
      if (!response.ok) throw new Error('Network response was not ok');
      
      const data: BattleData = await response.json();
      setBattle(data);
      setGameState('playing');
    } catch (error) {
      console.error("Mining error:", error);
      setGameState('error');
    }
  };

  useEffect(() => {
    startNewBattle();
  }, []);

  const handleGuess = (choice: 'a' | 'b') => {
    if (gameState !== 'playing' || !battle) return;
    
    setUserSelection(choice);
    setGameState('revealed');

    const isAWinner = battle.avg_a > battle.avg_b;
    const correct = (choice === 'a' && isAWinner) || (choice === 'b' && !isAWinner);

    if (correct) {
      setStreak(s => s + 1);
    } else {
      setStreak(0);
    }
  };

  if (gameState === 'loading') {
    return (
      <div className="h-screen bg-slate-950 flex flex-col items-center justify-center text-cyan-400">
        <RefreshCw className="animate-spin mb-4" size={48} />
        <h2 className="text-xl font-mono tracking-widest animate-pulse">MINERANDO DADOS...</h2>
      </div>
    );
  }

  if (gameState === 'error') {
    return (
      <div className="h-screen bg-slate-950 flex flex-col items-center justify-center text-red-400">
        <Activity size={48} className="mb-4" />
        <h2 className="text-xl font-bold">ERRO NA API DO FLASK</h2>
        <button onClick={startNewBattle} className="mt-4 underline">Tentar novamente</button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white font-sans p-6 md:p-12">
      {/* HUD Section */}
      <header className="max-w-5xl mx-auto flex justify-between items-end mb-16">
        <div>
          <h1 className="text-5xl font-black italic tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">
            TRENDMINE
          </h1>
          <p className="text-[10px] text-slate-500 font-mono mt-1 uppercase tracking-widest">
            Stochastic Discovery Engine 2026
          </p>
        </div>
        <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 px-8 py-3 rounded-2xl flex items-center gap-4 shadow-2xl">
          <Trophy className="text-yellow-500" size={24} />
          <span className="text-3xl font-black font-mono">{streak}</span>
        </div>
      </header>

      {/* Categorization Badge */}
      <div className="flex justify-center mb-12">
        <div className="px-6 py-2 rounded-full bg-slate-900 border border-slate-700 shadow-inner">
          <span className="text-slate-400 text-xs font-bold mr-2">THEME:</span>
          <span className="text-cyan-400 font-black uppercase tracking-wider">{battle?.theme}</span>
        </div>
      </div>

      {/* Battle Grid */}
      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10 hidden md:block">
          <div className="w-20 h-20 bg-slate-950 border-8 border-slate-900 rounded-full flex items-center justify-center font-black italic text-2xl text-slate-700">
            VS
          </div>
        </div>

        <CompetitorCard 
          name={battle!.competitor_a}
          score={battle!.avg_a}
          isRevealed={gameState === 'revealed'}
          isSelected={userSelection === 'a'}
          isWinner={battle!.avg_a > battle!.avg_b}
          onClick={() => handleGuess('a')}
        />

        <CompetitorCard 
          name={battle!.competitor_b}
          score={battle!.avg_b}
          isRevealed={gameState === 'revealed'}
          isSelected={userSelection === 'b'}
          isWinner={battle!.avg_b > battle!.avg_a}
          onClick={() => handleGuess('b')}
        />
      </main>

      {/* Navigation */}
      {gameState === 'revealed' && (
        <footer className="mt-16 flex justify-center">
          <button 
            onClick={startNewBattle}
            className="group bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black px-16 py-5 rounded-2xl text-2xl transition-all transform hover:scale-105 active:scale-95 shadow-[0_0_40px_rgba(6,182,212,0.3)]"
          >
            PRÓXIMO ALVO
          </button>
        </footer>
      )}
    </div>
  );
};

// --- Sub-Component Props Interface ---
interface CardProps {
  name: string;
  score: number;
  isRevealed: boolean;
  isSelected: boolean;
  isWinner: boolean;
  onClick: () => void;
}

const CompetitorCard: React.FC<CardProps> = ({ name, score, isRevealed, isSelected, isWinner, onClick }) => {
  return (
    <button
      onClick={onClick}
      disabled={isRevealed}
      className={`
        relative h-80 md:h-[450px] rounded-[40px] p-10 flex flex-col justify-center items-center text-center transition-all duration-700 border-4
        ${!isRevealed ? 'bg-slate-900 border-slate-800 hover:border-cyan-500 hover:shadow-[0_0_50px_rgba(6,182,212,0.1)] active:scale-95' : ''}
        ${isRevealed && isWinner ? 'bg-cyan-500/10 border-cyan-500 shadow-[0_0_60px_rgba(6,182,212,0.2)]' : ''}
        ${isRevealed && !isWinner ? 'bg-slate-950 border-slate-900 grayscale opacity-40' : ''}
        ${isSelected && !isWinner ? 'border-red-600 bg-red-900/10' : ''}
      `}
    >
      <h2 className="text-4xl md:text-6xl font-black uppercase tracking-tighter leading-none mb-6">
        {name}
      </h2>
      
      {isRevealed && (
        <div className="flex flex-col items-center animate-in zoom-in duration-500">
          <span className="text-6xl font-mono font-black text-white">
            {Math.round(score)}
          </span>
          <div className="h-1 w-12 bg-cyan-500 mt-4 rounded-full" />
          <p className="text-[10px] uppercase font-bold text-slate-500 mt-3 tracking-widest">
            Search Interest Index
          </p>
        </div>
      )}
    </button>
  );
};

export default TrendMineGame;