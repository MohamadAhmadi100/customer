import re

from fastapi import HTTPException, Query
from pydantic import BaseModel, validator, Field


class CustomerAuth(BaseModel):
    customer_phone_number: str = Field(
        title="شماره موبایل",
        alias="customerPhoneNumber",
        name="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="string",
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


class CustomerVerifyOTP(BaseModel):
    customer_phone_number: str = Field(
        title="شماره موبایل",
        alias="customerPhoneNumber",
        name="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="str",
        type="tel",
        isRquired=True,
        regexPattern="^09[0-9]{9}$",
    )

    customer_code: str = Field(
        title="رمز یک بار مصرف",
        description="otp code must be string and len 4 character",
        name="customerCode",
        alias="customerCode",
        placeholder="4563",
        minLength=4,
        maxLength=4,
        dataType="string",
        type="text",
        isRequired=True,
        regexPattern="^[0-9]{4}$",
    )

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("customer_code")
    def validate_otp(cls, code):
        pattern = r"^[0-9]{4}$"
        match = re.fullmatch(pattern, code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid otp"})
        return code


class CustomerVerifyPassword(BaseModel):
    customer_phone_number: str = Field(
        title="شماره موبایل",
        alias="customerPhoneNumber",
        name="customerPhoneNumber",
        placeholder="09371654426",
        description="phone number must be string and len 11 character",
        minLength=11,
        maxLength=11,
        dataType="string",
        type="tel",
        isRquired=True,
        regexPattern="^09[0-9]{9}$",
    )
    customer_password: str = Field(
        title="رمز عبور",
        alias="customerPassword",
        name="customerPassword",
        placeholder="qwer1234QWER",
        description="password must be string and len between 8 and 32 character",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="password",
        isRquired=True,
        regexPattern="^^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$",
    )
    # customer_login_type: str = Field(
    #     title="شیوه ورود کاربر",
    #     alias="customerLoginType",
    #     name="customerLoginType",
    #     description="customerLoginType must be `otp` or `password`",
    #     dataType="string",
    #     type="hidden",
    #     isRquired=True,
    # )

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("customer_password")
    def validate_password(cls, code):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$"
        match = re.fullmatch(pattern, code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid password"})
        return code
    #
    # @validator("customer_login_type")
    # def validate_password(cls, code_type):
    #     if code_type == "otp" and code_type == "password":
    #         raise HTTPException(status_code=422, detail={"error": "Please enter a valid login type"})
    #     return code_type
