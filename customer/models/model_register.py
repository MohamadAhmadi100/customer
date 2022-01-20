from customer.helper.connection import MongoConnection


class Customer:
    __slots__ = [
        "customer_phone_number",
        "customer_password",
        "customer_first_name",
        "customer_last_name",
        "customer_addresses",
        "customer_last_name",
        "costumer_address",
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
            pyload = {"costumerPhoneNumber": self.customer_phone_number}
            return True if mongo.collection.find_one(pyload) else False

    def is_exists_national_id(self) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"costumerNationalID": self.customer_national_id}
            return True if mongo.collection.find_one(pipeline_find) else False

    def is_login(self, password: str) -> bool:
        with MongoConnection() as mongo:
            pipeline_find = {"costumerPhoneNumber": self.customer_phone_number, "costumerPassword": password}
            return True if mongo.collection.find_one(pipeline_find) else False

    def set_password(self, password: str) -> None:
        self.customer_password = password

    def is_mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"costumerPhoneNumber": self.customer_phone_number}
            result = mongo.collection.find_one(pipeline_find)
            return True if result.get("costumerIsMobileConfirm") else False

    def is_customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"costumerPhoneNumber": self.customer_phone_number}
            result = mongo.collection.find_one(pipeline_find)
            return True if result.get("costumerIsConfirm") else False

    def mobile_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"costumerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"costumerIsMobileConfirm": True}}
            result = mongo.collection.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def customer_confirm(self):
        with MongoConnection() as mongo:
            pipeline_find = {"costumerPhoneNumber": self.customer_phone_number}
            pipeline_set = {"$set": {"costumerIsConfirm": True}}
            result = mongo.collection.update_one(pipeline_find, pipeline_set)
            return True if result.acknowledged else False

    def save(self, ):
        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(self.__dict__)
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
            "costumerPhoneNumber": self.customer_phone_number,
            "costumerFirstName": self.customer_first_name,
            "costumerLastName": self.customer_last_name,
            "costumerNationalID": self.customer_national_id,
            "costumerIsMobileConfirm": False,
            "costumerIsConfirm": False,
            "costumerAddresses": [
                {
                    "customerCity": self.customer_city,
                    "customerProvince": self.customer_province,
                    "costumerProvinceCode": self.customer_province_code,
                    "costumerAddress": self.customer_address
                }
            ],
            "customerAddress:": {
                "customerCity": self.customer_city,
                "customerProvince": self.customer_province,
                "costumerProvinceCode": self.customer_province_code,
                "costumerAddress": self.customer_address
            },
            "costumerType": self.CUSTOMER_TYPE,
            "customerPassword": "",
        }
