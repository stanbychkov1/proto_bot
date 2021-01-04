import logging

from dotenv import load_dotenv
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from utilis import send_feedback, send_feedback_by_email, write_down_info

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()

EMAIL, FULL_NAME, FEEDBACK = range(3)


def start(update: Update, context: CallbackContext) -> int:
    """Вступительное обращение бота"""

    update.message.reply_text(
        'Привет! Здесь вы можете оставить обратную связь.\n'
        'Напишите ваше полное имя.',
    )
    write_down_info(update, context)
    return FULL_NAME


def full_name(update: Update, context: CallbackContext) -> int:
    """Получение имени клиента"""

    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишите ваш e-mail для обратной связи.',
        reply_markup=ReplyKeyboardRemove(),
    )
    write_down_info(update, context)
    return EMAIL


def email(update: Update, context: CallbackContext) -> int:
    """Получение email клиента"""

    user = update.message.from_user
    logger.info("Email of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Теперь вы можете оставить вашу обратную связь.',
        reply_markup=ReplyKeyboardRemove(),
    )
    write_down_info(update, context)
    return FEEDBACK


def feedback(update: Update, context: CallbackContext) -> int:
    """Получение фидбэка от клиента"""

    user = update.message.from_user
    logger.info("User %s left a feedback.", user.first_name)
    update.message.reply_text(
        'В ближайшее время мы с вами обязательно свяжемся.',
        reply_markup=ReplyKeyboardRemove(),
    )
    write_down_info(update, context)
    send_feedback(update, context)
    send_feedback_by_email(update, context)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Остановка бота"""

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Спасибо за вашу обратную связь. Она помогает нам развиваться.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
