from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    ime: str
    prezime: str
    email: EmailStr
    broj_telefona: str
    lozinka: str

class UserRead(BaseModel):
    id: int
    ime: str
    prezime: str
    email: EmailStr
    broj_telefona: str

    class Config:
        orm_mode = True

from typing import Optional

class UserUpdate(BaseModel):
    ime: Optional[str] = None
    prezime: Optional[str] = None
    email: Optional[EmailStr] = None
    broj_telefona: Optional[str] = None
    lozinka: Optional[str] = None