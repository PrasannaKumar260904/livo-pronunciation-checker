import type { AssessmentResponse } from "@/types/assessment";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ??
  "http://localhost:8000";

export async function createAssessment(file: File): Promise<AssessmentResponse> {
  const formData = new FormData();
  formData.append("audio", file);

  const response = await fetch(`${API_BASE_URL}/api/v1/assessments`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    const detail = payload?.detail ?? "Assessment request failed.";
    throw new Error(detail);
  }

  return response.json() as Promise<AssessmentResponse>;
}

