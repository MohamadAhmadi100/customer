from customer.helper.connection import MongoConnection


class Profile:
    __slots__ = [
        "customer_phone_number",
        "customer_first_name",
        "customer_last_name",
        "customer_email",
        "customer_national_id",
        "customer_city",
        "customer_province",
        "customer_ofogh_code"

    ]

    def __init__(self, data):
        self.customer_phone_number: str = data.get("customer_phone_number")
        self.customer_first_name: str = data.get("customer_first_name")
        self.customer_last_name: str = data.get("customer_last_name")
        self.customer_email: str = data.get("customer_email")
        self.customer_national_id: str = data.get("customer_national_id")
        self.customer_city: str = data.get("customer_city")
        self.customer_province: str = data.get("customer_province")
        self.customer_ofogh_code: int = data.get("customer_ofogh_code")
        # self.customer_postal_code: str = customer_postal_code

    def get_profile_data(self):
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
            # "customerIsMobileConfirm": data.get("customerIsMobileConfirm"),
            # "customerIsConfirm": data.get("customerIsConfirm"),
            # "customerIsActive": data.get("customerIsActive"),
            "customerCity": data.get("customerCity"),
            "customerProvince": data.get("customerProvince"),
            "customerProvinceCode": data.get("customerProvinceCode"),
            "customerAddress": data.get("customerAddress"),
            "customerType": data.get("customerType"),
            "customerShopeName": data.get("customerShopeName"),
            "customerAccoountNumber": data.get("customerAccoountNumber"),
            "customerOfoghCode": data.get("customerOfoghCode")

        }

    def create_obj_to_update_profile(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            customer_data = mongo.customer.find_one(pipeline_find, {'_id': 0})
            if customer_data is not None:

                return {"customerPhoneNumber": self.customer_phone_number or customer_data.get("customerPhoneNumber"),
                        "customerFirstName": self.customer_first_name or customer_data.get("customerFirstName"),
                        "customerLastName": self.customer_last_name or customer_data.get("customerLastName"),
                        "customerEmail": self.customer_last_name or customer_data.get("customerEmail"),
                        "customerNationalID": self.customer_national_id or customer_data.get("customerNationalID"),
                        "customerCity": self.customer_city or customer_data.get("customerCity"),
                        "customerProvince": self.customer_province or customer_data.get("customerProvince"),
                        "customerOfoghCode": self.customer_ofogh_code or customer_data.get("customerOfoghCode")}

            else:
                return False

    def update_profile(self):
        try:
            if self.create_obj_to_update_profile():
                with MongoConnection() as mongo:
                    mongo.customer.update_one({"customerPhoneNumber": self.customer_phone_number},
                                              {"$set": self.create_obj_to_update_profile()})
                return {"type": True, "message": "success"}
            else:
                return {"type": True, "message": "کابری با این اطلاعات وجود ندارد"}
        except TypeError:
            return {"type": False, "message": "Error"}
