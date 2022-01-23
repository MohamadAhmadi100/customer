from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Header
from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from starlette import status


class AuthHandler:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    SECRET_KEY = "a5cad81912ad25eb12920bf6357d799773887f77291fec95c345fd136078bf2c"
    refresh_exp = timedelta(days=1)
    access_exp = timedelta(days=0, minutes=20)

    def generate_hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, user_password: str, hashed_password: str) -> str:
        return self.pwd_context.verify(user_password, hashed_password)

    def encode_access_token(self, user_name: str) -> str:
        pay_load = {
            'exp': datetime.utcnow() + self.access_exp,
            'iat': datetime.utcnow(),
            'sub': user_name,
            'scope': 'access'
        }
        return jwt.encode(pay_load, self.SECRET_KEY, algorithm='HS256').decode("utf-8")

    def encode_refresh_token(self, user_name: str) -> str:
        pay_load = {
            'exp': datetime.utcnow() + self.refresh_exp,
            'iat': datetime.utcnow(),
            'sub': user_name,
            'scope': 'refresh'
        }
        return jwt.encode(pay_load, self.SECRET_KEY, algorithm='HS256').decode("utf-8")

    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='access token has expired')
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    def decode_refresh_token(self, token: str):
        """
        decode refresh token and if the token wasn't expired call
        encode_access to generate new access token and if there was
         problem it will return 401
        :param token: refresh token
        :return:
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            user_name = payload["sub"]
            new_access_token = self.encode_access_token(user_name)
            return new_access_token
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='refresh token has expired')
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    def check_current_user_tokens(self, access: str = Header('access'), refresh: str = Header('refresh')):
        try:
            self.decode_access_token(access)
        except:
            self.decode_refresh_token(refresh)
