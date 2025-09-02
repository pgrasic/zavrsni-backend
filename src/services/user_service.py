
from sqlalchemy.orm import Session
from src.models.user import Korisnik
from src.schemas.user_schema import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def create_user(user: UserCreate, db: Session):
        existing = db.query(Korisnik).filter(
            (Korisnik.broj_telefona == user.broj_telefona) 
        ).first()
        if existing:
            return None
        hashed_lozinka = pwd_context.hash(user.lozinka)
        db_user = Korisnik(
            ime=user.ime,
            prezime=user.prezime,
            email=user.email,
            hashed_lozinka=hashed_lozinka
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user(user_id: int, db: Session):
        return db.query(Korisnik).filter(Korisnik.id == user_id).first()

    @staticmethod
    async def get_all_users(db: Session):
        return db.query(Korisnik).all()

    @staticmethod
    async def update_user(user_id: int, user_update: UserUpdate, db: Session):
        db_user = db.query(Korisnik).filter(Korisnik.id == user_id).first()
        if not db_user:
            return None
        update_data = user_update.dict(exclude_unset=True)
        if "lozinka" in update_data:
            update_data["hashed_lozinka"] = pwd_context.hash(update_data.pop("lozinka"))
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(user_id: int, db: Session):
        db_user = db.query(Korisnik).filter(Korisnik.id == user_id).first()
        if not db_user:
            return None
        db.delete(db_user)
        db.commit()
        return db_user