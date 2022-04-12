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
    return bool(result.acknowledged)


def save_logout_log(customer_id: str) -> bool:
    with MongoConnection() as mongo:
        result: list = list(
            mongo.log.find({"customerID": customer_id}, {'_id': 0}).limit(1).sort("customerCreateTime", -1))
        login_time = time.time()
        if len(result):
            try:
                login_time = result[0].get("customerActionTime")
            except IndexError:
                ...

    pipe_line = {
        "customerID": customer_id,
        "customerAction": "login",
        "customerActionTime": time.time(),
        "customerStayRateTime": time.time() - login_time
    }
    with MongoConnection() as mongo:
        result = mongo.log.insert_one(pipe_line)
    return bool(result.acknowledged)
