export type AssessmentStatus = "queued" | "processing" | "completed" | "failed";

export type AssessmentResponse = {
  id: string;
  status: AssessmentStatus;
};

