from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class RemindersLog(Base):
    __tablename__ = "reminders_log"

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey("korisnici.id"), nullable=False, index=True)
    lijek_id = Column(Integer, ForeignKey("lijekovi.id"), nullable=False)
    status = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.now(), nullable=False)

    korisnik = relationship("Korisnik", backref="reminder_logs")
    lijek = relationship("Lijek", backref="reminder_logs")
