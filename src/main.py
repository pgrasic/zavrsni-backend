from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import HTTPBearer

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

# JWT security scheme for Swagger UI
app.openapi_schema = None

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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

from apscheduler.schedulers.background import BackgroundScheduler
from src.db.database import SessionLocal
from src.services.reminder_service import process_reminders

def start_scheduler():
    scheduler = BackgroundScheduler()
    def job():
        db = SessionLocal()
        import asyncio
        asyncio.run(process_reminders(db))
        db.close()
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler.start()

@app.on_event("startup")
def startup_event():
    start_scheduler()

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


