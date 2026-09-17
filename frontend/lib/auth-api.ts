import { apiFetch } from "./api";
import {
  RegisterResponse,
  TokenResponse,
  User,
} from "./types";

export async function register(
  email: string,
  password: string,
): Promise<RegisterResponse> {
  return apiFetch<RegisterResponse>(
    "/api/v1/auth/register",
    {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
      }),
    },
  );
}

export async function login(
  email: string,
  password: string,
): Promise<TokenResponse> {
  return apiFetch<TokenResponse>(
    "/api/v1/auth/login",
    {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
      }),
    },
  );
}

export async function getCurrentUser(): Promise<User> {
  return apiFetch<User>(
    "/api/v1/auth/me",
  );
}