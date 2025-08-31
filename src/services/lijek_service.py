from sqlalchemy.orm import Session
from src.models.lijek import Lijek

def get_lijek_by_id(db: Session, lijek_id: int):
    return db.query(Lijek).filter(Lijek.id == lijek_id).first()

def get_all_lijekovi(db: Session):
    return db.query(Lijek).all()

def create_lijek(db: Session, naziv: str, opis: str, doza: str):
    lijek = Lijek(
        naziv=naziv,
        opis=opis,
        doza=doza
    )
    db.add(lijek)
    db.commit()
    db.refresh(lijek)
    return lijek

def update_lijek(db: Session, lijek_id: int, **kwargs):
    lijek = get_lijek_by_id(db, lijek_id)
    if not lijek:
        return None
    for key, value in kwargs.items():
        setattr(lijek, key, value)
    db.commit()
    db.refresh(lijek)
    return lijek

def delete_lijek(db: Session, lijek_id: int):
    lijek = get_lijek_by_id(db, lijek_id)
    if not lijek:
        return None
    db.delete(lijek)
    db.commit()
    return lijek
