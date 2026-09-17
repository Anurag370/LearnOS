import type {
  Metadata,
  Viewport,
} from "next";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider } from "@/context/ThemeContext";
import "./globals.css";


const themeInitScript = `(function () {
  try {
    var stored = localStorage.getItem('learnos_theme');
    var dark = stored === 'dark' ||
      (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches);
    if (dark) {
      document.documentElement.classList.add('dark');
    }
  } catch (e) {}
})();`;


export const metadata: Metadata = {
  title: "LearnOS",
  description: "Agentic Learning Management System",
};

export const viewport: Viewport = {
  colorScheme: "light dark",
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: themeInitScript,
          }}
        />
      </head>
      <body>
        <AuthProvider>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}