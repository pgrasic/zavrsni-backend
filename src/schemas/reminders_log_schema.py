from pydantic import BaseModel
from datetime import datetime


class RemindersLogCreate(BaseModel):
    korisnik_id: int
    lijek_id: int
    status: str


class RemindersLogRead(BaseModel):
    id: int
    korisnik_id: int
    lijek_id: int
    status: str
    changed_at: datetime

    class Config:
        orm_mode = True
