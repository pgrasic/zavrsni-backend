from src.models.lijek import Lijek
from src.models.user import Korisnik
from src.services.korisnik_lijek_service import KorisnikLijekService
from collections import Counter
from sqlalchemy.orm import Session

class StatsService:
    @staticmethod
    async def get_stats(db: Session):
        sent_reminders = await KorisnikLijekService.get_all(db)
        confirmed_reminders = await KorisnikLijekService.get_all_confirmed_reminders(db)
        total_users = db.query(Korisnik).count()
        total_meds = db.query(Lijek).count()
        lijekova_po_korisniku = Counter(getattr(t, 'korisnik_id', None) for t in sent_reminders)
        most_loaded_user = max(lijekova_po_korisniku, key=lijekova_po_korisniku.get, default=None)
        total = sum(lijekova_po_korisniku.values()) or 1
        lijek_relative = {
            str(korisnik_id): round(count / total, 3)
            for korisnik_id, count in lijekova_po_korisniku.items()
        }
        return {
            "total_users": total_users,
            "total_meds": total_meds,
            "sent_reminders": len(sent_reminders),
            "confirmed_reminders": len(confirmed_reminders),
            "most_loaded_user": most_loaded_user,
            "lijek_relative": lijek_relative
        }