import { apiFetch } from "./api";
import {
  Course,
  Enrollment,
} from "./types";


export async function getCourses(): Promise<Course[]> {
  return apiFetch<Course[]>(
    "/api/v1/courses",
  );
}


export async function enrollInCourse(
  courseId: number,
): Promise<Enrollment> {
  return apiFetch<Enrollment>(
    `/api/v1/courses/${courseId}/enroll`,
    {
      method: "POST",
    },
  );
}


export async function getEnrollment(
  courseId: number,
): Promise<Enrollment> {
  return apiFetch<Enrollment>(
    `/api/v1/courses/${courseId}/enrollment`,
  );
}