# Deployment

## Frontend: Vercel

Set the Vercel project root to `frontend/`.

Required environment variable:

```bash
NEXT_PUBLIC_API_BASE_URL=https://your-railway-backend.up.railway.app
```

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
```

Railway can use the included `Procfile`:

```bash
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Local Development Origins

The backend allows these frontend origins by default:

- `http://localhost:3000`
- `http://127.0.0.1:3000`

