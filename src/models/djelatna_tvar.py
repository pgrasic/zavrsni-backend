from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .vezne_tablice import djelatna_tvar_lijek
class DjelatnaTvar(Base):
    __tablename__ = "djelatne_tvari"

    id = Column(Integer, primary_key=True, index=True)
    naziv = Column(String, unique=True, index=True, nullable=False)

    lijekovi = relationship("Lijek", secondary=djelatna_tvar_lijek, back_populates="djelatne_tvari")