import json
import re

from customer.helper.connection import AttributeMongoConnection
from customer.models.model_profile import Profile
from customer.models.model_register import Customer
from customer.modules.auth import AuthHandler


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_to_snake(camel_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def convert_case(dict_data, action):
    function = camel_to_snake if action == 'snake' else snake_to_camel
    new_dict = {}
    if isinstance(dict_data, dict):
        for key, value in dict_data.items():
            if isinstance(value, dict):
                new_value = convert_case(value, action)
                new_key = function(key) if key not in ['B2B', 'B2C', 'B2G'] else key
                new_dict[new_key] = new_value
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    new_value = convert_case(item, action)
                    new_list.append(new_value)
                new_key = function(key)
                new_dict[new_key] = new_list
            else:
                new_key = function(key)
                new_dict[new_key] = value
        return new_dict
    if isinstance(dict_data, list):
        new_list = []
        for item in dict_data:
            new_value = convert_case(item, action)
            new_list.append(new_value)
        return new_list
    return dict_data


def get_customer_attributes():
    with AttributeMongoConnection() as mongo:
        return list(mongo.customer_attributes.find({}, {"_id": 0}))


def get_raw_profile(customer_phone_number: str):
    profile = Profile({"customer_phone_number": customer_phone_number})
    if result := profile.get_profile_data():
        return {"success": True, "message": result, "status_code": 200}
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}


def get_profile(customer_phone_number: dict):
    customer_phone_number = customer_phone_number.get('phone_number')
    profile = Profile({"customer_phone_number": customer_phone_number})
    if result := profile.get_profile_data():
        attributes = get_customer_attributes()
        attrs = convert_case(attributes, "camel")
        for attr in attrs:
            if result.get(attr.get("name")) is None or not None:
                attr["value"] = result.get(attr.get("name"))
                # result.append(attr)
        if result.get("customerStatus") == "cancel":
            attrs.append({"profileStatus": "لغو شده"})
        elif result.get("customerStatus") == "pend":
            attrs.append({"profileStatus": "در انتظار تایید"})
        elif result.get("customerStatus") == "confirm" and result.get("customerIsActive"):
            attrs.append({"profileStatus": "تایید شده"})
        else:
            attrs.append({"profileStatus": "اعتبار سنجی شماره موبایل"})
        return {"success": True, "message": attrs, "status_code": 200}
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}


def edit_profile_data(customer_phone_number: dict, data: str):
    data = json.loads(data)
    if type(data) == dict:
        data = data.get("data")
    flag = False
    if type(data) == dict:
        for _key, value in data.items():
            if value:
                flag = True
    if not flag:
        return {"success": False, "error": "تغییری در مقادیر داده نشد. لطفا اطلاعات را به درستی تغییر دهید",
                "status_code": 400}
    if customer_phone_number:
        print(data)
        data["customerPhoneNumber"] = customer_phone_number
        profile = Profile(data)
        return profile.update_profile()
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}


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
                customer.change_default_delivery(data)
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
        if not customer.get_customer().get("customerPhoneNumber"):
            return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
        if not customer.is_unique_national_id(data.get('informalNationalID')):
            return {"success": False, "status_code": 417,
                    "error": f"اطلاعات {data.get('informalFirstName')} {data.get('informalLastName')} تکراری است "}
        if result := customer.add_informal(data):
            if kosar_data := customer.kosar_getter(informal_flag=True,
                                                   national_id=data.get('informalNationalID')):
                return {"success": True, "status_code": 200, "kosarData": kosar_data,
                        "message": f"{data.get('informalFirstName')} {data.get('informalLastName')} با موفقیت ثبت شد "}
            return {"success": True, "status_code": 200,
                    "message": f"{data.get('informalFirstName')} {data.get('informalLastName')} با موفقیت ثبت شد "}
        elif result is None:
            return {"success": False, "status_code": 400,
                    "error": "دسترسی شما محدود شده است. لطفا با پشتیبانی تماس بگیرید "}
        else:
            return {"success": False, "status_code": 417,
                    "error": f"اطلاعات {data.get('informalFirstName')} {data.get('informalLastName')} تکراری است "}
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


def get_customer_data_by_id_league(customer_id_list: list):
    if result := Customer.get_customers_by_id_league(customer_id_list):
        return {"success": True, "message": result, "status_code": 200}
    elif result is None:
        return {"success": False, "error": "کاربری با مشخصات فوق پیدا نشد", "status_code": 417}
