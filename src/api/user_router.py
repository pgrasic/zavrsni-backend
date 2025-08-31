from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.user_schema import UserCreate, UserUpdate, UserRead  
from services.user_service import UserService  # Pretpostavljamo da postoji UserService  
from db.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await UserService.create_user(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Broj telefona već registriran")
    return db_user


@router.get("/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    db_user = await UserService.get_user(id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    return db_user

@router.put("/{id}")
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = await UserService.update_user(id, user, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = await UserService.delete_user(id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("")
async def get_all_users(db: Session = Depends(get_db)):
    return await UserService.get_all_users(db)

