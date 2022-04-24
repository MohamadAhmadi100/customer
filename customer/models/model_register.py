import json
import time
from datetime import datetime

import requests

from customer.helper.connection import MongoConnection
from customer.modules.auth import AuthHandler
from customer.modules.date_convertor import jalali_datetime


class Customer:
    __slots__ = [
        "customer_phone_number",
        "customer_id",
        "customer_password",
        "customer_first_name",
        "customer_last_name",
        "customer_national_id"
    ]

    CUSTOMER_TYPE: tuple = ('B2B',)

    def __init__(self, phone_number: str):
        self.customer_phone_number: str = phone_number
        self.customer_id: int = 0
        self.customer_password: str = ""
        self.customer_first_name: str = ""
        self.customer_last_name: str = ""
        self.customer_national_id: str = ""

    def set_activity(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsActive": False}}
            result: object = mongo.customer.update_one(query_operator, set_operator)
        return bool(result.acknowledged)

    def is_exists_phone_number(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            return bool(mongo.customer.find_one(query_operator))

    def is_exists_national_id(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerNationalID": self.customer_national_id}
            return bool(mongo.customer.find_one(query_operator))

    def login(self, password: str) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number, "customerPassword": password}
            return bool(mongo.customer.find_one(query_operator))

    def is_mobile_confirm(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"customerIsMobileConfirm": 1}
            result: dict = mongo.customer.find_one(query_operator, projection_operator)
            return bool(result.get("customerIsMobileConfirm"))

    def is_customer_confirm(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"customerIsConfirm": 1}
            result: dict = mongo.customer.find_one(query_operator, projection_operator)
            return bool(result.get("customerIsConfirm"))

    def mobile_confirm(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsMobileConfirm": True}}
            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)

    def customer_confirm(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsConfirm": True}}
            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)

    def get_next_sequence_customer_id(self) -> int:
        with MongoConnection() as mongo:
            if not mongo.customer.find_one():
                self.customer_id = 0
                return True
            else:
                result = mongo.customer.find({}, {'customerID': 1}).limit(1).sort("customerCreateTime", -1)
                try:
                    self.customer_id = result[0].get("customerID") + 1
                except IndexError:
                    return False
                else:
                    return True

    def get_customer(self):
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"_id": 0, "customerPassword": 0}
            result: dict = mongo.customer.find_one(query_operator, projection_operator) or {}

            # Todo delete request
            url = f"http://devaddr.aasood.com/address/customer_addresses?customerId={result.get('customerID')}"
            customer_addresses = requests.get(url)
            customer_addresses = json.loads(customer_addresses.content)
            result["addresses"] = customer_addresses.get("result")
            return result

    def save(self) -> bool:
        if not self.get_next_sequence_customer_id():
            return False
        customer_data: dict = self.__dict__
        customer_data["customerID"] = self.customer_id
        customer_data["customerCreateTime"] = time.time()
        customer_data["customerJalaliCreateTime"] = jalali_datetime(datetime.now())
        customer_data["customerEmail"] = ""
        customer_data["customerShopName"] = ""
        customer_data["customerAccountNumber"] = ""
        with MongoConnection() as mongo:
            result: object = mongo.customer.insert_one(customer_data)
        return bool(result.acknowledged)

    def set_data(
            self,
            customer_phone_number,
            customer_first_name,
            customer_last_name,
            customer_national_id,
            customer_password
    ) -> None:
        self.customer_phone_number = customer_phone_number
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_national_id = customer_national_id
        self.customer_password = customer_password

    @property
    def __dict__(self) -> dict:
        return {
            "customerPhoneNumber": self.customer_phone_number,
            "customerID": self.customer_id,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
            "customerNationalID": self.customer_national_id,
            "customerIsMobileConfirm": False,
            "customerIsConfirm": False,
            "customerIsActive": True,
            "customerType": self.CUSTOMER_TYPE,
            "customerPassword": self.customer_password,
        }

    def get_customer_password(self):
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"_id": 0}
            return mongo.customer.find_one(query_operator, projection_operator) or {}

    def change_customer_password(self, password: str) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            hashed_password: str = AuthHandler().generate_hash_password(password)
            set_operator = {"$set": {"customerPassword": hashed_password}}
            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)
