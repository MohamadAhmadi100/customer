import json

from config import VALID_PROFILE_KEYS
from customer.models.model_profile import Profile
from customer.models.model_register import Customer
from customer.modules.getter import GetData
from customer.modules.setter import Filter
from customer.modules.temporary_password import TempPassword


def set_dealership(staff_user_id, customer_phone_number):
    customer = Customer(customer_phone_number)
    if not customer.get_customer():
        return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}
    if not customer.is_customer_active():
        return {
            "success": False,
            "error": "کاربر فعال نیست. برای ایجاد نماینده تایید کاربر الزامی است",
            "status_code": 401
        }
    kosar_data = customer.kosar_getter(informal_flag=False, customer_type=["B2B2C"]) or {}
    if not kosar_data:
        return {
            "success": False,
            "error": "اطلاعات کاربر تکمیل نشده است. برای ایجاد نماینده به اطلاعات کامل کاربر نیاز است",
            "status_code": 401
        }
    # wallet_data
    if not customer.convert_to_dealership():
        return {"success": False, "status_code": 417, "error": "مشکلی رخ داده است. لطفا مجددا امتحان کنید"}
