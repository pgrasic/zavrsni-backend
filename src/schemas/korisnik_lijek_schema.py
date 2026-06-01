from pydantic import BaseModel, ConfigDict
from datetime import datetime

class KorisnikLijekCreate(BaseModel):
    korisnik_id: int
    lijek_id: int
    pocetno_vrijeme: datetime
    razmak_sati: int
    kolicina: int = 1

class KorisnikLijekUpdate(BaseModel):
    pocetno_vrijeme: datetime
    razmak_sati: int
    kolicina: int

class KorisnikLijekRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    korisnik_id: int
    lijek_id: int
    pocetno_vrijeme: datetime
    razmak_sati: int
    kolicina: int
    status: str = "pending"
