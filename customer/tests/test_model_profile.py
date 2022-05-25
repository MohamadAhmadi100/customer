from unittest import mock
from pytest_mock import class_mocker
from customer.tests.helper import fixtures
from customer.models.model_profile import Profile


class TestProfile:
    profile = Profile({"customer_phone_number": "0"})
    helper = mock.create_autospec(fixtures.mock_connection)

    def test_extra_connection(self):
        self.helper.assert_not_called()

    def test_get_profile_data(self, mocker: class_mocker):
        spy = mocker.spy(Profile, "get_profile_data")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert type(self.profile.get_profile_data()) is dict
        assert type(spy.spy_return) is dict
        assert spy.call_count == 1

    def test_create_obj_to_update_profile(self, mocker: class_mocker):
        spy = mocker.spy(Profile, "create_obj_to_update_profile")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert type(self.profile.create_obj_to_update_profile()) is dict
        assert type(spy.spy_return) is dict
        assert spy.call_count == 1

    def test_update_profile(self, mocker: class_mocker):
        spy = mocker.spy(Profile, "create_obj_to_update_profile")
        mocker.patch(
            "customer.helper.connection.MongoConnection.__enter__").return_value.__enter__.return_value = "self"
        assert type(self.profile.create_obj_to_update_profile()) is dict
        assert type(spy.spy_return) is dict
        assert spy.call_count == 1
