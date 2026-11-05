def calculate_subtotal(prices: list[float]) -> float:
    """Calculate subtotal from a list of prices."""
    total = 0.0
    for price in prices:
        if price < 0:
            raise ValueError(f"Price cannot be negative: {price}")
        total += price
    return round(total, 2)


def apply_discount(subtotal: float, discount_percent: float) -> float:
    """Apply percentage discount (0-100) to subtotal."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount percent must be between 0 and 100")
    discounted = subtotal * (1.0 - (discount_percent / 100.0))
    return round(discounted, 2)


def apply_fixed_discount(amount: float, fixed_discount: float) -> float:
    """Apply fixed discount amount to an amount."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if fixed_discount < 0:
        raise ValueError("Fixed discount cannot be negative")
    if fixed_discount > amount:
        raise ValueError("Fixed discount cannot exceed amount")
    return round(amount - fixed_discount, 2)


def apply_tax(amount: float, tax_rate: float) -> float:
    """Apply tax rate to an amount."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    return round(amount * (1.0 + tax_rate), 2)


def calculate_order_total(
    prices: list[float],
    discount_percent: float = 0.0,
    tax_rate: float = 0.0,
    fixed_discount: float = 0.0,
) -> float:
    """Calculate the final order total.

    The percentage discount (0-100) is applied to the subtotal first, followed
    by the fixed discount deduction; the tax rate is then applied to the
    resulting discounted amount.
    """
    subtotal = calculate_subtotal(prices)
    discounted = apply_discount(subtotal, discount_percent)
    after_fixed = apply_fixed_discount(discounted, fixed_discount)
    return apply_tax(after_fixed, tax_rate)
