from dotenv import load_dotenv
load_dotenv()
from fastapi_mail import MessageSchema
import asyncio
from src.utils.mail_config import fast_mail
from fastapi_mail import MessageSchema


async def test_send():
    message = MessageSchema(
        subject="Volim te <3",
        recipients=["markog19@gmail.com"],  
        body="Puno puno najvise!",
        subtype="plain"
    )
    await fast_mail.send_message(message)

if __name__ == "__main__":
    asyncio.run(test_send())