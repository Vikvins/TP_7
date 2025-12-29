import pytest
from domain.order import Order, OrderLine, Money, OrderStatus
from application.pay_order_usecase import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway

def test_pay_order_success():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order("1")
    order.add_line(OrderLine("Item1", 2, Money(50)))
    repo.save(order)

    usecase = PayOrderUseCase(repo, gateway)
    result = usecase.execute("1")
    assert result["status"] == OrderStatus.PAID
    assert result["total"].amount == 100

def test_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order("2")
    repo.save(order)

    usecase = PayOrderUseCase(repo, gateway)
    with pytest.raises(ValueError):
        usecase.execute("2")

def test_pay_order_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order("3")
    order.add_line(OrderLine("Item1", 1, Money(30)))
    repo.save(order)

    usecase = PayOrderUseCase(repo, gateway)
    usecase.execute("3")
    with pytest.raises(ValueError):
        usecase.execute("3")

def test_modify_after_pay():
    order = Order("4")
    order.add_line(OrderLine("Item1", 1, Money(20)))
    order.pay()
    with pytest.raises(ValueError):
        order.add_line(OrderLine("Item2", 1, Money(10)))

def test_total_calculation():
    order = Order("5")
    order.add_line(OrderLine("Item1", 2, Money(10)))
    order.add_line(OrderLine("Item2", 1, Money(20)))
    assert order.total().amount == 40
