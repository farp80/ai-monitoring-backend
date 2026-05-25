from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import Settings
from app.models.user import AuthProvider, User
from app.schemas.auth import LoginRequest


def upsert_user(db: Session, payload: LoginRequest) -> User:
    now = datetime.now(timezone.utc)
    user = (
        db.query(User)
        .filter(
            User.provider == payload.provider,
            User.provider_user_id == payload.provider_user_id,
        )
        .one_or_none()
    )

    if user is None:
        user = User(
            email=payload.email.lower(),
            display_name=payload.display_name,
            provider=payload.provider,
            provider_user_id=payload.provider_user_id,
            avatar_url=payload.avatar_url,
            last_login_at=now,
        )
        db.add(user)
    else:
        user.email = payload.email.lower()
        user.display_name = payload.display_name
        user.avatar_url = payload.avatar_url
        user.updated_at = now
        user.last_login_at = now

    db.commit()
    db.refresh(user)
    return user


def create_access_token(user_id: str, settings: Settings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expire_minutes
    )
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(
        payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str, settings: Settings) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        sub = payload.get("sub")
        return sub if isinstance(sub, str) else None
    except JWTError:
        return None


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).one_or_none()


def provider_from_email_domain(email: str) -> AuthProvider | None:
    domain = email.split("@")[-1].lower()
    if domain in {"gmail.com", "googlemail.com"}:
        return AuthProvider.google
    if domain in {"yahoo.com", "ymail.com", "rocketmail.com"}:
        return AuthProvider.yahoo
    if domain in {
        "outlook.com",
        "hotmail.com",
        "live.com",
        "msn.com",
        "microsoft.com",
    }:
        return AuthProvider.microsoft
    return None
