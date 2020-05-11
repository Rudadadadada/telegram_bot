from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import time
import datetime
from data import TOKEN


REQUEST_KWARGS = {'proxy_url': 'socks5://127.0.0.1:9150'}
# REQUEST_KWARGS = {}


def get_time(update, context):
    time_time = time.asctime().split()
    update.message.reply_text(time_time[3])


def get_date(update, context):
    time_time = time.asctime().split()
    update.message.reply_text(time_time[1] + ' ' + time_time[2] + ' ' + time_time[-1])


def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text(f'Вернусь через {due} секунд')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def unset_timer(update, context):
    if 'job' not in context.chat_data:
        update.message.reply_text('Нет активного таймера')
        return
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']
    update.message.reply_text('Хорошо, вернулся сейчас!')


def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("set_timer", set_timer,
                                          pass_args=True,
                                          pass_job_queue=True,
                                          pass_chat_data=True))
    dispatcher.add_handler(CommandHandler("unset", unset_timer,
                                          pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('date', get_date))
    dispatcher.add_handler(CommandHandler('time', get_time))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
