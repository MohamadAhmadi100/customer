from fastapi import APIRouter
from fastapi import Response, status

from customer.models.model_register import Customer
from customer.validators import validation_register

router_register = APIRouter(
    prefix="/register",
    tags=["register"]
)


@router_register.post("/")
def register(value: validation_register.CustomerRegister, response: Response):
    # TODO fixed status code
    customer = Customer(phone_number=value.customer_phone_number)
    customer.set_data(
        customer_phone_number=value.customer_phone_number,
        customer_first_name=value.customer_first_name,
        customer_last_name=value.customer_last_name,
        customer_address=value.customer_address,
        customer_city=value.customer_city,
        customer_province=value.customer_province,
        customer_province_code=value.customer_province_code,
        customer_national_id=value.customer_province_code
    )
    if customer.is_exists_phone_number() and customer.is_exists_national_id():
        response.status_code = status.HTTP_409_CONFLICT
        message = {
            "hasRegistered": True,
            "massage": "You are already registered",
            "label": "شما قبلا ثبت نام کرده اید.",
            "redirect": "login"
        }
    else:
        if customer.save():
            response.status_code = status.HTTP_201_CREATED
            # TODO crate token
            # response.headers["refreshToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
            # response.headers["accessToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
            message = {"massage": "You have registered correctly ", "label": "شما به درستی ثبت نام شدید"}
        else:
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            message = {
                "massage": "an error occurred during the registration process. Please try again ",
                "label": "خطایی در روند ثبت نام رخ داده است لطفا دوباره امتحان کنید"
            }
    return message
