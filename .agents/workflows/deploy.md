---
description: How to deploy CommentAnalytics to Vercel and backend alternatives
---

# Deployment Guide

This guide covers how to deploy the **CommentAnalytics** application.

## 1. Frontend Deployment (Vercel)

The React frontend is perfectly suited for Vercel.

### Steps:
1. Go to [Vercel](https://vercel.com) and sign in with GitHub.
2. Click **Add New** > **Project**.
3. Import the `CommentAnalytics` repository.
4. **Project Settings**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Environment Variables**:
   - Add `VITE_API_BASE_URL` pointing to your deployed backend URL (see below).
6. Click **Deploy**.

---

## 2. Backend Deployment (The "ML Reality Check")

> [!WARNING]
> **Vercel is NOT recommended for this specific backend.**
> The Python backend uses `torch`, `transformers`, and `spacy`, which total over 1GB in size. 
> Vercel's Serverless Functions have a **250MB limit** (uncompressed) and often time out during heavy ML inference.

### Recommended Alternative: Railway.app (Easiest)
Railway handles Docker and persistent volumes, which is ideal for ML models.

1. Create a `Dockerfile` in the `backend/` directory (see below).
2. Connect your GitHub repo to Railway.
3. Add the `YOUTUBE_API_KEY` to the service variables.
4. It will automatically detect the Dockerfile and deploy.

### Dockerfile for Backend:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 3. Monorepo Configuration (If using Vercel for both)

If you still want to attempt a Vercel-only deployment (using a lighter model or a different runtime), you would need a `vercel.json` at the root:

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/backend/app/main.py" },
    { "source": "/(.*)", "destination": "/frontend/$1" }
  ]
}
```

> [!IMPORTANT]
> You would need to refactor the backend to fit Vercel's Python Runtime (placing the entry point in an `api/` folder or using a bridge).
