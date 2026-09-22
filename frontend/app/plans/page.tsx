"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";
import { getLearningGoals } from "@/lib/learning-goal-api";
import {
  getLearningPlanByGoal,
  getLearningPlans,
  updateLearningPlanItemStatus,
} from "@/lib/learning-plan-api";
import { LearningGoal, LearningPlan } from "@/lib/types";

export default function PlansPage() {
  const [goals, setGoals] = useState<LearningGoal[]>([]);
  const [plans, setPlans] = useState<LearningPlan[]>([]);

  const [loading, setLoading] = useState(true);
  const [updatingItem, setUpdatingItem] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPlans() {
      try {
        setLoading(true);
        setError(null);

        const [goalData, planData] = await Promise.all([
          getLearningGoals(),
          getLearningPlans(),
        ]);

        setGoals(goalData);
        setPlans(planData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load learning plans."
        );
      } finally {
        setLoading(false);
      }
    }

    loadPlans();
  }, []);

  function goalForPlan(plan: LearningPlan): LearningGoal | undefined {
    return goals.find((goal) => goal.id === plan.learning_goal_id);
  }

  async function handleStatusChange(
    plan: LearningPlan,
    itemId: number,
    status: string
  ) {
    try {
      setUpdatingItem(itemId);
      setError(null);

      await updateLearningPlanItemStatus(itemId, { status });

      const updatedPlan = await getLearningPlanByGoal(
        plan.learning_goal_id
      );

      setPlans((current) =>
        current.map((item) =>
          item.id === updatedPlan.id ? updatedPlan : item
        )
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to update lesson status."
      );
    } finally {
      setUpdatingItem(null);
    }
  }

  if (loading) {
    return (
      <AppShell>
        <div className="p-6">
          <p className="text-muted">Loading learning plans...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <main className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-strong">
            Learning Plans
          </h1>

          <p className="mt-1 text-muted">
            Follow your planned learning journeys step by step.
          </p>
        </div>

        {error && (
          <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
            {error}
          </div>
        )}

        {goals.length === 0 && (
          <div className="rounded-xl border border-outline bg-surface-1 p-6">
            <h2 className="text-lg font-medium text-strong">
              No learning goals
            </h2>

            <p className="mt-2 text-muted">
              Create a learning goal before viewing your learning
              plans.
            </p>
          </div>
        )}

        {goals.length > 0 && plans.length === 0 && (
          <div className="rounded-xl border border-outline bg-surface-1 p-6">
            <h2 className="text-lg font-medium text-strong">
              No learning plans yet
            </h2>

            <p className="mt-2 text-muted">
              Your learning plans have not been generated yet.
            </p>
          </div>
        )}

        <section className="space-y-6">
          {plans.map((plan) => {
            const goal = goalForPlan(plan);

            return (
              <section
                key={plan.id}
                className="rounded-xl border border-outline bg-surface-1 p-6"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-sm text-dim">
                      {goal ? "Goal" : `Goal #${plan.learning_goal_id}`}
                    </p>

                    <h2 className="mt-1 text-lg font-medium text-strong">
                      {goal?.description ?? "Unknown goal"}
                    </h2>
                  </div>

                  <span className="rounded-full border border-outline px-3 py-1 text-xs text-muted">
                    {plan.status}
                  </span>
                </div>

                <div className="mt-6 space-y-3">
                  {plan.items.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between gap-4 rounded-xl border border-outline bg-surface-1 p-5"
                    >
                      <div className="flex items-center gap-4">
                        <div className="flex h-9 w-9 items-center justify-center rounded-full border border-outline text-sm text-muted">
                          {item.position}
                        </div>

                        <div>
                          <p className="font-medium text-strong">
                            Lesson {item.lesson_id}
                          </p>

                          <p className="text-sm text-dim">
                            Position {item.position}
                          </p>
                        </div>
                      </div>

                      <select
                        value={item.status}
                        disabled={updatingItem === item.id}
                        onChange={(event) =>
                          handleStatusChange(
                            plan,
                            item.id,
                            event.target.value
                          )
                        }
                        className="rounded-lg border border-outline bg-surface-1 px-3 py-2 text-sm text-strong outline-none"
                      >
                        <option value="PENDING">Pending</option>

                        <option value="IN_PROGRESS">
                          In Progress
                        </option>

                        <option value="COMPLETED">Completed</option>

                        <option value="SKIPPED">Skipped</option>
                      </select>
                    </div>
                  ))}
                </div>
              </section>
            );
          })}
        </section>
      </main>
    </AppShell>
  );
}