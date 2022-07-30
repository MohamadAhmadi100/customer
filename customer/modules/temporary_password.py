import json
import random
import string
import time
from typing import Optional, Union, Tuple

import redis

from config import config


class TempPassword:
    client = redis.Redis(host=config.REDIS_HOST,
                         port=config.REDIS_PORT,
                         username=config.REDIS_USER,
                         password=config.REDIS_PASS,
                         decode_responses=True,
                         db=config.REDIS_DB
                         )

    def __init__(self, phone_number: str):
        self.phone_number: str = f"{phone_number}_password"
        self.password: str = ""
        self.password_length: int = 8

    def generator(self) -> str:
        for _ in range(self.password_length):
            self.password += random.choice(string.hexdigits)
        return self.password

    def save(self, resend_time=2, expire_time=1800) -> None:
        value_dict = {
            "password": self.password,
            "exp_time": time.time() + resend_time
        }
        with self.client as r:
            r.set(self.phone_number, json.dumps(value_dict))
            r.expire(self.phone_number, expire_time)

    def get_password(self, phone_number: Optional[str] = None) -> Union[dict, bool]:
        if phone_number:
            phone_number: str = f"{phone_number}_password"
        else:
            phone_number: str = self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        return json.loads(value).get("password") if value else False

    def is_verify_password(self, phone_number: Optional[str] = None):
        if phone_number:
            phone_number: str = f"{phone_number}_password"
        else:
            phone_number: str = self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        return bool(value and json.loads(value).get("verify"))

    def is_expire_password(self, receive_password: Optional[str] = None, phone_number: Optional[str] = None) -> bool:
        phone_number: str = phone_number or self.phone_number
        receive_password: str = self.password if receive_password is None else receive_password
        with self.client as r:
            value: bytes = r.get(phone_number)
        password: str = json.loads(value).get("password") if value else None
        return bool(password and password == receive_password)

    def is_expire_password_time(self, phone_number: Optional[str] = None) -> Union[Tuple[bool, int]]:
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.get(phone_number)
        exp_time: float = json.loads(value).get("exp_time") if value else None
        remaining_time: float = exp_time - time.time() if exp_time else 0
        return (True, 0) if remaining_time < 1 else (False, int(remaining_time))

    def delete_password(self, phone_number: Optional[str] = None) -> bool:
        phone_number: str = phone_number or self.phone_number
        with self.client as r:
            value: bytes = r.expire(phone_number, 1)
            return bool(value)
