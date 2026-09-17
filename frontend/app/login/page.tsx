"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/context/AuthContext";


export default function LoginPage() {
  const router = useRouter();

  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login(email, password);

      router.push("/dashboard");
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Login failed",
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-0 px-4">
      <div className="w-full max-w-md rounded-xl border border-outline bg-surface-1 p-8">
        <h1 className="mb-2 text-3xl font-bold text-strong">
          Welcome back
        </h1>

        <p className="mb-8 text-muted">
          Login to continue learning.
        </p>

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm text-label"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              className="w-full rounded-lg border border-input bg-surface-2 px-4 py-3 text-strong outline-none focus:border-blue-500"
              placeholder="student@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm text-label"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              className="w-full rounded-lg border border-input bg-surface-2 px-4 py-3 text-strong outline-none focus:border-blue-500"
              placeholder="Your password"
            />
          </div>

          {error && (
            <p className="rounded-lg bg-error-bg p-3 text-sm text-error-text">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 px-4 py-3 font-medium text-white hover:bg-blue-500 disabled:opacity-50"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-muted">
          Don&apos;t have an account?{" "}
          <a
            href="/register"
            className="text-accent hover:text-blue-300"
          >
            Create one
          </a>
        </p>
      </div>
    </main>
  );
}