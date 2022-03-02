import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME: str = os.getenv('APP_NAME')
    SMS_SENDER_NUMBER: str = os.getenv('SMS_SENDER_NUMBER')
    SMS_API_TOKEN: str = os.getenv('SMS_API_TOKEN')
    SMS_TEMPLATE: str = os.getenv('logincode')

    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASS: str = os.getenv("MONGO_PASS")
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_DB: str = os.getenv("MONGO_DB")
    MONGO_DB_LOG: str = os.getenv("MONGO_DB_LOG")
    CUSTOMER_COLLECTION: str = os.getenv("CUSTOMER_COLLECTION")
    LOG_COLLECTION: str = os.getenv("LOG_COLLECTION")

    RABBIT_HOST: str = os.getenv("RABBIT_HOST")


config = Config()
