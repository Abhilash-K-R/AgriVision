import { DiagnosisResponse, FeedbackRequest, HealthResponse, PredictionHistoryResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const API_PREFIX = "/api/v1";

// Simple error class for API errors
export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let msg = `API error ${res.status}`;
    try {
      const data = await res.json();
      msg = (data?.detail ?? data?.message) || msg;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(res.status, msg);
  }
  return (await res.json()) as T;
}

export const api = {
  async health(): Promise<HealthResponse> {
    const res = await fetch(`${API_BASE}${API_PREFIX}/health`, {
      method: "GET",
      credentials: "omit",
    });
    return handleResponse<HealthResponse>(res);
  },

  async predict(imageFile: File): Promise<DiagnosisResponse> {
    const form = new FormData();
    form.append("image", imageFile);

    const res = await fetch(`${API_BASE}${API_PREFIX}/predict`, {
      method: "POST",
      body: form,
      credentials: "omit",
    });
    return handleResponse<DiagnosisResponse>(res);
  },

  async feedback(payload: FeedbackRequest): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE}${API_PREFIX}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      credentials: "omit",
    });
    return handleResponse<{ message: string }>(res);
  },

  async history(page = 1, pageSize = 20): Promise<PredictionHistoryResponse> {
    const res = await fetch(
      `${API_BASE}${API_PREFIX}/history?page=${page}&page_size=${pageSize}`,
      { method: "GET", credentials: "omit" }
    );
    return handleResponse<PredictionHistoryResponse>(res);
  },
};
