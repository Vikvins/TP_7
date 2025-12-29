class FakePaymentGateway:
    def charge(self, order_id, money):
        return True
