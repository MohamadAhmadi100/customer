from abc import abstractmethod, ABC

from customer.helper.connection import MongoConnection


# -----------------------------------------------#
# ------------------ Base Model -----------------#
class CustomerBase(ABC):
    __slots__ = ["costumerPhoneNumber", "costumerPassword"]

    def __init__(self):
        self.phone_number: str = ""
        self.password: str = ""

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    @staticmethod
    def is_exists(self, phone_number) -> bool:
        with MongoConnection() as mongo:
            pyload = {"costumerPhoneNumber": phone_number}
            project = {"_id": 0}
            result: dict = mongo.collection.find_one(pyload, project)
        return True if result else False

    def is_login(self, password: str) -> bool:
        with MongoConnection() as mongo:
            pyload = {
                "costumerPhoneNumber": self.phone_number,
                "costumerPassword": password,
            }
            project = {"_id": 0}
            result: dict = mongo.collection.find_one(pyload, project)
        return True if result else False

    def set_password(self, password):
        self.password = password

    @abstractmethod
    def save(self): ...

    @property
    @abstractmethod
    def __dict__(self): ...


# ------------------ Base Model -----------------#
# -----------------------------------------------#


# -----------------------------------------------#
# -------------------- B2C ----------------------#
class CustomerB2C(CustomerBase):
    CUSTOMER_TYPE: tuple = ('B2C',)

    def __init__(self, phone_number: str):
        super().__init__(phone_number)

    def save(self):
        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(self.__dict__)
        return True if result.acknowledged else False

    @property
    def __dict__(self):
        return {
            "costumerPhoneNumber": self.phone_number,
            "costumerFirstName": "",
            "costumerLastName": ""
        }


# -------------------- B2C ----------------------#
# -----------------------------------------------#


# -----------------------------------------------#
# -------------------- B2B ----------------------#
class CustomerB2B(CustomerBase):
    CUSTOMER_TYPE: tuple = ('B2C', 'B2B')

    def save(self):
        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(self.__dict__)
        return True if result.acknowledged else False

    @property
    def __dict__(self):
        return {
            "costumerPhoneNumber": self.phone_number,
            "costumerFirstName": "",
            "costumerLastName": "",
            "costumerAddresses": [
                {
                    "costumerProvinceCode": "",
                    "costumerAddress": ""
                }
            ],
            "costumerNationalID"
            "costumerType": self.CUSTOMER_TYPE,
            "customerPassword": self.password,
            "customerAddress:": {
                "customerProvince": "test",
                "customerCity": "test"
            }
        }


# -------------------- B2C ----------------------#
# -----------------------------------------------#

# ----------------- Handler --------------------#
# -----------------------------------------------#


class Customer:
    customer_type = ""

    @classmethod
    def set_type(cls, customer_type):
        cls.customer_type = customer_type

    @classmethod
    def object(cls):
        if cls.customer_type == "B2C":
            return CustomerB2C
        elif cls.customer_type == "B2B":
            return CustomerB2B()
        else:
            return CustomerBase
