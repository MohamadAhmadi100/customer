import json

from customer.models.model_register import Customer
from customer.models.model_profile import Profile
from customer.controllers import router_auth
from customer.modules.auth import AuthHandler


def get_profile(customer_phone_number: dict):
    customer_phone_number = customer_phone_number.get('phone_number')
    profile = Profile({"customer_phone_number": customer_phone_number})
    if result := profile.get_profile_data():
        return {"success": True, "message": result, "status_code": 200}
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 401}


def edit_profile_data(customer_phone_number: dict, data: str):
    if customer_phone_number:
        data = json.loads(data)
        data["customerPhoneNumber"] = customer_phone_number
        profile = Profile(data)
        return profile.update_profile()


def change_customer_password(data: dict):
    try:
        customer = Customer(data.get("customer_phone_number"))
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    customer_password = customer.get_customer_password().get("customerPassword")
    if AuthHandler().verify_password(data.get("customer_old_password"), customer_password):
        if customer.change_customer_password(data.get("customer_new_password")):
            return {"success": True, "status_code": 200,
                    "message": {"message": "رمز عبور با موفقیت تغییر کرد"}}
        return {"success": False, "status_code": 417, "error": "خطایی رخ داده است"}
    return {"success": False, "status_code": 422, "error": "رمز عبور قدیمی اشتباه است"}


def add_delivery_person(data: dict = None) -> dict:
    # sourcery skip: merge-nested-ifs
    try:
        customer_phone_number = data.get("customer_phone_number")
        customer = Customer(customer_phone_number)
        data = json.loads(data.get("delivery"))
        if not data.get("deliveryMobileNumber"):
            if default_delivery := customer.retrieve_default_delivery():
                return {"success": True, "status_code": 200, "message": {"data": default_delivery}}
            return {"success": False, "status_code": 404, "error": "پیک ثبت نشده است"}
        if deliveries := customer.retrieve_delivery_persons():
            exists = False
            for delivery in deliveries:
                if data.get("deliveryMobileNumber") == delivery.get("deliveryMobileNumber"):
                    exists = True
            if exists:
                if customer.change_default_delivery(data):
                    return {"success": True, "status_code": 200,
                            "message": {"message": "پیک اصلی با موفقیت تغییر کرد", "data": data}}
            if customer.add_delivery(data):
                return {"success": True, "status_code": 201,
                        "message": {"message": "پیک با موفقیت ثبت شد", "data": data}}
        return {"success": False, "status_code": 417,
                "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}
    except Exception as e:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}


def get_delivery_persons(data) -> dict:
    try:
        phone_number = data.get("customer_phone_number")
        customer = Customer(phone_number)
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    if persons := customer.retrieve_delivery_persons():
        return {"success": True, "status_code": 200, "message": {"data": list(persons)}}
    return {"success": False, "status_code": 404, "error": "برای شما پیک ثبت نشده است"}


def create_informal(data: dict) -> dict:
    try:
        mobile_number: str = data.get("customer_mobile_number")
        customer = Customer(mobile_number)
        data = json.loads(data.get("informal"))
        if customer.add_informal(data):
            return {"success": True, "status_code": 200,
                    "message": f"{data.get('informalFirstName')} با موفقیت ثبت شد "}
        else:
            return {"success": False, "status_code": 417,
                    "error": f"اطلاعات {data.get('informalFirstName')} تکراری است"}
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}


def get_informal(data: dict):
    try:
        if customer := Customer(data.get("customer_mobile_number")):
            if informal := customer.get_informal_person(str(data.get("informal_national_id"))):
                return {"success": True, "status_code": 200, "message": informal}
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    except Exception as e:
        return {"success": False, "status_code": 417, "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}


def get_all_informal_persons(data: dict):
    try:
        if customer := Customer(data.get("customer_mobile_number")):
            if informal_persons := customer.get_informal_persons():
                return {"success": True, "status_code": 200, "message": informal_persons}
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    except Exception as e:
        return {"success": False, "status_code": 417, "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}
