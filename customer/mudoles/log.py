import time

from customer.helper.connection import MongoConnection


def save_login_log(customer_id: str) -> bool:
    pipe_line = {
        "customerID": customer_id,
        "customerAction": "logout",
        "customerActionTime": time.time()
    }
    with MongoConnection() as mongo:
        result = mongo.log.insert_one(pipe_line)
    return True if result.acknowledged else False


def save_logout_log(customer_id: str) -> bool:
    with MongoConnection() as mongo:
        result: object = mongo.log.find({"customerID": customer_id}, {'_id': 0}).limit(1).sort("customerCrateTime", -1)

        # TODO handel index error
        login_time = result[0].get("customerActionTime")

    pipe_line = {
            "customerID": customer_id,
            "customerAction": "login",
            "customerActionTime": time.time(),
            "customerStayRateTime": time.time() - login_time
    }
    with MongoConnection() as mongo:
        result = mongo.log.insert_one(pipe_line)
    return True if result.acknowledged else False


