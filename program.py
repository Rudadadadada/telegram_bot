from telegram.ext import Updater, MessageHandler, Filters
from data import TOKEN


# REQUEST_KWARGS = {'proxy_url': 'socks5://127.0.0.1:9150'}
REQUEST_KWARGS = {}


def echo(update, context):
    update.message.reply_text(f'Я получил сообщение {update.message.text}')


def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
