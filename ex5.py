from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from data import TOKEN

# REQUEST_KWARGS = {'proxy_url': 'socks5://127.0.0.1:9150'}
REQUEST_KWARGS = {}


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?\n"
        "Чтобы пропустить вопрос, воспользуйтесь командой /skip.")
    return 1


def first_response(update, context):
    locality = update.message.text
    update.message.reply_text(
        "Какая погода в городе {locality}?".format(**locals()))
    return 2


def second_response(update, context):
    weather = update.message.text
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def skip(update, context):
    update.message.reply_text('Какая погода у вас за окном?')
    return 2


def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CommandHandler('skip', skip),
                MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)]
                },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()