from fastapi import APIRouter

from customer.models.model_register import Customer
from customer.mudoles.otp import OTP
from fastapi import Response, status

from customer.validators import validation_auth

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router_auth.get("/")
def check_is_registered():
    form = validation_auth.CustomerAuth.schema().get("properties").copy()
    return form


@router_auth.post("/")
def check_is_registered(value: validation_auth.CustomerAuth, response: Response):
    # TODO fixed status code
    customer = Customer(phone_number=value.customer_phone_number)

    if customer.is_exists_phone_number():
        redirect = "/auth/login/" if customer.is_mobile_confirm() else "/auth/verify-otp/"
        response.status_code = status.HTTP_202_ACCEPTED
        message = {
            "costumerIsMobileConfirm": customer.is_mobile_confirm(),
            "costumerIsConfirm": customer.is_customer_confirm(),
            "hasRegistered": True,
            "massage": "You are already registered",
            "label": "شما قبلا ثبت نام کرده اید.",
            "redirect": redirect
        }
    else:
        response.status_code = status.HTTP_200_OK
        message = {
            "hasRegistered": False,
            "massage": "You are not registered yet",
            "label": "شما قبلا ثبت نام نکرده اید",
            "redirect": "/register/"
        }
    return message


@router_auth.post("/send-otp/")
def send_otp(value: validation_auth.CustomerAuth, response: Response):
    otp = OTP(value.customer_phone_number)

    is_expire, expire_time = otp.is_expire_otp_time()
    if is_expire:
        otp.generate_code(otp_code_length=4)
        otp.save()
        otp.send()
        response.status_code = status.HTTP_200_OK
        message = {"massage": "send OTP code", "label": "کد OTP ارسال شد"}
    else:
        response.status_code = status.HTTP_423_LOCKED
        message = {
            "massage": f" try after {expire_time} seconds",
            "label": f"  لطفا بعد از {expire_time} ثانیه تلاش کنید ",
        }
    return message


@router_auth.post("/verify-otp/")
def register(value: validation_auth.CustomerVerifyOTP, response: Response):
    # TODO fixed status code
    otp = OTP(value.customer_phone_number)
    if otp.get_otp() and otp.get_otp() == value.customer_code:
        customer = Customer(phone_number=value.customer_phone_number)
        if customer.mobile_confirm():
            response.status_code = status.HTTP_201_CREATED
            message = {"massage": "otp code is valid", "label": "کد وارد شده صحیح است"}
        else:
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            message = {"massage": "sorry try again later", "label": "مشکلی رخ داده است لطفا بعدا امتحان کنید"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        message = {"massage": "otp code is wrong", "label": "کد وارد شده صحیح نمی‌باشد"}
    return message


@router_auth.get("/login/otp/")
def login_otp():
    form = validation_auth.CustomerVerifyOTP.schema().get("properties").copy()
    return form


@router_auth.post("/login/otp/")
def login_otp(value: validation_auth.CustomerVerifyOTP, response: Response):
    # TODO fixed status code

    customer = Customer(phone_number=value.customer_phone_number)
    otp = OTP(value.customer_phone_number)
    if customer.is_exists_phone_number():
        if otp.get_otp() and otp.get_otp(value.customer_phone_number) == value.customer_code:
            response.status_code = status.HTTP_200_OK
            response.headers["refreshToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
            response.headers["accessToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
            # TODO create token
            message = {"massage": "you are successfully login", "label": "شما به درستی وارد شدید"}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            message = {"massage": "the otp code is incorrect", "label": "کد وارد شده صحیح نمی‌باشد"}
    else:
        response.status_code = status.HTTP_200_OK
        message = {
            "hasRegistered": False,
            "massage": "you have not registered before",
            "label": "شما قبلا ثبت نام نکرده اید",
            "redirect": "/register/"
        }
    return message


@router_auth.get("/login/password/")
def login_otp():
    form = validation_auth.CustomerVerifyPassword.schema().get("properties").copy()
    return form


@router_auth.post("/login/password/")
def login_password(value: validation_auth.CustomerVerifyPassword, response: Response):
    # TODO fixed status code
    customer = Customer(phone_number=value.customer_phone_number)

    if customer.is_exists_phone_number():
        if customer.is_login(value.customer_password):
            if customer.mobile_confirm():
                response.status_code = status.HTTP_200_OK
                response.headers["refreshToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
                response.headers["accessToken"] = "OLFGM&#$DSWFVI(%#@WEDSDFJKLKIULfrdg$$"
                # TODO create token
                message = {"massage": "you are successfully login", "label": "شما به درستی وارد شدید"}
            else:
                response.status_code = status.HTTP_202_ACCEPTED
                message = {
                    "costumerIsMobileConfirm": customer.is_mobile_confirm(),
                    "costumerIsConfirm": customer.is_customer_confirm(),
                    "hasRegistered": True,
                    "massage": "your account has not been verified",
                    "label": "شماره موبایل شما تایید نشده است",
                }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            message = {"massage": "password is incorrect", "label": "پسورد اشتباه است"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        message = {
            "hasRegistered": False,
            "massage": "you are not registered yet",
            "label": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
    return message
