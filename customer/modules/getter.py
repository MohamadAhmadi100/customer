from customer.helper.connection import MongoConnection


class GetData:
    def __int__(self):
        ...

    @staticmethod
    def handle_sort(sort_type):
        return -1 if sort_type == "desc" else 1

    def executor(self, queries: dict, number_of_records: str = "15", page: str = "1", sort_name: str = "customerID",
                 sort_type: str = "asc", search_query=None):
        if search_query is None:
            search_query = {}
        print(number_of_records, page, sort_type, sort_name)
        sort_type = self.handle_sort(sort_type)
        with MongoConnection() as mongo:
            try:
                customers = list(mongo.customer.find(
                    queries, {"_id": False}).limit(int(number_of_records)).skip(
                    int(number_of_records) * (int(page) - 1)).sort(sort_name,
                                                                   sort_type))
                total_count = mongo.customer.count_documents(queries)
                data = {
                    "data": customers,
                    "totalCount": total_count,
                }
                return {"success": True, "message": data, "status_code": 200}
            except Exception as e:
                return {"success": False, "error": e, "status_code": 404}
