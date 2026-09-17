import { getAccessToken } from "./auth";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

let unauthorizedHandler: (() => void) | null = null;

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export function setUnauthorizedHandler(
  handler: (() => void) | null,
): void {
  unauthorizedHandler = handler;
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const token = getAccessToken();

  const headers = new Headers(options?.headers);

  headers.set("Content-Type", "application/json");

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = `API request failed: ${response.status} ${response.statusText}`;

    try {
      const errorData = await response.json();

      if (typeof errorData?.detail === "string") {
        message = errorData.detail;
      }
    } catch {
      // Response did not contain JSON.
    }

    if (response.status === 401) {
      unauthorizedHandler?.();
    }

    throw new ApiError(message, response.status);
  }

  return response.json();
}