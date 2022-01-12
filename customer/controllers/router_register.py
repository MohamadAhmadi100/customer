from fastapi import APIRouter
from fastapi import Response, status

from customer.models.model_register import CustomerB2C
from customer.mudoles.otp import OTP
from customer.validators import validation_register

router_register = APIRouter(
    prefix="/register",
    tags=["register"],
    responses={404: {"error": "Not found"}},
)


@router_register.post("/send-otp/")
async def root(value: validation_register.CustomerSchemas, response: Response):
    # TODO fixed status code

    customer = CustomerB2C(phone_number=value.phone_number)
    if not customer.is_exists():
        otp = OTP(value.phone_number)
        is_expire, expire_time = otp.is_expire_otp_time()
        if is_expire:
            otp.set_otp_code_length(3)
            otp.generate_code()
            otp.save_otp()
            otp.send_otp_code()
            response.status_code = status.HTTP_200_OK
            massage = {
                "massage": "sent otp",
                "label": "کد ثبت نام ارسال شد"
            }
        else:
            response.status_code = status.HTTP_423_LOCKED
            massage = {
                "massage": f" Try after {expire_time} seconds",
                "label": f"  لطفا بعد از {expire_time} ثانیه تلاش کنید ",  # TODO check label
            }
    else:
        response.status_code = status.HTTP_409_CONFLICT
        massage = {
            "massage": "You are already registered",
            "label": "شما قبلا ثبت نام کرده اید."
        }
    return massage


@router_register.post("/verify-otp/")
def root(value: validation_register.CustomerVerify, response: Response):
    # TODO fixed status code

    otp = OTP(value.phone_number)
    if otp.get_otp() and otp.get_otp(value.phone_number).get("code") == value.otp_code:
        response.status_code = status.HTTP_201_CREATED
        message = {"massage": "otp code is valid"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        message = {"massage": "otp code is wrong"}
    return message


@router_register.post("/set-password/")
def root(value: validation_register.CustomerSetPassword, response: Response):
    customer = CustomerB2C(phone_number=value.phone_number)
    result = customer.save()

    if result:
        response.status_code = status.HTTP_201_CREATED
        message = {"massage": "you have successfully registered"}
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        message = {"massage": "You did not register"}

    return message
