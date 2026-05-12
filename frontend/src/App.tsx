import "./index.css";
import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import TrendmineNavBar from "./components/navBar";
import Home from "./pages/home";
import Battle from "./pages/battle";
import TopicsPage from "./pages/topics";
import AuthPage from "./pages/auth";
import TrendMineFooter from "./components/footer";

export default function App() {
  const [score] = useState(0);
  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20">
      <TrendmineNavBar score={score} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="battle" element={<Battle />} />
        <Route path="topics" element={<TopicsPage />} />
        <Route path="log_in" element={<AuthPage />} />
        <Route path="sign_in" element={<AuthPage />} />
      </Routes>
      <TrendMineFooter />
    </div>
  );
}
