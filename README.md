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

Backend environment variables:

```bash
APP_NAME=Livo Pronunciation Checker API
APP_ENV=development
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
MAX_UPLOAD_SIZE_MB=25
UPLOAD_DIR=/tmp/livo-pronunciation-checker/uploads
TRANSCRIPTION_MODEL_SIZE=base
TRANSCRIPTION_DEVICE=cpu
TRANSCRIPTION_COMPUTE_TYPE=int8
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

For production, set `APP_ENV=production`, configure
`BACKEND_CORS_ORIGINS` to the deployed Vercel URL, and set
`NEXT_PUBLIC_API_BASE_URL` in Vercel to the deployed Railway backend URL.

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
- `POST /api/v1/assessments` accepts `.wav`, `.mp3`, `.m4a`, and `.webm` uploads, validates file type, upload size, and 30-45 second duration, stores the validated audio in the configured temporary upload directory, returns structured transcription data, computes deterministic pronunciation analysis metrics, and includes concise AI feedback when the feedback provider is available.

The API does not implement phoneme analysis, pronunciation scoring with an LLM, or word-level mispronunciation claims.

## Deployment

- Frontend: Vercel, configured from `frontend/`.
- Backend: Railway, configured from `backend/`.

See [docs/deployment.md](docs/deployment.md) for environment variables and platform setup.
