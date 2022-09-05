import json
import random
import time
from typing import Optional, Union, Tuple

import redis
import requests

from config import config


class OTP:
    client = redis.Redis(host=config.REDIS_HOST,
                         port=config.REDIS_PORT,
                         username=config.REDIS_USER,
                         password=config.REDIS_PASS,
                         decode_responses=True,
                         db=config.REDIS_DB
                         )
    SMS_SENDER_NUMBER: config.SMS_SENDER_NUMBER
    SMS_API_TOKEN: str = config.SMS_API_TOKEN
    SMS_TEMPLATE: str = config.SMS_TEMPLATE

    def __init__(self, phone_number: Optional[str] = None):
        self.phone_number: str = phone_number
        self.otp_code: str = ""
        self.otp_code_length: int = 4

    def generate_code(self, otp_code_length) -> str:
        for _ in range(otp_code_length):
            self.otp_code += str(random.randint(0, 9))  # type: str
            print(self.otp_code)
        return self.otp_code

    def send(self) -> tuple:
        url = f"https://api.kavenegar.com/v1/{self.SMS_API_TOKEN}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"token={self.otp_code}&"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True

    def save(self, resend_time=120, expire_time=600) -> None:
        resend_time = 120
        value_dict = {
            "code": self.otp_code,
            "exp_time": time.time() + resend_time
        }
        with self.client as r:
            r.set(self.phone_number, json.dumps(value_dict))
            r.expire(self.phone_number, expire_time)

    def get_otp(self, phone_number: Optional[str] = None) -> Union[dict, bool]:
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        return json.loads(value).get("code") if value else False

    def is_verify_otp(self, phone_number: Optional[str] = None):
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        return bool(value and json.loads(value).get("verify"))

    def is_expire_otp(self, receive_otp_code: Optional[str] = None, phone_number: Optional[str] = None) -> bool:
        phone_number: str = phone_number or self.phone_number
        receive_otp_code: str = self.otp_code if receive_otp_code is None else receive_otp_code
        with self.client as r:
            value: bytes = r.get(phone_number)
        otp_code: str = json.loads(value).get("code") if value else None
        return bool(otp_code and otp_code == receive_otp_code)

    def is_expire_otp_time(self, phone_number: Optional[str] = None) -> Union[Tuple[bool, int]]:
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        exp_time: float = json.loads(value).get("exp_time") if value else None
        remaining_time: float = exp_time - time.time() if exp_time else 0
        return (True, 0) if remaining_time < 1 else (False, int(remaining_time))

    def delete_otp(self, phone_number: Optional[str] = None) -> bool:
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.expire(phone_number, 1)
            return bool(value)
