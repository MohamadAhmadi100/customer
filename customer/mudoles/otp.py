import json
import random
import time
from typing import Optional, Union, Tuple

import redis
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

    def set_otp_code_length(self, length: int) -> None:
        """ set number between 3 and 6 character"""
        self.otp_code_length = length

    def generate_code(self) -> str:
        for i in range(self.otp_code_length):
            self.otp_code += str(random.randint(0, 9))  # type: str
        return self.otp_code

    # TODO rewrite
    def send_otp_code(self) -> tuple:
        params = {
            "sender": self.SENDER_NUM,  # type: str
            "receptor": self.phone_number,  # type: str
            "message": f" کد فعال سازی: {self.otp_code} \n آسود"
        }
        try:
            response: list = self.API.sms_send(params)
            if (response[0].get("status") < 6) or (response[0].get("status") == 10):
                return {"message": "success"}, True
            else:
                return {"message": response}, False
        except Exception as e:
            return {"error": e}, False

    def save_otp(self, resend_time=120, expire_time=600) -> None:
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
        return json.loads(value) if value else False

    def is_expire_otp(
            self, receive_otp_code: Optional[str] = None,
            phone_number: Optional[str] = None
    ) -> bool:
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
