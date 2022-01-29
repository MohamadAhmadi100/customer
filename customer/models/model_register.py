import time

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
        "customer_province_code",
        "customer_address",
        "customer_national_id"
    ]

    CUSTOMER_TYPE: tuple = ('B2C', 'B2B')

    def __init__(self, phone_number: str):
        self.customer_phone_number = phone_number
        self.customer_password: str = ""
        self.customer_first_name: str = ""
        self.customer_last_name: str = ""
        self.customer_address: str = ""
        self.customer_city: str = ""
        self.customer_province: str = ""
        self.customer_province_code: str = ""
        self.customer_address: str = ""
        self.customer_national_id: str = ""

    def is_exists_phone_number(self) -> bool:
        with MongoConnection() as mongo:
            pyload = {"customerPhoneNumber": self.customer_phone_number}
            return True if mongo.collection.find_one(pyload) else False

    def is_exists_national_id(self) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"customerNationalID": self.customer_national_id}
            return True if mongo.collection.find_one(pipeline_find) else False

    def is_login(self, password: str) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number, "customerPassword": password}
            return True if mongo.collection.find_one(pipeline_find) else False

    def is_mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            result = mongo.collection.find_one(pipeline_find)
            return True if result.get("customerIsMobileConfirm") else False

    def is_customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            result = mongo.collection.find_one(pipeline_find)
            return True if result.get("customerIsConfirm") else False

    def mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"customerIsMobileConfirm": True}}
            result = mongo.collection.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"customerIsConfirm": True}}
            result = mongo.collection.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def set_password(self, password: str) -> None:
        self.customer_password = password

    @staticmethod
    def get_next_sequence_customer_id() -> int:
        with MongoConnection() as mongo:
            if not mongo.collection.find_one():
                return 0
            else:
                result = mongo.collection.find({}, {'_id': 0}).limit(1).sort("customerCrateTime", -1)
                return result[0].get("customerID") + 1

    def save(self) -> bool:
        customer_data = self.__dict__
        customer_data["customerID"] = self.get_next_sequence_customer_id()
        customer_data["customerCrateTime"] = time.time()

        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(customer_data)
        return True if result.acknowledged else False

    def set_data(
            self,
            customer_phone_number,
            customer_first_name,
            customer_last_name,
            customer_address,
            customer_city,
            customer_province,
            customer_province_code,
            customer_national_id,
    ) -> None:
        self.customer_phone_number = customer_phone_number
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_address = customer_address
        self.customer_city = customer_city
        self.customer_province = customer_province
        self.customer_province_code = customer_province_code
        self.customer_address = customer_address
        self.customer_national_id = customer_national_id

    @property
    def __dict__(self) -> dict:
        return {
            "customerPhoneNumber": self.customer_phone_number,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
            "customerNationalID": self.customer_national_id,
            "customerIsMobileConfirm": False,
            "customerIsConfirm": False,
            "customerAddresses": [
                {
                    "customerCity": self.customer_city,
                    "customerProvince": self.customer_province,
                    "customerProvinceCode": self.customer_province_code,
                    "customerAddress": self.customer_address
                }
            ],
            "customerAddress:": {
                "customerCity": self.customer_city,
                "customerProvince": self.customer_province,
                "customerProvinceCode": self.customer_province_code,
                "customerAddress": self.customer_address
            },
            "customerType": self.CUSTOMER_TYPE,
            "customerPassword": "",
        }
