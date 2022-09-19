import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME: str = os.getenv('APP_NAME')
    SMS_SENDER_NUMBER: str = os.getenv('SMS_SENDER_NUMBER')
    SMS_API_TOKEN: str = os.getenv('SMS_API_TOKEN')
    SMS_TEMPLATE: str = os.getenv('SMS_TEMPLATE')
    SMS_CANCEL_STATUS_TEMPLATE: str = os.getenv('SMS_CANCEL_STATUS_TEMPLATE')
    SMS_ACTIVATE_TEMPLATE: str = os.getenv('SMS_ACTIVATE_TEMPLATE')
    SMS_REGISTER_TEMPLATE: str = os.getenv('SMS_REGISTER_TEMPLATE')

    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASS: str = os.getenv("MONGO_PASS")
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT"))

    OLD_MONGO_USER: str = os.getenv("OLD_MONGO_USER")
    OLD_MONGO_PASS: str = os.getenv("OLD_MONGO_PASS")
    OLD_MONGO_HOST: str = os.getenv("OLD_MONGO_HOST")
    OLD_MONGO_PORT: int = int(os.getenv("OLD_MONGO_PORT"))

    ATTRIBUTE_MONGO_USER: str = os.getenv('ATTRIBUTE_MONGO_USER')
    ATTRIBUTE_MONGO_PASS: str = os.getenv("ATTRIBUTE_MONGO_PASS")
    ATTRIBUTE_MONGO_HOST: str = os.getenv("ATTRIBUTE_MONGO_HOST")
    ATTRIBUTE_MONGO_PORT: int = int(os.getenv("ATTRIBUTE_MONGO_PORT"))

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

    TELEGRAM_ID: str = os.getenv("TELEGRAM_ID")
    TELEGRAM_REQUEST_URL: str = os.getenv("TELEGRAM_REQUEST_URL")
    DEBUG_MODE: bool = int(os.getenv("DEBUG_MODE"))


VALID_PROFILE_KEYS = ["customerPhoneNumber", "customerFirstName", "customerLastName", "customerRegionCode",
                      "customerStateName", "customerCityName", "customerPostalCode", "customerClass", "customerType",
                      "customerJalaliCreateTime", "customerShopName", "customerNationalID", "customerJalaliConfirmDate",
                      "customerShopLocation", "customerEducation", "customerDocumentStatus", "customerShopPostalCode",
                      "customerEmail", "customerShopStatus", "customerAddress", "customerStatus", "customerID",
                      "customerOfoghCode", "customerAccFormalAccCode", "customerSelCustomerCode",
                      "customerActiveCredit", "customerCreditAmount"]
VALID_GRID_KEYS = ["customerID", "customerFirstName", "customerLastName", "customerMobileNumber",
                   "customerJalaliCreateTime", "customerStatus", "customerNationalID"]
KOSAR_REGION_CODES = {"R1": "1", "TE": "9", "TO": "8", "TC": "4", "TWN": "7", "TN": "10", "R4": "5", "R5": "6",
                      "TW": "11", "R2": "2", "R3": "3"}
config = Config()
