#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import json
import logging

import requests
from telegram.ext import (BaseFilter, CommandHandler, Filters, MessageHandler,
                          Updater)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Load config file
with open('config.json') as config_file:
    CONFIGURATION = json.load(config_file)


class FilterSender(BaseFilter):

    def filter(self, message):
        return not CONFIGURATION["authorized_chat_ids"] or message.chat_id in list(CONFIGURATION["authorized_chat_ids"])


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
# def start(bot, update):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def callback_status(bot, job):
    result = checkRpi()
    if result['status'] != 'ok':
        dump = json.dumps(result, indent=2)
        bot.send_message(chat_id=job.context, text=dump)


def start(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text='Health check is ON...')
    cleanup_queue(job_queue)
    job_queue.run_repeating(callback_status, 60, context=update.message.chat_id)
    job_queue.enabled = True


def stop(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text='Health check is OFF...')
    job_queue.enabled = False
    cleanup_queue(job_queue)


def cleanup_queue(job_queue):
    for job in job_queue.jobs():
        job.schedule_removal()


def checkRpi():
    response = requests.get("http://192.168.31.40:8085")
    return json.loads(response.text)


def status(bot, update):
    dump = json.dumps(checkRpi(), indent=2)
    bot.send_message(chat_id=update.message.chat_id, text=dump)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(CONFIGURATION["telegram_token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

    # Filter
    fs = FilterSender()

    dp.add_handler(CommandHandler("start", start, filters=fs, pass_job_queue=True))
    dp.add_handler(CommandHandler("stop", stop, filters=fs, pass_job_queue=True))
    dp.add_handler(CommandHandler("status", status, filters=fs))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # Filter messages
    dp.add_handler(MessageHandler(fs & Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
