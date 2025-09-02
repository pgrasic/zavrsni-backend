from dotenv import load_dotenv
import pytest
from unittest.mock import AsyncMock, patch
from src.services.reminder_service import send_reminder_email

load_dotenv()

@pytest.mark.asyncio
async def test_send_reminder_email_sends_correct_message():
    # Mock fast_mail.send_message
    with patch('src.services.reminder_service.fast_mail.send_message', new_callable=AsyncMock) as mock_send:
        to_email = "markog19@gmail.com"
        lijek_naziv = "Paracetamol"
        kolicina = 2
        await send_reminder_email(to_email, lijek_naziv, kolicina)
        # Check that send_message was called once
        assert mock_send.call_count == 1
        # Check the message content
        args, kwargs = mock_send.call_args
        message = args[0]
        assert message.subject == f"Podsjetnik za lijek: {lijek_naziv}"
        assert message.recipients == [to_email]
        assert f"Količina: {kolicina}" in message.body
