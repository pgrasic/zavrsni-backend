from fastapi import APIRouter, Depends, HTTPException,status
from typing import List
from src.schemas.auth_schema import RegisterSchema, TokenSchema, LoginSchema
from services.auth_service import AuthService
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=TokenSchema)
async def register(user: RegisterSchema, db: Session = Depends(get_db)):
    db_user = await AuthService.register(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Neuspješna registracija")
    return db_user

#@router.get("/me")
#async def get_me():
#    pass

@router.post("/login", response_model=TokenSchema)
async def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = await AuthService.login(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Neispravni podaci")
    return db_user

@router.post("/logout")
async def logout(db: Session = Depends(get_db)):
    db_user = await AuthService.logout(db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Neuspješna odjava")
    return db_user