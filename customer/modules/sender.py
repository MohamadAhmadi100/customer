import requests
from config import config


class SmsSender:
    SMS_SENDER_NUMBER: config.SMS_SENDER_NUMBER
    SMS_API_TOKEN: str = config.SMS_API_TOKEN
    SMS_CANCEL_STATUS_TEMPLATE: str = config.SMS_CANCEL_STATUS_TEMPLATE
    RAKIANO_SMS_CANCEL_STATUS_TEMPLATE: str = config.RAKIANO_SMS_CANCEL_STATUS_TEMPLATE
    SMS_ACTIVATE_TEMPLATE: str = config.SMS_ACTIVATE_TEMPLATE
    RAKIANO_SMS_ACTIVATE_TEMPLATE: str = config.RAKIANO_SMS_ACTIVATE_TEMPLATE
    SMS_REGISTER_TEMPLATE: str = config.SMS_REGISTER_TEMPLATE
    RAKIANO_SMS_REGISTER_TEMPLATE: str = config.RAKIANO_SMS_REGISTER_TEMPLATE

    def __init__(self, phone_number, customer_type="B2B"):
        self.phone_number = phone_number
        self.customer_type = customer_type

    def cancel_status(self, first_name, last_name) -> tuple:
        url = f"https://api.kavenegar.com/v1/{self.SMS_API_TOKEN}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"token={first_name}&"
        url += f"token2={last_name}&"
        if self.customer_type == "B2B":
            url += f"template={self.SMS_CANCEL_STATUS_TEMPLATE}"
        else:
            url += f"template={self.RAKIANO_SMS_CANCEL_STATUS_TEMPLATE}"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True

    def activate_status(self, first_name, last_name) -> tuple:
        url = f"https://api.kavenegar.com/v1/{self.SMS_API_TOKEN}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"token={first_name}&"
        url += f"token2={last_name}&"
        if self.customer_type == "B2B":
            url += f"template={self.SMS_ACTIVATE_TEMPLATE}"
        else:
            url += f"template={self.RAKIANO_SMS_ACTIVATE_TEMPLATE}"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True

    def register(self, first_name, last_name) -> tuple:
        url = f"https://api.kavenegar.com/v1/{self.SMS_API_TOKEN}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"token={first_name}&"
        url += f"token2={last_name}&"
        if self.customer_type == "B2B":
            url += f"template={self.SMS_REGISTER_TEMPLATE}"
        else:
            url += f"template={self.RAKIANO_SMS_REGISTER_TEMPLATE}"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True
