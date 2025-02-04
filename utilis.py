import json
import logging
import os
import smtplib
import telegram
from typing import List

from dotenv import load_dotenv
from telegram import Message, Update
from telegram.ext import CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()

USER_INFO = os.getenv('CLIENTS_JSON')
EMAIL_FROM = os.getenv('EMAIL_FROM')
PASSWORD = os.getenv('PASSWORD')
CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
EMAIL_TO = os.getenv('EMAIL_TO')
SMTP = os.getenv('SMTP')


bot = telegram.Bot(token=TELEGRAM_TOKEN)


def write_json(data, filename=USER_INFO):
    """Запись в файл json"""

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def write_down_info(update: Update, context: CallbackContext):
    """Запись информации"""

    user = update.message.from_user
    chat_id = str(update.effective_message.chat_id)
    username = user['username']
    f = open(USER_INFO)
    data = json.load(f)
    if chat_id not in data.keys():
        logger.info('Writing down User chat id')
        data[chat_id] = [f'@{username}', ]
        write_json(data)
    else:
        logger.info('Writing down User infos')
        data[chat_id].append(update.message.text)
        write_json(data)
    f.close()


def find_client(update: Update,
        context: CallbackContext, feedback=None) -> List[str]:
    """Поиск фидбэека для отправки в чат или эмейл"""

    chat_id = str(update.effective_message.chat_id)
    f = open(USER_INFO)
    data = json.load(f)
    if chat_id in data.keys():
        feedback = data[chat_id]
    f.close()
    return feedback


def send_feedback(update: Update, context: CallbackContext) -> Message:
    """Отправка фидбэка в чат автора"""

    text = find_client(update, context)
    return bot.send_message(
        chat_id=CHAT_ID,
        text='\n'.join(text))


def send_feedback_by_email(update: Update, context: CallbackContext):
    """Отправка письма с фидбэком на почту автора"""

    text = find_client(update, context)
    port = 465
    with smtplib.SMTP_SSL(SMTP, port) as server:
        server.login(EMAIL_FROM, PASSWORD)
        logger.info('Server logged in')
        server.sendmail(EMAIL_FROM, EMAIL_TO, '\n'.join(text))
        logger.info('Email send to Author')
        server.quit()
