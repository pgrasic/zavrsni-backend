# app/routers/korisnik_lijek.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.korisnik_lijek_service import KorisnikLijekService
from src.schemas.korisnik_lijek_schema import KorisnikLijekCreate, KorisnikLijekRead
from sqlalchemy.orm import Session
from src.utils.dependencies import get_current_user
from src.db.database import get_db
router = APIRouter()

@router.post("", response_model=KorisnikLijekRead)
async def create(entry: KorisnikLijekCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.create(entry, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry

@router.get("/{korisnik_id}/{lijek_id}", response_model=KorisnikLijekRead)
async def get_one(korisnik_id: int, lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.get_one(korisnik_id, lijek_id, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry

@router.put("/{korisnik_id}/{lijek_id}", response_model=KorisnikLijekRead)
async def update(korisnik_id: int, lijek_id: int, entry: KorisnikLijekCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.update(korisnik_id, lijek_id, entry, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry

@router.delete("/{korisnik_id}/{lijek_id}")
async def delete(korisnik_id: int, lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.delete(korisnik_id, lijek_id, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry


@router.post("/{korisnik_id}/{lijek_id}/confirm")
async def confirm_reminder(korisnik_id: int, lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.update_status(korisnik_id, lijek_id, "confirmed", db)
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik potvrđen"}

@router.post("/{korisnik_id}/{lijek_id}/postpone")
async def postpone_reminder(korisnik_id: int, lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.update_status(korisnik_id, lijek_id, "postponed", db)
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik odgođen"}

@router.post("/{korisnik_id}/{lijek_id}/skip")
async def skip_reminder(korisnik_id: int, lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.update_status(korisnik_id, lijek_id, "skipped", db)
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik preskočen"}

@router.get("", response_model=List[KorisnikLijekRead])
async def get_all(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await KorisnikLijekService.get_all_for_user(current_user.id, db)

