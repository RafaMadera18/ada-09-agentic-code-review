# Human Review Decisions

## Change
CR-002: Fixed-amount discount support in calculator service

### RF-01
- **Reviewer severity**: MUST FIX
- **Human decision**: ACCEPTED
- **Reason**: The finding is technically sound and well-evidenced. Missing `if amount < 0:` causes negative amounts to trigger the `fixed_discount > amount` branch, returning a misleading error message ("Fixed discount cannot exceed amount") rather than indicating an invalid amount. This directly violates AC-003-9 and the architecture convention requiring clear `ValueError` diagnostics.
- **Required action**: Add explicit check `if amount < 0: raise ValueError("Amount cannot be negative")` as the first line of `apply_fixed_discount`.

### RF-02
- **Reviewer severity**: MUST FIX
- **Human decision**: ACCEPTED
- **Reason**: The test suite produced false confidence by testing only `apply_fixed_discount(100.0, -10.0)` while neglecting negative amounts (`-50.0, 10.0` and `-50.0, 0.0`). Testing both boundaries is required to verify AC-003-9.
- **Required action**: Add unit test assertions in `test_apply_fixed_discount_negative` covering negative amounts.

### RF-03
- **Reviewer severity**: SHOULD FIX
- **Human decision**: ACCEPTED
- **Reason**: `calculate_order_total` combines multiple business rules; omitting negative fixed discount and edge-case boundary checks leaves integration regressions unchecked.
- **Required action**: Add test cases in `test_calculator.py` for `calculate_order_total` with negative fixed discount and fixed discount exceeding post-discount subtotal.

### RF-04
- **Reviewer severity**: SHOULD FIX
- **Human decision**: MODIFIED
- **Reason**: The docstring is indeed outdated, but rather than verbose prose, it should follow the concise style established across `src/calculator.py`.
- **Final severity**: SHOULD FIX
- **Required action**: Update `calculate_order_total` docstring to document `fixed_discount` and the 4-step sequence concisely.

### RF-05
- **Reviewer severity**: OPTIONAL
- **Human decision**: ACCEPTED
- **Reason**: Adding a fractional cents test is straightforward, low-risk, and ensures floating-point rounding precision is safeguarded.
- **Final severity**: OPTIONAL
- **Required action**: Include `apply_fixed_discount(100.0, 15.556)` in `test_apply_fixed_discount_valid`.

## Human Gate
[x] Return to coder-agent  
[ ] Ready for final re-review  
[ ] Stop / escalate  
