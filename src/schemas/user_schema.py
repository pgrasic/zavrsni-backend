from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    ime: str
    prezime: str
    email: EmailStr
    lozinka: str

class UserRead(BaseModel):
    id: int
    ime: str
    prezime: str
    email: EmailStr

    class Config:
        orm_mode = True

from typing import Optional

class UserUpdate(BaseModel):
    ime: Optional[str] = None
    prezime: Optional[str] = None
    email: Optional[EmailStr] = None
    broj_telefona: Optional[str] = None
    lozinka: Optional[str] = None