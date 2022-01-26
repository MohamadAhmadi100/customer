from fastapi import APIRouter, Depends
from fastapi import Response, status

from customer.mudoles.auth import AuthHandler
from customer.validators import validation_profile

from customer.models.model_register import Customer

router_profile = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

auth_handler = AuthHandler()


@router_profile.post("/set-password/")
def set_password(
        value: validation_profile.CustomerSetPassword,
        response: Response,
        outh_header=Depends(auth_handler.check_current_user_tokens)
):
    customer = Customer(phone_number=value.customer_phone_number)
    if customer.save():
        response.status_code = status.HTTP_200_OK
        response.headers["accessToken"] = outh_header["accessToken"]
        response.headers["refreshToken"] = outh_header["refreshToken"]
        message = {"message": "ثبت نام شما با موفقیت انجام شد"}
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        message = {"massage": "ثبت نام شما با مشکل مواجه شد لطفا دوباره سعی کنید"}
    return message
