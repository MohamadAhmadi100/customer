import datetime

import requests

from customer.helper.connection import MongoConnection


def nid_phone_verify(phone_number, nid):
    # with MongoConnection() as mongo:
    #     db_result = mongo.shahkar.find_one({"phone_number": phone_number, "nid": nid}, {"_id": 0})
    #     if db_result:
    #         return db_result.get("result")
        shahkar_result = shahkar_verify(phone_number, nid)
        # mongo.shahkar.insert_one({"phone_number": phone_number, "nid": nid, "result": shahkar_result})
        return shahkar_result


def shahkar_verify(phone_number, nid):
    try:
        get_token_response = requests.request(
            "POST",
            "https://op1.pgsb.ir/oauth/token",
            headers={
                'Authorization': 'Basic ODNiMTk3NjBlN2JjNDQzN2I2ZjIxNWE3M2VlN2E1ZTU6VEhsSWJiZG5acWt1TmFYYQ==',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data='grant_type=password&username=zarrinco&password=ByZr6f5q6Q'
        )
        print(get_token_response)


        access_token = get_token_response.json().get("access_token")

        data_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-2]

        shahkar_response = requests.request(
            "POST",
            "https://op1.pgsb.ir/api/client/apim/v1/shahkaar/gwsh/serviceIDmatching",
            headers={
                'pid': '634d040f9c33600fa3411728',
                'Authorization': f'Bearer {access_token}',
                'basicAuthorization': 'Basic SG9zaG1hbmRfemFyaW5fcGdzYjpDalhhMDRTRTElNVA=',
                'Content-Type': 'application/json',
            },
            json={
                "serviceType": "2",
                "identificationType": "0",
                "identificationNo": nid,
                "requestId": f"1076{data_time}01",
                "serviceNumber": phone_number
            })
        print(shahkar_response)
        return True if shahkar_response.json().get("result", {}).get("data", {}).get("result", {}).get("data", {}).get(
            "result") == "OK." else False
    except:
        return None


# script for all customers
# with MongoConnection() as mongo:
#     all_customers = list(
#         mongo.customer.find({}, {"_id": 0, "customerID": 1, "customerNationalID": 1,
#                                  "customerPhoneNumber": 1}))

# verified = []
# rejected = []
# unknown = []

# for customer in all_customers:
# shahkar_result = nid_phone_verify("09358270867", "4610298899")
# if shahkar_result:
#     verified.append(customer)
# elif shahkar_result is None:
#     unknown.append(customer)
# else:
#     rejected.append(customer)

# print("verified: ", verified)
# print("rejected: ", rejected)
# print("unknown: ", unknown)
