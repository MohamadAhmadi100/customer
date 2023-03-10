from customer.helper.connection import MongoConnection
from config import VALID_GRID_KEYS

ACCOUNTING_VALID_GRID_KEYS = ["customerFirstName", "customerLastName", "customerJalaliConfirmDate",
                              "customerSelCustomerCode", "customerType", "customerStatus", "customerIsActive"]


class GetData:
    def __int__(self):
        ...

    @staticmethod
    def handle_sort(sort_type):
        return -1 if sort_type == "desc" else 1

    def executor(self, queries: dict, number_of_records: str = "15", page: str = "1", sort_name: str = "customerID",
                 sort_type: str = "asc", search_query=None, api_type="main"):
        if search_query is None:
            search_query = {}
        sort_type = self.handle_sort(sort_type)
        with MongoConnection() as mongo:
            try:
                customers = list(mongo.customer.find(
                    queries, {"_id": False}).limit(int(number_of_records)).skip(
                    int(number_of_records) * (int(page) - 1)).sort(sort_name,
                                                                   sort_type))
                # total_count = len(list(mongo.customer.find(queries, {"_id": False})))
                total_count = mongo.customer.count_documents(queries)
                result = []
                for customer in customers:
                    if api_type == "accounting":
                        record = {grid_attribute: customer.get(grid_attribute) for grid_attribute in
                                  ACCOUNTING_VALID_GRID_KEYS}
                    else:
                        record = {grid_attribute: customer.get(grid_attribute) for grid_attribute in VALID_GRID_KEYS}
                    record["customerMobileNumber"] = customer.get("customerPhoneNumber")
                    if type(customer.get("customerTypes")) == list and len(customer.get("customerTypes")):
                        new_type = []
                        for t in customer.get("customerTypes"):
                            if t == "B2B":
                                new_type.append("????????")
                            elif t == "B2B2C":
                                new_type.append("??????????????")
                            elif t == "B2C":
                                new_type.append("??????????????")
                        record["customerTypes"] = new_type
                    record["customerStateName"] = customer.get("customerStateName")
                    record["customerCityName"] = customer.get("customerCityName")
                    record["customerRegionCode"] = customer.get("customerRegionCode")

                    if customer.get("customerAddress") and type(customer.get("customerAddress")) == list and type(
                            customer.get("customerAddress")[0]) == dict:
                        if not record["customerStateName"]:
                            record["customerStateName"] = customer.get("customerAddress")[0].get("customerStateName")
                        if not record["customerCityName"]:
                            record["customerCityName"] = customer.get("customerAddress")[0].get("customerCityName")
                        if not record["customerRegionCode"]:
                            record["customerRegionCode"] = customer.get("customerAddress")[0].get("customerRegionCode")
                    result.append(record)
                data = {
                    "data": result,
                    "totalCount": total_count,
                }
                return {"success": True, "message": data, "status_code": 200}
            except Exception as e:
                return {"success": False, "error": e, "status_code": 404}
