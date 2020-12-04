import os

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, ConversationHandler, MessageHandler,
                          Updater)

from feedback_bot import (EMAIL, FEEDBACK, FULL_NAME, cancel, email, feedback,
                          full_name, start)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FULL_NAME: [MessageHandler(filters=None, callback=full_name)],
            EMAIL: [MessageHandler(filters=None, callback=email)],
            FEEDBACK: [MessageHandler(filters=None, callback=feedback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
