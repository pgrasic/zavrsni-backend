from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

load_dotenv()


from src.db.database import engine
from src.models.base import Base
Base.metadata.create_all(bind=engine)

from src.api.user_router import router as user_router
from src.api.lijek_router import router as lijek_router
from src.api.auth_router import router as auth_router
from src.api.korisnik_lijek_router import router as korisnik_lijek_router
from src.api.stats_router import router as stats_router

app = FastAPI(
    title="Medication Reminder Backend",
    description="Backend API for medication reminders and management",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_router, prefix="/korisnici", tags=["Korisnici"])
app.include_router(lijek_router, prefix="/lijekovi", tags=["Lijekovi"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(korisnik_lijek_router, prefix="/korisnik-lijek", tags=["KorisnikLijek"])
app.include_router(stats_router, prefix="/stats", tags=["Stats"])
    
@app.get("/")
async def root():
    return {"message": "Medication Reminder Backend API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "medication-reminder-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


