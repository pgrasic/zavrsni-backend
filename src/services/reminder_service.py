from sqlalchemy.orm import Session
from datetime import datetime
from src.models.user import Korisnik
from src.models.lijek import Lijek
from src.models.vezne_tablice import korisnik_lijek
from src.utils.mail_config import fast_mail
from fastapi_mail import MessageSchema
import logging
API_BASE = "http://localhost:8080"
async def send_reminder_email(to_email, lijek_naziv, kolicina, korisnik_id, lijek_id):
    confirm_url = f"{API_BASE}/korisnik-lijek/{korisnik_id}/{lijek_id}/confirm"
    postpone_url = f"{API_BASE}/korisnik-lijek/{korisnik_id}/{lijek_id}/postpone"
    skip_url = f"{API_BASE}/korisnik-lijek/{korisnik_id}/{lijek_id}/skip"
    
    html_body = (
        f"<p>Vrijeme je za uzimanje lijeka <strong>{lijek_naziv}</strong>. Količina: {kolicina}</p>"
        f"<p><a href=\"{confirm_url}\">Potvrdi uzimanje</a></p>"
        f"<p><a href=\"{postpone_url}\">Odgodi</a></p>"
        f"<p><a href=\"{skip_url}\">Preskoči</a></p>"
    )
    subject = f"Podsjetnik za lijek: {lijek_naziv}"
    # send HTML message (many mail clients will render; plain fallback is in html as well)
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=html_body,
        subtype="html"
    )
    try:
        await fast_mail.send_message(message)
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")

def get_due_reminders(db: Session):
    now = datetime.now()
    results = db.execute(
        korisnik_lijek.select()
    ).fetchall()
    due = []
    for r in results:
        elapsed = (now - r.pocetno_vrijeme).total_seconds()
        interval = r.razmak_sati * 3600
        if interval == 0:
            continue  # skip reminders with zero interval to avoid ZeroDivisionError
        if elapsed >= 0 and (elapsed % interval) < 60:
            due.append(r)
    return due

async def process_reminders(db: Session):
    due_reminders = get_due_reminders(db)
    for r in due_reminders:
        user = db.query(Korisnik).filter_by(id=r.korisnik_id).first()
        print("Processing reminder for user:", user.email if user else "Unknown user")
        lijek = db.query(Lijek).filter_by(id=r.lijek_id).first()
        if user and lijek:
            await send_reminder_email(user.email, lijek.naziv, r.kolicina, r.korisnik_id, r.lijek_id)
