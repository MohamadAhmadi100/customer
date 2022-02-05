import pymongo
from config import config


class MongoConnection:
    __slots__ = ["__client", "__db_name", "collection", "__instance", "__db_name_log"]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(MongoConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__client = pymongo.MongoClient(
            config.MONGO_HOST,
            username=config.MONGO_USER,
            password=config.MONGO_PASS
        )
        self.__db_name = self.__client[config.MONGO_DB]
        self.__db_name_log = self.__client[config.MONGO_DB_LOG]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()

    @property
    def customer(self):
        return self.__db_name[config.CUSTOMER_COLLECTION]

    @property
    def profile(self):
        return self.__db_name[config.PROFILE_COLLECTION]

    @property
    def log(self):
        return self.__db_name_log[config.LOG_COLLECTION]
