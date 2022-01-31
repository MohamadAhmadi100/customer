from pydantic import BaseSettings


class Config(BaseSettings):
    MONGO_USER = 'root'
    MONGO_PASS = 'qweasdQWEASD'
    MONGO_HOST = '200.100.100.223:27017'
    MONGO_DB = "db-customer"
    CUSTOMER_COLLECTION = "customer"
    PROFILE_COLLECTION = "profile"


config = Config()
