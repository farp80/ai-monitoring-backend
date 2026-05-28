# ai-monitoring-backend

FastAPI backend with federated login (Gmail/Google, Yahoo, Microsoft).

## Quick start

```bash
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require
python main.py
```

## Auth API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Login; returns user + JWT |
| GET | `/api/auth/me` | Current user (Bearer token) |
| GET | `/api/auth/providers` | Supported IdPs and email domains |
| GET | `/health` | Health check |

### Login request

```json
{
  "provider": "google",
  "email": "user@gmail.com",
  "display_name": "Jane Doe",
  "provider_user_id": "oauth-subject-id",
  "avatar_url": "https://..."
}
```

`provider`: `google` | `yahoo` | `microsoft`

### Login response

```json
{
  "user": {
    "id": "uuid",
    "email": "user@gmail.com",
    "display_name": "Jane Doe",
    "provider": "google",
    "provider_user_id": "oauth-subject-id",
    "avatar_url": null,
    "created_at": "2026-05-25T12:00:00Z",
    "updated_at": "2026-05-25T12:00:00Z",
    "last_login_at": "2026-05-25T12:00:00Z"
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```
