"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";
import { useAuth } from "@/context/AuthContext";
import {
  getCourses,
  getEnrollment,
} from "@/lib/course-api";

import { Course } from "@/lib/types";


export default function DashboardPage() {
  const { user } = useAuth();

  const [course, setCourse] =
    useState<Course | null>(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {
    async function loadEnrollment() {
      try {
        const courses = await getCourses();

        for (const currentCourse of courses) {
          try {
            await getEnrollment(
              currentCourse.id,
            );

            setCourse(currentCourse);

            break;
          } catch {
            // Current user isn't enrolled.
          }
        }
      } finally {
        setLoading(false);
      }
    }

    loadEnrollment();
  }, []);


  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">

        <div>
          <h1 className="text-3xl font-bold text-strong">
            Welcome back 👋
          </h1>

          <p className="mt-2 text-muted">
            Let&apos;s continue your learning journey.
          </p>
        </div>


        <div className="mt-8 grid gap-6 md:grid-cols-3">

          <div className="rounded-xl border border-outline bg-surface-1 p-6">
            <p className="text-sm text-dim">
              Current Course
            </p>

            <h2 className="mt-2 text-xl font-semibold text-strong">
              {loading
                ? "Loading..."
                : course?.title ||
                  "No course enrolled"}
            </h2>

            <p className="mt-2 text-sm text-muted">
              {course
                ? "You're enrolled and ready to learn."
                : "Explore courses to get started."}
            </p>
          </div>


          <div className="rounded-xl border border-outline bg-surface-1 p-6">
            <p className="text-sm text-dim">
              Learning Goal
            </p>

            <h2 className="mt-2 text-xl font-semibold text-strong">
              No goal configured
            </h2>

            <p className="mt-2 text-sm text-muted">
              We&apos;ll configure this in Phase 3.
            </p>
          </div>


          <div className="rounded-xl border border-outline bg-surface-1 p-6">
            <p className="text-sm text-dim">
              Progress
            </p>

            <h2 className="mt-2 text-xl font-semibold text-strong">
              0%
            </h2>

            <p className="mt-2 text-sm text-muted">
              Start your first lesson.
            </p>
          </div>

        </div>


        <div className="mt-8 rounded-xl border border-outline bg-surface-1 p-6">
          <h2 className="text-xl font-semibold text-strong">
            Your Learning Journey
          </h2>

          <p className="mt-2 text-muted">
            LearnOS will build a personalized learning
            path based on your goals, available time,
            performance, and mastery.
          </p>

          <div className="mt-6 grid gap-4 md:grid-cols-4">

            {[
              ["🎯", "Set Goal"],
              ["🧠", "Learn"],
              ["📝", "Assess"],
              ["📈", "Adapt"],
            ].map(([icon, title]) => (
              <div
                key={title}
                className="rounded-lg border border-outline p-4"
              >
                <div className="text-2xl">
                  {icon}
                </div>

                <p className="mt-2 font-medium text-strong">
                  {title}
                </p>
              </div>
            ))}

          </div>
        </div>


        <p className="mt-6 text-xs text-dim">
          Signed in as {user?.email}
        </p>

      </div>
    </AppShell>
  );
}