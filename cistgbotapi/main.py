import logging
import time
from multiprocessing import Process
from typing import List

import schedule  # https://schedule.readthedocs.io/en/stable/
import uvicorn
from cistgbot.bot import send_message, configure as configure_bot
from fastapi import FastAPI

import cistgbotapi.repository.message as message_rep
from cistgbotapi.config import settings, load_json_settings
from cistgbotapi.database import create_db, SessionLocal
from cistgbotapi.models import Message
from cistgbotapi.routers import message, user, authentication

logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(message)s')
app = FastAPI()
app.include_router(message.router)
app.include_router(user.router)
app.include_router(authentication.router)

db = SessionLocal()


def send_messages():
    messages: List[Message] = message_rep.get_to_sent(db)
    for m in messages:
        logging.info(f'Send message "{m.message}" to {m.recipient.name}')
        send_message(m.message, [m.recipient.tg_chat_id])
        message_rep.sent(m.id, db)


def start_scheduler() -> None:
    configure_bot(**settings.default.tgbot,
                  intents=load_json_settings(settings.default.tgbot.intents_source))

    send_messages()
    schedule.every(1).seconds.do(send_messages)

    while True:
        schedule.run_pending()
        time.sleep(1)


@app.get("/")
async def root():
    return {"message": "Root content"}


if __name__ == "__main__":
    create_db()
    Process(target=start_scheduler).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
