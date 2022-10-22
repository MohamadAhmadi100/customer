import pymongo
from config import config


class MongoConnection:
    __slots__ = ["__client", "__db_name", "collection", "__instance", "__db_name_log", "__db_name_counter"]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(MongoConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__client = pymongo.MongoClient(
            config.MONGO_HOST,
            config.MONGO_PORT,
            username=config.MONGO_USER,
            password=config.MONGO_PASS
        )
        self.__db_name = self.__client["db-customer"]
        self.__db_name_log = self.__client["db-log"]
        # self.__db_name_counter = self.__client["counter"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()

    @property
    def customer(self):
        return self.__db_name["customer"]

    @property
    def log(self):
        return self.__db_name_log["log"]

    @property
    def counter(self):
        return self.__db_name["customer"].counter

    @property
    def shahkar(self):
        return self.__db_name['shahkar']


class OldMongoConnection:
    __slots__ = ["__client", "__db_name", "collection", "__instance"]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(OldMongoConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__client = pymongo.MongoClient(
            config.OLD_MONGO_HOST,
            config.OLD_MONGO_PORT,
            username=config.OLD_MONGO_USER,
            password=config.OLD_MONGO_PASS
        )
        self.__db_name = self.__client["mainDB"]
        # self.__db_name_log = self.__client["db-log"]
        # self.__db_name_counter = self.__client["counter"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()

    @property
    def customers(self):
        return self.__db_name["customers"]


class AttributeMongoConnection:
    __slots__ = ["__client", "__db_name", "collection", "__instance"]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(AttributeMongoConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__client = pymongo.MongoClient(
            config.ATTRIBUTE_MONGO_HOST,
            config.ATTRIBUTE_MONGO_PORT,
            username=config.ATTRIBUTE_MONGO_USER,
            password=config.ATTRIBUTE_MONGO_PASS
        )
        self.__db_name = self.__client["db-attribute"]
        # self.__db_name_log = self.__client["db-log"]
        # self.__db_name_counter = self.__client["counter"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()

    @property
    def customer_attributes(self):
        return self.__db_name["customer"]
