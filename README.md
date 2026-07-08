# Livo Pronunciation Checker

Production-ready monorepo scaffold for an AI-powered English pronunciation assessment web application.

Users will upload a 30-45 second English audio recording and receive pronunciation feedback once the assessment pipeline is implemented. This scaffold intentionally does not include placeholder AI, scoring, or analysis logic.

## Repository Structure

```text
.
├── frontend/  # Next.js App Router, TypeScript, Tailwind CSS
├── backend/   # FastAPI, modular Python API
└── docs/      # Architecture and deployment notes
```

## Prerequisites

- Node.js 20+
- Python 3.11+
- npm

## Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

The frontend runs on [http://localhost:3000](http://localhost:3000).

## Backend

```bash
cd backend
cp .env.example .env
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs on [http://localhost:8000](http://localhost:8000).

The first transcription request may download the configured `faster-whisper`
model unless it is already cached in the deployment environment.

For backend tests:

```bash
cd backend
pip install -r requirements-dev.txt
pytest
ruff format --check app tests
ruff check app tests
```

## Current API Surface

- `GET /health` returns service health.
- `POST /api/v1/assessments` accepts `.wav`, `.mp3`, `.m4a`, and `.webm` uploads, validates file type, upload size, and 30-45 second duration, stores the validated audio in the configured temporary upload directory, returns structured transcription data, and computes deterministic pronunciation analysis metrics.

The API does not yet implement phoneme analysis, LLM feedback, coaching suggestions, or word-level mispronunciation claims.

## Deployment

- Frontend: Vercel, configured from `frontend/`.
- Backend: Railway, configured from `backend/`.

See [docs/deployment.md](docs/deployment.md) for environment variables and platform setup.
