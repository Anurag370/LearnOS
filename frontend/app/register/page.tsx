"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { register } from "@/lib/auth-api";


export default function RegisterPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await register(email, password);

      setSuccess(
        "Account created successfully. Redirecting to login...",
      );

      setTimeout(() => {
        router.push("/login");
      }, 1000);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Registration failed",
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="flex min-h-screen items-center justify-center bg-surface-0 px-4">
      <div className="w-full max-w-md rounded-xl border border-outline bg-surface-1 p-8">
        <h1 className="mb-2 text-3xl font-bold text-strong">
          Create your account
        </h1>

        <p className="mb-8 text-muted">
          Start your LearnOS learning journey.
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
              minLength={8}
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              className="w-full rounded-lg border border-input bg-surface-2 px-4 py-3 text-strong outline-none focus:border-blue-500"
              placeholder="Minimum 8 characters"
            />
          </div>

          {error && (
            <p className="rounded-lg bg-error-bg p-3 text-sm text-error-text">
              {error}
            </p>
          )}

          {success && (
            <p className="rounded-lg bg-success-bg p-3 text-sm text-success-text">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 px-4 py-3 font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Creating account..."
              : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-muted">
          Already have an account?{" "}
          <a
            href="/login"
            className="text-accent hover:text-blue-300"
          >
            Login
          </a>
        </p>
      </div>
    </main>
  );
}