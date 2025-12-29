class PayOrderUseCase:
    def __init__(self, order_repository, payment_gateway):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: str):
        order = self.order_repository.get_by_id(order_id)
        order.pay()
        self.payment_gateway.charge(order_id, order.total())
        self.order_repository.save(order)
        return {
            "order_id": order.order_id,
            "status": order.status,
            "total": order.total()
        }
