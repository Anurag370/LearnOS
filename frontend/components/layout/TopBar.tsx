"use client";

import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";


export default function TopBar() {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();


  return (
    <header className="flex h-16 items-center justify-between border-b border-outline bg-surface-0 px-6">

      <div>
        <p className="text-sm text-muted">
          Learning Workspace
        </p>
      </div>


      <div className="flex items-center gap-3">
        <button
          onClick={toggleTheme}
          aria-label={
            theme === "dark"
              ? "Switch to light mode"
              : "Switch to dark mode"
          }
          className="flex h-9 w-9 items-center justify-center rounded-lg text-lg transition hover:bg-surface-hover"
        >
          {theme === "dark" ? "☀️" : "🌙"}
        </button>

        <div className="text-right">
          <p className="text-sm font-medium text-strong">
            {user?.email}
          </p>

          <p className="text-xs text-muted">
            {user?.role}
          </p>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600/20 text-accent">
          {user?.email?.charAt(0).toUpperCase()}
        </div>
      </div>

    </header>
  );
}