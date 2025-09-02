from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    ime: str
    prezime: str
    email: EmailStr
    lozinka: str

class LoginSchema(BaseModel):
    email: EmailStr
    lozinka: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"