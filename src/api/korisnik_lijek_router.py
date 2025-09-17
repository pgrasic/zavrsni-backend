
import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.korisnik_lijek_service import KorisnikLijekService
from src.schemas.korisnik_lijek_schema import KorisnikLijekCreate, KorisnikLijekRead
from sqlalchemy.orm import Session
from src.utils.dependencies import get_current_user
from src.db.database import get_db
router = APIRouter()

@router.post("")
async def create(entry: KorisnikLijekCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.create(entry, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return {"success": db_entry}
@router.get("/{lijek_id}", response_model=KorisnikLijekRead)
async def get_one(lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.get_one(current_user.id, lijek_id, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry

@router.put("/{lijek_id}", response_model=KorisnikLijekRead)
async def update(lijek_id: int, entry: KorisnikLijekCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.update(current_user.id, lijek_id, entry, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry

@router.delete("/{lijek_id}")
async def delete(lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_entry = await KorisnikLijekService.delete(current_user.id, lijek_id, db)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Korisnik-Lijek veza nije pronađena")
    return db_entry


@router.post("/{lijek_id}/confirm")
async def confirm_reminder(lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.create_reminder(current_user.id, lijek_id, "confirmed", db, changed_at=datetime.datetime.now())
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik potvrđen"}

@router.post("/{lijek_id}/skip")
async def skip_reminder(lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.update_status_skipped(current_user.id, lijek_id, "skipped", db)
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik preskočen"}

@router.post("/{lijek_id}/snooze")
async def snooze_reminder(lijek_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = await KorisnikLijekService.update_status_snooze(current_user.id, lijek_id, "snoozed", db)
    if not result:
        raise HTTPException(status_code=404, detail="Podsjetnik nije pronađen")
    return {"message": "Podsjetnik odgođen"}

@router.get("", response_model=List[KorisnikLijekRead])
async def get_all(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
     
    result = await KorisnikLijekService.get_all_for_user(current_user.id, db)
    print("Fetched reminders:", result)
    return result
