from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services.stats import StatsService
from src.utils.dependencies import admin_required
from src.db.database import get_db

router = APIRouter()


@router.get("")
async def get_stats(db: Session = Depends(get_db), current_user=Depends(admin_required)):
    db_stats = await StatsService.get_stats(db)
    if not db_stats:
        raise HTTPException(status_code=404, detail="Statistika nije pronađena")
    return db_stats


@router.get("/adherence")
async def get_adherence(db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return await StatsService.get_adherence_timeline(db)


@router.get("/heatmap")
async def get_heatmap(db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return await StatsService.get_missed_heatmap(db)
