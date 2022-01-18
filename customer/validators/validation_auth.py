import re

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field


class CustomerAuth(BaseModel):
    customer_phone_number: str = Field(
        title="شماره موبایل",
        alias="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="str",
        type="tel",
        isRquired=True,
        regexPattern="^09[0-9]{9}$",
    )

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number


class CustomerSendOTP(BaseModel):
    customer_phone_number: str = Field(
        alias="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="str",
        type="tel",
        isRequired=True,
        regexPattern="^09[0-9]{9}$",
    )

    # TODO validate code type

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number


class CustomerVerifyOTP(BaseModel):
    customer_phone_number: str = Field(
        alias="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="str",
        type="tel",
        isRequired=True,
        regexPattern="^09[0-9]{9}$",
    )
    customer_password: str = Field(
        description="password must be string and len between 8 and 32 character",
        alias="customerCode",
    )
    customer_code: str = Field(
        description="password must be string and len between 4 and 8 character",
        alias="customerCode"
    )

    # TODO validate code type

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("customer_code")
    def validate_otp(cls, code):
        pattern = r"^[0-9]{3,8}$"
        match = re.fullmatch(pattern, code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid otp"})
        return code


class CustomerVerifyPassword(BaseModel):
    customer_phone_number: str = Field(
        alias="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="str",
        type="tel",
        isRequired=True,
        regexPattern="^09[0-9]{9}$",
    )
    customer_password: str = Field(
        description="password must be string and len between 8 and 32 character",
        alias="customerCode",
    )

    # TODO validate code type

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("customer_code")
    def validate_otp(cls, code):
        pattern = r"^[0-9]{3,8}$"
        match = re.fullmatch(pattern, code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid otp"})
        return code
