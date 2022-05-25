from faker.providers import person, phone_number
from customer.controllers import router_auth
from customer.models.model_register import Customer
from customer.modules.auth import AuthHandler
from pytest_mock import class_mocker, module_mocker, session_mocker
from customer.modules.otp import OTP
from customer.tests.helper import fixtures
from unittest import mock


# class TestOtp:
#     helper = mock.create_autospec(fixtures.mock_otp)
#
#     def test_otp_call(self, mocker):
#         self.helper.assert_not_called()
#         # otp = OTP()
#         otp = mocker.patch("customer.modules.otp").Otp
#         assert otp.get_otp(str(phone_number)) is False
#         assert otp.get_otp(str(phone_number)) is True


class TestAuthHandler:
    def test_generate_hash_password(self):
        auth = AuthHandler()
        assert type(auth.generate_hash_password("abcd")) is str

    def test_verify_password(self):
        auth = AuthHandler()
        assert auth.verify_password("abcd", "$2b$12$mkq849z85o9nmutK3uQuZ.Da/Ksjc1JX06ZEL8UQo5qIm7RSGRN6C") is True
        assert auth.verify_password("abcd", "$2b$12$mkq849z85o9nmutK3uQuZ.Da/Khjc1JX06ZEL8UQo5qIm7RSGRN6C") is False


class TestAuth:
    customer = Customer("09358270867")

    def test_check_is_registered(self, mocker: class_mocker):
        mocker.patch(
            "customer.models.model_register.Customer.is_exists_phone_number").return_value = True
        mocker.patch(
            "customer.models.model_register.Customer.is_mobile_confirm").return_value = True
        assert (router_auth.check_is_registered("09358270867")).get("message").get("hasRegistered") is True
        mocker.patch(
            "customer.models.model_register.Customer.is_exists_phone_number").return_value = False
        assert (router_auth.check_is_registered("09358270867")).get("message").get("hasRegistered") is False

    def test_verify_otp_code(self, mocker: module_mocker):
        mocker.patch("customer.controllers.router_auth").Otp.get_otp.return_value = "1111"
        mocker.patch(
            "customer.models.model_register.Customer.mobile_confirm").return_value = True
        assert (router_auth.verify_otp_cod("09358270867", "4444")).get("status_code") == 401
        assert (router_auth.verify_otp_cod("09358270867", "4444")).get("success") is False

    def test_checking_login_otp_code(self, mocker: class_mocker):
        mocker.patch(
            "customer.models.model_register.Customer.is_exists_phone_number").return_value = True
        mocker.patch("customer.modules.otp").return_value.get_otp.return_value = "1111"
        assert router_auth.checking_login_otp_code("09358270867", "555555").get("status_code") == 401

    def test_checking_login_password(self, mocker: class_mocker):
        mocker.patch(
            "customer.models.model_register.Customer.get_customer_password").return_value = {
            "customerPassword": "password", "customerIsMobileConfirm": True}
        mocker.patch(
            "customer.modules.auth.AuthHandler.verify_password").return_value.verify_password.return_value = True
        mocker.patch(
            "customer.models.model_register.Customer.get_customer").return_value.get_customer.return_value = True
        assert router_auth.checking_login_password("09358270867", "555555").get("status_code") == 202

    def test_save_logout(self, mocker: class_mocker):
        assert router_auth.save_logout(person.__dict__).get("success") is True

    def test_forget_password(self, mocker: module_mocker):
        mocker.patch(
            "customer.models.model_register.Customer.is_exists_phone_number").return_value = True
        mocker.patch(
            "customer.models.model_register.Customer.change_customer_password").return_value = True
        assert router_auth.forget_password("09358270867", "1111").get("success") is True
