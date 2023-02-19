VALID_PERIOD_FILTERS = ["customerJalaliCreateTime", "customerJalaliConfirmDate"]
VALID_VALUE_FILTERS = ["customerStatus", "customerStateName", "customerCityName", "customerRegionCode", "customerType",
                       "customerTypes", "customerIsActive", "customerActiveCredit"]
VALID_SEARCH_FIELDS = ["customerFirstName", "customerLastName", "customerPhoneNumber", "customerNationalID"]
VALID_NULL_FIELDS = ["customerSelCustomerCode"]


class Filter:
    def __init__(self):
        self.valid_period_filters: list = VALID_PERIOD_FILTERS or []
        self.valid_value_filters: list = VALID_VALUE_FILTERS or []
        self.valid_search_fields: list = VALID_SEARCH_FIELDS or []
        self.valid_null_filters: list = VALID_NULL_FIELDS or []
        self.period_filters: dict = {}
        self.value_filters: dict = {}
        self.null_filters: dict = {}

    def set_period_filters(self, periods: dict) -> dict:
        self.period_filters = {filter_: value for filter_, value in periods.items() if
                               filter_ in self.valid_period_filters and value and type(value) == dict}
        period = {}
        for filter_, value in self.period_filters.items():
            if value.get("start") and value.get("end"):
                value["$gt"] = value.get("start")
                value["$lt"] = value.get("end")
                del value["start"]
                del value["end"]
                period[filter_] = value
        return period

    def set_value_filters(self, values: dict) -> dict:
        self.value_filters = {}
        for filter_, value in values.items():
            if filter_ in self.valid_value_filters and (value or value is False or value == 0):
                # todo: return comment!
                if type(value) == list:
                    self.value_filters[filter_] = {"$in": value}
                elif filter_ == "customerStateName":
                    self.value_filters["customerAddress.customerStateName"] = value
                elif filter_ == "customerCityName":
                    self.value_filters["customerAddress.customerCityName"] = value
                elif filter_ == "customerRegionCode":
                    self.value_filters["customerAddress.customerRegionCode"] = value
                else:
                    self.value_filters[filter_] = value
        return self.value_filters

    def set_null_filters(self, values: dict) -> dict:
        self.null_filters = {}
        for filter_, value in values.items():
            if filter_ in self.valid_null_filters and value:
                self.null_filters[filter_] = {"$ne": None}
            if filter_ in self.valid_null_filters and value is False:
                self.null_filters[filter_] = None
        return self.null_filters

    def set_search_query(self, search_phrase):
        search_list = [{search_field: {"$regex": search_phrase}} for search_field in self.valid_search_fields]
        return {"$or": search_list} if search_list else {}
