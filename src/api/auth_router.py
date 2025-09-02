from fastapi import APIRouter, Depends, HTTPException,status
from typing import List
from src.schemas.auth_schema import RegisterSchema, TokenSchema, LoginSchema
from src.services.auth_service import AuthService
from src.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=TokenSchema)
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    try:
        print("Register route called", user.email)
        db_user = AuthService.register(user, db)
        if not db_user:
            raise HTTPException(status_code=400, detail="Neuspješna registracija")
        access_token = AuthService.create_access_token({"sub": str(db_user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#@router.get("/me")
#async def get_me():
#    pass

@router.post("/login", response_model=TokenSchema)
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = AuthService.login(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Neispravni podaci")
    return db_user

@router.post("/logout")
def logout(db: Session = Depends(get_db)):
    db_user = AuthService.logout(db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Neuspješna odjava")
    return db_user