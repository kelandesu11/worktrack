from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_subject_from_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import LoginMfaRequiredResponse, LoginRequest, RefreshRequest, RegisterRequest, TokenResponse


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = db.execute(
        select(User).where(
            or_(User.email == payload.email, User.username == payload.username)
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> TokenResponse | LoginMfaRequiredResponse:
    user = db.execute(
        select(User).where(
            or_(
                User.email == payload.username_or_email,
                User.username == payload.username_or_email,
            )
        )
    ).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.totp_enabled:
        import pyotp

        if not payload.totp_code:
            return LoginMfaRequiredResponse()

        if not user.totp_secret or not pyotp.TOTP(user.totp_secret).verify(payload.totp_code):
            raise HTTPException(status_code=401, detail="Invalid TOTP code")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
        user=user,
    )


def refresh_user_token(db: Session, payload: RefreshRequest) -> TokenResponse:
    try:
        user_id = int(get_subject_from_token(payload.refresh_token, "refresh"))
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
        user=user,
    )