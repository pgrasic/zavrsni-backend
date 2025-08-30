from sqlalchemy import Column, Integer, String
from .vezne_tablice import korisnik_lijek
from sqlalchemy.orm import relationship

from .base import Base


class Korisnik(Base):
    __tablename__ = "korisnici"

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String, unique=True, index=True, nullable=False)
    prezime = Column(String, unique=True, index=True, nullable=False)
    broj_telefona = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_lozinka = Column(String, nullable=False)

    lijekovi = relationship("Lijek", secondary=korisnik_lijek, back_populates="korisnici")
