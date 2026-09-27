"use client";

import { FormEvent, useState } from "react";

import AppShell from "@/components/layout/AppShell";
import { askTutor } from "@/lib/tutor-api";
import { TutorCitation } from "@/lib/types";

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: TutorCitation[];
}

export default function TutorPage() {
  const [question, setQuestion] = useState("");
  const [courseId, setCourseId] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    if (!courseId) {
      setError("Please enter a course ID.");
      return;
    }

    const parsedCourseId = Number(courseId);

    if (!Number.isInteger(parsedCourseId) || parsedCourseId <= 0) {
      setError("Course ID must be a positive number.");
      return;
    }

    setError("");

    const userMessage: Message = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [...previous, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await askTutor({
        course_id: parsedCourseId,
        question: trimmedQuestion,
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        citations: response.citations,
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Something went wrong while contacting the tutor.";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="mx-auto flex max-w-5xl flex-col gap-6">
        <div>
          <h1 className="text-3xl font-bold">LearnOS Tutor</h1>
          <p className="mt-2 text-gray-400">
            Ask questions about your course material.
          </p>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900 p-4">
          <label className="mb-2 block text-sm font-medium">
            Course ID
          </label>

          <input
            type="number"
            min="1"
            value={courseId}
            onChange={(event) => setCourseId(event.target.value)}
            placeholder="e.g. 1"
            className="w-full rounded-lg border border-gray-700 bg-gray-950 px-4 py-3 outline-none focus:border-blue-500"
          />
        </div>

        <div className="min-h-[400px] space-y-4 rounded-xl border border-gray-800 bg-gray-950 p-6">
          {messages.length === 0 ? (
            <div className="flex h-[350px] items-center justify-center text-center text-gray-500">
              <div>
                <p className="text-lg">Ask your first question 🚀</p>
                <p className="mt-2 text-sm">
                  The tutor will answer using the course knowledge base.
                </p>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-xl px-4 py-3 ${
                    message.role === "user"
                      ? "bg-blue-600 text-white"
                      : "border border-gray-800 bg-gray-900"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>

                  {message.role === "assistant" &&
                    message.citations &&
                    message.citations.length > 0 && (
                      <div className="mt-4 border-t border-gray-700 pt-3">
                        <p className="mb-2 text-xs font-semibold uppercase text-gray-400">
                          Sources
                        </p>

                        <div className="space-y-2">
                          {message.citations.map((citation) => (
                            <div
                              key={citation.chunk_id}
                              className="rounded-lg bg-gray-950 p-2 text-xs text-gray-400"
                            >
                              <p>
                                Chunk #{citation.chunk_id}
                              </p>

                              <p>
                                {citation.source}
                              </p>

                              {citation.page_number !== null && (
                                <p>
                                  Page {citation.page_number}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="flex justify-start">
              <div className="rounded-xl border border-gray-800 bg-gray-900 px-4 py-3 text-gray-400">
                Thinking...
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="rounded-lg border border-red-800 bg-red-950/40 p-4 text-sm text-red-300">
            {error}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="flex gap-3"
        >
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something about the course..."
            disabled={loading}
            className="flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-3 outline-none focus:border-blue-500 disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="rounded-xl bg-blue-600 px-6 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Asking..." : "Ask"}
          </button>
        </form>
      </div>
    </AppShell>
  );
}