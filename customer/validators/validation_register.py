from typing import Optional

from pydantic import BaseModel, Field


class CustomerRegister(BaseModel):
    customer_phone_number: str = Field(description="", alias="customerPhoneNumber")
    customer_first_name: str = Field(description="", alias="customerFirstName")
    customer_last_name: str = Field(description="", alias="customerLastName")
    customer_national_id: str = Field(description="", alias="customerAddresses")
    customer_city: Optional[str] = Field(alias="customerCity")
    customer_address: Optional[str] = Field(alias="customerAddress")
    customer_province: Optional[str] = Field(alias="customerProvince")
    customer_province_code: Optional[str] = Field(alias="customerProvinceCode")
