import json

from fastapi import Response, Depends
from fastapi import status, APIRouter

from customer.models.model_register import Customer
from customer.mudoles.auth import AuthHandler
from customer.mudoles.otp import OTP
from customer.validators import validation_auth

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

auth_handler = AuthHandler()


# generate and send mobile number validations to front side

@router_auth.get("/")
def mobile_number_validation_generator():
    form = validation_auth.CustomerAuth.schema().get("properties").copy()
    return form


# mobile number generator and validation
@router_auth.post("/")
def check_is_registered(
        response: Response,
        value: validation_auth.CustomerAuth
):
    # TODO fixed status code
    # checking is exist mobile number in db
    customer = Customer(phone_number=value.customer_phone_number)
    if customer.is_exists_phone_number():
        redirect = "login" if customer.is_mobile_confirm() else "loginOtp"
        response.status_code = status.HTTP_202_ACCEPTED
        message = {
            "customerIsMobileConfirm": customer.is_mobile_confirm(),
            "hasRegistered": True,
            "massage": "شما قبلا ثبت نام کرده اید.",
            "redirect": redirect
        }
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        message = {
            "hasRegistered": False,
            "massage": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
    return message


@router_auth.post("/send-otp/")
def send_otp_code(value: validation_auth.CustomerAuth, response: Response):
    otp = OTP(value.customer_phone_number)

    is_expire, expire_time = otp.is_expire_otp_time()
    if is_expire:
        otp.generate_code(otp_code_length=4)
        otp.save()
        otp.send()
        response.status_code = status.HTTP_202_ACCEPTED
        message = {"massage": "کد OTP ارسال شد"}
    else:
        response.status_code = status.HTTP_423_LOCKED
        message = {
            "message": f"  لطفا بعد از {expire_time} ثانیه تلاش کنید ",
        }
    return message


@router_auth.post("/verify-otp/")
def verify_otp_cod(value: validation_auth.CustomerVerifyOTP, response: Response):
    # TODO fixed status code
    otp = OTP(value.customer_phone_number)
    if otp.get_otp() and otp.get_otp() == value.customer_code:
        customer = Customer(phone_number=value.customer_phone_number)
        if customer.mobile_confirm():
            response.status_code = status.HTTP_202_ACCEPTED
            message = {"massage": "کد وارد شده صحیح است"}
        else:
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            message = {"error": "مشکلی رخ داده است لطفا بعدا امتحان کنید"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        message = {"error": "کد وارد شده صحیح نمی‌باشد"}
    return message


@router_auth.get("/login/otp/")
def otp_form_generator():
    form = validation_auth.CustomerVerifyOTP.schema().get("properties").copy()
    return {"fields": form}


@router_auth.post("/login/otp/")
def checking_login_otp_code(
        value: validation_auth.CustomerVerifyOTP,
        response: Response,
):
    customer = Customer(phone_number=value.customer_phone_number)
    otp = OTP(value.customer_phone_number)
    if customer.is_exists_phone_number():
        if otp.get_otp() and otp.get_otp(value.customer_phone_number) == value.customer_code:
            response.status_code = status.HTTP_200_OK
            response.headers["refreshToken"] = auth_handler.encode_refresh_token(user_name=value.customer_phone_number)
            response.headers["accessToken"] = auth_handler.encode_access_token(user_name=value.customer_phone_number)

            message = {
                "massage": "شما به درستی وارد شدید",
                "data": customer.get_customer()
            }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            message = {"error": "کد وارد شده صحیح نمی‌باشد"}
    else:
        response.status_code = status.HTTP_200_OK
        message = {
            "hasRegistered": False,
            "massage": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
    return message


@router_auth.get("/login/password/")
def otp_form_generator():
    form = validation_auth.CustomerVerifyPassword.schema().get("properties").copy()
    return {"fields": json.dumps(form)}


@router_auth.post("/login/password/")
def checking_login_password(
        value: validation_auth.CustomerVerifyPassword,
        response: Response,
):
    # TODO fixed status code
    customer = Customer(phone_number=value.customer_phone_number)
    if customer.is_exists_phone_number():
        if customer.is_login(value.customer_password):
            if customer.mobile_confirm():

                response.status_code = status.HTTP_200_OK
                response.headers["refreshToken"] = auth_handler.encode_refresh_token(
                    user_name=value.customer_phone_number
                )
                response.headers["accessToken"] = auth_handler.encode_access_token(
                    user_name=value.customer_phone_number
                )
                message = {
                    "massage": "شما به درستی وارد شدید",
                    "data": customer.get_customer()

                }
            else:
                response.status_code = status.HTTP_202_ACCEPTED
                message = {
                    "customerIsMobileConfirm": customer.is_mobile_confirm(),
                    "customerIsConfirm": customer.is_customer_confirm(),
                    "hasRegistered": True,
                    "massage": "شماره موبایل شما تایید نشده است",
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            message = {"error": "پسورد اشتباه است"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        message = {
            "hasRegistered": False,
            "error": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
    return message


@router_auth.post("/check-token/")
def check_token(
        response: Response,
        auth_header=Depends(auth_handler.check_current_user_tokens)
):
    response.status_code = status.HTTP_202_ACCEPTED
    username, token_dict = auth_header

    response.headers["accessToken"] = token_dict.get("access_token")
    response.headers["refreshToken"] = token_dict.get("refresh_token")
    customer = Customer(username)
    return {"data": customer.get_customer()}
