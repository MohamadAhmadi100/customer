import pymongo


class MongoConnection:
    __slots__ = ["__client", "__db_name", "collection", "_instance"]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(MongoConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.__client = pymongo.MongoClient()
        self.__db_name = self.__client['db-customer']
        self.collection = self.__db_name['customer']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()
