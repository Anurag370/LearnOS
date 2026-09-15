"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";

type HealthResponse = {
  status: string;
  service: string;
};

type DatabaseHealthResponse = {
  status: string;
  database: string;
  result: number;
};

export default function HealthPage() {
  const [backend, setBackend] =
    useState<HealthResponse | null>(null);

  const [database, setDatabase] =
    useState<DatabaseHealthResponse | null>(null);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function checkHealth() {
      try {
        const [backendHealth, databaseHealth] =
          await Promise.all([
            apiFetch<HealthResponse>("/health"),
            apiFetch<DatabaseHealthResponse>("/health/db"),
          ]);

        setBackend(backendHealth);
        setDatabase(databaseHealth);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to connect to backend",
        );
      }
    }

    checkHealth();
  }, []);

  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-3xl font-bold">
          LearnOS System Health
        </h1>

        <div className="mt-8 space-y-4">
          <section className="rounded-lg border p-4">
            <h2 className="font-semibold">Backend</h2>

            {backend ? (
              <p className="mt-2 text-green-600">
                ✓ {backend.service} — {backend.status}
              </p>
            ) : (
              <p className="mt-2">Checking...</p>
            )}
          </section>

          <section className="rounded-lg border p-4">
            <h2 className="font-semibold">Database</h2>

            {database ? (
              <p className="mt-2 text-green-600">
                ✓ PostgreSQL — {database.status}
              </p>
            ) : (
              <p className="mt-2">Checking...</p>
            )}
          </section>

          {error && (
            <section className="rounded-lg border border-red-300 p-4">
              <p className="text-red-600">
                ✕ {error}
              </p>
            </section>
          )}
        </div>
      </div>
    </main>
  );
}