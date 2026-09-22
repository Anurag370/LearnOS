export interface User {
  id: number;
  email: string;
  role: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterResponse {
  id: number;
  email: string;
  role: string;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string | null;
}

export interface Enrollment {
  id: number;
  user_id: number;
  course_id: number;
  status: string;
  enrolled_at: string;
}

export interface LearningGoal {
  id: number;
  user_id: number;
  course_id: number;
  description: string;
  target_date: string | null;
  desired_outcome: string | null;
  status: string;
}

export interface CreateLearningGoalRequest {
  course_id: number;
  description: string;
  target_date?: string | null;
  desired_outcome?: string | null;
}

export interface UpdateLearningGoalRequest {
  description?: string;
  target_date?: string | null;
  desired_outcome?: string | null;
}

export interface LearningPlanItem {
  id: number;
  plan_id: number;
  lesson_id: number;
  position: number;
  status: string;
}

export interface LearningPlan {
  id: number;
  user_id: number;
  learning_goal_id: number;
  status: string;
  items: LearningPlanItem[];
}

export interface LearningPlanItemStatusUpdate {
  status: string;
}