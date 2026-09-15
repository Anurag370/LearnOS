"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";

type Course = {
  id: number;
  title: string;
  slug: string;
  description: string | null;
};

type Enrollment = {
  id: number;
  user_id: number;
  course_id: number;
  status: string;
  enrolled_at: string;
};

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState<number | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCourses() {
      try {
        const data = await apiFetch<Course[]>("/api/v1/courses");
        setCourses(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load courses",
        );
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  async function enroll(courseId: number) {
    setEnrolling(courseId);
    setMessage(null);
    setError(null);

    try {
      const enrollment = await apiFetch<Enrollment>(
        `/api/v1/courses/${courseId}/enroll`,
        {
          method: "POST",
        },
      );

      setMessage(
        `Successfully enrolled in course #${enrollment.course_id}`,
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to enroll",
      );
    } finally {
      setEnrolling(null);
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-5xl">
        <h1 className="text-3xl font-bold">
          Courses
        </h1>

        {message && (
          <p className="mt-4 text-green-600">
            ✓ {message}
          </p>
        )}

        {error && (
          <p className="mt-4 text-red-600">
            ✕ {error}
          </p>
        )}

        {loading && (
          <p className="mt-6">
            Loading courses...
          </p>
        )}

        {!loading && !error && (
          <div className="mt-8 grid gap-6 md:grid-cols-2">
            {courses.map((course) => (
              <article
                key={course.id}
                className="rounded-xl border p-6 shadow-sm"
              >
                <h2 className="text-xl font-semibold">
                  {course.title}
                </h2>

                <p className="mt-2 text-gray-600">
                  {course.description}
                </p>

                <button
                  onClick={() => enroll(course.id)}
                  disabled={enrolling === course.id}
                  className="mt-6 rounded-lg border px-4 py-2 font-medium hover:bg-gray-100 disabled:opacity-50"
                >
                  {enrolling === course.id
                    ? "Enrolling..."
                    : "Enroll"}
                </button>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}