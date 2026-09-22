import { apiFetch } from "./api";
import {
  LearningPlan,
  LearningPlanItemStatusUpdate,
} from "./types";

export async function getLearningPlans(): Promise<
  LearningPlan[]
> {
  return apiFetch<LearningPlan[]>("/api/v1/learning-plans");
}

export async function getLearningPlanByGoal(
  goalId: number
): Promise<LearningPlan> {
  return apiFetch<LearningPlan>(
    `/api/v1/learning-plans/goal/${goalId}`
  );
}

export async function getLearningPlan(
  planId: number
): Promise<LearningPlan> {
  return apiFetch<LearningPlan>(
    `/api/v1/learning-plans/${planId}`
  );
}

export async function updateLearningPlanItemStatus(
  itemId: number,
  data: LearningPlanItemStatusUpdate
): Promise<LearningPlan> {
  return apiFetch<LearningPlan>(
    `/api/v1/learning-plans/items/${itemId}/status`,
    {
      method: "PUT",
      body: JSON.stringify(data),
    }
  );
}