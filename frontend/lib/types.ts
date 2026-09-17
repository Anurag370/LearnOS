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