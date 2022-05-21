import pytest


@pytest.fixture
def mock_connection(mocker):
    yield mocker.patch("customer.helper.connection.MongoConnection")
