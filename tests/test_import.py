from dotenv import load_dotenv
load_dotenv()

import asyncio
from src.db.database import SessionLocal
from src.services.lijek_service import LijekService

async def run_import():
    db = SessionLocal()
    file_path = "C:/Users/User/Downloads/HALMED.xlsx"  # Zamijeni s pravim imenom datoteke
    result = await LijekService.import_djelatne_tvari_from_excel(file_path, db)

    result = await LijekService.import_lijekovi_from_excel(file_path, db)
    db.close()

if __name__ == "__main__":
    asyncio.run(run_import())
