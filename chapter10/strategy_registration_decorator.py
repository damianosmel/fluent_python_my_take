from decimal import Decimal
from strategy import Customer,LineItem,Order
from typing import Callable

Promotion = Callable[[Order],Decimal]
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    promos_name_discount = [ (promo.__name__,promo(order)) for promo in promos]
    promo_max_discount_name,promo_max_discount_value = max(promos_name_discount,key=lambda tuple_:tuple_[1])
    print(f"Promotion(s) with maximum discount: {promo_max_discount_name}")
    return promo_max_discount_value

@promotion
def fidelity(order: Order) -> Decimal:
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

@promotion
def large_order(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = set(item.product for item in order.cart)
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

if __name__ == "__main__":
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, Decimal('0.5')),
            LineItem('apple', 10, Decimal('1.5')),
            LineItem('watermelon', 5, Decimal(5))]
    banana_cart = [LineItem('banana', 30, Decimal('.5')), LineItem('apple', 10, Decimal('1.5'))]
    long_cart = [LineItem(str(i),1,Decimal(1)) for i in range(12)]

    joe_banana_cart_best_promo = Order(joe,banana_cart,best_promo)
    print(f" Joe - banana cart - best promo: {joe_banana_cart_best_promo}")