"use client";

import { ReactNode } from "react";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";


interface AppShellProps {
  children: ReactNode;
}


export default function AppShell({
  children,
}: AppShellProps) {
  return (
    <ProtectedRoute>
      <div className="flex min-h-screen bg-surface-0">

        <Sidebar />

        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar />

          <main className="flex-1 p-6">
            {children}
          </main>
        </div>

      </div>
    </ProtectedRoute>
  );
}