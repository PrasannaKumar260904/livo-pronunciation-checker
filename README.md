# 🎙️ AI English Pronunciation Assessment

A production-ready web application for evaluating spoken English pronunciation from a **30–45 second English audio recording**.

The application validates uploaded audio, generates a speech transcript, computes pronunciation-related speaking metrics, identifies potential fluency issues, and optionally generates AI-assisted coaching feedback.

This project was developed as part of the **Livo AI Software Engineer Assessment**.

---

# 🚀 Live Demo

### Frontend

https://livo-pronunciation-checker-blue.vercel.app

### Backend Health Check

https://livo-pronunciation-checker-api.onrender.com/health

---
# 📸 Screenshots

## Upload Page

![Upload Page](docs/screenshots/upload.png)

---

## Processing

![Processing](docs/screenshots/processing.png)

---

## Results

![Results](docs/screenshots/result1.png)
![Results](docs/screenshots/result2.png)

# ✨ Features

- 🎤 Upload 30–45 second English audio recordings
- ✅ Audio validation (duration, format, and file size)
- 📝 Speech transcription using Faster-Whisper
- 📊 Deterministic pronunciation analysis
- 📈 Speaking rate analysis
- ⏸️ Pause detection
- 📄 Transcript generation
- 🤖 Optional AI-generated coaching feedback
- ⚠️ Pronunciation and fluency issue detection
- 📱 Responsive modern UI
- 🛡️ Graceful fallback when AI feedback is unavailable

---

# 🛠 Tech Stack

## Frontend

- Next.js (App Router)
- TypeScript
- Tailwind CSS

## Backend

- FastAPI
- Python 3.11
- Faster-Whisper
- Mutagen
- Pydantic
- OpenAI Chat Completions API (optional)

## Deployment

- Frontend: Vercel
- Backend: Render

---

# 📁 Project Structure

```text
.
├── frontend/      # Next.js frontend
├── backend/       # FastAPI backend
└── docs/          # Architecture & deployment documentation
```

---

# 🏗 System Architecture

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
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
 Upload Validation
 Audio Duration Validation
 Speech Transcription
 (Faster-Whisper)
 Pronunciation Analysis
 AI Feedback (Optional)
```

---

# ⚙️ Local Setup

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

> The first transcription request may download the configured Faster-Whisper model if it is not already cached.

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

# 🔑 Environment Variables

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

# 📡 API

## POST

```
/api/v1/assessments
```

### Supported Formats

- WAV
- MP3
- M4A
- WebM

### Response

Returns a JSON response containing:

- Upload metadata
- Speech transcript
- Pronunciation score
- Speaking metrics
- Potential pronunciation/fluency issues
- Optional AI coaching feedback

---

# 🧪 Running Tests

## Backend

```bash
cd backend

pytest

ruff format --check app tests

ruff check app tests
```

## Frontend

```bash
cd frontend

npm run lint

npm run typecheck

npm run build
```

---

# 🚀 Deployment

## Frontend

- Vercel

## Backend

- Render

Deployment instructions are available in:

```
docs/deployment.md
```

---

# 🔮 Future Improvements

- Word-level pronunciation scoring
- Phoneme alignment
- Real-time microphone recording
- Streaming transcription
- Audio waveform visualization
- User authentication
- Assessment history
- Progress tracking
- Persistent storage
- Batch audio assessment

---

# 📄 License

This project was developed as part of the **Livo AI Software Engineer Assessment** and is provided for demonstration and educational purposes.