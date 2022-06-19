import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME: str = os.getenv('APP_NAME')
    SMS_SENDER_NUMBER: str = os.getenv('SMS_SENDER_NUMBER')
    SMS_API_TOKEN: str = os.getenv('SMS_API_TOKEN')
    SMS_TEMPLATE: str = os.getenv('SMS_TEMPLATE')

    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASS: str = os.getenv("MONGO_PASS")
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT"))

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT"))
    REDIS_USER: str = os.getenv("REDIS_USER")
    REDIS_PASS: str = os.getenv("REDIS_PASS")
    REDIS_DB: int = int(os.getenv("REDIS_DB"))

    RABBIT_HOST: str = os.getenv("RABBIT_HOST")
    RABBIT_PORT: str = int(os.getenv("RABBIT_PORT"))
    RABBIT_USER: str = os.getenv("RABBIT_USER")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS")

    VALID_PERIOD_FILTERS: list = os.getenv("VALID_PERIOD_FILTERS")
    VALID_VALUE_FILTERS: list = os.getenv("VALID_VALUE_FILTERS")
    VALID_SEARCH_FIELDS: list = os.getenv("VALID_SEARCH_FIELDS")

    VALID_GRID_KEYS: list = os.getenv("VALID_GRID_KEYS")


VALID_PROFILE_KEYS = ["customerPhoneNumber", "customerFirstName", "customerLastName", "customerId",
                      "customerProvince", "customerCity", "customerPostalCode", "customerClass", "customerType",
                      "customerJalaliCreateTime", "customerShopName", "customerNationalID", "customerJalaliConfirmDate",
                      "customerShopLocation", "customerEducation", "customerDocumentStatus", "customerShopPostalCode",
                      "customerEmail", "customerShopStatus", "customerAddress", "customerStatus", "customerID"]
VALID_GRID_KEYS = ["customerID", "customerFirstName", "customerLastName", "customerMobileNumber",
                   "customerJalaliCreateTime", "customerStatus", "customerLastOrderDate", "customerWholeOrderNumber",
                   "customerWholeOrderAmount"]
config = Config()
