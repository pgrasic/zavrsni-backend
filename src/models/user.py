from sqlalchemy import Column, Integer, String, Boolean
from .vezne_tablice import korisnik_lijek
from sqlalchemy.orm import relationship
from .base import Base

class Korisnik(Base):
    __tablename__ = "korisnici"

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String, index=True, nullable=False)
    prezime = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # email moze biti null
    hashed_lozinka = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)   # false je obicni korisnik, a true je admin

    lijekovi = relationship("Lijek", secondary=korisnik_lijek, back_populates="korisnici")
