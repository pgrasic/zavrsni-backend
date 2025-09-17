import pytest
from src.utils.mail_config import send_email
from src.models.user import Korisnik
from src.models.lijek import Lijek

@pytest.mark.asyncio
def test_send_user_meds_email(db_session):

    user = Korisnik(email="markog19@example.com", ime="Marko", prezime="Galic")
    db_session.add(user)
    db_session.commit()
    meds = [
        Lijek(naziv="Med1", idDjelatnaTvar=1, nestasica=False),
        Lijek(naziv="Med2", idDjelatnaTvar=2, nestasica=True)
    ]
    for med in meds:
        db_session.add(med)
    db_session.commit()
    user.lijekovi = meds
    db_session.commit()

    med_list = "\n".join([f"- {med.naziv}" for med in user.lijekovi])
    subject = "Your Medications"
    body = f"Hello {user.ime},\n\nHere are your medications:\n{med_list}"

    result = send_email(to=user.email, subject=subject, body=body)
    assert result 
