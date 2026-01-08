from decimal import Decimal
from strategy import Order
from strategy import (fidelity_promo, bulk_item_promo, large_order_promo)

promos = [promo for name, promo in globals().items() if name.endswith('_promo') and name != 'best_promo']

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

if __name__ == "__main__":
    print("globals:")
    print('\n'.join([str(item) for item in globals().items()]))