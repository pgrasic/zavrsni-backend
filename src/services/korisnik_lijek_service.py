import datetime

from src.models.reminders_log import RemindersLog
from src.models.vezne_tablice import korisnik_lijek
from sqlalchemy.orm import Session
from sqlalchemy import select

class KorisnikLijekService:
	@staticmethod
	async def get_all_for_user(korisnik_id, db: Session):
		stmt = db.execute(
			korisnik_lijek.select().where(
				korisnik_lijek.c.korisnik_id == korisnik_id
			)
		)
		return stmt.fetchall()
	@staticmethod
	async def update_status_snooze(korisnik_id, lijek_id, status, db: Session):
		row = db.execute(
			korisnik_lijek.select().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		).fetchone()
		if not row:
			return False
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status=status, pocetno_vrijeme= row.pocetno_vrijeme + datetime.timedelta(minutes=15))
		)
		await KorisnikLijekService.create_reminder(korisnik_id, lijek_id, status, db, changed_at=datetime.datetime.now())
		return stmt
	@staticmethod
	async def update_status_skipped(korisnik_id, lijek_id, status, db: Session):
		row = db.execute(
			korisnik_lijek.select().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		).fetchone()
		if not row:
			return False
		now = datetime.datetime.now()

		interval = datetime.timedelta(hours=row.razmak_sati)
		next_time = row.pocetno_vrijeme + interval
		while next_time <= now:
			next_time += interval
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status=status, pocetno_vrijeme=next_time)
		)
		await KorisnikLijekService.create_reminder(korisnik_id, lijek_id, status, db, changed_at=now)
		db.commit()
		return stmt.rowcount > 0
	@staticmethod
	async def confirm_medication(korisnik_id, lijek_id, db: Session):
		row = db.execute(
			korisnik_lijek.select().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		).fetchone()
		if not row:
			return None
		now = datetime.datetime.now()
		interval = datetime.timedelta(hours=row.razmak_sati)
		elapsed = now - row.pocetno_vrijeme
		periods_passed = int(elapsed.total_seconds() / interval.total_seconds())
		# Anchor the schedule to the ideal dose time, not the actual confirmation moment,
		# so late/early confirmations don't drift the ongoing schedule.
		next_pocetno = row.pocetno_vrijeme + periods_passed * interval
		db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status="confirmed", pocetno_vrijeme=next_pocetno)
		)
		db.add(RemindersLog(
			korisnik_id=korisnik_id,
			lijek_id=lijek_id,
			status="confirmed",
			changed_at=now
		))
		db.commit()
		return True

	@staticmethod
	async def create_reminder(korisnik_id, lijek_id, status, db: Session, changed_at):
			remainderCreate = {
					"korisnik_id": korisnik_id,
					"lijek_id": lijek_id,
					"status": status,
					"changed_at": changed_at
			}
			remainderCreate_dict = dict(remainderCreate)
			remainder = RemindersLog(**remainderCreate_dict)
			db.add(remainder)
			db.commit()
			db.refresh(remainder)
			return remainder	

	@staticmethod
	async def create(entry, db: Session):
		stmt = db.execute(
			korisnik_lijek.insert().values(**entry.dict())
		)
		db.commit()
		return stmt.rowcount > 0    

	@staticmethod
	async def get_one(korisnik_id, lijek_id, db):
		stmt = db.execute(
			korisnik_lijek.select().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		)
		return stmt.fetchone()

	@staticmethod
	async def update(korisnik_id, lijek_id, entry, db: Session):
		db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(**entry.dict())
		)
		db.commit()
		return db.execute(
			korisnik_lijek.select().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		).fetchone()

	@staticmethod
	async def delete(korisnik_id, lijek_id, db: Session):
		stmt = db.execute(
			korisnik_lijek.delete().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			)
		)
		db.commit()
		return stmt.rowcount > 0

	@staticmethod
	async def get_all(db: Session):
		stmt = db.execute(
			korisnik_lijek.select()
		)
		return stmt.fetchall()

	@staticmethod
	async def get_all_confirmed_reminders(db: Session):
		stmt = db.execute(
			select(RemindersLog).where(RemindersLog.status == "confirmed")
		)

		return stmt.scalars().all()

	@staticmethod
	async def get_last_log(korisnik_id, lijek_id, db: Session):
		result = db.execute(
			select(RemindersLog)
			.where(
				(RemindersLog.korisnik_id == korisnik_id) &
				(RemindersLog.lijek_id == lijek_id)
			)
			.order_by(RemindersLog.changed_at.desc())
			.limit(1)
		)
		return result.scalars().first()