import { getCourses, getEnrollment } from "./course-api";
import { getLearningGoals } from "./learning-goal-api";
import { Course, LearningGoal } from "./types";

export interface DashboardData {
  course: Course | null;
  goals: LearningGoal[];
}

export async function getDashboardData(): Promise<DashboardData> {
  const [courses, goals] = await Promise.all([
    getCourses(),
    getLearningGoals(),
  ]);

  let enrolledCourse: Course | null = null;

  for (const course of courses) {
    try {
      await getEnrollment(course.id);

      enrolledCourse = course;
      break;
    } catch {
    }
  }

  return {
    course: enrolledCourse,
    goals,
  };
}