from abc import abstractmethod, ABC

from customer.helper.connection import MongoConnection


class CustomerBase(ABC):
    __slots__ = ["phone_number", "customer_password"]

    def __init__(self, phone_number: str):
        self.phone_number: str = phone_number
        self.customer_password: str = ""

    def is_exists(self) -> bool:
        with MongoConnection() as mongo:
            pyload = {"phoneNumber": self.phone_number}
            project = {"_id": 0}
            result: dict = mongo.collection.find_one(pyload, project)
        return True if result else False

    def set_password(self, password):
        self.customer_password = password

    @abstractmethod
    def save(self): ...


class CustomerB2C(CustomerBase):
    CUSTOMER_TYPE: tuple = ('B2C',)

    def __init__(self, phone_number: str):
        super().__init__(phone_number)

    def save(self):
        pyload = {
            "phoneNumber": self.phone_number,
            "costumerType": self.CUSTOMER_TYPE,
            "customerPassword": self.customer_password
        }
        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(pyload)

        return True if result.acknowledged else False


class CustomerB2B(CustomerBase):
    CUSTOMER_TYPE: tuple = ('B2C', 'B2B')

    def __init__(self, phone_number: str):
        super().__init__(phone_number)

    def save(self):
        pyload = {
            "costumerPhoneNumber": self.phone_number,
            "costumerType": self.CUSTOMER_TYPE,
            "customerPassword": self.customer_password
        }
        with MongoConnection() as mongo:
            result = mongo.collection.insert_one(pyload)

        return True if result.acknowledged else False

