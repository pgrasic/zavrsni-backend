from src.services.user_service import UserService
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
        korisnici_id = Counter(getattr(t, 'korisnik_id', None) for t in sent_reminders)
        korisnici = []
        for korisnik_id in korisnici_id:
            print(f"Korisnik ID: {korisnik_id}, Count: {korisnici_id[korisnik_id]}")
            korisnik = await UserService.get_user(korisnik_id, db)
            if korisnik:
                korisnici.append(korisnik)
        lijek_relative = {}
        total = len(korisnici) or 1
        
        for korisnik in korisnici:
            reminders = await KorisnikLijekService.get_all_for_user(korisnik.id, db)
            lijek_relative[str(korisnik.email.split("@")[0])] = round(len(reminders) / total, 3)

        return {
            "total_users": total_users,
            "total_meds": total_meds,
            "sent_reminders": len(sent_reminders),
            "confirmed_reminders": len(confirmed_reminders),
            "lijek_relative": lijek_relative
        }