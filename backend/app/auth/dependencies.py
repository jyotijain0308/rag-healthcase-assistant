from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.auth.jwt_handler import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return {
            "user_id": payload.get("sub"),
            "role": payload.get("role")
        }
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )