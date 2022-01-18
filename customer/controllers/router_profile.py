from fastapi import APIRouter
from fastapi import Response, status
from customer.validators import validation_profile

from customer.models.model_register import Customer

router_profile = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router_profile.post("/set-password/")
def set_password(value: validation_profile.CustomerSetPassword, response: Response):
    customer = Customer(phone_number=value.customer_phone_number)
    if customer.save():
        response.status_code = status.HTTP_200_OK
        message = {"massage": "you have successfully registered", "label": "ثبت نام شما با موفقیت انجام شد"}
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        message = {"massage": "your registration failed ", "label": "ثبت نام شما با مشکل مواجه شد لطفا دوباره سعی کنید"}
    return message
