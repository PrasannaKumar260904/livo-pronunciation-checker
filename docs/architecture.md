# Architecture

## Overview

The application is split into a frontend and backend so the web UI can deploy independently from the assessment API.

```text
Browser
  |
  | HTTPS
  v
Next.js frontend
  |
  | API request with audio upload
  v
FastAPI backend
  |
  | Future assessment workflow
  v
Pronunciation analysis services
```

## Frontend

- Next.js App Router for routing and server/client component boundaries.
- TypeScript for application code.
- Tailwind CSS for styling.
- A small API client isolates backend URL configuration.

The first screen is the usable upload experience, not a marketing page.

## Backend

The backend follows a modular FastAPI layout:

- `app/main.py` creates the FastAPI application and middleware.
- `app/api/` owns HTTP routers.
- `app/services/` will own business workflows.
- `app/models/` owns request and response schemas.
- `app/utils/` owns shared helpers.

No scoring, transcription, forced alignment, or AI model orchestration is implemented yet.

## Future Assessment Flow

When business logic is added, the expected flow is:

1. Validate uploaded audio format and duration.
2. Store or stream the audio to an assessment pipeline.
3. Run transcription, pronunciation analysis, and issue detection.
4. Return score, highlighted issues, and actionable feedback.

