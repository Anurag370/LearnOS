import { apiFetch } from "./api";
import {
  CreateLearningGoalRequest,
  LearningGoal,
  UpdateLearningGoalRequest,
} from "./types";

export async function getLearningGoals(): Promise<LearningGoal[]> {
  return apiFetch<LearningGoal[]>("/api/v1/learning-goals");
}

export async function createLearningGoal(
  data: CreateLearningGoalRequest,
): Promise<LearningGoal> {
  return apiFetch<LearningGoal>("/api/v1/learning-goals", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateLearningGoal(
  goalId: number,
  data: UpdateLearningGoalRequest,
): Promise<LearningGoal> {
  return apiFetch<LearningGoal>(
    `/api/v1/learning-goals/${goalId}`,
    {
      method: "PUT",
      body: JSON.stringify(data),
    },
  );
}