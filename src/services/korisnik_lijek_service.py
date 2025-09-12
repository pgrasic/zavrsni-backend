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
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status=status, pocetno_vrijeme=datetime.datetime.now() + datetime.timedelta(hours=1))
		)
		await KorisnikLijekService.create_reminder(korisnik_id, lijek_id, status, db, changed_at=datetime.datetime.now() + datetime.timedelta(hours=1))
		return stmt
	@staticmethod
	async def update_status_skipped(korisnik_id, lijek_id, status, db: Session):
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status=status, pocetno_vrijeme=datetime.datetime.now()+ datetime.timedelta(days=1))
		)
		db.execute(RemindersLog.__table__.insert().values(
			korisnik_id=korisnik_id,
			lijek_id=lijek_id,
			status=status,
			changed_at=datetime.datetime.now() + datetime.timedelta(days=1)
		))
		await KorisnikLijekService.create_reminder(korisnik_id, lijek_id, status, db, changed_at=datetime.datetime.now() + datetime.timedelta(days=1))
		db.commit()
		return stmt.rowcount > 0
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
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(**entry.dict())
		)
		db.commit()
		return entry

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
		# return ORM objects
		return stmt.scalars().all()