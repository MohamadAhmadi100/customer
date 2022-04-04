from customer.helper.connection import MongoConnection


class Profile:
    __slots__ = [
        "customer_phone_number",
        "customer_first_name",
        "customer_last_name",
        "customer_national_id",
        "customer_city",
        "customer_province",

    ]

    def __init__(self, data):
        self.customer_phone_number = data.get("customer_phone_number")
        self.customer_first_name: str = data.get("customer_first_name")
        self.customer_last_name: str = data.get("customer_last_name")
        self.customer_national_id: str = data.get("customer_national_id")
        self.customer_city: str = data.get("customer_city")
        self.customer_province: str = data.get("customer_province")
        # self.customer_postal_code: str = customer_postal_code

    def get_profile_data(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            customer = mongo.customer.find_one(pipeline_find, {'_id': 0})
            if customer:
                result = self.set_data(customer)
                return result
            else:
                return False

    def set_data(self, data):

        return {
            "customerPhoneNumber": data.get("customerPhoneNumber"),
            "customerFirstName": data.get("customerFirstName"),
            "customerLastName": data.get("customerLastName"),
            "customerNationalID": data.get("customerNationalID"),
            # "customerIsMobileConfirm": data.get("customerIsMobileConfirm"),
            # "customerIsConfirm": data.get("customerIsConfirm"),
            # "customerIsActive": data.get("customerIsActive"),
            "customerCity": data.get("customerCity"),
            "customerProvince": data.get("customerProvince"),
            "customerProvinceCode": data.get("customerProvinceCode"),
            "customerAddress": data.get("customerAddress"),
            "customerType": data.get("customerType"),
            "customerEmail": data.get("customerEmail"),
            "customerShopeName": data.get("customerShopeName"),
            "customerAccoountNumber": data.get("customerAccoountNumber"),

        }

    def create_obj_to_update_profile(self):
        with MongoConnection() as mongo:
            pipeline_find = {"customerPhoneNumber": self.customer_phone_number}
            customer_data = mongo.customer.find_one(pipeline_find, {'_id': 0})
            if customer_data is not None:

                return {
                    "customerPhoneNumber": self.customer_phone_number if self.customer_phone_number else customer_data.get(
                        "customerPhoneNumber"),
                    "customerFirstName": self.customer_first_name if self.customer_first_name else customer_data.get(
                        "customerFirstName"),
                    "customerLastName": self.customer_last_name if self.customer_last_name else customer_data.get(
                        "customerLastName"),
                    "customerNationalID": self.customer_national_id if self.customer_national_id else customer_data.get(
                        "customerNationalID"),
                    "customerCity": self.customer_city if self.customer_city else customer_data.get("customerCity"),
                    "customerProvince": self.customer_province if self.customer_province else customer_data.get(
                        "customerProvince"),
                }
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
