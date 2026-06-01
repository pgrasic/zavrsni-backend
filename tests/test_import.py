from dotenv import load_dotenv
load_dotenv()

import asyncio
import src.models.user
import src.models.lijek
import src.models.djelatna_tvar
import src.models.vezne_tablice
import src.models.reminders_log
from src.db.database import SessionLocal
from src.services.lijek_service import LijekService

FILE_PATH = "/Users/petragrasic/Desktop/zavrsni_za_smotru/back/Halmed_Lijekovi_168bee89087875.xlsx"


def test_import_djelatne_tvari():
    db = SessionLocal()
    try:
        asyncio.run(LijekService.import_djelatne_tvari_from_excel(FILE_PATH, db))
    finally:
        db.close()


def test_import_lijekovi():
    db = SessionLocal()
    try:
        asyncio.run(LijekService.import_lijekovi_from_excel(FILE_PATH, db))
    finally:
        db.close()
