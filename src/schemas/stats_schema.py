from pydantic import BaseModel, ConfigDict

class StatsCreate(BaseModel):
    korisnik_id: int
    lijek_id: int
    doza: float
    vrijeme: str

class StatsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    korisnik_ime: str
    lijek_ime: str
    doza: float
    vrijeme: str
