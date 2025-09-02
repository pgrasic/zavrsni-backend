from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table

from .base import Base

korisnik_lijek = Table(
    "korisnik_lijek",
    Base.metadata,
    Column("korisnik_id", Integer, ForeignKey("korisnici.id")),
    Column("lijek_id", Integer, ForeignKey("lijekovi.id")),
    Column("pocetno_vrijeme", DateTime, nullable=False),
    Column("razmak_sati", Integer, nullable=False),
    Column("kolicina", Integer, nullable=False, default=1),
    Column("status", String, nullable=False, default="pending")
)

djelatna_tvar_lijek = Table(
    "djelatna_tvar_lijek",
    Base.metadata,
    Column("djelatne_tvari_id", Integer, ForeignKey("djelatne_tvari.id")),
    Column("lijek_id", Integer, ForeignKey("lijekovi.id"))
)
