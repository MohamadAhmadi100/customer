import re

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field


class CustomerSetPassword(BaseModel):
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
    customer_password: str = Field(description="", alias="customer_password")

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number

    @validator("customer_password")
    def not_valid_ip(cls, password):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$"
        match = re.fullmatch(pattern, password)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid password"})
        return password
