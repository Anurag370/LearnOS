"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { useAuth } from "@/context/AuthContext";


const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: "🏠",
  },
  {
    name: "Courses",
    href: "/courses",
    icon: "📚",
  },
  {
    name: "Goals",
    href: "/goals",
    icon: "🎯",
  },
  {
    name: "Progress",
    href: "/progress",
    icon: "📊",
  },
  {
    name: "AI Tutor",
    href: "/tutor",
    icon: "🤖",
  },
];


export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const { logout } = useAuth();


  function handleLogout() {
    logout();
    router.push("/login");
  }


  return (
    <aside className="flex min-h-screen w-64 flex-col border-r border-outline bg-surface-0">

      <div className="border-b border-outline p-6">
        <Link
          href="/dashboard"
          className="text-2xl font-bold text-strong"
        >
          Learn<span className="text-accent">OS</span>
        </Link>

        <p className="mt-1 text-xs text-muted">
          Intelligent Learning Platform
        </p>
      </div>


      <nav className="flex-1 p-4">
        <div className="space-y-1">
          {navigation.map((item) => {
            const active =
              pathname === item.href ||
              pathname.startsWith(
                `${item.href}/`,
              );

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm transition ${
                  active
                    ? "bg-blue-600/10 text-accent"
                    : "text-muted hover:bg-surface-hover hover:text-strong"
                }`}
              >
                <span>{item.icon}</span>

                <span>{item.name}</span>
              </Link>
            );
          })}
        </div>
      </nav>


      <div className="border-t border-outline p-4">
        <Link
          href="/profile"
          className="mb-2 flex items-center gap-3 rounded-lg px-4 py-3 text-sm text-muted hover:bg-surface-hover hover:text-strong"
        >
          <span>⚙️</span>
          <span>Profile</span>
        </Link>

        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm text-muted hover:bg-surface-hover hover:text-strong"
        >
          <span>🚪</span>
          <span>Logout</span>
        </button>
      </div>

    </aside>
  );
}