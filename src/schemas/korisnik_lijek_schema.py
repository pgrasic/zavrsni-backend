from pydantic import BaseModel, ConfigDict
from datetime import datetime

class KorisnikLijekCreate(BaseModel):
    korisnik_id: int
    lijek_id: int
    pocetno_vrijeme: datetime
    razmak_sati: int
    kolicina: int = 1

class KorisnikLijekRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # v2 replacement for orm_mode
    korisnik_id: int
    lijek_id: int
    pocetno_vrijeme: datetime
    razmak_sati: int
    kolicina: int
