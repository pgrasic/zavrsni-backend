from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.lijek_schema import LijekCreate, LijekRead
from services.lijek_service import LijekService
from db.database import get_db

router = APIRouter()

@router.get("/{id}")
async def get_med(id: int, db: Session = Depends(get_db)):
    db_lijek = await LijekService.get_med(id, db)
    if not db_lijek:
        raise HTTPException(status_code=404, detail="Lijek nije pronađen")
    return db_lijek

@router.post("")
async def create_med(med: LijekCreate, db: Session = Depends(get_db)):
    db_lijek = await LijekService.create_med(med, db)
    if not db_lijek:
        raise HTTPException(status_code=404, detail="Lijek nije pronađen")
    return db_lijek


@router.delete("/{id}")
async def delete_med(id: int, db: Session = Depends(get_db)):
    db_lijek = await LijekService.delete_med(id, db)
    if not db_lijek:
        raise HTTPException(status_code=404, detail="Lijek nije pronađen")
    return db_lijek 

@router.get("")
async def get_all_meds(db: Session = Depends(get_db)):
    return await LijekService.get_all_meds(db)
    