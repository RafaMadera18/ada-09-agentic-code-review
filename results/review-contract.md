# Review Contract

## Change
CR-002: Fixed-amount discount support in calculator service

## Requirements / Acceptance Criteria
- FR-003 / REQ-003: Percentage & Promotional Discount calculation
- AC-003-8: `apply_fixed_discount(amount: float, fixed_discount: float) -> float` returns `amount - fixed_discount` rounded to 2 decimals.
- AC-003-9: Negative `amount` or negative `fixed_discount` passed to `apply_fixed_discount` raises `ValueError`.
- AC-003-10: `fixed_discount` exceeding `amount` passed to `apply_fixed_discount` raises `ValueError`.
- AC-003-11: `fixed_discount` is optional in `calculate_order_total` defaulting to `0.0`. Sequencing must be: subtotal -> percentage discount -> fixed discount -> tax.

## Architecture Constraints
- Expected dependency flow: `tests/` -> `src/`. `src/calculator.py` must only use standard library, no I/O, no network, no global mutable state.
- Business-rule location: All calculation logic and input validation must reside in `src/calculator.py`.
- Protected boundaries: `REQUIREMENTS.md`, `generated/`, `.github/workflows/` must not be modified without explicit authorization. No third-party dependencies.

## Review Rules
- Verify requirement coverage: Ensure all acceptance criteria AC-003-8 to AC-003-11 are genuinely implemented and verified.
- Verify every called API/dependency exists in production code (standard library only).
- Check architecture boundaries and conventions (pure functions, `ValueError` on bad inputs, rounding to 2 decimals).
- Inspect tests for masking / false confidence: check for missing boundary tests (e.g. negative amount, zero amount, compound discount edge cases).
- Check regression and backward-compatibility behavior (existing tests pass, positional/keyword argument compatibility).
- Identify unnecessary technical debt (outdated docstrings, unhandled edge cases).
- Cite evidence for every finding (file, line number, concrete code or test deficiency).

## Severity
- **MUST FIX**: Requirement violation, regression, security/integrity risk, hallucinated API/dependency, broken architecture constraint, or defect that makes the change unsafe to approve.
- **SHOULD FIX**: Significant maintainability, coverage, design, or clarity issue that does not block the requested behavior.
- **OPTIONAL**: Non-blocking improvement outside the minimum acceptance threshold.
