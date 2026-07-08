# 🎙️ AI English Pronunciation Assessment

A production-ready AI-powered web application that evaluates English pronunciation from a 30–45 second speech recording.

Users upload an audio recording and receive:

- 🎯 Pronunciation Score
- 📝 Speech Transcript
- 📊 Speaking Metrics
- ⚠️ Potential Pronunciation & Fluency Issues
- 🤖 AI-generated Coaching Feedback

Built as part of the **Livo AI Software Engineer Assessment**.

---

# Demo

Frontend (Vercel)

> Add after deployment

Backend API (Railway)

> Add after deployment

---

# Features

- Upload English audio (30–45 seconds)
- Audio validation
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

```
.
├── frontend/
├── backend/
└── docs/
```

---

# Architecture

```
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
      ├── Speech Transcription
      ├── Pronunciation Analysis
      └── AI Feedback Generation
```

---

# Local Setup

## Clone

```bash
git clone <repo-url>
cd livo-pronunciation-checker
```

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

```
APP_ENV=
BACKEND_CORS_ORIGINS=
MAX_UPLOAD_SIZE_MB=
UPLOAD_DIR=

TRANSCRIPTION_MODEL_SIZE=
TRANSCRIPTION_DEVICE=
TRANSCRIPTION_COMPUTE_TYPE=

OPENAI_API_KEY=
OPENAI_MODEL=
```

## Frontend

```
NEXT_PUBLIC_API_BASE_URL=
```

---

# API

## POST

```
/api/v1/assessments
```

Accepts

- WAV
- MP3
- M4A
- WebM

Returns

- Upload information
- Transcript
- Pronunciation score
- Speaking metrics
- Detected issues
- AI feedback (optional)

---

# Deployment

Frontend

- Vercel

Backend

- Railway

Detailed deployment steps are available in:

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
- User authentication
- Assessment history
- Progress tracking

---

# License

Created for the **Livo AI Software Engineer Assessment**.