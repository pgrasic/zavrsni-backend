from src.models.vezne_tablice import korisnik_lijek
from sqlalchemy.orm import Session

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
	async def update_status(korisnik_id, lijek_id, status, db: Session):
		stmt = db.execute(
			korisnik_lijek.update().where(
				(korisnik_lijek.c.korisnik_id == korisnik_id) &
				(korisnik_lijek.c.lijek_id == lijek_id)
			).values(status=status)
		)
		db.commit()
		return stmt.rowcount > 0

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
		return stmt.rowcount > 0

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
