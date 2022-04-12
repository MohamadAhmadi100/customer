from config import config


class Filter:
    def __init__(self):
        self.valid_period_filters: list = config.VALID_PERIOD_FILTERS or []
        self.valid_value_filters: list = config.VALID_VALUE_FILTERS or []
        self.period_filters: dict = {}
        self.value_filters: dict = {}

    def set_period_filters(self, periods: dict) -> dict:
        self.period_filters = {filter_: value for filter_, value in periods.items() if
                               filter_ in self.valid_period_filters and value and type(value) == dict}
        for filter_, value in self.period_filters.items():
            if value.get("start") and value.get("end"):
                value["$gte"] = value.get("start")
                value["$lt"] = value.get("end")
                del value["start"]
                del value["end"]
        return self.period_filters

    def set_value_filters(self, values: dict) -> dict:
        self.value_filters = {filter_: value for filter_, value in values.items() if
                              filter_ in self.valid_value_filters and value and type(value) != dict}
        return self.value_filters


a = Filter()
print(a.set_period_filters({
    "registerDate": {"start": "1401-01-16 11:25:00", "end": "1401-01-18 23:25:00"},
    "lastOrderDate": {"start": "1401-01-17 11:25:00", "end": "1401-01-18 23:25:00"},
    "customerID": 12}))
