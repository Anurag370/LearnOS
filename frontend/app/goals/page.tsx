"use client";

import { FormEvent, useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";
import {
  createLearningGoal,
  getLearningGoals,
} from "@/lib/learning-goal-api";
import { getCourses } from "@/lib/course-api";
import { Course, LearningGoal } from "@/lib/types";

export default function GoalsPage() {
  const [goals, setGoals] = useState<LearningGoal[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);

  const [courseId, setCourseId] = useState("");
  const [description, setDescription] = useState("");
  const [targetDate, setTargetDate] = useState("");
  const [desiredOutcome, setDesiredOutcome] = useState("");

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);

        const [goalData, courseData] = await Promise.all([
          getLearningGoals(),
          getCourses(),
        ]);

        setGoals(goalData);
        setCourses(courseData);

        if (courseData.length > 0) {
          setCourseId(String(courseData[0].id));
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load learning goals.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!courseId || !description.trim()) {
      setError("Course and goal description are required.");
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const goal = await createLearningGoal({
        course_id: Number(courseId),
        description: description.trim(),
        target_date: targetDate || null,
        desired_outcome: desiredOutcome.trim() || null,
      });

      setGoals((current) => [goal, ...current]);

      setDescription("");
      setTargetDate("");
      setDesiredOutcome("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to create learning goal.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-5xl space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-white">
            Learning Goals
          </h1>

          <p className="mt-2 text-gray-400">
            Tell LearnOS what you want to achieve so your learning
            journey can adapt around your goal.
          </p>
        </div>

        <section className="rounded-2xl border border-gray-800 bg-gray-900 p-6">
          <h2 className="text-xl font-semibold text-white">
            Create a Goal
          </h2>

          <form
            onSubmit={handleSubmit}
            className="mt-6 space-y-5"
          >
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-300">
                Course
              </label>

              <select
                value={courseId}
                onChange={(event) => setCourseId(event.target.value)}
                className="w-full rounded-lg border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-blue-500"
              >
                <option value="">Select a course</option>

                {courses.map((course) => (
                  <option
                    key={course.id}
                    value={course.id}
                  >
                    {course.title}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-300">
                What do you want to achieve?
              </label>

              <textarea
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
                placeholder="Example: Learn DSA from beginner to interview level"
                rows={4}
                className="w-full rounded-lg border border-gray-700 bg-gray-950 px-4 py-3 text-white placeholder-gray-600 outline-none focus:border-blue-500"
              />
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Target Date
                </label>

                <input
                  type="date"
                  value={targetDate}
                  onChange={(event) =>
                    setTargetDate(event.target.value)
                  }
                  className="w-full rounded-lg border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Desired Outcome
                </label>

                <input
                  type="text"
                  value={desiredOutcome}
                  onChange={(event) =>
                    setDesiredOutcome(event.target.value)
                  }
                  placeholder="Example: Solve medium-level problems"
                  className="w-full rounded-lg border border-gray-700 bg-gray-950 px-4 py-3 text-white placeholder-gray-600 outline-none focus:border-blue-500"
                />
              </div>
            </div>

            {error && (
              <div className="rounded-lg border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting || loading}
              className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {submitting ? "Creating..." : "Create Goal"}
            </button>
          </form>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-white">
            Your Goals
          </h2>

          {loading ? (
            <p className="mt-4 text-gray-400">
              Loading goals...
            </p>
          ) : goals.length === 0 ? (
            <div className="mt-4 rounded-2xl border border-dashed border-gray-700 p-8 text-center">
              <p className="text-gray-400">
                You haven&apos;t created a learning goal yet.
              </p>
            </div>
          ) : (
            <div className="mt-4 space-y-4">
              {goals.map((goal) => {
                const course = courses.find(
                  (item) => item.id === goal.course_id,
                );

                return (
                  <div
                    key={goal.id}
                    className="rounded-2xl border border-gray-800 bg-gray-900 p-6"
                  >
                    <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                      <div>
                        <p className="text-sm text-blue-400">
                          {course?.title ?? "Course"}
                        </p>

                        <h3 className="mt-1 text-lg font-semibold text-white">
                          {goal.description}
                        </h3>
                      </div>

                      <span className="w-fit rounded-full bg-green-950 px-3 py-1 text-xs font-medium text-green-400">
                        {goal.status}
                      </span>
                    </div>

                    {goal.desired_outcome && (
                      <p className="mt-4 text-gray-400">
                        <span className="font-medium text-gray-300">
                          Outcome:
                        </span>{" "}
                        {goal.desired_outcome}
                      </p>
                    )}

                    {goal.target_date && (
                      <p className="mt-2 text-sm text-gray-500">
                        Target: {goal.target_date}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </AppShell>
  );
}