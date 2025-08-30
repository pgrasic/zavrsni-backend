from sqlalchemy import Column, ForeignKey, Integer, String
from .vezne_tablice import korisnik_lijek, djelatna_tvar_lijek
from sqlalchemy.orm import relationship

from .base import Base

class Lijek(Base):
    __tablename__ = "lijekovi"

    id = Column(Integer, primary_key=True, index=True)
    idKategorija = Column(Integer, ForeignKey("kategorije.id"), nullable=False)
    idDjelatnaTvar = Column(Integer, ForeignKey("djelatne_tvari.id"), nullable=False)
    naziv = Column(String, unique=True, index=True, nullable=False)
    opis = Column(String, nullable=False)
    cijena = Column(Integer, nullable=False)

    korisnici = relationship("Korisnik", secondary=korisnik_lijek, back_populates="lijekovi")
    djelatne_tvari = relationship("DjelatnaTvar", secondary=djelatna_tvar_lijek, back_populates="lijekovi")
