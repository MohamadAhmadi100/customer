import json
import random
import time
from typing import Optional, Union, Tuple

import redis
import requests
from kavenegar import KavenegarAPI


class OTP:
    API = KavenegarAPI("535041646375714D57613535695561696E7355724A796B2B5657715833434939")
    SENDER_NUM = "10005007009009"

    def __init__(self, phone_number: Optional[str] = None):
        self.phone_number: str = phone_number
        self.otp_code: str = ""
        self.otp_code_length: int = 4

    def set_api(self, api: str = None) -> None:
        self.API = KavenegarAPI(api)

    def set_sender_num(self, num: str) -> None:
        self.SENDER_NUM = num

    def generate_code(self, otp_code_length) -> str:
        for i in range(otp_code_length):
            self.otp_code += str(random.randint(0, 9))  # type: str
        return self.otp_code

    # TODO rewrite
    def send(self) -> tuple:
        token = "535041646375714D57613535695561696E7355724A796B2B5657715833434939"
        template = "logincode"
        url = f"https://api.kavenegar.com/v1/{token}/verify/lookup.json?"
        url += f"receptor={self.phone_number}&"
        url += f"token={self.otp_code}&"
        url += f"template={template}"
        try:
            result = requests.post(url)
        except Exception as e:
            return {"error": e}, False
        else:
            return {"message": result}, True

    def save(self, resend_time=120, expire_time=600) -> None:
        value_dict = {
            "code": self.otp_code,
            "exp_time": time.time() + resend_time
        }
        with redis.Redis() as r:
            r.set(self.phone_number, json.dumps(value_dict))
            r.expire(self.phone_number, expire_time)

    def get_otp(self, phone_number: Optional[str] = None) -> Union[dict, bool]:
        phone_number: str = self.phone_number if phone_number is None else phone_number
        with redis.Redis() as r:
            value: bytes = r.get(phone_number)
        return json.loads(value).get("code") if value else False

    def is_verify_otp(self, phone_number: Optional[str] = None):
        phone_number: str = self.phone_number if phone_number is None else phone_number
        with redis.Redis() as r:
            value: bytes = r.get(phone_number)
        return True if value and json.loads(value).get("verify") else False

    def is_expire_otp(self, receive_otp_code: Optional[str] = None, phone_number: Optional[str] = None) -> bool:
        phone_number: str = self.phone_number if phone_number is None else phone_number
        receive_otp_code: str = self.otp_code if receive_otp_code is None else receive_otp_code
        with redis.Redis() as r:
            value: bytes = r.get(phone_number)
        otp_code: str = json.loads(value).get("code") if value else None
        return True if otp_code and otp_code == receive_otp_code else False

    def is_expire_otp_time(self, phone_number: Optional[str] = None) -> Union[Tuple[bool, int]]:
        phone_number: str = self.phone_number if phone_number is None else phone_number
        with redis.Redis() as r:
            value: bytes = r.get(phone_number)
        exp_time: float = json.loads(value).get("exp_time") if value else None
        remaining_time: float = exp_time - time.time() if exp_time else 0
        return (True, 0) if remaining_time < 1 else (False, int(remaining_time))
