import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class LogHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        LogHandler.log_folder_create()
        super().__init__(*args, **kwargs)

    def doRollover(self):
        dates = []
        if os.path.isfile("app.log.8"):
            dates.extend(os.path.getmtime(f"app.log.{i}") for i in range(1, 8))
            should_remove = sorted(dates, reverse=True).pop(-1)
            os.remove(f"app.log.{should_remove}")
        super().doRollover()

    @staticmethod
    def log_folder_create():
        if not os.path.exists("log"):
            os.mkdir("log")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        LogHandler("log/app.log", mode='a',
                   maxBytes=5_000_000,
                   backupCount=8),
    ]
)


# functions below add log whenever we call them
# and each one is called based on the log we want to put

def connection_log(host, port, headers):
    sys.stdout.write("\033[0;32m")
    print(" [x] Consumer running on host \"" + host + ":" + str(port) + "\" , "
          + "headers : " + str(headers), end="")
    sys.stdout.write("\033[1;36m")
    print(" -- Waiting for Requests ...")


def action_log(message, app_name):
    sys.stdout.write("\033[1;31m")
    print("\n => Entry action: ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Entry action: {message.get(app_name).get('action')}")
    print(message.get(app_name).get("action"))


def request_log(message, app_name):
    sys.stdout.write("\033[1;31m")
    print("                  Request:  ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Request: {message.get(app_name).get('body')}")
    print(message.get(app_name).get("body"))


def response_log(message):
    sys.stdout.write("\033[1;31m")
    print("                  Response: ", end="")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.info(f"Response: {message}")
    print(message)


def pika_exception_log(error):
    sys.stdout.write("\033[1;31m")
    sys.stdout.write("\033[;1m\033[1;34m")
    logging.error(f"Error: {error}")
    print(error)
