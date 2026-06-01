import os
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.user import Korisnik
from src.models.lijek import Lijek
from src.models.vezne_tablice import korisnik_lijek
from src.utils.mail_config import fast_mail
from src.utils.auth import create_action_token
from fastapi_mail import MessageSchema
import logging

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")

async def send_reminder_email(to_email, lijek_naziv, kolicina, lijek_id, korisnik_id, nestasica: bool = False):
    confirm_url = f"{FRONTEND_BASE_URL}/action?token={create_action_token(korisnik_id, lijek_id, 'confirm')}"
    snooze_url  = f"{FRONTEND_BASE_URL}/action?token={create_action_token(korisnik_id, lijek_id, 'snooze')}"
    skip_url    = f"{FRONTEND_BASE_URL}/action?token={create_action_token(korisnik_id, lijek_id, 'skip')}"
    
    warning_html = ""
    if nestasica:
        warning_html = (
            "<p style=\"color:darkred;font-weight:bold;\">Oprez! Vaš lijek je u nestašici! "
            "Posavjetujte se o mogućim zamjenama s liječnikom ili ljekarnikom.</p>"
        )

    html_body = (
        f"{warning_html}"
        f"<p>Vrijeme je za uzimanje lijeka <strong>{lijek_naziv}</strong>. Količina: {kolicina}</p>"
        f"<p><a href=\"{confirm_url}\">Potvrdi uzimanje</a></p>"
        f"<p><a href=\"{snooze_url}\">Odgodi za 15 minuta</a></p>"
        f"<p><a href=\"{skip_url}\">Preskoči danas</a></p>"
    )
    subject = f"Podsjetnik za lijek: {lijek_naziv}"
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
            continue 
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
            await send_reminder_email(user.email, lijek.naziv, r.kolicina, r.lijek_id, r.korisnik_id, nestasica=bool(lijek.nestasica))
