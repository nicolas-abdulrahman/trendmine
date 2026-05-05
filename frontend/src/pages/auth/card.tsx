import React, { useState } from "react";
import { Mail, Lock, User, Loader2, AlertCircle } from "lucide-react";
import { GithubIcon } from "./icon";
import { useNavigate } from "react-router-dom";

interface AuthCardProps {
  initialMode?: "login" | "signup";
}

const AuthCard: React.FC<AuthCardProps> = ({ initialMode = "login" }) => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(initialMode === "login");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleLogin = async () => {
    setIsLoading(true);
    setErrorMessage("");
    try {
      const response = await fetch("/api/log_in", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("user", JSON.stringify(data.user));
        navigate("/");
      } else {
        setErrorMessage(
          data.detail || "Invalid credentials. Please try again.",
        );
      }
    } catch (error) {
      setErrorMessage("Connection error. Is the server running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignIn = async () => {
    setIsLoading(true);
    setErrorMessage("");
    console.log("signing in", formData);
    try {
      const response = await fetch("/api/sign_up", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // Auto login after sign up
        await handleLogin();
      } else {
        setErrorMessage(data.detail || "Could not create account.");
      }
    } catch (error) {
      setErrorMessage("Connection error. Please check your internet.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isLogin) {
      handleLogin();
    } else {
      handleSignIn();
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setErrorMessage(""); // Limpa erros ao trocar de aba
  };

  return (
    <div className="relative bg-surface-container-lowest/80 backdrop-blur-2xl p-8 md:p-12 rounded-xl shadow-[0_20px_50px_rgba(56,39,76,0.12)] border border-white/20">
      {/* Branding Area */}
      <div className="text-center mb-10">
        <h1 className="text-4xl md:text-5xl font-display font-black italic tracking-tighter text-primary mb-2">
          {isLogin ? "Login" : "Sign Up"}
        </h1>
        <p className="text-on-surface-variant text-sm font-medium">
          {isLogin
            ? "Welcome back to the arena."
            : "Join the electric knowledge arena."}
        </p>
      </div>

      {/* Social Logins */}
      <div className="space-y-4 mb-8">
        <button
          type="button"
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-3 bg-white hover:bg-surface-container-low border border-outline-variant/30 py-4 px-6 rounded-full transition-all duration-300 disabled:opacity-50"
        >
          <img
            alt="Google"
            className="w-6 h-6"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuAEJrm3EC_gZ8CzHF6LNg-6sLFBViA_cLoop1uVKQGPSVjEgkwkEqYBD3IB7p6S79XSF8POzo-JcMdZH8WkxEog-pzM8fiE4x38RCrlClzwoTQ2W04p1WBSICT__02dMwqtiUjaMBkrj-_x-mHN_nC0CSu-9I3JvJnCzqsH2IzI1sbz54SycYbT8jAHt0lMF6-XPu45divL0bVBesIVYYj5o_UoLezH-dpNpWRXnuKbDIwN54AYO6RHy1LMvw8NNCmDAlIMPzSiceyg"
          />
          <span className="font-body font-bold text-on-surface tracking-tight">
            Continue with Google
          </span>
        </button>

        <button
          type="button"
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-3 bg-[#24292f] hover:bg-[#24292f]/90 text-white py-4 px-6 rounded-full transition-all duration-300 shadow-lg shadow-black/10 group disabled:opacity-50"
        >
          <GithubIcon size={20} />
          <span className="font-body font-bold tracking-tight">
            Continue with GitHub
          </span>
        </button>
      </div>

      {/* Divider */}
      <div className="flex items-center gap-4 mb-8">
        <div className="h-[1px] flex-grow bg-outline-variant/20"></div>
        <span className="text-on-surface-variant font-label text-sm font-bold uppercase tracking-widest">
          or
        </span>
        <div className="h-[1px] flex-grow bg-outline-variant/20"></div>
      </div>

      {/* Error Message Display */}
      {errorMessage && (
        <div className="mb-6 p-4 bg-error/10 border border-error/20 rounded-xl flex items-center gap-3 text-error animate-in fade-in slide-in-from-top-2 duration-300">
          <AlertCircle size={18} className="flex-shrink-0" />
          <p className="text-xs font-bold leading-tight">{errorMessage}</p>
        </div>
      )}

      {/* Credentials Form */}
      <form className="space-y-5" onSubmit={handleSubmit}>
        {/* NAME FIELD (Only for Sign Up) */}
        {!isLogin && (
          <div>
            <label className="block text-on-surface font-label text-sm font-bold mb-2 ml-4">
              Full Name
            </label>
            <div className="relative">
              <input
                className="w-full bg-surface-container-low border-none focus:ring-4 focus:ring-primary-fixed/40 rounded-lg py-4 px-6 text-on-surface placeholder:text-outline/60 font-body transition-all disabled:opacity-50"
                placeholder="Enter your name"
                type="text"
                required
                disabled={isLoading}
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
              />
              <User
                size={18}
                className="absolute right-5 top-1/2 -translate-y-1/2 text-primary/40"
              />
            </div>
          </div>
        )}

        <div>
          <label className="block text-on-surface font-label text-sm font-bold mb-2 ml-4">
            Email Address
          </label>
          <div className="relative">
            <input
              className="w-full bg-surface-container-low border-none focus:ring-4 focus:ring-primary-fixed/40 rounded-lg py-4 px-6 text-on-surface placeholder:text-outline/60 font-body transition-all disabled:opacity-50"
              placeholder="bob@domain.com"
              type="email"
              required
              disabled={isLoading}
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
            <Mail
              size={18}
              className="absolute right-5 top-1/2 -translate-y-1/2 text-primary/40"
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2 ml-4 mr-4">
            <label className="text-on-surface font-label text-sm font-bold">
              Password
            </label>
            {isLogin && (
              <a
                className="text-primary font-label text-xs font-bold hover:underline"
                href="#forgot"
              >
                Forgot?
              </a>
            )}
          </div>
          <div className="relative">
            <input
              className="w-full bg-surface-container-low border-none focus:ring-4 focus:ring-primary-fixed/40 rounded-lg py-4 px-6 text-on-surface placeholder:text-outline/60 font-body transition-all disabled:opacity-50"
              placeholder="••••••••"
              type="password"
              required
              disabled={isLoading}
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
            />
            <Lock
              size={18}
              className="absolute right-5 top-1/2 -translate-y-1/2 text-primary/40"
            />
          </div>
        </div>

        <button
          className="w-full bg-gradient-to-br from-primary to-primary-container text-on-primary font-display font-extrabold text-lg py-5 px-8 rounded-full shadow-lg shadow-primary/20 hover:scale-[1.03] active:scale-95 transition-all duration-300 mt-4 flex items-center justify-center disabled:opacity-70 disabled:hover:scale-100"
          type="submit"
          disabled={isLoading}
        >
          {isLoading ? (
            <Loader2 className="animate-spin" size={24} />
          ) : (
            <>{isLogin ? "Login" : "Create Account"}</>
          )}
        </button>
      </form>

      {/* Footer Links */}
      <div className="mt-10 text-center">
        <p className="text-on-surface-variant font-body text-sm font-medium">
          {isLogin ? "Don't have an account?" : "Already have an account?"}
          <button
            onClick={toggleMode}
            className="text-primary font-bold hover:underline ml-1"
          >
            {isLogin ? "Sign up" : "Log in"}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthCard;
