# Deployment

## Frontend: Vercel

Set the Vercel project root to `frontend/`.

Required environment variable:

```bash
NEXT_PUBLIC_API_BASE_URL=https://your-railway-backend.up.railway.app
```

Do not point `NEXT_PUBLIC_API_BASE_URL` to `localhost` in Vercel.

Build settings:

- Install command: `npm install`
- Build command: `npm run build`
- Output directory: managed by Next.js

## Backend: Railway

Set the Railway service root to `backend/`.

Required environment variables:

```bash
APP_ENV=production
BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app
MAX_UPLOAD_SIZE_MB=25
UPLOAD_DIR=/tmp/livo-pronunciation-checker/uploads
TRANSCRIPTION_MODEL_SIZE=base
TRANSCRIPTION_DEVICE=cpu
TRANSCRIPTION_COMPUTE_TYPE=int8
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_API_KEY` is required for AI feedback. If it is omitted, assessment
requests still return upload, transcription, and analysis data with
`feedback: null`.

Railway can use the included `Procfile`:

```bash
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

The backend pins Python with `runtime.txt`. Uploaded audio is stored in the
configured temporary upload directory only for the duration of request
processing and is deleted after the assessment response is created.

## Local Development Origins

The backend allows these frontend origins by default:

- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Deployment Checklist

### GitHub

- Ensure `.env`, `.env.local`, `.venv`, `node_modules`, `.next`, upload
  directories, caches, and build artifacts are not committed.
- Commit the frontend `package-lock.json` and backend dependency files.
- Run backend tests and frontend checks before merging to the deployment branch.

### Railway Backend

- Set the Railway service root to `backend/`.
- Confirm Railway detects Python from `runtime.txt`.
- Set all backend environment variables listed above.
- Set `BACKEND_CORS_ORIGINS` to the deployed Vercel URL only.
- Confirm the start command is `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`.
- Confirm `/health` responds after deployment.
- Submit a valid 30-45 second audio upload and verify temp files are not retained.

### Vercel Frontend

- Set the Vercel project root to `frontend/`.
- Set `NEXT_PUBLIC_API_BASE_URL` to the deployed Railway backend URL.
- Run the Vercel build with `npm run build`.
- Confirm the deployed UI can submit to the Railway API without CORS errors.
- Confirm validation errors render in the UI without browser alerts.
