import json

from customer.models.model_register import Customer
from customer.modules.otp import OTP
from customer.modules import log


# mobile number generator and validation
def check_is_registered(
        customer_phone_number: str
):
    # TODO fixed status code
    # checking is exist mobile number in db
    customer = Customer(phone_number=customer_phone_number)
    if customer.is_exists_phone_number():
        redirect = "login" if customer.is_mobile_confirm() else "loginOtp"
        status_code = 308
        message = {
            "customerIsMobileConfirm": customer.is_mobile_confirm(),
            "hasRegistered": True,
            "massage": "شما قبلا ثبت نام کرده اید.",
            "redirect": redirect
        }
    else:
        status_code = 308
        message = {
            "hasRegistered": False,
            "massage": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
    return {"success": True, "status_code": status_code, "message": message}


def send_otp_code(customer_phone_number: str):
    otp = OTP(customer_phone_number)

    is_expire, expire_time = otp.is_expire_otp_time()
    if is_expire:
        otp.generate_code(otp_code_length=4)
        otp.save()
        otp.send()
        return {"success": True, "status_code": 202, "message": {"massage": "کد OTP ارسال شد"}}
    else:
        message = {
            "message": f"  لطفا بعد از {expire_time} ثانیه تلاش کنید ",
        }
        return {"success": False, "status_code": 406, "message": message}


def verify_otp_cod(customer_phone_number: str, customer_code: str):
    # TODO fixed status code
    otp = OTP(customer_phone_number)
    if otp.get_otp() and otp.get_otp() == customer_code:
        customer = Customer(phone_number=customer_phone_number)
        if customer.mobile_confirm():
            message = {"massage": "کد وارد شده صحیح است"}
            return {"success": True, "status_code": 202, "message": message}
        else:
            message = {"error": "مشکلی رخ داده است لطفا بعدا امتحان کنید"}
            return {"success": False, "status_code": 417, "message": message}
    else:
        message = {"error": "کد وارد شده صحیح نمی‌باشد"}
        return {"success": False, "status_code": 401, "message": message}


def checking_login_otp_code(
        customer_phone_number: str, customer_code: str
):
    customer = Customer(phone_number=customer_phone_number)
    otp = OTP(customer_phone_number)
    if customer.is_exists_phone_number():
        if otp.get_otp() and otp.get_otp(customer_phone_number) == customer_code:
            log.save_login_log(customer_phone_number)
            message = {
                "massage": "شما به درستی وارد شدید",
                "data": customer.get_customer()
            }
            return {"success": True, "status_code": 202, "message": message}
        else:
            return {"success": False, "status_code": 401, "error": "کد وارد شده صحیح نمی‌باشد"}
    else:
        message = {
            "hasRegistered": False,
            "massage": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
        return {"success": False, "status_code": 308, "message": message}


def checking_login_password(
        customer_phone_number: str, customer_password: str
):
    # TODO fixed status code
    customer = Customer(phone_number=customer_phone_number)
    if customer.is_exists_phone_number():
        if customer.is_login(customer_password):
            if customer.mobile_confirm():
                log.save_login_log(customer_phone_number)
                message = {
                    "massage": "شما به درستی وارد شدید",
                    "data": customer.get_customer()
                }
                return {"success": True, "status_code": 202, "message": message}
            else:
                message = {
                    "customerIsMobileConfirm": customer.is_mobile_confirm(),
                    "customerIsConfirm": customer.is_customer_confirm(),
                    "hasRegistered": True,
                    "massage": "شماره موبایل شما تایید نشده است",
                }
                return {"success": False, "status_code": 406, "message": message}
        else:
            message = {"error": "پسورد اشتباه است"}
            return {"success": False, "status_code": 401, "message": message}
    else:
        message = {
            "hasRegistered": False,
            "error": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
        return {"success": False, "status_code": 401, "message": message}


def save_logout(
        username: str
):
    result = log.save_logout_log(username)
    if result:
        # redirect to home page
        return {"success": True, "status_code": 202, "message": {"massage": "خروج انجام شد"}}
    else:
        return {"success": False, "status_code": 417, "message": {"massage": "خطایی رخ داده است"}}

