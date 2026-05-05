import "./index.css";
import { useState } from "react";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import TrendmineNavBar from "./components/navBar";
import TrendMineFooter from "./components/footer";
import Home from "./pages/home";
import Battle from "./pages/battle";
import TopicsPage from "./pages/topics";
import SignInPage from "./pages/auth";
import AuthPage from "./pages/auth";

export default function App() {
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(0);
  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20">
      <TrendmineNavBar
        is_logged_in={false}
        score={score}
        best={best}
        current={"Play"}
      />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="battle" element={<Battle />} />
        <Route path="topics" element={<TopicsPage />} />
        <Route path="log_in" element={<AuthPage />} />
        <Route path="sign_in" element={<AuthPage />} />
      </Routes>
    </div>
  );
}
