import re

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field

PHONE_NUMBER_DESCRIPTION = "phone number must be string and len 11 character"
OTP_CODE_DESCRIPTION = "phone number must be string and len between 3 and 8 character"


class CustomerSchemas(BaseModel):
    phone_number: str = Field(description=PHONE_NUMBER_DESCRIPTION, alias="phoneNumber")

    @validator("phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number


class CustomerVerify(BaseModel):
    phone_number: str = Field(description=PHONE_NUMBER_DESCRIPTION, alias="phoneNumber")
    otp_code: str = Field(description=OTP_CODE_DESCRIPTION, alias="otpCode")

    @validator("phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("otp_code")
    def not_valid_ip(cls, otp_code):
        pattern = r"^[0-9]{3,6}$"
        match = re.fullmatch(pattern, otp_code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid otp"})
        return otp_code


class CustomerSetPassword(BaseModel):
    phone_number: str = Field(description=PHONE_NUMBER_DESCRIPTION, alias="phoneNumber")
    password: str = Field(description=OTP_CODE_DESCRIPTION, alias="otpCode")

    @validator("phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("password")
    def not_valid_ip(cls, password):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$"
        match = re.fullmatch(pattern, password)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid password"})
        return password
