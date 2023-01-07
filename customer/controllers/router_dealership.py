from customer.models.model_register import Customer


def set_dealership(staff_user_id, customer_phone_number):
    customer = Customer(customer_phone_number)
    if not (data := customer.get_customer()):
        return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}
    if not customer.is_customer_active():
        return {
            "success": False,
            "error": "کاربر فعال نیست. برای ایجاد نماینده تایید کاربر الزامی است",
            "status_code": 401
        }
    kosar_data = customer.kosar_getter(informal_flag=False, customer_type=["B2B2C"]) or {}
    if not kosar_data or not data.get("customerSelCustomerCode") or not data.get("customerAccFormalAccCode"):
        return {
            "success": False,
            "error": "اطلاعات کاربر تکمیل نشده است. برای ایجاد نماینده اطلاعات کامل کاربر مورد نیاز است",
            "status_code": 401
        }
    return {"success": True, "status_code": 200, "customer_id": data.get("customerId"),
            "message": "وضعیت کاربر با موفقیت به نماینده آسود تغییر کرد"} if customer.convert_to_dealership() else {
        "success": False, "status_code": 417, "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}


def remove_dealership(staff_user_id, customer_phone_number):
    customer = Customer(customer_phone_number)
    if not customer.get_customer():
        return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}
    return {"success": True, "status_code": 200,
            "message": "وضعیت کاربر با موفقیت از نماینده آسود به مشتری عادی تغییر کرد"} if customer.remove_dealership() else {
        "success": False, "status_code": 417, "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}


class Request:
    def __init__(self, **kwargs):
        # self.customer_region_code = None
        # self.customer_address = None
        # self.customer_city_id = None
        self.customer_email = None
        # self.customer_state_id = None
        # self.customer_verify_password = None
        # self.customer_password = None
        self.customer_national_id = None
        # self.customer_postal_code = None
        # self.customer_state_name = None
        # self.customer_city_name = None
        self.customer_last_name = None
        self.customer_first_name = None
        self.customer_phone_number = None
        # self.customer_document_status = None
        self.customer_type = None
        # self.customer_ofogh_code = None
        self.__dict__.update(kwargs)


def register_dealership_final_customer(customer_phone_number: str, data: dict):
    dealership = Customer(phone_number=customer_phone_number)
    result = dealership.get_customer()
    if type(result.get("customerTypes")) != list or ("B2B2C" not in result.get("customerTypes")):
        return {
            "success": False,
            "error": "دسترسی شما محدود شده است. لطفا با پشتیبانی آسود تماس بگیرید",
            "status_code": 401
        }
    value = Request(**data)
    customer = Customer(phone_number=value.customer_phone_number)
    customer_data = customer.get_customer()
    is_exists_phone_number = customer_data.get("customerPhoneNumber")
    is_exists_national_id = customer_data.get("customerNationalID")
    if is_exists_phone_number or is_exists_national_id or not customer.is_unique_national_id(
            value.customer_national_id):
        return _register_output(customer, value)
    customer.set_data(
        customer_phone_number=value.customer_phone_number,
        customer_first_name=value.customer_first_name,
        customer_last_name=value.customer_last_name,
        customer_national_id=value.customer_national_id,
        # customer_state_name=value.customer_state_name,
        # customer_city_name=value.customer_city_name,
        # customer_city_id=value.customer_city_id,
        # customer_postal_code=value.customer_postal_code,
        # customer_address=value.customer_address,
        # customer_region_code=value.customer_region_code,
        # customer_state_id=value.customer_state_id,
        # customer_ofogh_code=value.customer_ofogh_code,
        customer_type=["B2C"]
    )
    if customer.save():
        customer.set_dealership_activity()
        customer_result = customer.get_customer()
        customer_id = customer_result.get("customerID")
        kosar_data = customer.kosar_getter()
        message = {
            "message": "اطلاعات خرید مشتری با موفقیت ثبت شد",
            "data": {
                "customerID": customer_id,
                "customerPhoneNumber": value.customer_phone_number,
                "customerStatus": customer_result.get("customerStatus"),
                "customerIsActive": True
            }
        }
        dealership.add_dealership_customer(customer_id=customer_data.get("customerID"),
                                           customer_phone_number=data.get("customerPhoneNumber"),
                                           customer_national_id=data.get("customerNationalID"))
        return {"success": True, "message": message, "kosarData": kosar_data, "status_code": 201}
    else:
        message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
        return {"success": False, "error": message, "status_code": 417}


def _register_output(customer, value):
    customer.set_dealership_activity()
    customer_result = customer.get_customer()
    customer_id = customer_result.get("customerID")
    kosar_data = customer.kosar_getter(customer_type=["B2C"])
    message = {
        "hasRegistered": True,
        "message": "اطلاعات کاربر با موفقیت ثبت شد",
        "data": {
            "customerID": customer_id,
            "customerPhoneNumber": value.customer_phone_number,
            "customerStatus": customer_result.get("customerStatus"),
            "customerIsActive": True
        }
    }
    return {"success": True, "message": message, "kosarData": kosar_data, "status_code": 200}


# ============================================
class RequestDealership:
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


def register_dealership(customer_phone_number: str, data: dict):
    value = RequestDealership(**data)
    customer = Customer(phone_number=value.customer_phone_number)
    customer_data = customer.get_customer()
    is_exists_phone_number = customer_data.get("customerPhoneNumber")
    is_exists_national_id = customer_data.get("customerNationalID")

    if is_exists_phone_number or is_exists_national_id or not customer.is_unique_national_id(
            value.customer_national_id):
        message = {
            "hasRegistered": True,
            "message": "اطلاعات کاربر تکراری است",
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
        customer_state_name=value.customer_state_name,
        customer_city_name=value.customer_city_name,
        customer_city_id=value.customer_city_id,
        customer_postal_code=value.customer_postal_code,
        customer_address=value.customer_address,
        customer_region_code=value.customer_region_code,
        customer_state_id=value.customer_state_id,
        customer_ofogh_code=value.customer_ofogh_code,
        customer_document_status=value.customer_document_status,
        customer_type=["B2B2C"],
    )
    if customer.save():
        return success_result(customer, value)
    message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
    return {"success": False, "error": message, "status_code": 417}


def success_result(customer, value):
    # customer.set_dealership_activity()
    customer_result = customer.get_customer()
    customer_id = customer_result.get("customerID")
    kosar_data = customer.kosar_getter(customer_type=["B2B2C"])
    message = {
        "message": "اطلاعات نماینده با موفقیت ثبت شد",
        "data": {
            "customerID": customer_id,
            "customerPhoneNumber": value.customer_phone_number,
            "customerStatus": customer_result.get("customerStatus"),
            "customerIsActive": True
        }
    }
    return {"success": True, "message": message, "kosarData": kosar_data, "status_code": 201}
