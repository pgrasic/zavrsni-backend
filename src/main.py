import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

from src.db.database import engine, SessionLocal
from src.models.base import Base
from src.models.lijek import Lijek
import src.models.user                # noqa: F401
import src.models.djelatna_tvar       # noqa: F401
import src.models.vezne_tablice       # noqa: F401
import src.models.reminders_log       # noqa: F401
Base.metadata.create_all(bind=engine)

from src.services.lijek_service import LijekService
from src.services.reminder_service import process_reminders
from src.api.user_router import router as user_router
from src.api.lijek_router import router as lijek_router
from src.api.auth_router import router as auth_router
from src.api.korisnik_lijek_router import router as korisnik_lijek_router
from src.api.stats_router import router as stats_router

EXCEL_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Halmed_Lijekovi_168bee89087875.xlsx")
)


def start_scheduler():
    scheduler = BackgroundScheduler()

    def reminders_job():
        db = SessionLocal()
        try:
            asyncio.run(process_reminders(db))
        finally:
            db.close()

    def import_lijekovi_job():
        db = SessionLocal()
        try:
            asyncio.run(LijekService.import_djelatne_tvari_from_excel(EXCEL_PATH, db))
            asyncio.run(LijekService.import_lijekovi_from_excel(EXCEL_PATH, db))
        finally:
            db.close()

    scheduler.add_job(reminders_job, "interval", minutes=1)
    scheduler.add_job(import_lijekovi_job, "interval", weeks=1)
    scheduler.start()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    start_scheduler()

    db = SessionLocal()
    try:
        if db.query(Lijek).count() == 0:
            print("Empty DB — importing medications from Excel...")
            await LijekService.import_djelatne_tvari_from_excel(EXCEL_PATH, db)
            await LijekService.import_lijekovi_from_excel(EXCEL_PATH, db)
            print("Import complete.")
    finally:
        db.close()

    yield


app = FastAPI(
    title="Medication Reminder Backend",
    description="Backend API for medication reminders and management",
    version="1.0.0",
    lifespan=lifespan,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
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


@app.get("/")
async def root():
    return {"message": "Medication Reminder Backend API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "medication-reminder-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
