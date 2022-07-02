import time
from datetime import datetime
import re
from pymongo.errors import WriteError

import config
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
        "customer_national_id",
        "customer_status",
        "customer_province",
        "customer_city",
        "customer_city_id",
        "customer_postal_code",
        "customer_address",
        "customer_region_code",
        "customer_province_id",
        "customer_email"
    ]

    CUSTOMER_TYPE: tuple = ('B2B',)

    def __init__(self, phone_number: str):
        self.customer_phone_number: str = phone_number
        self.customer_id: int = 0
        self.customer_password: str = ""
        self.customer_first_name: str = ""
        self.customer_last_name: str = ""
        self.customer_national_id: str = ""
        self.customer_status: str = "pend"
        self.customer_province: str = ""
        self.customer_city: str = ""
        self.customer_city_id: str = ""
        self.customer_postal_code: str = ""
        self.customer_address: str = ""
        self.customer_region_code: str = ""
        self.customer_province_id: str = ""
        self.customer_email: str = ""

    def set_activity(self) -> bool:
        """
        make customerIsActive flag to false in database through initial
        :return: mongo collection acknowledged as bool
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsActive": False}}
            set_status_operator = {"$set": {"customerStatus": "pend"}}
            result: object = mongo.customer.update_one(query_operator, set_operator)
            status_result: object = mongo.customer.update_one(query_operator, set_status_operator)
        return bool(result.acknowledged) and bool(status_result.acknowledged)

    def activate(self):
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsActive": True}}
            result: object = mongo.customer.update_one(query_operator, set_operator)
        return bool(result.acknowledged)

    def is_exists_phone_number(self) -> bool:
        """
        :return: a flag showing repeated customer mobile number
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            return bool(mongo.customer.find_one(query_operator))

    def is_exists_national_id(self) -> bool:
        """
        :return: a flag showing repeated customer national id
        """
        with MongoConnection() as mongo:
            query_operator = {"customerNationalID": self.customer_national_id}
            return bool(mongo.customer.find_one(query_operator))

    def login(self, password: str) -> bool:
        """
        check user mobile number and password for login
        :param password: "HASHED!" password for checking database
        :return: a bool showing customer data exists
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number, "customerPassword": password}
            return bool(mongo.customer.find_one(query_operator))

    def is_mobile_confirm(self) -> bool:
        """
        :return: a bool showing customer mobile confirm status
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"customerIsMobileConfirm": 1}
            result: dict = mongo.customer.find_one(query_operator, projection_operator)
            return bool(result.get("customerIsMobileConfirm"))

    def is_customer_confirm(self) -> bool:
        """
        :return: a bool showing customer confirm status
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"customerIsConfirm": 1}
            result: dict = mongo.customer.find_one(query_operator, projection_operator)
            return bool(result.get("customerIsConfirm"))

    def is_customer_active(self) -> bool:
        """
        :return: a bool showing customer active flag
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"customerIsActive": 1}
            result: dict = mongo.customer.find_one(query_operator, projection_operator)
            return bool(result.get("customerIsActive"))

    def mobile_confirm(self) -> bool:
        """
        :return: a bool showing success update mobile confirm for customer
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsMobileConfirm": True}}
            set_status_operator = {"$set": {"customerStatus": "pend"}}

            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)

    def customer_confirm(self) -> bool:
        """
        :return: a bool showing success update confirm status for customer
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_operator = {"$set": {"customerIsConfirm": True}}
            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)

    def get_next_sequence_customer_id(self) -> bool:
        """
        auto increment id generator for self object
        :return: True if customer is the first obj or correct id has been generated
        """
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

    def get_customer(self) -> dict:
        """
        :return: customer data as a dict
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"_id": 0, "customerPassword": 0}
            return mongo.customer.find_one(query_operator, projection_operator) or {}

    def save(self) -> bool:
        if not self.get_next_sequence_customer_id():
            return False
        customer_data: dict = self.__dict__
        customer_data["customerID"] = self.customer_id
        customer_data["customerCreateTime"] = time.time()
        customer_data["customerJalaliCreateTime"] = jalali_datetime(datetime.now())
        customer_data["customerStatus"] = "pend"
        customer_data["customerIsActive"] = False
        customer_data["customerIsMobileConfirm"] = False
        with MongoConnection() as mongo:
            result: object = mongo.customer.insert_one(customer_data)
        return bool(result.acknowledged)

    def set_data(
            self,
            customer_phone_number,
            customer_first_name,
            customer_last_name,
            customer_national_id,
            customer_password,
            customer_province,
            customer_city,
            customer_city_id,
            customer_postal_code="",
            customer_address="",
            customer_region_code="",
            customer_province_id=""

    ) -> None:
        self.customer_phone_number = customer_phone_number
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_national_id = customer_national_id
        self.customer_password = customer_password
        self.customer_province = customer_province
        self.customer_city = customer_city
        self.customer_city_id = customer_city_id
        self.customer_postal_code = customer_postal_code
        self.customer_address = customer_address
        self.customer_region_code = customer_region_code
        self.customer_province_id = customer_province_id

    @property
    def __dict__(self) -> dict:
        return {
            "customerPhoneNumber": self.customer_phone_number,
            "customerID": self.customer_id,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
            "customerEmail": self.customer_email,
            "customerNationalID": self.customer_national_id,
            "customerIsMobileConfirm": False,
            "customerIsActive": False,
            "customerType": self.CUSTOMER_TYPE,
            "customerPassword": self.customer_password,
            "customerStatus": self.customer_status,
            "customerCity": self.customer_city,
            "customerProvince": self.customer_province,
            "customerCityId": self.customer_city_id,
            "customerProvinceId": self.customer_province_id,
            "customerAddress": self.customer_address
        }

    def get_customer_password(self):
        """
        :return: customer data with HASHED! password
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"_id": 0}
            return mongo.customer.find_one(query_operator, projection_operator) or {}

    def change_customer_password(self, password: str) -> bool:
        """
        change user password
        :param password: UN-HASHED! phrase
        :return: a bool showing password has changed
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            hashed_password: str = AuthHandler().generate_hash_password(password)
            set_operator = {"$set": {"customerPassword": hashed_password}}
            result = mongo.customer.update_one(query_operator, set_operator)
            return bool(result.acknowledged)

    def change_default_delivery(self, person_info: dict) -> bool or None:
        """
        :param person_info: a dict contained delivery mobile number, address
        :return: a bool flag showing success process
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        identifier = [{"element.deliveryMobileNumber": person_info.get("deliveryMobileNumber")}]
        set_operator = {"$set": {"customerDeliveryPersons.$[element]": person_info}}
        set_default_operator = {"$set": {"customerDefaultDeliveryPerson": person_info}}
        with MongoConnection() as mongo:
            try:
                result = mongo.customer.update_one(
                    query_operator,
                    set_operator,
                    array_filters=identifier,
                    upsert=True
                )
                mongo.customer.update_one(query_operator, set_default_operator, upsert=True)
                if result.acknowledged and result.matched_count:
                    return True
                return False
            except WriteError:
                return False

    def add_delivery(self, person_info: dict) -> bool:
        """
        :param person_info: a dict contained delivery mobile number, address
        :return: a bool flag showing success process
        """
        push_operator = {"$push": {"customerDeliveryPersons": person_info}}
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_default_operator = {"$set": {"customerDefaultDeliveryPerson": person_info}}
        with MongoConnection() as mongo:
            result = mongo.customer.update_one(query_operator, push_operator, upsert=True)
            mongo.customer.update_one(query_operator, set_default_operator, upsert=True)
            return bool(result.acknowledged)

    def retrieve_delivery_persons(self) -> list or None:
        """

        :return: a list of 5 last delivery persons data for a customer or None
        """
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            projection_operator = {"_id": 0}
            try:
                return mongo.customer.find_one(query_operator, projection_operator).get("customerDeliveryPersons")[
                       -5:] or []
            except Exception as e:
                return None

    def retrieve_default_delivery(self) -> dict:
        """
        :return: a single delivery dict data
        """
        with MongoConnection() as mongo:
            try:
                query_operator = {"customerPhoneNumber": self.customer_phone_number}
                return mongo.customer.find_one(query_operator, {"_id": 0}).get("customerDefaultDeliveryPerson")
            except Exception as e:
                return {}

    def add_informal(self, informal_info: dict) -> bool or None:
        """
        :param informal_info: a dict contained informal mobile_number, national_id, name, family and kosar_code
        :return: a bool flag showing success process
        """
        informal_info["informalID"] = self.get_next_sequence_informal_id()
        push_operator = {"$push": {"customerInformalPersons": informal_info}}
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_flag_operator = {"$set": {"customerHasInformal": True}}
        with MongoConnection() as mongo:
            informal_persons: list = mongo.customer.find_one(query_operator).get("customerInformalPersons") or []
            if len(informal_persons) >= 5:
                return None
            for informal in informal_persons:
                if informal.get("informalNationalID") == informal_info.get("informalNationalID") or informal.get(
                        "informalMobileNumber") == informal_info.get("informalMobileNumber"):
                    return False
            result = mongo.customer.update_one(query_operator, push_operator, upsert=True)
            mongo.customer.update_one(query_operator, set_flag_operator, upsert=True)
            return bool(result.acknowledged)

    def get_next_sequence_informal_id(self) -> int or bool:
        """
        auto increment id generator for informal object
        :return: True if informal is the first obj or correct id has been generated
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if customer := mongo.customer.find_one(query_operator, projection_operator):
                    return len(customer.get("customerInformalPersons") or 0)
                else:
                    return False
            except Exception as e:
                return True

    def get_informal_person(self, national_id: str) -> dict or bool:
        """
        finds a extra person matches national_id and customer mobile_number
        :param national_id: 10 - digits int and unique
        :return:
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if persons := mongo.customer.find_one(query_operator, projection_operator).get(
                        "customerInformalPersons"):
                    return next((person for person in persons if national_id == person.get("informalNationalID")),
                                False)
            except Exception:
                return False

    def get_informal_persons(self) -> dict or bool:
        """
        finds a extra person matches national_id and customer mobile_number
        :param national_id: 10 - digits int and unique
        :return:
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                return mongo.customer.find_one(query_operator, projection_operator).get(
                    "customerInformalPersons") or None
            except Exception:
                return False

    def cancel_status(self) -> bool or None:
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerStatus": "cancel"}}
        set_active_operator = {"$set": {"customerIsActive": False}}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    active_result = mongo.customer.update_one(query_operator, set_active_operator)
                    return bool(result.acknowledged) and bool(active_result.acknowledged)
                return False
            except Exception:
                return

    def confirm_status(self) -> bool or None:
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerStatus": "confirm"}}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return

    def get_status(self) -> str or None:
        """
        get customer status
        :return: str phrase pend, cancel, confirm
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if customer := mongo.customer.find_one(query_operator, projection_operator):
                    return customer.get("customerStatus")
                else:
                    return None
            except Exception as e:
                return None

    def set_has_informal(self, hasInformal: bool) -> bool or None:
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"hasInformal": hasInformal}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return False

    @staticmethod
    def unique_national_id(national_id):
        query_operator = {"customerNationalID": national_id}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                return not mongo.customer.find_one(query_operator, projection_operator)
            except Exception:
                return False

    def kosar_getter(self):
        """
        syncs needed data for kosar service
        :return: a dict contained user data
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if customer := mongo.customer.find_one(query_operator, projection_operator):
                    return {
                        "customerId": customer.get("customerID"),
                        "IsPerson": True,
                        "gnr_Person_Name": customer.get("customerFirstName") or False,
                        "gnr_Person_Family": customer.get("customerLastName") or False,
                        "gnr_Person_NationalCode": customer.get("customerNationalID") or False,
                        "mainFormalGroupingName": f'{customer.get("customerFirstName")} {customer.get("customerLastName")}',
                        "sel_CustomerMainGroup_Code": config.KOSAR_REGION_CODES.get(customer.get("customerRegionCode"),
                                                                                    "0"),
                        "AddressDTOLst": [
                            {
                                "gnr_Address_No": customer.get("customerAddress")[0].get("customerCityName"),
                                "gnr_Address_Street": customer.get("customerAddress")[0].get("customerStreet"),
                                "gnr_Land_PhoneCode": "021"
                            }
                        ],
                        "PhoneDTOLst": [
                            {
                                "gnr_Phone_Priority": 1,
                                "gnr_Phone_No": customer.get("customerAddress")[0].get("customerTelephone"),
                                "gnr_Land_PhoneCode": "021"
                            }
                        ]
                    }
                else:
                    return None
            except Exception as e:
                return None

    def kosar_setter(self, acc_FormalAcc_Id, acc_FormalAcc_Code):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        set_operator = {"$set": {
            "customerSelCustomerCode": acc_FormalAcc_Id,
            "customerAccFormalAccCode": acc_FormalAcc_Code
        }}
        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return None

    def get_wallet_data(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if customer := mongo.customer.find_one(query_operator, projection_operator):
                    return {
                        "customer_id": customer.get("customerID"),
                        "phone_number": self.customer_phone_number,
                        "customer_name": f"{customer.get('customerFirstName')} {customer.get('customerLastName')}"
                    }
                else:
                    return None
            except Exception as e:
                return None

    @staticmethod
    def get_customers_by_id(id_list):
        query_operator = {"customerID": {"$in": id_list}}
        projection_operator = {"customerFirstName": 1, "customerLastName": 1, "customerSelCustomerCode": 1, "_id": 0}
        with MongoConnection() as mongo:
            try:
                return list(mongo.customer.find(query_operator, projection_operator))
            except Exception:
                return []

    @staticmethod
    def find_customers(name: str):
        query_operator = {"customerID": {"$in": name}}
        projection_operator = {"customerID": 1, "_id": 0}
        regx = re.compile("^foo", re.IGNORECASE)
        # db.users.find_one({"files": regx})
        with MongoConnection() as mongo:
            try:
                return list(mongo.customer.find(query_operator, projection_operator))
            except Exception:
                return []
