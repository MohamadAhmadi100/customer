from config import config


class Filter:
    def __init__(self):
        self.valid_period_filters: list = config.VALID_PERIOD_FILTERS or []
        self.valid_value_filters: list = config.VALID_VALUE_FILTERS or []
        self.valid_search_fields: list = config.VALID_SEARCH_FIELDS or []
        self.period_filters: dict = {}
        self.value_filters: dict = {}

    def set_period_filters(self, periods: dict) -> dict:
        self.period_filters = {filter_: value for filter_, value in periods.items() if
                               filter_ in self.valid_period_filters and value and type(value) == dict}
        for filter_, value in self.period_filters.items():
            if value.get("start") and value.get("end"):
                value["$gt"] = value.get("start")
                value["$lt"] = value.get("end")
                del value["start"]
                del value["end"]
        return self.period_filters

    def set_value_filters(self, values: dict) -> dict:
        self.value_filters = {filter_: value for filter_, value in values.items() if
                              filter_ in self.valid_value_filters and value}
        return self.value_filters

    def set_search_query(self, search_phrase):
        return {search_field: {"$regex": search_phrase} for search_field in list(self.valid_search_fields) if
                len(list(self.valid_search_fields))} or {}
