"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";
import {
  enrollInCourse,
  getCourses,
  getEnrollment,
} from "@/lib/course-api";

import { Course } from "@/lib/types";


export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrolledCourses, setEnrolledCourses] =
    useState<Set<number>>(new Set());

  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] =
    useState<number | null>(null);

  const [error, setError] = useState("");


  useEffect(() => {
    async function loadCourses() {
      try {
        const courseData = await getCourses();

        setCourses(courseData);

        const enrolled = new Set<number>();

        await Promise.all(
          courseData.map(async (course) => {
            try {
              await getEnrollment(course.id);
              enrolled.add(course.id);
            } catch {
              // 404 means the current user is not enrolled.
            }
          }),
        );

        setEnrolledCourses(enrolled);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load courses",
        );
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);


  async function handleEnroll(courseId: number) {
    setError("");
    setEnrolling(courseId);

    try {
      await enrollInCourse(courseId);

      setEnrolledCourses(
        (previous) =>
          new Set(previous).add(courseId),
      );
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Enrollment failed",
      );
    } finally {
      setEnrolling(null);
    }
  }


  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">

        <div>
          <h1 className="text-3xl font-bold text-strong">
            Courses
          </h1>

          <p className="mt-2 text-muted">
            Explore courses and start learning.
          </p>
        </div>


        {error && (
          <div className="mt-6 rounded-lg border border-error-border bg-error-bg text-error-text">
            {error}
          </div>
        )}


        {loading ? (
          <div className="mt-8 text-muted">
            Loading courses...
          </div>
        ) : courses.length === 0 ? (
          <div className="mt-8 rounded-xl border border-outline bg-surface-1 p-8 text-center">
            <p className="text-muted">
              No courses available yet.
            </p>
          </div>
        ) : (
          <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">

            {courses.map((course) => {
              const enrolled =
                enrolledCourses.has(course.id);

              const isEnrolling =
                enrolling === course.id;


              return (
                <div
                  key={course.id}
                  className="flex flex-col rounded-xl border border-outline bg-surface-1 p-6"
                >

                  <div className="flex-1">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/10 text-2xl">
                      📚
                    </div>

                    <h2 className="text-xl font-semibold text-strong">
                      {course.title}
                    </h2>

                    <p className="mt-3 text-sm leading-6 text-muted">
                      {course.description ||
                        "Start learning with LearnOS."}
                    </p>
                  </div>


                  <div className="mt-6">

                    {enrolled ? (
                      <div className="flex items-center justify-center rounded-lg border border-success-border bg-success-bg text-success-text">
                        ✓ Enrolled
                      </div>
                    ) : (
                      <button
                        onClick={() =>
                          handleEnroll(course.id)
                        }
                        disabled={isEnrolling}
                        className="w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-medium text-strong hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        {isEnrolling
                          ? "Enrolling..."
                          : "Enroll"}
                      </button>
                    )}

                  </div>

                </div>
              );
            })}

          </div>
        )}

      </div>
    </AppShell>
  );
} 