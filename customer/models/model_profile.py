from customer.models.model_register import Customer


class Profile:

    def __init__(self, phone_num):
        self.customer = Customer(phone_num)
