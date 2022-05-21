from customer.models.model_profile import Profile


class TestProfile:
    profile = Profile({"customer_phone_number": "0"})
    helper = mock.create_autospec(fixtures.mock_connection)

