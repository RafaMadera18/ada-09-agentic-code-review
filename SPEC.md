# Specification

Verifiable behavior for each requirement in `REQUIREMENTS.md`. Acceptance criteria are named AC-<requirement number>-<n>. Each one maps to an automated test.

Adding acceptance criteria for an existing REQ is allowed. Adding or editing a REQ needs human approval.

## REQ-001: Subtotal Calculation

Function: `calculate_subtotal(prices: list[float]) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-001-1 | Returns the sum of the prices rounded to 2 decimals. `[10.5, 20.0, 5.25]` returns `35.75`. | `test_calculate_subtotal_valid` |
| AC-001-2 | An empty list returns `0.0`. | `test_calculate_subtotal_valid` |
| AC-001-3 | Any negative price raises `ValueError`. | `test_calculate_subtotal_negative` |

## REQ-002: Tax Application

Function: `apply_tax(amount: float, tax_rate: float) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-002-1 | Returns `amount * (1 + tax_rate)` rounded to 2 decimals. `apply_tax(100.0, 0.16)` returns `116.0`. | `test_apply_tax_valid` |
| AC-002-2 | A negative amount raises `ValueError`. | `test_apply_tax_negative_amount` |
| AC-002-3 | A negative tax rate raises `ValueError`. | `test_apply_tax_negative_rate` |

## REQ-003: Percentage Discount

Function: `apply_discount(subtotal: float, discount_percent: float) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-003-1 | Returns `subtotal * (1 - discount_percent / 100)` rounded to 2 decimals. `(100.0, 10.0)` returns `90.0`, `(100.0, 0.0)` returns `100.0`, `(100.0, 100.0)` returns `0.0`. | `test_apply_discount_valid` |
| AC-003-2 | A discount below 0 or above 100 raises `ValueError`. | `test_apply_discount_invalid` |
| AC-003-3 | A negative subtotal raises `ValueError`. | `test_apply_discount_invalid` |
| AC-003-4 | When a discount and a tax rate are both applied, the discount is applied first and the tax is calculated on the discounted amount (from "before tax calculation" in REQ-003). | `test_calculate_order_total_discount_then_tax` |
| AC-003-8 | `apply_fixed_discount(amount, fixed_discount)` returns `amount - fixed_discount` rounded to 2 decimals. | `test_apply_fixed_discount_valid` |
| AC-003-9 | Negative `amount` or negative `fixed_discount` passed to `apply_fixed_discount` raises `ValueError`. | `test_apply_fixed_discount_negative` |
| AC-003-10 | A `fixed_discount` exceeding `amount` passed to `apply_fixed_discount` raises `ValueError`. | `test_apply_fixed_discount_exceeds_amount` |

## Order Total (combines REQ-001, REQ-002, REQ-003)

Function: `calculate_order_total(prices: list[float], discount_percent: float = 0.0, tax_rate: float = 0.0) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-001-4 | `calculate_order_total` with only prices returns the subtotal. `[10.5, 20.0, 5.25]` returns `35.75` and `[]` returns `0.0`. | `test_calculate_order_total_defaults`, `test_calculate_order_total_empty` |
| AC-001-5 | A negative price passed to `calculate_order_total` raises `ValueError`. | `test_calculate_order_total_negative_price` |
| AC-002-4 | `calculate_order_total` applies the tax rate to the discounted subtotal. `([100.0], 0.0, 0.16)` returns `116.0`. | `test_calculate_order_total_defaults` |
| AC-002-5 | A negative tax rate passed to `calculate_order_total` raises `ValueError`. | `test_calculate_order_total_negative_tax_rate` |
| AC-003-5 | `calculate_order_total([100.0, 50.0], 10.0, 0.16)` returns `156.6`; a 100% discount returns `0.0`. | `test_calculate_order_total_discount_then_tax`, `test_calculate_order_total_full_discount` |
| AC-003-6 | A discount outside 0-100 passed to `calculate_order_total` raises `ValueError`. | `test_calculate_order_total_invalid_discount` |
| AC-003-7 | `discount_percent` and `tax_rate` are optional and default to `0.0`. | `test_calculate_order_total_defaults` |
| AC-003-11 | `fixed_discount` is optional and defaults to `0.0`. Order total applies percentage discount first, then fixed discount, then tax. | `test_calculate_order_total_fixed_discount` |

## Conventions that apply to every criterion

- Invalid input raises `ValueError`.
- Returned amounts are rounded to 2 decimals.
- See `ARCHITECTURE.md` for module boundaries.
