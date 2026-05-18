import React, { useState, useEffect } from "react";
import TopicCard from "./card";
import TopicListItem from "./list";
import TopicGridButton from "./grid";
import { getTopicImage } from "../../utils/getTopicImage";
import { Code2 } from "lucide-react";
import {
  Gamepad2,
  Map,
  ChessKnight,
  Sword,
  Puzzle,
  Joystick,
  Terminal,
  ArrowRight,
  Bolt,
  Trophy,
} from "lucide-react";
import {
  Globe,
  AppWindow,
  Building2,
  Lightbulb, // Tech
} from "lucide-react";
import { BrazilIcon, IconB } from "./icons";
import { useNavigate } from "react-router-dom";
interface Team {
  displayName: string;
  wikipediaName: string;
  image: string;
}

const TopicsPage: React.FC = () => {
  // 1. STATE MANAGEMENT
  const [teams, setTeams] = useState<Team[]>([
    {
      displayName: "Sport",
      wikipediaName: "Sport Club do Recife",
      image: "",
    },
    {
      displayName: "Náutico",
      wikipediaName: "Clube Náutico Capibaribe",
      image: "",
    },
    {
      displayName: "Santa Cruz",
      wikipediaName: "Santa Cruz Futebol Clube",
      image: "",
    },
    {
      displayName: "Palmeiras",
      wikipediaName: "Sociedade Esportiva Palmeiras",
      image: "",
    },
  ]);

  const [selectedTeam, setSelectedTeam] = useState<string[]>(["Série A"]);
  const [selectedGenres, setSelectedGenres] = useState<string[]>(["Adventure"]);
  const [selectedTechs, setSelectedTechs] = useState<string[]>([
    "Programming Languages",
  ]);

  const navigate = useNavigate();
  const send_form = async () => {
    const req = `topics=football[${selectedGenres.join(",")
    }tech[${selectedTechs.join(",")
    }games[${selectedTechs.join(",")}]`;
    navigate(`/battle?${req}`);
    }

  // 2. WIKIPEDIA IMAGE FETCHING
  useEffect(() => {
    const fetchImages = async () => {
      const updatedTeams = await Promise.all(
        teams.map(async (team) => ({
          ...team,
          image: await getTopicImage(team.wikipediaName),
        })),
      );
      setTeams(updatedTeams);
    };
    fetchImages();
  }, []);

  // 3. SELECTION HANDLERS
  const toggleSelection = (
    name: string,
    state: string[],
    setState: React.Dispatch<React.SetStateAction<string[]>>,
  ) => {
    if (state.includes(name)) {
      setState(state.filter((item) => item !== name));
    } else {
      setState([...state, name]);
    }
  };

  return (
    <div className="mesh-gradient min-h-screen text-on-surface selection:bg-primary-container selection:text-on-primary-container">
      <main className="relative z-10 max-w-4xl mx-auto px-6 pt-12 pb-32">
        {/* HERO SECTION */}
        <header className="mb-12">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-2xl bg-primary flex items-center justify-center shadow-lg transform -rotate-6">
              <Bolt className="text-white" size={28} fill="currentColor" />
            </div>
            <span className="font-headline font-black text-2xl tracking-tighter text-primary">
              Selecione os temas para o duelo
            </span>
          </div>

          <p className="font-body text-xl text-on-surface-variant max-w-xl leading-relaxed"></p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          {/* TEAMS SECTION (7 cols) */}
          <section className="md:col-span-7 bg-surface-container-low/60 backdrop-blur-xl rounded-xl p-8 kinetic-shadow">
            <div className="flex items-center gap-4 mb-8">
              <div className="p-3 bg-secondary-container rounded-2xl">
                <Trophy className="text-on-secondary-container" size={24} />
              </div>
              <h2 className="font-headline font-bold text-2xl tracking-tight">
                Football
              </h2>
            </div>

            <div className="flex flex-wrap gap-4">
              {[
                {
                  name: "Série A",
                  wiki: "Campeonato_Brasileiro_Série_A",
                  icon: Trophy,
                },
                { name: "Clubes BR", wiki: "Brazil_Clubs", icon: BrazilIcon },
                {
                  name: "Série B",
                  wiki: "Campeonato_Brasileiro_Série_B",
                  icon: IconB,
                },
                { name: "Global", wiki: "Global_Football_Teams", icon: Globe },
              ].map((item) => (
                <TopicCard
                  key={item.wiki}
                  name={item.name}
                  // Assuming your TopicCard can handle an icon if image is missing
                  Icon={item.icon}
                  isActive={selectedTeam.includes(item.name)}
                  onClick={() =>
                    toggleSelection(item.name, selectedTeam, setSelectedTeam)
                  }
                />
              ))}
            </div>
          </section>

          {/* GAMES SECTION (5 cols) */}
          <section className="md:col-span-5 bg-surface-container-high/60 backdrop-blur-xl rounded-xl p-8 kinetic-shadow">
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-primary-container rounded-2xl">
                {/* Gamepad icon for the section header */}
                <Gamepad2 className="text-on-primary-container" size={24} />
              </div>
              <h2 className="font-headline font-bold text-2xl tracking-tight">
                Games
              </h2>
            </div>

            <div className="space-y-3">
              {[
                {
                  name: "Adventure",
                  wiki: "Adventure_games",
                  icon: Map,
                },
                {
                  name: "Strategy",
                  wiki: "Strategy_video_games",
                  icon: ChessKnight,
                },
                {
                  name: "RPG",
                  wiki: "Role-playing_video_games",
                  icon: Sword,
                },
                {
                  name: "Puzzle",
                  wiki: "Puzzle_video_games",
                  icon: Puzzle,
                },
                {
                  name: "Simulation",
                  wiki: "Category:Simulation_video_games",
                  icon: Joystick,
                },
              ].map((genre) => (
                <TopicListItem
                  key={genre.wiki}
                  name={genre.name} // Short name for UI
                  Icon={genre.icon}
                  isActive={selectedGenres.includes(genre.name)}
                  onClick={() =>
                    toggleSelection(
                      genre.name,
                      selectedGenres,
                      setSelectedGenres,
                    )
                  }
                />
              ))}
            </div>
          </section>
          {/* TECHNOLOGY SECTION (Full Width) */}
          <section className="md:col-span-12 bg-surface-container-highest/40 backdrop-blur-xl rounded-xl p-8 kinetic-shadow">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-on-surface rounded-2xl">
                  <Terminal className="text-surface" size={24} />
                </div>
                <h2 className="font-headline font-bold text-2xl tracking-tight">
                  Technologies
                </h2>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {[
                {
                  name: "Programming Languages",
                  wiki: "Programming_languages",
                  icon: Code2,
                },
                { name: "Apps", wiki: "software", icon: AppWindow },
                {
                  name: "Software Companies",
                  wiki: "Software_companies",
                  icon: Building2,
                },
                {
                  name: "Concepts",
                  wiki: "programming_concepts",
                  icon: Lightbulb,
                },
              ].map((tech) => (
                <TopicGridButton
                  key={tech.wiki}
                  name={tech.name}
                  Icon={tech.icon}
                  isActive={selectedTechs.includes(tech.name)}
                  onClick={() =>
                    toggleSelection(tech.name, selectedTechs, setSelectedTechs)
                  }
                />
              ))}
            </div>
          </section>
        </div>

        {/* STICKY FOOTER */}
        <div className="fixed bottom-0 left-0 w-full p-8 flex justify-center pointer-events-none z-50">
          <div className="w-full max-w-lg bg-surface/80 backdrop-blur-2xl p-4 rounded-full shadow-2xl pointer-events-auto border border-white/20">
            <button
            onClick={send_form}
             className="w-full h-16 bg-gradient-to-r from-primary to-primary-container text-on-primary font-headline font-extrabold text-xl rounded-full transition-all duration-300 hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-4 group">
              <span>Play</span>
              <ArrowRight className="group-hover:translate-x-2 transition-transform" />
            </button>
          </div>
        </div>
      </main>

      {/* BACKGROUND DECORATIONS */}
      <div className="fixed top-1/4 -left-20 w-64 h-64 bg-secondary-container rounded-full blur-[120px] opacity-20 pointer-events-none"></div>
      <div className="fixed bottom-1/4 -right-20 w-80 h-80 bg-primary-container rounded-full blur-[140px] opacity-20 pointer-events-none"></div>
    </div>
  );
};

export default TopicsPage;
