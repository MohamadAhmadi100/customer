import pytest


@pytest.fixture
def mock_connection(mocker):
    yield mocker.patch("customer.helper.connection.MongoConnection")


@pytest.fixture
def mock_otp(mocker):
    yield mocker.patch("customer.modules.otp.Otp.get_otp")
