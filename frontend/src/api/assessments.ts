import type { ApiErrorDetail, AssessmentResponse } from "@/types/assessment";

const API_BASE_URL = getApiBaseUrl();

export class AssessmentApiError extends Error {
  detail?: ApiErrorDetail | string;
  status: number;

  constructor(message: string, status: number, detail?: ApiErrorDetail | string) {
    super(message);
    this.name = "AssessmentApiError";
    this.status = status;
    this.detail = detail;
  }
}

export async function createAssessment(file: File): Promise<AssessmentResponse> {
  const formData = new FormData();
  formData.append("audio", file);

  const response = await fetch(`${API_BASE_URL}/api/v1/assessments`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { detail?: ApiErrorDetail | string }
      | null;
    const detail = payload?.detail;
    const message =
      typeof detail === "object" && detail?.message
        ? detail.message
        : typeof detail === "string"
          ? detail
          : "Assessment request failed.";

    throw new AssessmentApiError(message, response.status, detail);
  }

  return response.json() as Promise<AssessmentResponse>;
}

function getApiBaseUrl() {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "");

  if (!apiBaseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is required.");
  }

  return apiBaseUrl;
}
