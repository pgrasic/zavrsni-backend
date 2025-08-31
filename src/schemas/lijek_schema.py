from pydantic import BaseModel, ConfigDict

class LijekCreate(BaseModel):
    naziv: str
    opis: str
    idKategorija: int
    idDjelatnaTvar: int

class LijekRead(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id: int
    naziv: str
    opis: str
    idKategorija: int
    idDjelatnaTvar: int
