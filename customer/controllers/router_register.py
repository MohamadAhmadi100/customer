from customer.models.model_register import Customer
from customer.modules import log
from customer.modules.auth import AuthHandler
from customer.modules.shahkar import nid_phone_verify

auth_handler = AuthHandler()


class Request:
    def __init__(self, **kwargs):
        self.customer_region_code = None
        self.customer_address = None
        self.customer_city_id = None
        self.customer_email = None
        self.customer_state_id = None
        self.customer_verify_password = None
        self.customer_password = None
        self.customer_national_id = None
        self.customer_postal_code = None
        self.customer_state_name = None
        self.customer_city_name = None
        self.customer_last_name = None
        self.customer_first_name = None
        self.customer_phone_number = None
        self.customer_document_status = None
        self.customer_type = None
        self.customer_ofogh_code = None
        self.__dict__.update(kwargs)


def register(data: dict):
    value = Request(**data)
    customer = Customer(phone_number=value.customer_phone_number)
    customer_data = customer.get_customer()
    is_exists_phone_number = customer_data.get("customerPhoneNumber")
    is_exists_national_id = customer_data.get("customerNationalID")

    if is_exists_phone_number or is_exists_national_id or not customer.is_unique_national_id(
            value.customer_national_id):
        message = {
            "hasRegistered": True,
            "message": "شما قبلا ثبت نام کرده اید.",
            "redirect": "login"
        }
        return {"success": False, "error": message, "status_code": 308}
    else:
        if value.customer_password != value.customer_verify_password:
            return {"success": False, "error": "رمز عبور و تکرار آن با هم برابر نیستند.", "status_code": 422}
        # verify_phone = nid_phone_verify(value.customer_phone_number, value.customer_national_id)
        # if not verify_phone:
        #     if verify_phone is not None:
        #         return {"success": False, "error": "کدملی و شماره تلفن از طرف سامانه شاهکار رد شد.", "status_code": 422}
        #     return {"success": False, "error": "دسترسی به سامانه شاهکار با خطا مواجه شد.", "status_code": 422}
        customer.set_data(
            customer_phone_number=value.customer_phone_number,
            customer_first_name=value.customer_first_name,
            customer_last_name=value.customer_last_name,
            customer_national_id=value.customer_national_id,
            customer_state_name=value.customer_state_name,
            customer_city_name=value.customer_city_name,
            customer_city_id=value.customer_city_id,
            customer_postal_code=value.customer_postal_code,
            customer_address=value.customer_address,
            customer_region_code=value.customer_region_code,
            customer_state_id=value.customer_state_id,
            customer_ofogh_code=value.customer_ofogh_code,
            customer_document_status=value.customer_document_status,
            customer_type=value.customer_type or ["B2B"],
            customer_password=auth_handler.generate_hash_password(value.customer_password)
        )
        if customer.save():
            log.save_login_log(value.customer_phone_number)
            customer.set_activity()
            customer_result = customer.get_customer()
            customer_id = customer_result.get("customerID")
            message = {
                "message": "ثبت نام شما با موفقیت انجام شد",
                "data": {
                    "customerID": customer_id,
                    "customerStatus": customer.customer_status,
                    "customerIsActive": False
                }
            }
            if value.customer_type == ["B2C"]:
                kosar_data = customer.kosar_getter(customer_type=value.customer_type)
                customer.set_rakiano_activity()
                message = {
                    "message": "اطلاعات شما با موفقیت ثبت شد",
                    "data": {
                        "customerID": customer_id,
                        "customerPhoneNumber": value.customer_phone_number,
                        "customerStatus": customer_result.get("customerStatus"),
                        "customerIsActive": True,
                    }
                }
                return {"success": True, "message": message, "kosarData": kosar_data,
                        "userData": customer.get_wallet_data() or {}, "status_code": 201}
            return {"success": True, "message": message, "status_code": 201}
        else:
            message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
            return {"success": False, "error": message, "status_code": 417}
