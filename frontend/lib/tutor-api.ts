import { apiFetch } from "./api";
import { TutorAnswerResponse } from "./types";

export interface TutorQuestionRequest {
  course_id: number;
  question: string;
}

export async function askTutor(
  data: TutorQuestionRequest
): Promise<TutorAnswerResponse> {
  return apiFetch<TutorAnswerResponse>("/api/v1/tutor/ask", {
    method: "POST",
    body: JSON.stringify(data),
  });
}