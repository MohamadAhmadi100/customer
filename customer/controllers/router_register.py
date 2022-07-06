import json
import requests
from customer.models.model_register import Customer
from customer.modules import log
from customer.modules.auth import AuthHandler

auth_handler = AuthHandler()


class Request:
    def __init__(self, **kwargs):
        self.customer_region_code = None
        self.customer_address = None
        self.customer_city_id = None
        self.customer_email = None
        self.customer_province_id = None
        self.customer_verify_password = None
        self.customer_password = None
        self.customer_national_id = None
        self.customer_postal_code = None
        self.customer_province = None
        self.customer_city = None
        self.customer_last_name = None
        self.customer_first_name = None
        self.customer_phone_number = None
        self.customer_delivery_persons = None
        self.__dict__.update(kwargs)


def register(data: dict, test):
    print(test)
    value = Request(**data)
    customer = Customer(phone_number=value.customer_phone_number)
    customer_data = customer.get_customer()
    is_exists_phone_number = customer_data.get("customerPhoneNumber")
    is_exists_national_id = customer_data.get("customerNationalID")
    is_unique_national_id = customer.unique_national_id(customer_data.get("customerNationalID"))
    if is_exists_phone_number or is_exists_national_id or not is_unique_national_id:
        message = {
            "hasRegistered": True,
            "message": "شما قبلا ثبت نام کرده اید.",
            "redirect": "login"
        }
        return {"success": False, "error": message, "status_code": 308}
    else:
        if value.customer_password != value.customer_verify_password:
            return {"success": False, "error": "رمز عبور و تکرار آن با هم برابر نیستند.", "status_code": 422}
        customer.set_data(
            customer_phone_number=value.customer_phone_number,
            customer_first_name=value.customer_first_name,
            customer_last_name=value.customer_last_name,
            customer_national_id=value.customer_national_id,
            customer_province=value.customer_province,
            customer_city=value.customer_city,
            customer_city_id=value.customer_city_id,
            customer_postal_code=value.customer_postal_code,
            customer_address=value.customer_address,
            customer_region_code=value.customer_region_code,
            customer_province_id=value.customer_province_id,
            customer_password=auth_handler.generate_hash_password(value.customer_password)
        )
        if customer.save():  # save customer and return result as bool
            # url = "http://devaddr.aasood.com/address/insert"
            # customer_address_data = {"customerName": f'{value.customer_first_name} {customer.customer_last_name}',
            #                          "customerId": customer_data.get("customerID"),
            #                          "stateName": value.customer_province, "cityName": value.customer_city,
            #                          "stateId": value.customer_province_id, "cityId": value.customer_city_id,
            #                          "postalCode": value.customer_postal_code, "street": value.customer_address,
            #                          "isDefault": True, "regionCode": value.customer_region_code, "alley": "",
            #                          "plaque": "", "unit": "", "tel": value.customer_phone_number}

            log.save_login_log(value.customer_phone_number)
            # requests.post(url, data=json.dumps(customer_address_data))
            customer.set_activity()
            customer_id = customer.get_customer().get("customerID")
            message = {
                "message": "ثبت نام شما با موفقیت انجام شد",
                "data": {
                    "customerID": customer_id,
                    "customerStatus": customer.customer_status,
                    "customerIsActive": False
                }
            }
            return {"success": True, "message": message, "status_code": 201}
        else:
            message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
            return {"success": False, "error": message, "status_code": 417}
