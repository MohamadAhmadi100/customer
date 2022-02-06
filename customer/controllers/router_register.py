import json

import requests
from fastapi import APIRouter, HTTPException
from fastapi import Response, status

from customer.models.model_register import Customer
from customer.mudoles import log
from customer.mudoles.auth import AuthHandler
from customer.validators import validation_register

router_register = APIRouter(
    prefix="/register",
    tags=["register"]
)

auth_handler = AuthHandler()


@router_register.get("/")
def register_validation_generator():
    form = validation_register.CustomerRegister.schema().get("properties").copy()
    return {"fields": form}


@router_register.post("/")
def register(
        response: Response,
        value: validation_register.CustomerRegister,
):
    customer = Customer(phone_number=value.customer_phone_number)
    customer.set_data(
        customer_phone_number=value.customer_phone_number,
        customer_first_name=value.customer_first_name,
        customer_last_name=value.customer_last_name,
        customer_city=value.customer_city,
        customer_province=value.customer_province,
        customer_postal_code=value.customer_postal_code,
        customer_national_id=value.customer_national_id,
        customer_password=value.customer_password
    )

    if customer.is_exists_phone_number() or customer.is_exists_national_id():
        response.status_code = status.HTTP_409_CONFLICT
        message = {
            "hasRegistered": True,
            "massage": "شما قبلا ثبت نام کرده اید.",
            "redirect": "login"
        }
    else:
        if value.customer_password != value.customer_verify_password:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise HTTPException(status_code=422, detail={"error": "رمز عبور های وارد شده یکسان نیستند"})
        if customer.save():
            url = "http://devaddr.aasood.com/address/insert"
            customer_data = customer.get_customer()
            customer_address_data = {
                "customerName": value.customer_first_name + " " + customer.customer_last_name,
                "customerId": customer_data.get("customerID"),
                "stateName": value.customer_province,
                "cityName": value.customer_city,
                "stateId": value.customer_province_id,
                "cityId": value.customer_city_id,
                "postalCode": value.customer_postal_code,
                "street": value.customer_address,
                "isDefault": True,
                "regionCode": value.customer_region_code,
                "alley": "",
                "plaque": "",
                "unit": "",
                "tel": value.customer_phone_number
            }
            log.save_login_log(value.customer_phone_number)

            requests.post(url, data=json.dumps(customer_address_data))
            response.headers["refreshToken"] = auth_handler.encode_refresh_token(user_name=value.customer_phone_number)
            response.headers["accessToken"] = auth_handler.encode_access_token(user_name=value.customer_phone_number)
            response.status_code = status.HTTP_201_CREATED
            message = {
                "massage": "ثبت نام شما با موفقیت انجام شد",
            }
        else:
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            message = {"error": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"}
    return message
