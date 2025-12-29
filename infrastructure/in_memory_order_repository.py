class InMemoryOrderRepository:
    def __init__(self):
        self.orders = {}

    def get_by_id(self, order_id):
        if order_id not in self.orders:
            raise ValueError("Order not found")
        return self.orders[order_id]

    def save(self, order):
        self.orders[order.order_id] = order
