import time
from datetime import datetime

from pymongo.errors import WriteError

import config
from customer.helper.connection import MongoConnection
from customer.helper.connection import OldMongoConnection
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
        "customer_state_name",
        "customer_city_name",
        "customer_city_id",
        "customer_postal_code",
        "customer_address",
        "customer_region_code",
        "customer_state_id",
        "customer_email",
        "customer_document_status",
        "customer_type",
        "customer_ofogh_code"
    ]

    DEFAULT_CUSTOMER_TYPE: tuple = ('B2B',)
    CUSTOMER_TYPES: tuple = ('B2B',)

    def __init__(self, phone_number: str):
        self.customer_phone_number: str = phone_number
        self.customer_id: int = 0
        self.customer_password: str = ""
        self.customer_first_name: str = ""
        self.customer_last_name: str = ""
        self.customer_national_id: str = ""
        self.customer_status: str = "pend"
        self.customer_state_name: str = ""
        self.customer_city_name: str = ""
        self.customer_city_id: str = ""
        self.customer_postal_code: str = ""
        self.customer_address: str = ""
        self.customer_region_code: str = ""
        self.customer_state_id: str = ""
        self.customer_email: str = ""
        self.customer_document_status: str = ""
        self.customer_type: list = []
        self.customer_ofogh_code: str = ""

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

    def set_dealership_activity(self) -> bool:
        with MongoConnection() as mongo:
            query_operator = {"customerPhoneNumber": self.customer_phone_number}
            set_status_operator = {"$set": {"customerIsActive": True, "customerStatus": "confirm",
                                            "customerIsMobileConfirm": True}}
            status_result: object = mongo.customer.update_one(query_operator, set_status_operator)
        return bool(status_result.acknowledged)

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
            return result.get("customerIsMobileConfirm")

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

    def get_next_sequence_customer_id(self) -> int:
        """
        auto increment id generator for self object
        :return: True if customer is the first obj or correct id has been generated
        """
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                customer_id = mongo.counter.find_one({"type": "customer"}, projection_operator)
                if customer_id is not None:
                    self.customer_id = customer_id.get("customerId") + 1
                    mongo.counter.update_one({"type": "customer"}, {"$set": {"customerId": self.customer_id}})
                    if customer_id.get("customerId") < 20000:
                        mongo.counter.update_one({"type": "customer"}, {"$set": {"customerId": 20000}})
                else:
                    mongo.counter.insert_one({"type": "customer", "customerId": 20000})
                    self.customer_id = 20000
                return True
            except Exception:
                return False

    # def get_next_sequence_customer_id(self) -> bool:
    #     """
    #     auto increment id generator for self object
    #     :return: True if customer is the first obj or correct id has been generated
    #     """
    #     with MongoConnection() as mongo:
    #         if not mongo.customer.find_one():
    #             self.customer_id = 0
    #             return True
    #         else:
    #             result = mongo.customer.find({}, {'customerID': 1}).limit(1).sort("customerCreateTime", -1)
    #             try:
    #                 self.customer_id = result[0].get("customerID") + 1
    #             except IndexError:
    #                 return False
    #             else:
    #                 return True

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
        customer_data["customerDateTimeCreateTime"] = str(datetime.now()).split(".")[0]
        customer_data["customerJalaliCreateTime"] = jalali_datetime(datetime.now())
        customer_data["customerStatus"] = "pend"
        customer_data["customerIsActive"] = False
        customer_data["customerIsMobileConfirm"] = False
        customer_data["customerHasInformal"] = False
        with MongoConnection() as mongo:
            result: object = mongo.customer.insert_one(customer_data)
        return bool(result.acknowledged)

    def set_data(
            self,
            customer_phone_number,
            customer_first_name,
            customer_last_name,
            customer_national_id,
            customer_state_name,
            customer_city_name,
            customer_city_id,
            customer_type,
            customer_password=None,
            customer_ofogh_code="",
            customer_postal_code="",
            customer_address="",
            customer_region_code="",
            customer_state_id="",
            customer_document_status="",

    ) -> None:
        self.customer_phone_number = customer_phone_number
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_national_id = customer_national_id
        self.customer_password = customer_password
        self.customer_state_name = customer_state_name
        self.customer_city_name = customer_city_name
        self.customer_city_id = customer_city_id
        self.customer_postal_code = customer_postal_code
        self.customer_address = customer_address
        self.customer_region_code = customer_region_code
        self.customer_state_id = customer_state_id
        self.customer_document_status = customer_document_status
        self.customer_type = customer_type
        self.customer_ofogh_code = customer_ofogh_code

    @property
    def __dict__(self) -> dict:
        return {
            "customerPhoneNumber": self.customer_phone_number,
            "customerID": self.customer_id,
            "customerFirstName": self.customer_first_name,
            "customerLastName": self.customer_last_name,
            "customerEmail": self.customer_email,
            "customerNationalID": self.customer_national_id,
            "customerType": self.customer_type,
            "customerTypes": self.customer_type,
            "customerPassword": self.customer_password,
            "customerStatus": self.customer_status,
            "customerCityName": self.customer_city_name,
            "customerStateName": self.customer_state_name,
            "customerCityId": self.customer_city_id,
            "customerStateId": self.customer_state_id,
            "customerRegionCode": self.customer_region_code,
            "customerAddress": self.customer_address,
            "customerDocumentStatus": self.customer_document_status,
            "customerOfoghCode": self.customer_ofogh_code
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
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        with MongoConnection() as mongo:
            customer = mongo.customer.find_one(query_operator)
            if not customer.get("customerHasInformal"):
                return
            informal_persons: list = customer.get("customerInformalPersons", [])
            if len(informal_persons) >= 5:
                return
            for informal in informal_persons:
                if informal.get("informalNationalID") == informal_info.get("informalNationalID") or informal.get(
                        "informalMobileNumber") == informal_info.get("informalMobileNumber"):
                    return False
            if not self.get_next_sequence_customer_id():
                return False
            informal_info["customerID"] = self.customer_id
            informal_info["customerType"] = ["informal"]
            informal_info["customerAccFormalAccCode"] = None
            informal_info["customerSelCustomerCode"] = None
            push_operator = {"$push": {"customerInformalPersons": informal_info}}
            result = mongo.customer.update_one(query_operator, push_operator, upsert=True)
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
        finds an extra person matches national_id and customer mobile_number
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
        set_operator = {
            "$set":
                {
                    "customerStatus": "cancel",
                    "customerIsActive": False,
                    "customerCancelDatetime": time.time(),
                    "customerJalaliCancelDatetime": jalali_datetime(datetime.now())
                }
        }
        # set_active_operator = {"$set": {"customerIsActive": False}}
        # set_date_operator = {"$set": {"customerCancelDatetime": time.time()}}
        # set_jalali_date_operator = {"$set": {"customerJalaliCancelDatetime": jalali_datetime(datetime.now())}}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    # active_result = mongo.customer.update_one(query_operator, set_active_operator)
                    return bool(result.acknowledged)  # and bool(active_result.acknowledged)
                return False
            except Exception:
                return

    def confirm_status(self) -> bool or None:
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {
            "$set": {"customerStatus": "confirm", "customerJalaliConfirmDate": jalali_datetime(datetime.now()),
                     "customerConfirmDate": time.time()}}
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

    def get_has_informal(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if customer := mongo.customer.find_one(query_operator, projection_operator):
                    return customer.get("customerHasInformal") or False
                return False
            except Exception:
                return None

    def set_has_informal(self, customerHasInformal: bool) -> bool or None:
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerHasInformal": customerHasInformal}}
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

    @staticmethod
    def is_unique_national_id(national_id: str) -> bool or None:
        """
        A func for find out is national id unique
        :param national_id: customer national id
        :return: True if national id is unique, False for national id exists and None for Exception
        """
        query_operator = {"customerNationalID": national_id}
        informal_query_operator = {"customerInformalPersons.informalNationalID": national_id}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                return not mongo.customer.find_one(query_operator, projection_operator) and not list(
                    mongo.customer.find(informal_query_operator, projection_operator))
            except Exception:
                return

    def kosar_getter(self, informal_flag: bool = False, national_id: str = "", customer_type: list = None):
        """
        syncs needed data for kosar service
        :return: a dict contained user data
        """
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if not (customer := mongo.customer.find_one(query_operator, projection_operator)):
                    return None
                if type(customer.get("customerAddress")) == list and len(customer.get("customerAddress")):
                    address = customer.get("customerAddress")[0]
                    if type(address) == list:
                        address = address[0]
                else:
                    address = customer.get("customerAddress")
                if not informal_flag:
                    return {
                        "customerType": customer_type or customer.get("customerType"),
                        "customerId": customer.get("customerID"),
                        "IsPerson": True,
                        "gnr_Person_Name": customer.get("customerFirstName") or False,
                        "gnr_Person_Family": customer.get("customerLastName") or False,
                        "gnr_Person_NationalCode": customer.get("customerNationalID") or False,
                        "mainFormalGroupingName": f'{customer.get("customerFirstName")} {customer.get("customerLastName")}',
                        "sel_CustomerMainGroup_Code": config.KOSAR_REGION_CODES.get(
                            customer.get("customerRegionCode"),
                            "0"),
                        "AddressDTOLst": [
                            {
                                "gnr_Address_No": address.get("city_name"),
                                "gnr_Address_Street": address.get("street"),
                                "gnr_Land_PhoneCode": "021"
                            }
                        ],
                        "PhoneDTOLst": [
                            {
                                "gnr_Phone_Priority": 1,
                                "gnr_Phone_No": address.get("tel"),
                                "gnr_Land_PhoneCode": "021"
                            }
                        ]
                    }
                informal_persons: list = customer.get("customerInformalPersons")
                informal = {}
                for person in informal_persons:
                    if person.get("informalNationalID") == national_id:
                        informal = person
                if not informal:
                    return None
                try:
                    sel_CustomerMainGroup_Code = config.KOSAR_REGION_CODES.get(customer.get("customerRegionCode"),
                                                                               "0") or "0"
                except Exception:
                    sel_CustomerMainGroup_Code = "0"
                return {
                    "customerType": ["informal"],
                    "customerId": informal.get("customerID"),
                    "IsPerson": True,
                    "gnr_Person_Name": informal.get("informalFirstName") or False,
                    "gnr_Person_Family": informal.get("informalLastName") or False,
                    "gnr_Person_NationalCode": informal.get("informalNationalID") or False,
                    "mainFormalGroupingName": f'{informal.get("informalFirstName")} {informal.get("informalLastName")}',
                    "sel_CustomerMainGroup_Code": sel_CustomerMainGroup_Code,
                    "AddressDTOLst": [
                        {
                            "gnr_Address_No": customer.get("customerCityName", "تهران"),
                            "gnr_Address_Street": address.get("street") or "آسود",
                            "gnr_Land_PhoneCode": "021"
                        }
                    ],
                    "PhoneDTOLst": [
                        {
                            "gnr_Phone_Priority": 1,
                            "gnr_Phone_No": address.get("tel") or "88888888",
                            "gnr_Land_PhoneCode": "021"
                        }
                    ]
                }
            except Exception as e:
                return None

    def kosar_setter(self, sel_Customer_Code: str, acc_FormalAcc_Code: str, customer_type=None,
                     customer_national_id: str = ""):
        if customer_type is None or type(customer_type) != list:
            customer_type = ["B2B"]
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        informal_query_operator = {"customerPhoneNumber": self.customer_phone_number,
                                   "customerInformalPersons.informalNationalID": customer_national_id}
        projection_operator = {"_id": 0}
        set_operator = {"$set": {
            "customerSelCustomerCode": sel_Customer_Code,
            "customerAccFormalAccCode": acc_FormalAcc_Code
        }}
        informal_set_operator = {
            "$set":
                {
                    "customerInformalPersons.$.customerSelCustomerCode": sel_Customer_Code,
                    "customerInformalPersons.$.customerAccFormalAccCode": acc_FormalAcc_Code,
                }
        }
        with MongoConnection() as mongo:
            try:
                if customer_type[0] == "informal":
                    if mongo.customer.find_one(query_operator, projection_operator):
                        result = mongo.customer.update_one(informal_query_operator, informal_set_operator)
                        return bool(result.acknowledged)
                    return False
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return None

    # def is_kosar_set(self):

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
        projection_operator = {
            "first_name": "$customerFirstName",
            "last_name": "$customerLastName",
            "kowsar_number": "$customerSelCustomerCode",
            "customer_id": "$customerID",
            "_id": 0
        }
        with MongoConnection() as mongo:
            try:
                result = list(mongo.customer.find(query_operator, projection_operator))
                return {customer["customer_id"]: customer for customer in result}
            except Exception:
                return []

    @staticmethod
    def get_customers_by_id_league(customer_id_list):
        query_operator = {"customerID": {"$in": customer_id_list}}
        projection_operator = {
            "first_name": "$customerFirstName",
            "last_name": "$customerLastName",
            "customer_id": "$customerID",
            "customer_image": {
                "$switch": {
                    "branches": [
                        {"case": {"$ne": ["$customerImage", "null"]},
                         "then": "https://devapi.aasood.com/gallery_files/default-pic/profile-league/150x150.jpg"},
                        {"case": {"$ne": ["$customerImage", None]},
                         "then": "https://devapi.aasood.com/gallery_files/default-pic/profile-league/150x150.jpg"}
                    ],
                    "default": "$customerImage"
                }
            },
            "_id": 0
        }
        with MongoConnection() as mongo:
            try:
                result = list(mongo.customer.find(query_operator, projection_operator))
                return {customer["customer_id"]: customer for customer in result}
            except Exception:
                return []

    @staticmethod
    def find_customers(name: str):
        with MongoConnection() as mongo:
            result = list(mongo.customer.aggregate([
                {
                    "$project": {
                        "customerFullName": {
                            "$concat": ["$customerFirstName", " ", "$customerLastName"]
                        }
                        ,
                        "customerFirstName": 1,
                        "customerLastName": 1,
                        "customerID": 1,
                        "_id": 0
                    }
                },
                {
                    "$match": {
                        "$or": [
                            {
                                "customerFirstName": {"$regex": name}}
                            , {
                                "customerLastName": {"$regex": name}
                            },
                            {
                                "customerFullName": {"$regex": name}
                            }
                        ],
                    }
                },
                {
                    "$project": {
                        "customerID": 1
                    }
                }
            ]))
        return result

    def convert_to_dealership(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerType": ["B2B2C"]}, "$addToSet": {"customerTypes": "B2B2C"}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return

    def add_dealership_customer(self, customer_id, customer_phone_number, customer_national_id):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        push_operator = {
            "$push": {
                "customerDealershipPersons": {
                    "customerID": customer_id,
                    "customerPhoneNumber": customer_phone_number,
                    "customerNationalID": customer_national_id
                }
            }}
        with MongoConnection() as mongo:
            result = mongo.customer.update_one(query_operator, push_operator, upsert=True)
            return bool(result.acknowledged)

    def insert_main_db(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if not (customer := mongo.customer.find_one(query_operator, projection_operator)):
                    return
            except Exception:
                return
        customer_data: dict = {
            "entity_id": customer.get("customerID"),
            "firstName": customer.get("customerFirstName"),
            "lastName": customer.get("customerLastName"),
            "nId": customer.get("customerNationalID"),
            "shopName": customer.get("customerShopName"),
            "regionCode": customer.get("customerRegionCode"),
            "email": customer.get("customerEmail"),
            "city": customer.get("customerCityName"),
            "state": customer.get("customerStateName"),
            "mobileNumber": customer.get("customerPhoneNumber"),
            "sel_customer_code": customer.get("customerSelCustomerCode"),
            "acc_formal_acc_code": customer.get("customerAccFormalAccCode"),
            "customer_status": "Confirmed",
            "insert_time": [datetime.now()]
        }
        old_query_operator = {
            "$or":
                [
                    {"mobileNumber": self.customer_phone_number},
                    {"nId": self.customer_national_id}
                ]
        }
        with OldMongoConnection() as old_mongo:
            old_result = list(old_mongo.customers.find(old_query_operator))
            if len(old_result):
                print("repeated data")
                return
            result: object = old_mongo.customers.insert_one(customer_data)
            return bool(result.acknowledged)

    def get_status_sms_data(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        projection_operator = {"customerPhoneNumber": 1, "customerFirstName": 1, "customerLastName": 1}
        with MongoConnection() as mongo:
            try:
                return mongo.customer.find_one(query_operator, projection_operator) or None
            except Exception:
                return False

    @staticmethod
    def get_bi_customer_data(from_date, to_date):
        with MongoConnection() as mongo:
            try:
                return list(mongo.customer.aggregate(
                    [{'$match': {'customerDateTimeCreateTime': {'$gte': from_date, '$lte': to_date}}}, {
                        '$project': {'_id': 0, 'customerID': '$customerID', 'customerFirstName': '$customerFirstName',
                                     'customerLastName': '$customerLastName',
                                     'customerPhoneNumber': '$customerPhoneNumber',
                                     'customerIsActive': '$customerIsActive', 'customerStatus': '$customerStatus',
                                     'customerJalaliCreateTime': '$customerJalaliCreateTime',
                                     'customerOfoghCode': '$customerOfoghCode', 'customerShopName': '$customerShopName',
                                     'customerCityName': '$customerCityName', 'customerStateName': '$customerStateName',
                                     'customerCityId': '$customerCityId', 'customerStateId': '$customerStateId',
                                     'customerRegionCode': '$customerRegionCode',
                                     'customerNationalID': '$customerNationalID'}}]))

            except Exception:
                return []

    def active_credit(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerActiveCredit": True}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return

    def inactive_credit(self):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerActiveCredit": False}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return

    def set_credit_amount(self, credit_amount: int):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerCreditAmount": credit_amount}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if res := mongo.customer.find_one(query_operator, projection_operator):
                    if res.get("customerActiveCredit"):
                        result = mongo.customer.update_one(query_operator, set_operator)
                        return bool(result.acknowledged)
                    return
                return False
            except Exception:
                return False

    def set_customer_types(self, customer_type: str):
        query_operator = {"customerPhoneNumber": self.customer_phone_number}
        set_operator = {"$set": {"customerType": [customer_type]}, "$addToSet": {"customerTypes": customer_type}}
        projection_operator = {"_id": 0}

        with MongoConnection() as mongo:
            try:
                if mongo.customer.find_one(query_operator, projection_operator):
                    result = mongo.customer.update_one(query_operator, set_operator)
                    return bool(result.acknowledged)
                return False
            except Exception:
                return
