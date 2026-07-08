# 🎙️ AI English Pronunciation Assessment

A production-ready AI-powered web application that evaluates English pronunciation from a **30–45 second English speech recording**.

The application performs:

- 🎯 Pronunciation assessment
- 📝 Speech transcription
- 📊 Speaking metrics analysis
- ⚠️ Pronunciation & fluency issue detection
- 🤖 AI-generated coaching feedback

Built as part of the **Livo AI Software Engineer Assessment**.

---

# Features

- Upload English audio (30–45 seconds)
- Audio validation (duration, format, size)
- Speech transcription using Faster-Whisper
- Pronunciation analysis
- Speaking rate analysis
- Pause detection
- Transcript generation
- AI-generated personalized coaching
- Responsive modern UI
- Graceful fallback when AI feedback is unavailable

---

# Tech Stack

## Frontend

- Next.js (App Router)
- TypeScript
- Tailwind CSS

## Backend

- FastAPI
- Python 3.11
- Faster-Whisper
- OpenAI API
- Pydantic

## Deployment

- Vercel
- Railway

---

# Project Structure

```text
.
├── frontend/     # Next.js frontend
├── backend/      # FastAPI backend
└── docs/         # Architecture & deployment documentation
```

---

# Architecture

```text
Browser
      │
      ▼
Next.js Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Assessment Service
      │
      ├── Upload Validation
      ├── Audio Duration Validation
      ├── Speech Transcription (Faster-Whisper)
      ├── Pronunciation Analysis
      └── AI Feedback Generation
```

---

# Local Setup

## Prerequisites

- Node.js 20+
- Python 3.11+
- npm

---

## Backend

```bash
cd backend

python3.11 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload
```

Backend:

```
http://localhost:8000
```

> **Note:** The first transcription request may download the configured Faster-Whisper model if it is not already cached.

---

## Frontend

```bash
cd frontend

npm install

cp .env.example .env.local

npm run dev
```

Frontend:

```
http://localhost:3000
```

---

# Environment Variables

## Backend

```env
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

## Frontend

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

# API

## POST

```
/api/v1/assessments
```

Accepts:

- WAV
- MP3
- M4A
- WebM

Returns:

- Upload information
- Speech transcript
- Pronunciation score
- Speaking metrics
- Potential issues
- AI feedback (optional)

---

# Running Tests

Backend:

```bash
cd backend

pytest

ruff format --check app tests

ruff check app tests
```

Frontend:

```bash
cd frontend

npm run lint

npm run typecheck

npm run build
```

---

# Deployment

Frontend

- Vercel

Backend

- Railway

Deployment instructions are available in:

```
docs/deployment.md
```

---

# Future Improvements

- Word-level pronunciation scoring
- Phoneme alignment
- Real-time microphone recording
- Streaming transcription
- Audio waveform visualization
- User accounts
- Assessment history
- Progress tracking

---

# License

Created for the **Livo AI Software Engineer Assessment**.