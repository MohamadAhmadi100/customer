import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator, Field


class EditProfile(BaseModel):
    customer_phone_number: Optional[str] = Field(
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
    def validate_phone_num(cls, customer_phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, customer_phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return customer_phone_number

    customer_first_name: Optional[str] = Field(
        description="",
        title="نام",
        alias="customerFirstName",
        name="customerFirstName",
        placeholder="مهدی",
        minLength=2,
        maxLength=32,
        dataType="string",
        type="text",
        regexPattern="^[\\u0600-\\u06FF]{2,32}$",
        isRquired=False,
    )

    @validator("customer_first_name")
    def validate_customer_first_name(cls, customer_first_name):
        pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{2,16}$"
        match = re.fullmatch(pattern, customer_first_name)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid first name"})
        return customer_first_name

    customer_last_name: Optional[str] = Field(
        description="",
        alias="customerLastName",
        title="نام خانوادگی",
        name="customerLastName",
        placeholder="مهدوی",
        minLength=2,
        maxLength=32,
        dataType="string",
        type="text",
        regexPattern="^[\\u0600-\\u06FF]{2,32}$",
        isRquired=False,
    )

    @validator("customer_last_name")
    def validate_customer_last_name(cls, customer_last_name):
        pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{2,16}$"
        match = re.fullmatch(pattern, customer_last_name)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid last name"})
        return customer_last_name


    customer_national_id: Optional[str] = Field(
        description="",
        title="کد ملی",
        alias="customerNationalID",
        name="customerNationalID",
        placeholder="6150077698",
        minLength=10,
        maxLength=10,
        dataType="string",
        type="text",
        isRquired=False,
        regexPattern="^[0-9]{10}$",

    )

    @validator("customer_national_id")
    def validate_customer_national_id(cls, customer_national_id):
        pattern = r"^[0-9]{10}$"
        match = re.fullmatch(pattern, customer_national_id)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid national id"})
        return customer_national_id

    customer_city: Optional[str] = Field(
        alias="customerCity",
        description="",
        title="نام شهر",
        name="customerCity",
        placeholder="تهران",
        minLength=2,
        maxLength=32,
        dataType="string",
        type="text",
        regexPattern="^[\\u0600-\\u06FF]{2,32}$",
        isRquired=False,
    )

    @validator("customer_city")
    def validate_customer_city(cls, customer_city):
        pattern = r"^(?=.*?[\u0600-\u06FF])(\s)?.{2,32}$"
        match = re.fullmatch(pattern, customer_city)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid city"})
        return customer_city

    customer_province: Optional[str] = Field(
        alias="customerProvince",
        description="",
        title="استان",
        name="customerProvince",
        placeholder="تهران",
        minLength=2,
        maxLength=32,
        dataType="string",
        type="text",
        regexPattern="^[\\u0600-\\u06FF]{2,32}$",
        isRquired=False,
    )

    @validator("customer_province")
    def validate_customer_province(cls, customer_province):
        pattern = r"^(?=.*?[\u0600-\u06FF])(\s)?.{2,32}$"
        match = re.fullmatch(pattern, customer_province)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid province"})
        return customer_province
    #
    # customer_postal_code: Optional[str] = Field(
    #     alias="customerPostalCode",
    #     description="",
    #     title="کد پستی",
    #     name="customerPostalCode",
    #     placeholder="4571915113",
    #     minLength=10,
    #     maxLength=10,
    #     dataType="string",
    #     type="text",
    #     regexPattern="^[0-9]{10}$",
    #     isRquired=False,
    # )
    #
    # @validator("customer_postal_code")
    # def validate_customer_postal_code(cls, customer_postal_code):
    #     pattern = r"^[0-9]{10}$"
    #     match = re.fullmatch(pattern, customer_postal_code)
    #     if not match:
    #         raise HTTPException(status_code=422, detail={"error": "Please enter a valid province code"})
    #     return customer_postal_code

    # customer_province_code: Optional[str] = Field(
    #     description="",
    #     alias="customerProvinceCode",
    #     title="کد شهز",
    #     name="customerProvinceCode",
    #     minLength=1,
    #     maxLength=8,
    #     dataType="string",
    #     type="hidden",
    #     regexPattern="^[\\u0600-\\u06FF]{2,32}$",
    #     isRquired=True,
    # )
    #
    # @validator("customer_first_name")
    # def validate_customer_first_name(cls, customer_first_name):
    #     pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{2,16}$"
    #     match = re.fullmatch(pattern, customer_first_name)
    #     if not match:
    #         raise HTTPException(status_code=422, detail={"error": "Please enter a valid first name"})
    #     return customer_first_name

