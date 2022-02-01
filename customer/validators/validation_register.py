import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pydantic import validator


class CustomerRegister(BaseModel):
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
    customer_first_name: str = Field(
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
        isRquired=True,
    )

    customer_last_name: str = Field(
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
        isRquired=True,
    )

    customer_region_code: str = Field(
        description="",
        alias="customerRegionCode",
        # title="نام خانوادگی",
        name="customerRegionCode",
        minLength=1,
        maxLength=8,
        dataType="string",
        type="hidden",
        # regexPattern="^[\\u0600-\\u06FF]{2,32}$",
        isRquired=True,
    )
    customer_national_id: str = Field(
        description="",
        title="کد ملی",
        alias="customerNationalID",
        name="customerNationalID",
        placeholder="6150077698",
        minLength=10,
        maxLength=10,
        dataType="string",
        type="text",
        isRquired=True,
        regexPattern="^[0-9]{10}$",

    )
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
        isRquired=True,
    )
    customer_city_id: Optional[str] = Field(
        alias="customerCityID",
        description="",
        title="ای دی شهر",
        name="customerCityID",
        minLength=1,
        maxLength=8,
        dataType="string",
        type="hidden",
        regexPattern="^[0-9]{1,8}$",
        isRquired=True,
    )
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
        isRquired=True,
    )
    customer_province_id: Optional[str] = Field(
        alias="customerProvinceID",
        description="",
        title="ای دی استان",
        name="customerProvinceID",
        minLength=1,
        maxLength=8,
        dataType="string",
        type="hidden",
        # regexPattern="^[0-9]{1,8}$",
        isRquired=True,
    )
    customer_address: Optional[str] = Field(
        alias="customerAddress",
        description="",
        title="آدرس",
        name="customerAddress",
        placeholder="تهران پلاک ۳",
        minLength=8,
        maxLength=128,
        dataType="string",
        type="text",
        regexPattern="^[\\u0600-\\u06FF]{8,128}$",
        isRquired=False,
    )

    customer_postal_code: Optional[str] = Field(
        alias="customerPostalCode",
        description="",
        title="کد پستی",
        name="customerPostalCode",
        placeholder="4571915113",
        minLength=10,
        maxLength=10,
        dataType="string",
        type="text",
        regexPattern="^[0-9]{10}$",
        isRquired=False,
    )

    @validator("customer_phone_number")
    def validate_phone_num(cls, customer_phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, customer_phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return customer_phone_number

    @validator("customer_first_name")
    def validate_customer_first_name(cls, customer_first_name):
        pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{2,16}$"
        match = re.fullmatch(pattern, customer_first_name)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid first name"})
        return customer_first_name

    @validator("customer_last_name")
    def validate_customer_last_name(cls, customer_last_name):
        pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{2,16}$"
        match = re.fullmatch(pattern, customer_last_name)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid last name"})
        return customer_last_name

    @validator("customer_national_id")
    def validate_customer_national_id(cls, customer_national_id):
        pattern = r"^[0-9]{10}$"
        match = re.fullmatch(pattern, customer_national_id)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid national id"})
        return customer_national_id

    @validator("customer_city")
    def validate_customer_city(cls, customer_city):
        pattern = r"^(?=.*?[\u0600-\u06FF])(\s)?.{2,32}$"
        match = re.fullmatch(pattern, customer_city)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid city"})
        return customer_city

    @validator("customer_province")
    def validate_customer_province(cls, customer_province):
        pattern = r"^(?=.*?[\u0600-\u06FF])(\s)?.{2,32}$"
        match = re.fullmatch(pattern, customer_province)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid province"})
        return customer_province

    @validator("customer_address")
    def validate_customer_address(cls, customer_address):
        pattern = r"^(?=.*?[\u0600-\u06FF])([0-9,;-])?(\s)?.{4,128}$"
        match = re.fullmatch(pattern, customer_address)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid address"})
        return customer_address

    @validator("customer_postal_code")
    def validate_customer_postal_code(cls, customer_postal_code):
        pattern = r"^[0-9]{10}$"
        match = re.fullmatch(pattern, customer_postal_code)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid province code"})
        return customer_postal_code
    #
    # @validator("customer_province_id")
    # def validate_customer_province_id(cls, customer_province_id):
    #     pattern = r"^[0-9]{1,8}$"
    #     match = re.fullmatch(pattern, customer_province_id)
    #     if not match:
    #         raise HTTPException(status_code=422, detail={"error": "Please enter a valid address"})
    #     return customer_province_id
    #
    # @validator("customer_city_id")
    # def validate_customer_city_id(cls, customer_city_id):
    #     pattern = r"^[0-9]{1,8}$"
    #     match = re.fullmatch(pattern, customer_city_id)
    #     if not match:
    #         raise HTTPException(status_code=422, detail={"error": "Please enter a valid province code"})
    #     return customer_city_id
