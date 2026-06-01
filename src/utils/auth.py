import os
import datetime
import requests
from jose import jwt, JWTError
from fastapi import HTTPException, status

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256", "HS256"]
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

ACTION_TOKEN_EXPIRE_HOURS = 24

def create_action_token(korisnik_id: int, lijek_id: int, action: str) -> str:
    payload = {
        "sub": str(korisnik_id),
        "lijek_id": lijek_id,
        "action": action,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=ACTION_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_action_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired action token")

def get_jwk():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    return requests.get(jwks_url).json()["keys"]

def verify_jwt(token: str):
    unverified_header = jwt.get_unverified_header(token)
    if unverified_header.get("alg") == "HS256":
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    jwks = get_jwk()
    rsa_key = {}
    if "kid" not in unverified_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token header missing 'kid'")
    for key in jwks:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return payload
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")