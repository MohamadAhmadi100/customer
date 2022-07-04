import json

from config import VALID_PROFILE_KEYS
from customer.models.model_profile import Profile
from customer.models.model_register import Customer
from customer.modules.getter import GetData
from customer.modules.setter import Filter


def get_customers_grid_data(data: str = None):
    data = {} if data is None else json.loads(data)
    records = Filter()
    period_filters: dict = {}
    value_filters: dict = {}
    search_query: dict = {}
    if filters := data.get("filters"):
        period_filters: dict = records.set_period_filters(filters) or {}
        value_filters: dict = records.set_value_filters(filters) or {}
    if search_phrase := data.get("search"):
        search_query = records.set_search_query(search_phrase)
    filters = dict(period_filters, **value_filters, **search_query)
    print(filters)
    return GetData().executor(
        queries=filters,
        number_of_records=data.get("perPage") or "15",
        page=data.get("page") or "1",
        sort_name=data.get("sortName") or "customerID",
        sort_type=data.get("sortType") or "asc"
    )


def crm_get_profile(customer_phone_number: dict):
    customer_phone_number = customer_phone_number.get('phone_number')
    profile = Profile({"customer_phone_number": customer_phone_number})
    if result := profile.get_profile_data():
        customer = {grid_attribute: result.get(grid_attribute) or None for grid_attribute in VALID_PROFILE_KEYS}
        return {"success": True, "message": customer, "status_code": 200}
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 401}


def set_confirm_status(mobileNumber: str) -> dict:
    customer = Customer(mobileNumber)
    if not customer.is_exists_phone_number():
        return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}
    try:
        kosar_data = customer.kosar_getter() or {}
        for key, value in kosar_data.items():
            if not value:
                return {"success": False, "error": "اطلاعات کاربر تکمیل نشده است. کاربر فعال نشد", "status_code": 401}
        result = customer.confirm_status()
        mobile_confirm = customer.is_mobile_confirm()
        if result and mobile_confirm:
            customer.activate()
            data = customer.get_customer()
            if data.get("customerSelCustomerCode") and data.get("customerAccFormalAccCode"):
                return {
                    "success": True,
                    "message": "کاربر با موفقیت فعال شد",
                    "userData": customer.get_wallet_data() or {},
                    "status_code": 200,
                    # "kosarData": kosar_data,

                }
            return {
                "success": True,
                "message": "کاربر با موفقیت فعال شد",
                "userData": customer.get_wallet_data() or {},
                "kosarData": kosar_data,
                "status_code": 200
            }
        if result:
            return {
                "success": True,
                "message": "برای انجام خرید کاربر نیاز به تایید شماره موبایل با رمز یک بار مصرف دارد",
                "userData": customer.get_wallet_data() or {},
                "kosarData": kosar_data,
                "status_code": 200
            }
        return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 404}
    except Exception:
        return {"success": False, "error": "مشکلی به وجود آمد. لطفا مجددا تلاش کنید", "status_code": 404}


def set_cancel_status(mobileNumber: str) -> dict:
    customer = Customer(mobileNumber)
    if result := customer.cancel_status():
        return {"success": True, "message": "وضعیت کاربر با موفقیت به روز شد", "status_code": 200}
    elif result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}


def set_kosar_data(mobileNumber, kosarData) -> dict:
    customer = Customer(mobileNumber)
    if result := customer.kosar_setter(
            kosarData.get("sel_Customer_Code"),
            kosarData.get("acc_FormalAcc_Code")):
        return {"success": True, "message": "کاربر با موفقیت فعال شد", "status_code": 200}
    elif result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}


def edit_customers_grid_data(data):
    data = json.loads(data)
    if data.get("customerMobileNumber"):
        profile = Profile(data)
        return profile.update_profile()
    return {"status_code": 422, "success": False, "error": "ورود شماره موبایل الزامی است."}


def set_informal_flag(mobileNumber: str, hasInformal: bool):
    customer = Customer(mobileNumber)
    if result := customer.set_has_informal(hasInformal):
        return {"success": True, "message": "وضعیت غیر رسمی کاربر با موفقیت به روز شد", "status_code": 200}
    elif result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}


def get_customer_data_by_id(id_list: list):
    if result := Customer.get_customers_by_id(id_list):
        return {"success": True, "message": result, "status_code": 200}
    elif result is None:
        return {"success": False, "error": "کاربری با مشخصات فوق پیدا نشد", "status_code": 417}


def search_customers_by_name(phrase: str):
    result = Customer.find_customers(phrase)
    if result := [res["customerID"] for res in result]:
        return {"success": True, "message": result, "status_code": 200}
    elif result is None:
        return {"success": False, "error": "کاربری با مشخصات فوق پیدا نشد", "status_code": 417}
