from pydantic import BaseSettings


class Config(BaseSettings):
    MONGO_USER = 'root'
    MONGO_PASS = 'qweasdQWEASD'
    MONGO_HOST = '200.100.100.223:27017'
    MONGO_DB = "db-customer"
    MONGO_DB_LOG = "db-customer-log"
    CUSTOMER_COLLECTION = "customer"
    LOG_COLLECTION = "log"
    PROFILE_COLLECTION = "profile"


config = Config()
