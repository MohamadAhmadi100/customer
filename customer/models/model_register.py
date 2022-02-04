import json
import time
from typing import Tuple, Union, Any, Dict, Optional

import requests

from customer.helper.connection import MongoConnection


class Customer:
    __slots__ = [
        "customer_phone_number",
        "customer_password",
        "customer_first_name",
        "customer_last_name",
        "customer_addresses",
        "customer_last_name",
        "customer_address",
        "customer_city",
        "customer_province",
        "customer_postal_code",
        "customer_address",
        "customer_national_id"
    ]

    CUSTOMER_TYPE: tuple = ('B2B',)

    def __init__(self, phone_number: str):
        self.customer_phone_number = phone_number
        self.customer_password: str = ""
        self.customer_first_name: str = ""
        self.customer_last_name: str = ""
        self.customer_address: str = ""
        self.customer_city: str = ""
        self.customer_province: str = ""
        self.customer_postal_code: str = ""
        self.customer_address: str = ""
        self.customer_national_id: str = ""

    # Todo check acknowledged and return bool
    def set_activity(self):
        with MongoConnection() as mongo:
            pyload = {"customerPhoneNumber": self.customer_phone_number}
            pipe_line = {"$set": {"customerIsActive": False}}
            mongo.customer.find_one_and_update(pyload, pipe_line)

    def is_exists_phone_number(self) -> bool:
        with MongoConnection() as mongo:
            pyload = {"customerPhoneNumber": self.customer_phone_number}
            return True if mongo.customer.find_one(pyload) else False

    def is_exists_national_id(self) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"customerNationalID": self.customer_national_id}
            return True if mongo.customer.find_one(pipeline_find) else False

    def is_login(self, password: str) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number, "customerPassword": password}
            return True if mongo.customer.find_one(pipeline_find) else False

    def is_mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            result = mongo.customer.find_one(pipeline_find)
            return True if result.get("customerIsMobileConfirm") else False

    def is_customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            result = mongo.customer.find_one(pipeline_find)
            return True if result.get("customerIsConfirm") else False

    def mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"customerIsMobileConfirm": True}}
            result = mongo.customer.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"customerIsConfirm": True}}
            result = mongo.customer.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def set_password(self, password: str) -> None:
        self.customer_password = password

    @staticmethod
    def get_next_sequence_customer_id() -> int:
        with MongoConnection() as mongo:
            if not mongo.customer.find_one():
                return 0
            else:
                result = mongo.customer.find({}, {'_id': 0}).limit(1).sort("customerCrateTime", -1)
                return result[0].get("customerID") + 1

    def get_customer(self):
        with MongoConnection() as mongo:
            # delete request
            result: dict = mongo.customer.find_one({"customerPhoneNumber": self.customer_phone_number}, {"_id": 0})
            url = f"http://devaddr.aasood.com/address/customer_addresses?customerId={result.get('customerID')}"
            customer_addresses = requests.get(url)
            customer_addresses = json.loads(customer_addresses.content)
            result["addresses"] = customer_addresses.get("result")
            return result

    # edit oter_obj
    def save(self) -> bool:
        oter_obj = self.__dict__
        oter_obj["customerID"] = self.get_next_sequence_customer_id()
        oter_obj["customerCrateTime"] = time.time()

        with MongoConnection() as mongo:
            result: object = mongo.customer.insert_one(oter_obj)
        return True if result.acknowledged else False

    def set_data(
            self,
            customer_phone_number,
            customer_first_name,
            customer_last_name,
            customer_address,
            customer_city,
            customer_province,
            customer_postal_code,
            customer_national_id,
            customer_password
    ) -> None:
        self.customer_phone_number = customer_phone_number
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_address = customer_address
        self.customer_city = customer_city
        self.customer_province = customer_province
        self.customer_postal_code = customer_postal_code
        self.customer_address = customer_address
        self.customer_national_id = customer_national_id
        self.customer_password = customer_password

    @property
    def __dict__(self) -> dict:
        return {
            "customerPhoneNumber": self.customer_phone_number,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
            "customerNationalID": self.customer_national_id,
            "customerIsMobileConfirm": False,
            "customerIsConfirm": False,
            "customerIsActive": True,
            "customerType": self.CUSTOMER_TYPE,
            "customerPassword": self.customer_password,
            "customerEmail": "",
            "customerShopeName": "",
            "customerAccoountNumber": "",
        }
