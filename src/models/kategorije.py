from sqlalchemy import Column, Integer, String

from .base import Base

class Kategorija(Base):
    __tablename__ = "kategorije"

    id = Column(Integer, primary_key=True, index=True)
    naziv = Column(String, unique=True, index=True, nullable=False)
