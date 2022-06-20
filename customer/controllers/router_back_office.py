import json
import jdatetime
from config import VALID_GRID_KEYS, VALID_PROFILE_KEYS
from customer.modules.getter import GetData
from customer.modules.setter import Filter
from customer.models.model_register import Customer
from customer.models.model_profile import Profile


def get_customers_data():
    response = {
        "totalDataCount": 17,
        "sortable": ["customerID", "customerLastName", "customerCreateTime", "totalOrdersPrice", "lastOrderDate"],
        "data": [
            {
                "customerID": {
                    "value": 0,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "علی",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "عباسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09122546858",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1401-01-17 11:25:00",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },

                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1401-01-17 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 25,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 125000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2022/08/15/ali054.png",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["tehran", "special"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "13",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "اصفهان",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "اصفهان",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "031",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": "boolean"
                },
                "customerProvinceID": {
                    "value": "031",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4648574458",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4582",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "56852",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 0,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "علی",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "عباسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09122546858",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1401-01-17 11:25:00",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },

                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1401-01-17 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 25,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 125000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2022/08/15/ali054.png",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["tehran", "special"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "13",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "اصفهان",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "اصفهان",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "031",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": "boolean"
                },
                "customerProvinceID": {
                    "value": "031",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4648574458",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4582",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "56852",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 0,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "علی",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "عباسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09122546858",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1401-01-17 11:25:00",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },

                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1401-01-17 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 25,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 125000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2022/08/15/ali054.png",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["tehran", "special"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "13",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "اصفهان",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "اصفهان",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "031",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": "boolean"
                },
                "customerProvinceID": {
                    "value": "031",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4648574458",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4582",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "56852",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 0,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "علی",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "عباسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09122546858",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1401-01-17 11:25:00",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },

                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1401-01-17 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 25,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 125000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2022/08/15/ali054.png",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["tehran", "special"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "13",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "اصفهان",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "اصفهان",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "031",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": "boolean"
                },
                "customerProvinceID": {
                    "value": "031",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4648574458",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4582",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "56852",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 0,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "علی",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "عباسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09122546858",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1401-01-17 11:25:00",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },

                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1401-01-17 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 25,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 125000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2022/08/15/ali054.png",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["tehran", "special"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "13",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "اصفهان",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "اصفهان",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "031",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": "boolean"
                },
                "customerProvinceID": {
                    "value": "031",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4648574458",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4582",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "56852",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            },
            {
                "customerID": {
                    "value": 12,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "محمد",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "احمدی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09358270867",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-01-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-25 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 12,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 355000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/تصویر.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["gharb", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "1",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "شهرکرد",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "چهارمحال و بختیاری",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "038",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "038",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4610298842",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "2312",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "21546",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 12,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "محمد",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "احمدی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09358270867",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-01-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-25 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 12,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 355000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/تصویر.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["gharb", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "1",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "شهرکرد",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "چهارمحال و بختیاری",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "038",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "038",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4610298842",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "2312",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "21546",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 12,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "محمد",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "احمدی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09358270867",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-01-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": True,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": True,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-25 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 12,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 355000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/تصویر.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["gharb", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": "1",
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "شهرکرد",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "چهارمحال و بختیاری",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "038",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "038",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4610298842",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "2312",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "21546",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            },
            {
                "customerID": {
                    "value": 5648,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "ییبس",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "قاقلسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09132586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": False,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 0,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/sdssa.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["fgssa", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": None,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": None,
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": None,
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": None,
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": None,
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": None,
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": None,
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": None,
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 5648,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "ییبس",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "قاقلسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09132586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": False,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 0,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/sdssa.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["fgssa", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": None,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": None,
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": None,
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": None,
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": None,
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": None,
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": None,
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": None,
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 5648,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "ییبس",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "قاقلسی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09132586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": False,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1399-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 0,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/sdssa.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["fgssa", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": None,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": None,
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": None,
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": None,
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": None,
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": None,
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": None,
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": None,
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            },
            {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            }, {
                "customerID": {
                    "value": 48,
                    "label": "شناسه کاربر",
                    "order": 1,
                    "editable": False
                },
                "customerFirstName": {
                    "value": "نعیمه",
                    "label": "نام",
                    "order": 2,
                    "editable": True
                },
                "customerLastName": {
                    "value": "رضایی",
                    "label": "نام خانوادگی",
                    "order": 3,
                    "editable": True
                },
                "customerPhoneNumber": {
                    "value": "09112586455",
                    "label": "موبایل",
                    "order": 4,
                    "editable": True
                },
                "customerCreateTime": {
                    "value": "1400-11-15 12:37:53",
                    "label": "تاریخ ثبت نام",
                    "order": 5,
                    "editable": False
                },
                "customerIsConfirm": {
                    "value": False,
                    "label": "تایید مشتری",
                    "order": 6,
                    "editable": True
                },
                "customerIsActive": {
                    "value": False,
                    "label": "فعال/غیرفعال",
                    "order": 7,
                    "editable": True
                },
                "customerIsMobileConfirm": {
                    "value": True,
                    "label": "تایید موبایل",
                    "order": 8,
                    "editable": True
                },
                "lastOrderDate": {
                    "value": "1400-01-23 12:15:24",
                    "label": "تاریخ آخرین سفارش",
                    "order": 9,
                    "editable": False
                },
                "totalOrdersQuantity": {
                    "value": 0,
                    "label": "تعداد سفارشات",
                    "order": 10,
                    "editable": False
                },
                "totalOrdersPrice": {
                    "value": 10000000,
                    "label": "هزینه مجموع سفارشات",
                    "order": 11,
                    "editable": False
                },
                "avatar": {
                    "value": "https://devapi.aasood.com/gallery/2020/05/15/zzzzzzzzzzzzzzzzzzzzz.jpeg",
                    "label": "تصویر شناسه",
                    "order": 0,
                    "editable": True
                },
                "customerGroups": {
                    "value": ["aasood", "ordinary"],
                    "label": "گروه های مشتری",
                    "order": 12,
                    "editable": True
                },
                "customerRegionCode": {
                    "value": 5,
                    "label": "کد منطقه",
                    "order": 13,
                    "editable": True
                },
                "customerCity": {
                    "value": "تهران",
                    "label": "شهر",
                    "order": 14,
                    "editable": True
                },
                "customerProvince": {
                    "value": "تهران",
                    "label": "استان",
                    "order": 15,
                    "editable": True
                },
                "customerCityID": {
                    "value": "021",
                    "label": "کد شهر",
                    "order": 16,
                    "editable": True
                },
                "customerProvinceID": {
                    "value": "021",
                    "label": "کد استان",
                    "order": 17,
                    "editable": True
                },
                "customerNationalID": {
                    "value": "4585685522",
                    "label": "کد ملی",
                    "order": 18,
                    "editable": True
                },
                "selCustomerCode": {
                    "value": "4585",
                    "label": "کد مشتری کوثر",
                    "order": 19,
                    "editable": False
                },
                "accFormalAccCode": {
                    "value": "12311",
                    "label": "شناسه تفصیلی",
                    "order": 20,
                    "editable": False
                }
            },
        ]
    }
    return {"success": True, "message": response, "status_code": 200}


def get_customers_grid_data(data: str = None):
    data = {} if data is None else json.loads(data)
    records = Filter()
    period_filters: dict = {}
    value_filters: dict = {}
    search_query: dict = {}
    if filters := data.get("filters"):
        period_filters: dict = records.set_period_filters(filters) or {}
        value_filters: dict = records.set_value_filters(filters) or {}
    if search_phrase := data.get("search"):
        search_query = records.set_search_query(search_phrase)
    filters = dict(period_filters, **value_filters, **search_query)
    return GetData().executor(
        queries=filters,
        number_of_records=data.get("perPage") or "15",
        page=data.get("page") or "1",
        sort_name=data.get("sortName") or "customerID",
        sort_type=data.get("sortType") or "asc"
    )


def crm_get_profile(customer_phone_number: dict):
    customer_phone_number = customer_phone_number.get('phone_number')
    profile = Profile({"customer_phone_number": customer_phone_number})
    if result := profile.get_profile_data():
        customer = {grid_attribute: result.get(grid_attribute) or None for grid_attribute in VALID_PROFILE_KEYS}
        return {"success": True, "message": customer, "status_code": 200}
    return {"success": False, "error": "اطلاعاتی برای کاربر وجود ندارد", "status_code": 401}


def set_status(mobileNumber: str, status: str) -> dict:
    customer = Customer(mobileNumber)
    result = customer.set_status(status)
    if status == "cancel":
        if customer.cancel_status():
            return {"success": True, "message": "وضعیت کاربر با موفقیت به روز شد", "status_code": 200}
        elif result is None:
            return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
        else:
            return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}
    if status == "confirm":
        kosar_result = customer.kosar_getter()
        result = customer.confirm_status()
    if type(result) == dict and type(kosar_result) == dict:
        return {"success": True, "walletData": result, "kosarData": kosar_result,
                "message": "وضعیت کاربر با موفقیت به روز شد", "status_code": 200}
    elif result is None or kosar_result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}


def edit_customers_grid_data(data):
    data = json.loads(data)
    if data.get("customerMobileNumber"):
        profile = Profile(data)
        return profile.update_profile()
    return {"status_code": 422, "success": False, "error": "ورود شماره موبایل الزامی است."}


def set_informal_flag(mobileNumber: str, hasInformal: bool):
    customer = Customer(mobileNumber)
    if result := customer.set_has_informal(hasInformal):
        return {"success": True, "message": "وضعیت غیر رسمی کاربر با موفقیت به روز شد", "status_code": 200}
    elif result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}


def get_kosar_data(customerMobileNumber: str):
    customer = Customer(customerMobileNumber)
    if result := customer.kosar_getter():
        return {"success": True, "message": result, "status_code": 200}
    elif result is None:
        return {"success": False, "error": "لطفا مجددا تلاش کنید", "status_code": 417}
    else:
        return {"success": False, "error": "شماره موبایل وجود ندارد", "status_code": 404}
