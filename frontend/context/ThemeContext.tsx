"use client";

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";


type Theme = "light" | "dark";

const THEME_KEY = "learnos_theme";

function resolveSystemTheme(): Theme {
  if (
    typeof window === "undefined" ||
    !window.matchMedia
  ) {
    return "light";
  }

  return window.matchMedia(
    "(prefers-color-scheme: dark)",
  ).matches
    ? "dark"
    : "light";
}

function getInitialTheme(): Theme {
  if (typeof window === "undefined") {
    return "light";
  }

  const stored = localStorage.getItem(THEME_KEY);

  if (stored === "light" || stored === "dark") {
    return stored;
  }

  return resolveSystemTheme();
}


interface ThemeContextValue {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<
  ThemeContextValue | undefined
>(undefined);


export function ThemeProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [theme, setTheme] = useState<Theme>(getInitialTheme);


  useEffect(() => {
    const root = document.documentElement;

    root.classList.toggle("dark", theme === "dark");
  }, [theme]);


  function toggleTheme() {
    setTheme((previous) => {
      const next =
        previous === "dark" ? "light" : "dark";

      localStorage.setItem(THEME_KEY, next);

      return next;
    });
  }


  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}


export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error(
      "useTheme must be used inside ThemeProvider",
    );
  }

  return context;
}