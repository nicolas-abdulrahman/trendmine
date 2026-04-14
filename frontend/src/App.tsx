import "./index.css";
import { useState } from "react";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import TrendmineNavBar from "./components/navBar";
import TrendMineFooter from "./components/footer";
import Home from "./pages/home";
import Battle from "./pages/battle";

export default function App() {
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(12);
  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20">
      <TrendmineNavBar score={score} best={best} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="battle" element={<Battle />} />
      </Routes>
    </div>
  );
}
