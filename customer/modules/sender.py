import requests
from config import config


class SmsSender:
    SMS_SENDER_NUMBER: config.SMS_SENDER_NUMBER
    SMS_API_TOKEN: str = config.SMS_API_TOKEN
    SMS_TEMPLATE: str = config.SMS_TEMPLATE

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_cancel_status(self, first_name, last_name) -> tuple:
        url = f"https://api.kavenegar.com/v1/{self.SMS_API_TOKEN}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"name={first_name}&"
        url += f"family={last_name}&"
        url += f"template={self.SMS_TEMPLATE}"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True
