class OrderStatus:
    PENDING = "pending"
    PAID = "paid"

class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"{self.amount} {self.currency}"

class OrderLine:
    def __init__(self, name: str, qty: int, price: Money):
        self.name = name
        self.qty = qty
        self.price = price

    def total(self):
        return Money(self.qty * self.price.amount, self.price.currency)

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.lines = []
        self.status = OrderStatus.PENDING

    def add_line(self, line: OrderLine):
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)

    def total(self):
        total = Money(0)
        for line in self.lines:
            total += line.total()
        return total

    def pay(self):
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self.status = OrderStatus.PAID
