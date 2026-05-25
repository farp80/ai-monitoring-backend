# AI Monitoring Backend

Python FastAPI service for AI monitoring with federated email login.

## Layout

- `app/main.py` — FastAPI app, CORS, lifespan DB init
- `app/models/user.py` — `users` table (google / yahoo / microsoft)
- `app/routers/auth.py` — `/api/auth/login`, `/api/auth/me`, `/api/auth/providers`
- `app/services/auth.py` — upsert user, JWT issue/verify

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
python main.py
```

API docs: http://127.0.0.1:8000/docs

## Frontend auth flow

1. User signs in with Gmail, Yahoo, or Microsoft on the client (OAuth).
2. Client POSTs `LoginRequest` to `/api/auth/login`.
3. Store `access_token`; send `Authorization: Bearer <token>` on `/api/auth/me`.
