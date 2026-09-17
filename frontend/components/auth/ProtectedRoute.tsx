"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/context/AuthContext";


interface ProtectedRouteProps {
  children: ReactNode;
}


export default function ProtectedRoute({
  children,
}: ProtectedRouteProps) {
  const router = useRouter();

  const {
    loading,
    isAuthenticated,
  } = useAuth();


  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [
    loading,
    isAuthenticated,
    router,
  ]);


  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-surface-0 text-strong">
        Loading...
      </main>
    );
  }


  if (!isAuthenticated) {
    return null;
  }


  return <>{children}</>;
}