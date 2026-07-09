export type UploadSummary = {
  filename: string;
  duration_seconds: number;
  content_type: string;
  size_bytes: number;
};

export type TranscriptSegment = {
  start_seconds: number;
  end_seconds: number;
  text: string;
};

export type Transcript = {
  text: string;
  language: string | null;
  duration_seconds: number;
  segments: TranscriptSegment[];
};

export type AnalysisMetrics = {
  total_word_count: number;
  speaking_rate_wpm: number;
  pause_count: number;
  average_segment_duration_seconds: number;
};

export type PronunciationIssue = {
  category: string;
  severity: string;
  message: string;
};

export type PronunciationAnalysis = {
  score: number;
  metrics: AnalysisMetrics;
  issues: PronunciationIssue[];
};

export type PronunciationHighlight = {
  start_seconds: number;
  end_seconds: number;
  text: string;
  severity: string;
  issue: string;
  recommendation: string;
};

export type AssessmentFeedback = {
  overall_summary: string;
  strengths: string[];
  improvement_suggestions: string[];
  practice_recommendations: string[];
};

export type AssessmentResponse = {
  message: string;
  status: string;
  upload: UploadSummary;
  transcription: Transcript;
  analysis: PronunciationAnalysis;
  pronunciation_highlights: PronunciationHighlight[];
  feedback: AssessmentFeedback | null;
};

export type ApiErrorDetail = {
  code?: string;
  message?: string;
  [key: string]: unknown;
};
