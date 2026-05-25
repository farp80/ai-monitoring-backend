from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import AuthProvider


class LoginRequest(BaseModel):
    provider: AuthProvider = Field(
        ...,
        description="Federated IdP: google (Gmail), yahoo, or microsoft",
    )
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=255)
    provider_user_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Stable subject id from the IdP (sub / oid)",
    )
    avatar_url: str | None = Field(default=None, max_length=2048)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    provider: AuthProvider
    provider_user_id: str
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
