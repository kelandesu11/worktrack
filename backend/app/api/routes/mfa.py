import pyotp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.mfa import MessageResponse, MfaSetupResponse, MfaVerifyRequest
from app.services.activity_service import log_activity

router = APIRouter(prefix="/mfa", tags=["mfa"])
settings = get_settings()


@router.post("/setup", response_model=MfaSetupResponse)
def setup_mfa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    secret = pyotp.random_base32()
    current_user.totp_secret = secret
    current_user.totp_enabled = False
    db.add(current_user)
    db.commit()

    uri = pyotp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name=settings.totp_issuer)
    return MfaSetupResponse(secret=secret, provisioning_uri=uri)


@router.post("/verify", response_model=MessageResponse)
def verify_mfa(payload: MfaVerifyRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="MFA setup has not started")

    valid = pyotp.TOTP(current_user.totp_secret).verify(payload.code)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid code")

    current_user.totp_enabled = True
    db.add(current_user)
    log_activity(db, current_user.id, None, "mfa_enabled", {"user_id": current_user.id})
    db.commit()
    return MessageResponse(detail="MFA enabled")


@router.post("/disable", response_model=MessageResponse)
def disable_mfa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.totp_enabled = False
    current_user.totp_secret = None
    db.add(current_user)
    db.commit()
    return MessageResponse(detail="MFA disabled")
