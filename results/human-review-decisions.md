# Human Review Decisions

## Change
CR-002: Fixed-amount discount support in calculator service

### RF-01
- **Reviewer severity**: MUST FIX
- **Human decision**: ACCEPTED
- **Reason**: When `amount` is negative (for example `-50.0`), passing `fixed_discount=0` triggers `fixed_discount > amount` and raises `"Fixed discount cannot exceed amount"`. That message is misleading because the problem is the negative amount, not the discount. AC-003-9 and our architecture rules require explicit validation and a clear error message.
- **Required action**: Put `if amount < 0: raise ValueError("Amount cannot be negative")` at the top of `apply_fixed_discount`.

### RF-02
- **Reviewer severity**: MUST FIX
- **Human decision**: ACCEPTED
- **Reason**: The coder only tested a negative discount (`100.0, -10.0`). It never called the function with a negative amount, which is why RF-01 slipped past with green tests.
- **Required action**: Add calls with negative amounts to `test_apply_fixed_discount_negative` (`-50.0, 10.0` and `-50.0, 0.0`).

### RF-03
- **Reviewer severity**: SHOULD FIX
- **Human decision**: ACCEPTED
- **Reason**: `calculate_order_total` chains subtotal, percentage discount, fixed discount, and tax. We need tests for invalid fixed discounts in that full chain, especially when the discount is negative or larger than the balance left after the percentage discount.
- **Required action**: Add unit tests in `test_calculator.py` for negative fixed discount and fixed discount exceeding post-discount balance.

### RF-04
- **Reviewer severity**: SHOULD FIX
- **Human decision**: MODIFIED
- **Reason**: The docstring does need to mention `fixed_discount`, but let's keep it short like the other docstrings in `src/calculator.py` rather than adding a long multi-step explanation.
- **Final severity**: SHOULD FIX
- **Required action**: Update the docstring in `calculate_order_total` in one or two sentences explaining the sequence.

### RF-05
- **Reviewer severity**: OPTIONAL
- **Human decision**: ACCEPTED
- **Reason**: Quick check to prevent precision regressions with numbers like `15.556`. Low effort to include.
- **Final severity**: OPTIONAL
- **Required action**: Add an assertion with fractional cents in `test_apply_fixed_discount_valid`.

## Human Gate
[x] Return to coder-agent  
[ ] Ready for final re-review  
[ ] Stop / escalate  
