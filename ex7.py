from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from data import TOKEN


# REQUEST_KWARGS = {'proxy_url': 'socks5://127.0.0.1:9150'}
REQUEST_KWARGS = {}
poem = ['Природа с красоты своей',
        'Покрова снять не позволяет,',
        'И ты машинами не вынудишь у ней,',
        'Чего твой дух не угадает.']
str_num = 1
some = 0
bot_active = False
suphler_status = False


def start(update, context):
    global bot_active

    bot_active = True
    update.message.reply_text(poem[0])


def next(update, context):
    global bot_active, str_num, some, suphler_status

    if bot_active:
        message = update.message.text
        if message == poem[str_num + some]:
            if str_num + some != len(poem) - 1:
                suphler_status = False
                str_num += 1
                some = 1
                update.message.reply_text(poem[str_num])
            else:
                update.message.reply_text('Здорово! Может повторить?\nВведите /start')
                return stop(update, context)
        else:
            update.message.reply_text('Нет, не так. Вы можете воспользоваться командой '
                                      '/suphler для получения подсказки')
            suphler_status = True
    else:
        update.message.reply_text('Для того, чтобы начать диалог, введите /start')


def suphler(update, context):
    global str_num, bot_active, some, suphler_status

    if bot_active:
        if suphler_status:
            update.message.reply_text(f'Правильная строка:\n{poem[str_num + some]}')
        else:
            update.message.reply_text(f'Эта команда доступна в случае, когда вы ввели не правильную строку')
    else:
        update.message.reply_text('Для того, чтобы начать диалог, введите /start')


def stop(update, context):
    global str_num, bot_active, some, suphler_status

    bot_active = False
    suphler_status = False
    str_num = 1
    some = 0



def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    stop_handler = CommandHandler('stop', stop)
    updater.dispatcher.add_handler(stop_handler)

    suphler_handler = CommandHandler('suphler', suphler)
    updater.dispatcher.add_handler(suphler_handler)

    message_handler = MessageHandler(Filters.text, next)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
