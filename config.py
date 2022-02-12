import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME: str = os.getenv('APP_NAME')

    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASS: str = os.getenv("MONGO_PASS")
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_DB: str = os.getenv("MONGO_DB")
    MONGO_DB_LOG: str = os.getenv("MONGO_DB_LOG")
    CUSTOMER_COLLECTION: str = os.getenv("CUSTOMER_COLLECTION")
    LOG_COLLECTION: str = os.getenv("LOG_COLLECTION")
    PROFILE_COLLECTION: str = os.getenv("PROFILE_COLLECTION")

    RABBIT_HOST: str = os.getenv("RABBIT_HOST")


config = Config()
