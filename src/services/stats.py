import datetime
from collections import Counter, defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.lijek import Lijek
from src.models.reminders_log import RemindersLog
from src.models.user import Korisnik
from src.services.korisnik_lijek_service import KorisnikLijekService
from src.services.user_service import UserService


class StatsService:
    @staticmethod
    async def get_stats(db: Session):
        sent_reminders = await KorisnikLijekService.get_all(db)
        confirmed_reminders = await KorisnikLijekService.get_all_confirmed_reminders(db)
        total_users = db.query(Korisnik).count()
        total_meds = db.query(Lijek).count()
        korisnici_id = Counter(getattr(t, "korisnik_id", None) for t in sent_reminders)
        korisnici = []
        for korisnik_id in korisnici_id:
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
            "lijek_relative": lijek_relative,
        }

    @staticmethod
    async def get_adherence_timeline(db: Session):
        """Daily adherence rate (confirmed / (confirmed + skipped)) for the last 90 days."""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=90)
        logs = db.execute(
            select(RemindersLog)
            .where(
                RemindersLog.changed_at >= cutoff,
                RemindersLog.status.in_(["confirmed", "skipped"]),
            )
            .order_by(RemindersLog.changed_at)
        ).scalars().all()

        daily: dict = defaultdict(lambda: {"confirmed": 0, "skipped": 0})
        for log in logs:
            day = log.changed_at.date().isoformat()
            daily[day][log.status] += 1

        result = []
        for day in sorted(daily.keys()):
            c = daily[day]["confirmed"]
            s = daily[day]["skipped"]
            total = c + s
            result.append({
                "date": day,
                "rate": round(c / total, 4) if total > 0 else None,
                "confirmed": c,
                "total": total,
            })
        return result

    @staticmethod
    async def get_missed_heatmap(db: Session):
        """Count of skipped doses grouped by day-of-week (0=Mon) and hour-of-day (0-23)."""
        logs = db.execute(
            select(RemindersLog).where(RemindersLog.status == "skipped")
        ).scalars().all()

        grid: dict = defaultdict(int)
        for log in logs:
            dow = log.changed_at.weekday()   # 0 = Monday, 6 = Sunday
            hour = log.changed_at.hour        # 0-23
            grid[f"{dow}_{hour}"] += 1

        return dict(grid)
