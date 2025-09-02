from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.auth0 import verify_jwt
from src.db.database import get_db
from src.models.user import Korisnik
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
    except Exception:
        raise HTTPException(status_code=401, detail="Nedozvoljen pristup")
    payload = verify_jwt(token)
    user_id = payload.get("sub")
    user = db.query(Korisnik).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Korisnik nije pronađen")
    return user


def admin_required(current_user: Korisnik = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Nedozvoljen pristup")
    return current_user