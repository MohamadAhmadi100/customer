import time

from starlette.testclient import TestClient

from customer.main import app

client = TestClient(app)


def test_send_otp():
    # time.sleep(120)
    header = {"content-Type": "application/json"}
    url = "/send-otp/"

    response = client.post(url=url, headers=header, json={"phoneNumber": "09374"})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "09374165442689"})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "93716544266"})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": 98753763})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": ""})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "test"})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": None})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "null"})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": False})
    assert response.status_code == 422
    assert response.json() == {"error": "Please enter a valid phone number"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "09371654426"})
    assert response.status_code == 200
    assert response.json() == {"massage": "sent otp", "label": "کد ثبت نام ارسال شد"}

    response = client.post(url=url, headers=header, json={"phoneNumber": "09371654426"})
    assert response.status_code == 423
