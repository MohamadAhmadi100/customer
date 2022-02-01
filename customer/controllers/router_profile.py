from fastapi import APIRouter, Depends
from fastapi import Response, status

from customer.models.model_register import Customer
from customer.models.model_register import Customer
from customer.mudoles.auth import AuthHandler
from customer.validators import validation_profile, validation_auth

router_profile = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

auth_handler = AuthHandler()

@router_profile.get("/")
def get_profile(
        response: Response,
        auth_header=Depends(auth_handler.check_current_user_tokens),


):
    user,header = auth_header
    return user


@router_profile.put("/edit-data")
def edit_profile_data(
        response: Response,
        auth_header=Depends(auth_handler.check_current_user_tokens),
):

    pass

@router_profile.post("/set-password/")
def set_password(
        value: validation_profile.CustomerSetPassword,
        response: Response,
        auth_header=Depends(auth_handler.check_current_user_tokens)
):
    customer = Customer(phone_number=value.customer_phone_number)
    if customer.save():
        response.status_code = status.HTTP_200_OK
        response.headers["accessToken"] = auth_header["access_token"]
        response.headers["refreshToken"] = auth_header["refresh_token"]
        message = {"message": "رمز عبور با موفقیت تغییر کرد"}
    else:
        response.status_code = status.HTTP_417_EXPECTATION_FAILED
        message = {"massage": "تغییر رمز عبور با مشکل مواجه شد لطفا دوباره سعی کنید"}
    return message
>>>>>>> Stashed changes
