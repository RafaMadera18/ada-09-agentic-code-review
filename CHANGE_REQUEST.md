# Change Request

Change ID: CR-002

## Goal
Add fixed-amount discount support through a new pure function `apply_fixed_discount(amount: float, fixed_discount: float) -> float` and integrate an optional `fixed_discount: float = 0.0` parameter into `calculate_order_total(prices, discount_percent=0.0, tax_rate=0.0, fixed_discount=0.0) -> float` while preserving full backward compatibility for existing callers.

## Requirements Covered
- REQ-003 (Discounts)
- AC-003-8 (Fixed discount deduction rounded to 2 decimals)
- AC-003-9 (Validation against negative amounts and negative fixed discounts)
- AC-003-10 (Validation against fixed discounts exceeding amount)
- AC-003-11 (Discount sequencing in `calculate_order_total`: subtotal -> percentage discount -> fixed discount -> tax)

## Constraints
- Follow AGENTS.md.
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Preserve architecture boundaries: pure functions in `src/calculator.py`, standard library only, no I/O, raise `ValueError` on invalid inputs, round money outputs to 2 decimal places.
- Do not weaken existing tests.
- Maintain backward compatibility of `calculate_order_total`.

## Verification
- Unit tests cover valid fixed discounts, zero discount, discount matching amount, negative amount, negative discount, and discount exceeding amount.
- Unit tests verify order total calculation combining prices, percentage discount, fixed discount, and tax rate.
- All 27 existing tests pass without modification.
- Deterministic verification command (`verify_repo.sh` / standard suite) passes.

## Human Approval
Approved to implement: YES
Approved by: Rafael (Lead Reviewer / Human Gate 0)
Date: 2026-11-05
