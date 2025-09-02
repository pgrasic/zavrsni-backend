from pydantic import BaseModel, ConfigDict

class LijekCreate(BaseModel):
    naziv: str
    idDjelatnaTvar: int | None = None
    nestasica: bool
    accepted: bool | None = None

class LijekRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    naziv: str
    idDjelatnaTvar: int | None = None
    nestasica: bool
    accepted: bool
