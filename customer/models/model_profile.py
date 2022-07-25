from customer.helper.connection import MongoConnection


class Profile:
    __slots__ = [
        "customer_phone_number",
        "customer_first_name",
        "customer_last_name",
        "customer_email",
        "customer_national_id",
        "customer_city_name",
        "customer_city_id",
        "customer_state_name",
        "customer_state_Id",
        "customer_region_code",
        "customer_ofogh_code",
        "customer_shop_name",
        "customer_account_number",
        "customer_telephone_number",
        "customer_shop_status",
        "customer_shop_location",
        "customer_education",
        "customerInformalPersons",
        "customerHasInformal",
        "customer_postal_code",
        "customer_class",
        "customer_shop_postal_code",
        "customer_address",
        "customer_document_status",
        "customer_image"
    ]

    def __init__(self, data):
        self.customer_phone_number: str = data.get("customer_phone_number") or data.get(
            "customerPhoneNumber") or data.get("customerMobileNumber") or data.get("customer_mobile_number")
        self.customer_first_name: str = data.get("customer_first_name") or data.get("customerFirstName")
        self.customer_last_name: str = data.get("customer_last_name") or data.get("customerLastName")
        self.customer_email: str = data.get("customer_email") or data.get("customerEmail")
        self.customer_national_id: str = data.get("customer_national_id") or data.get("customerNationalID")
        self.customer_city_name: str = data.get("customer_city_name") or data.get("customerCityName")
        self.customer_city_id: str = data.get("customer_city_id") or data.get("customerCityId")
        self.customer_state_name: str = data.get("customer_state_name") or data.get("customerStateName")
        self.customer_state_Id: str = data.get("customer_state_id") or data.get("customerStateId")
        self.customer_region_code: str = data.get("customer_region_code") or data.get("customerRegionCode")
        self.customer_ofogh_code: str = data.get("customer_ofogh_code") or data.get("customerOfoghCode")
        self.customer_shop_name: str = data.get("customer_shop_name") or data.get("customerShopName")
        self.customer_account_number: str = data.get("customer_account_number") or data.get("customerAccountNumber")
        self.customer_telephone_number: str = data.get("customer_telephone_number") or data.get(
            "customerTelephoneNumber")
        self.customer_shop_status: str = data.get("customer_shop_status") or data.get("customerShopStatus")
        self.customer_shop_location: str = data.get("customer_shop_location") or data.get("customerShopLocation")
        self.customer_education: str = data.get("customer_education") or data.get("customerEducation")
        self.customer_postal_code: str = data.get("customer_postal_code") or data.get("customerPostalCode")
        self.customer_class: str = data.get("customer_class") or data.get("customerClass")
        self.customer_image: str = data.get("customer_image") or data.get("customerImage")
        self.customer_shop_postal_code: str = data.get("customer_shop_postal_code") or data.get(
            "customerShopPostalCode")
        # self.customer_address: list = data.get("customer_address") or data.get("customerAddress")
        self.customer_document_status: str = data.get("customer_document_status") or data.get("customerDocumentStatus")

    def get_profile_data(self) -> dict or None:
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            if customer := mongo.customer.find_one(pipeline_find, {'_id': 0}):
                return self.set_data(customer)
            else:
                return False

    def set_data(self, data):
        return {
            "customerPhoneNumber": data.get("customerPhoneNumber"),
            "customerFirstName": data.get("customerFirstName"),
            "customerLastName": data.get("customerLastName"),
            "customerEmail": data.get("customerEmail"),
            "customerNationalID": data.get("customerNationalID"),
            "customerIsMobileConfirm": data.get("customerIsMobileConfirm"),
            "customerIsConfirm": data.get("customerIsConfirm"),
            "customerIsActive": data.get("customerIsActive"),
            "customerCityName": data.get("customerCityName"),
            "customerStateName": data.get("customerStateName"),
            "customerRegionCode": data.get("customerRegionCode"),
            # "customerAddress": data.get("customerAddress"),
            "customerType": data.get("customerType"),
            "customerShopName": data.get("customerShopName"),
            "customerAccountNumber": data.get("customerAccountNumber"),
            "customerOfoghCode": data.get("customerOfoghCode"),
            "customerTelephoneNumber": data.get("customerTelephoneNumber"),
            "customerShopStatus": data.get("customerShopStatus"),
            "customerShopLocation": data.get("customerShopLocation"),
            "customerEducation": data.get("customerEducation"),
            "customerHasInformal": data.get("customerHasInformal"),
            "customerInformalPersons": data.get("customerInformalPersons"),
            "customerClass": data.get("customerClass"),
            "customerShopPostalCode": data.get("customerShopPostalCode"),
            "customerPostalCode": data.get("customerPostalCode"),
            "customerStatus": data.get("customerStatus"),
            "customerID": data.get("customerID"),
            "customerJalaliCreateTime": data.get("customerJalaliCreateTime"),
            "customerJalaliConfirmDate": data.get("customerJalaliConfirmDate"),
            "customerAccFormalAccCode": data.get("customerAccFormalAccCode"),
            "customerSelCustomerCode": data.get("customerSelCustomerCode"),
            "customerDocumentStatus": data.get("customerDocumentStatus"),
            "customerImage": data.get("customerImage")
        }

    def create_obj_to_update_profile(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            customer_data = mongo.customer.find_one(pipeline_find, {'_id': 0})
            if customer_data is not None:
                return {
                    # "customerPhoneNumber": self.customer_phone_number or customer_data.get("customerPhoneNumber"),
                    "customerFirstName": self.customer_first_name or customer_data.get("customerFirstName"),
                    "customerLastName": self.customer_last_name or customer_data.get("customerLastName"),
                    "customerEmail": self.customer_email or customer_data.get("customerEmail"),
                    # "customerNationalID": self.customer_national_id or customer_data.get("customerNationalID"),
                    # "customerCityName": self.customer_city_name or customer_data.get("customerCityName"),
                    # "customerStateName": self.customer_state_name or customer_data.get("customerStateName"),
                    "customerImage": self.customer_image or customer_data.get("customerImage"),
                    "customerOfoghCode": self.customer_ofogh_code or customer_data.get("customerOfoghCode"),
                    "customerShopName": self.customer_shop_name or customer_data.get("customerShopName"),
                    "customerAccountNumber": self.customer_account_number or customer_data.get(
                        "customerAccountNumber"),
                    "customerTelephoneNumber": self.customer_telephone_number or customer_data.get(
                        "customerTelephoneNumber"),
                    "customerShopStatus": self.customer_shop_status or customer_data.get("customerShopStatus"),
                    "customerShopLocation": self.customer_shop_location or customer_data.get(
                        "customerShopLocation"),
                    "customerEducation": self.customer_education or customer_data.get("customerEducation"),
                    "customerPostalCode": self.customer_postal_code or customer_data.get("customerPostalCode"),
                    "customerClass": self.customer_class or customer_data.get("customerClass"),
                    "customerShopPostalCode": self.customer_shop_postal_code or customer_data.get(
                        "customerShopPostalCode"),
                    "customerDocumentStatus": self.customer_document_status or customer_data.get(
                        "customerDocumentStatus"),
                    # "customerAddress": self.customer_address or customer_data.get("customerAddress"),
                }
            else:
                return False

    def update_profile(self):
        try:
            if obj := self.create_obj_to_update_profile():
                with MongoConnection() as mongo:
                    mongo.customer.update_one({"customerPhoneNumber": self.customer_phone_number},
                                              {"$set": obj})
                return {"status_code": 202, "success": True, "message": {"message": "اطلاعات با موفقیت به روز شد"}}
            else:
                return {"status_code": 404, "success": False, "error": "کاربری با این اطلاعات وجود ندارد"}
        except TypeError:
            return {"status_code": 417, "success": False, "error": "لطفا مجددا تلاش کنید"}

    def bc_create_obj_to_update_profile(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            customer_data = mongo.customer.find_one(pipeline_find, {'_id': 0})
            if customer_data is not None:
                return {
                    # "customerPhoneNumber": self.customer_phone_number or customer_data.get("customerPhoneNumber"),
                    "customerFirstName": self.customer_first_name or customer_data.get("customerFirstName"),
                    "customerLastName": self.customer_last_name or customer_data.get("customerLastName"),
                    "customerEmail": self.customer_email or customer_data.get("customerEmail"),
                    # "customerNationalID": self.customer_national_id or customer_data.get("customerNationalID"),
                    "customerCityName": self.customer_city_name or customer_data.get("customerCityName"),
                    "customerCityId": self.customer_city_id or customer_data.get("customerCityId"),
                    "customerStateName": self.customer_state_name or customer_data.get("customerStateName"),
                    "customerStateID": self.customer_state_Id or customer_data.get("customerStateID"),
                    "customerRegionCode": self.customer_region_code or customer_data.get("customerRegionCode"),
                    "customerOfoghCode": self.customer_ofogh_code or customer_data.get("customerOfoghCode"),
                    "customerShopName": self.customer_shop_name or customer_data.get("customerShopName"),
                    "customerAccountNumber": self.customer_account_number or customer_data.get(
                        "customerAccountNumber"),
                    "customerTelephoneNumber": self.customer_telephone_number or customer_data.get(
                        "customerTelephoneNumber"),
                    "customerShopStatus": self.customer_shop_status or customer_data.get("customerShopStatus"),
                    "customerShopLocation": self.customer_shop_location or customer_data.get(
                        "customerShopLocation"),
                    "customerEducation": self.customer_education or customer_data.get("customerEducation"),
                    "customerPostalCode": self.customer_postal_code or customer_data.get("customerPostalCode"),
                    "customerClass": self.customer_class or customer_data.get("customerClass"),
                    "customerShopPostalCode": self.customer_shop_postal_code or customer_data.get(
                        "customerShopPostalCode"),
                    "customerDocumentStatus": self.customer_document_status or customer_data.get(
                        "customerDocumentStatus"),
                    # "customerAddress": self.customer_address or customer_data.get("customerAddress"),
                }
            else:
                return False

    def back_office_update_profile(self):
        try:
            if obj := self.bc_create_obj_to_update_profile():
                with MongoConnection() as mongo:
                    mongo.customer.update_one({"customerPhoneNumber": self.customer_phone_number},
                                              {"$set": obj})
                return {"status_code": 202, "success": True, "message": {"message": "اطلاعات با موفقیت به روز شد"}}
            else:
                return {"status_code": 404, "success": False, "error": "کاربری با این اطلاعات وجود ندارد"}
        except TypeError:
            return {"status_code": 417, "success": False, "error": "لطفا مجددا تلاش کنید"}
