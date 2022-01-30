from pydantic import BaseSettings


class Config(BaseSettings):
    MONGO_USER = ''
    MONGO_PASS = ''
    MONGO_HOST = 'localhost:27017'
    MONGO_DB = "db-customer"
    CUSTOMER_COLLECTION = "customer"
    PROFILE_COLLECTION = "profile"


config = Config()
