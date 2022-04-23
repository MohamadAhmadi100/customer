from customer.helper.connection import MongoConnection


class GetData:
    def __int__(self):
        ...

    def set_query_parameters(self, queries):
        ...

    @staticmethod
    def data(queries: dict, number_of_records: str = 15, page: str = 1, sort_name: str = "name",
             sort_type: str = "desc"):
        with MongoConnection() as mongo:
            try:
                customers = list(mongo.customer.find(
                    queries, {"_id": False}).limit(int(number_of_records)).skip(
                    int(number_of_records) * (int(page) - 1)).sort(sort_name,
                                                                   sort_type))
                total_count = mongo.customer.find(
                    queries, {"_id": False}).limit(int(number_of_records)).skip(
                    int(number_of_records) * (int(page) - 1)).sort(sort_name,
                                                                   sort_type).count_documents()
                last_data = {
                    "data": customers,
                    "totalCount": total_count,
                }
                # return {"success": True, "message": last_data, "status_code": 200}
                return {"data": last_data}
            except Exception as e:
                return {"success": False, "error": "مشکل در اتصال به سرور", "status_code": 500}
        return False
