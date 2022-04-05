from customer.models.model_register import Customer
from customer.models.model_profile import Profile


# def get_profile(customer_phone_number: dict):
#     customer_phone_number = customer_phone_number.get('phone_number')
#     profile = Profile({"customer_phone_number": customer_phone_number})
#     result = profile.get_profile_data()
#     if result:
#         return {"success": True, "message": result, "status_code": 200}
#     return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 401}

# def edit_profile_data(
#         response: Response,
#         value: validation_profile.EditProfile,
#         auth_header=Depends(auth_handler.check_current_user_tokens),
#
# ):
#     customer_phone_number, header = auth_header
#     if customer_phone_number:
#         profile = Profile(customer_phone_number)
#         result = profile.update_profile(value)
#         response.status_code = status.HTTP_200_OK
#         response.headers["accessToken"] = header.get("access_token")
#         response.headers["refresh_token"] = header.get("refresh_token")
#         return result
#     response.status_code = status.HTTP_404_NOT_FOUND
#     message = {"message": "اطلاعاتی برای کاربر مورد نظر وجود ندارد"}
#     message = {"message": "اطلاعاتی برای کاربر مورد نظر وجود ندارد"}
#     return message
#
#
# def change_customer_password(
#         response: Response,
#         data: validation_profile.ChangePassword,
#         auth_header=Depends(auth_handler.check_current_user_tokens),
# ):
#     response.status_code = status.HTTP_202_ACCEPTED
#     phone_number, token_dict = auth_header
#     customer = Customer(phone_number)
#     profile = Profile(customer)
#     result = profile.change_password(data)
#     if result:
#         response.status_code = status.HTTP_200_OK
#         response.headers["accessToken"] = token_dict.get("access_token")
#         response.headers["refresh_token"] = token_dict.get("refresh_token")
#         message = {
#             "message": "رمز عبور با موفقیت بروز شد",
#         }
#         return message
#     response.status_code = status.HTTP_406_NOT_ACCEPTABLE
#     response.headers["accessToken"] = token_dict.get("access_token")
#     response.headers["refresh_token"] = token_dict.get("refresh_token")
#     message = {
#         "message": "رمز وارد شده صحیح نمی باشد",
#     }
#     return message
