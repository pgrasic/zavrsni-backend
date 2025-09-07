from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .vezne_tablice import korisnik_lijek, djelatna_tvar_lijek
from sqlalchemy.orm import relationship
from src.models.user import Korisnik

from .base import Base

class Lijek(Base):
    __tablename__ = "lijekovi"

    id = Column(Integer, primary_key=True, index=True)
    idDjelatnaTvar = Column(Integer, ForeignKey("djelatne_tvari.id"), nullable=True)
    naziv = Column(String, unique=True, index=True, nullable=False)
    nestasica = Column(Boolean, nullable=False)
    korisnici = relationship("Korisnik", secondary=korisnik_lijek, back_populates="lijekovi")
    djelatne_tvari = relationship("DjelatnaTvar", secondary=djelatna_tvar_lijek, back_populates="lijekovi")
    accepted = Column(Boolean, default=False)

