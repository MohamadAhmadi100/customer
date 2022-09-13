import logging
import traceback
from time import strftime, localtime
from config import config
import requests


def send_telegram_message(msg):
    req = config.TELEGRAM_REQUEST_URL + "send-message"
    requests.post(req, json={
        "text": msg,
        "parse_mode": "html"
    })


def exception_handler():
    now = strftime("%Y-%m-%d %H:%M", localtime())
    message = f'<b>{config.APP_NAME} | {now}</b>\n\n<pre language="python">' \
              f'Failed with exception:\n{traceback.format_exc()}</pre>\n{config.TELEGRAM_ID} 🤬'
    logging.error(message)
    if not config.DEBUG_MODE:
        send_telegram_message(message)
