#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.callback import callback_delete_message
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('help', get_help))


@restricted
def get_help(update, context):
    message = 'Send google drive link, or forward the information with google drive to save manually.\n' \
              'Need to use /sa and /folders for configuration\n\n' \
              'The following is the command of this BOT：\n\n' \
              '/folders - Set favorite folder\n' \
              '/sa - For private chat only, upload the ZIP folder containing sa, and write /sa in the title to set Service Account\n' \
              '/4999baoyue - Private chat only, business negotiation, please attach a message\n' \
              '/help - Output this help\n'
    rsp = update.message.reply_text(message)
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
