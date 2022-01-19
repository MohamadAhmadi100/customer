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
        minLength=4,
        maxLength=16,
        dataType="string",
        type="text",
        isRquired=True,
    )
    customer_last_name: str = Field(
        description="",
        alias="customerLastName",
        title="نام خانوادگی",
        name="customerLastName",
        placeholder="مهدوی",
        minLength=2,
        maxLength=16,
        dataType="string",
        type="text",
        isRquired=True,
    )
    customer_national_id: str = Field(
        description="",
        title="کد ملی",
        name="customerNationalID",
        placeholder="6150077698",
        minLength=10,
        maxLength=10,
        dataType="string",
        type="text",
        isRquired=True,
    )
    customer_city: Optional[str] = Field(
        alias="customerCity",
        description="",
        title="نام شهر",
        name="customerCity",
        placeholder="تهران",
        minLength=2,
        maxLength=16,
        dataType="string",
        type="text",
        isRquired=True,
    )
    customer_province: Optional[str] = Field(
        alias="customerProvince",
        description="",
        title="استان",
        name="customerProvince",
        placeholder="تهران",
        minLength=2,
        maxLength=16,
        dataType="string",
        type="text",
        isRquired=True,
    )
    customer_address: Optional[str] = Field(
        alias="customerAddress",
        description="",
        title="آدرس",
        name="customerAddress",
        placeholder="تهران پلاک ۳",
        minLength=8,
        maxLength=64,
        dataType="string",
        type="text",
        isRquired=False,
    )

    customer_province_code: Optional[str] = Field(
        alias="customerProvinceCode",
        description="",
        title="کد پستی",
        name="customerProvinceCode",
        placeholder="4571915113",
        minLength=10,
        maxLength=10,
        dataType="string",
        type="text",
        isRquired=False,
    )

    @validator("customer_phone_number")
    def validate_phone_num(cls, phone_number):
        pattern = r"^09[0-9]{9}$"
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise HTTPException(status_code=422, detail={"error": "Please enter a valid phone number"})
        return phone_number