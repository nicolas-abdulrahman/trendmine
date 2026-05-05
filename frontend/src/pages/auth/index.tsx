import React from "react";
import AuthCard from "./card";

const AuthPage: React.FC = () => {
  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4 relative overflow-hidden bg-surface">
      {/* Dynamic Background Bubbles */}
      <div className="absolute top-1/4 -left-20 w-64 h-64 bg-secondary-container rounded-full blur-[120px] opacity-20 pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-20 w-80 h-80 bg-primary-container rounded-full blur-[140px] opacity-20 pointer-events-none"></div>

      <main className="w-full max-w-md relative z-10">
        {/* Floating Accent Blobs */}
        <div className="absolute -top-12 -right-12 w-32 h-32 bg-tertiary-container rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-12 -left-12 w-40 h-40 bg-secondary-container rounded-full mix-blend-multiply filter blur-xl opacity-60 animate-blob animation-delay-2000"></div>

        <AuthCard />
      </main>
    </div>
  );
};

export default AuthPage;
