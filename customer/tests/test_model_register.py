import json
from faker.providers import person, phone_number
from unittest import mock
from customer.models.model_register import Customer
from pytest_mock import class_mocker
from customer.tests.helper import fixtures


# from starlette.testclient import TestClient
#
# client = TestClient(app)
#
#
# def test_send_otp():
#     # time.sleep(120)
#     header = {"content-Type": "application/json"}
#     url = "/send-otp/"
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "09374"})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "09374165442689"})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "93716544266"})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": 98753763})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": ""})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "test"})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": None})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "null"})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": False})
#     assert response.status_code == 422
#     assert response.json() == {"error": "Please enter a valid phone number"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "09371654426"})
#     assert response.status_code == 200
#     assert response.json() == {"massage": "sent otp", "label": "کد ثبت نام ارسال شد"}
#
#     response = client.post(url=url, headers=header, json={"phoneNumber": "09371654426"})
#     assert response.status_code == 423


# class TestCustomer(unittest.TestCase):
# @patch("connection.MongoConnection")


class TestCustomer:
    customer = Customer("09358270867")
    helper = mock.create_autospec(fixtures.mock_connection)

    def test_extra_connection(self):
        self.helper.assert_not_called()

    def test_set_activity(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "set_activity")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.set_activity() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_is_exists_phone_number(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "is_exists_phone_number")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.is_exists_phone_number() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_is_exists_national_id(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "is_exists_national_id")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.is_exists_national_id() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_login(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "login")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.login("self") is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_is_mobile_confirm(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "is_mobile_confirm")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.is_mobile_confirm() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_is_customer_confirm(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "is_customer_confirm")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.is_customer_confirm() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_mobile_confirm(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "mobile_confirm")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.mobile_confirm() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_customer_confirm(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "customer_confirm")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.customer_confirm() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_get_next_sequence_customer_id(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "get_next_sequence_customer_id")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.get_next_sequence_customer_id() is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_get_customer(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "get_customer")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = {"_id": "111"}
        with mock.patch("requests.get") as mock_request:
            url = "http://devaddr.aasood.com/address/customer_addresses?customerId="
            mock_request.return_value.content = json.dumps({"result": "foo"})
            mock_request.return_value.status_code = 200
            assert spy.spy_return is None
            assert spy.call_count == 0

    def test_get_customer_password(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "get_customer_password")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "Mocked Customer"
        mocker.patch(
            "customer.models.model_register.Customer.get_customer_password").return_value = "customer.object"
        assert self.customer.get_customer_password() == "customer.object"
        assert spy.spy_return is None
        assert spy.call_count == 0

    def test_change_customer_password(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "change_customer_password")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.change_customer_password("self.password") is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_change_default_delivery(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "change_default_delivery")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.change_default_delivery(person.__dict__) is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_add_delivery(self, mocker: class_mocker):
        spy = mocker.spy(Customer, "add_delivery")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert self.customer.add_delivery(person.__dict__) is True
        assert spy.spy_return is True
        assert spy.call_count == 1

    def test_retrieve_delivery_persons(self, mocker: class_mocker):
        customer = Customer(phone_number=str(phone_number))
        spy = mocker.spy(Customer, "retrieve_delivery_persons")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        mocker.patch(
            "customer.models.model_register.Customer.retrieve_delivery_persons").return_value = "customer.object"
        assert customer.retrieve_delivery_persons() == "customer.object"
        assert spy.spy_return is None
        assert spy.call_count == 0

    def test_retrieve_default_delivery(self, mocker: class_mocker):
        customer = Customer(phone_number=str(phone_number))
        spy = mocker.spy(Customer, "retrieve_default_delivery")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        mocker.patch(
            "customer.models.model_register.Customer.retrieve_default_delivery").return_value = "customer.object"
        assert customer.retrieve_default_delivery() == "customer.object"
        assert spy.spy_return is None
        assert spy.call_count == 0
