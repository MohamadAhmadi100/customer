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
    try:
        customer_phone_number = data.get("customer_phone_number")
        customer = Customer(customer_phone_number)
        if data is None:
            return {"success": True, "status_code": 200, "message": {"data": customer.retrieve_default_delivery()}}
        data = json.loads(data.get("delivery"))
    except Exception as e:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    if customer.add_delivery(data):
        return {"success": True, "status_code": 201,
                "message": {"message": "پیک با موفقیت ثبت شد", "data": data}}
    return {"success": True, "status_code": 200, "message": {"message": "پیک اصلی با موفقیت تغییر کرد", "data": data}}


def get_delivery_persons(data) -> dict:
    try:
        phone_number= data.get("customer_phone_number")
        customer = Customer(phone_number)
    except IndexError:
        return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
    if persons := customer.retrieve_delivery_persons():
        print(persons)
        return {"success": True, "status_code": 200, "message": {"data": [json.loads(person) for person in persons]}}
