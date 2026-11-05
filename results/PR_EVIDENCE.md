# PR Evidence

## Change
- **Change ID**: CR-002
- **PR / Branch**: `ada09/cr-002`
- **Base commit**: `0cd5e73`
- **Candidate commit**: `cbef67d` (`feat: implement CR-002`)
- **Fix commit**: `3a9b999` (`fix: address ADA-09 review findings`)

## Requirements / Acceptance Criteria
- **FR-003 / REQ-003**: Discounts (Percentage & Promotional Discounts)
- **AC-003-8**: `apply_fixed_discount(amount, fixed_discount)` returns `amount - fixed_discount` rounded to 2 decimals.
- **AC-003-9**: Negative `amount` or negative `fixed_discount` passed to `apply_fixed_discount` raises `ValueError`.
- **AC-003-10**: `fixed_discount` exceeding `amount` passed to `apply_fixed_discount` raises `ValueError`.
- **AC-003-11**: `fixed_discount` is optional in `calculate_order_total` defaulting to `0.0`. Order total applies percentage discount first, then fixed discount, then tax.

## Implementation
- **Coder report**: `results/coder-report.md`
- **Files changed**: `CHANGE_REQUEST.md`, `SPEC.md`, `TASKS.md`, `src/calculator.py`, `tests/test_calculator.py`, `results/*`
- **Commits**:
  - `cbef67d`: `feat: implement CR-002`
  - `3a9b999`: `fix: address ADA-09 review findings`

## Verification
- **Verification command**: `python -m unittest discover tests; python -m compileall -q src tests scripts; python scripts/check_repo_contract.py; python scripts/check_protected_paths.py`
- **Final result**: PASS
- **Tests**: 34/34 passing (0 failures, 0 errors)
- **Lint**: Clean compilation, 0 syntax errors
- **Security / repo checks**: REPO_CONTRACT: PASS, PROTECTED_PATHS: PASS

## Independent Review
- **Review report**: `results/review-report.md`
- **MUST FIX found**: 2 (RF-01: missing validation for negative amount; RF-02: test gap/false confidence)
- **SHOULD FIX found**: 2 (RF-03: composite order total edge tests; RF-04: outdated docstring)
- **OPTIONAL found**: 1 (RF-05: fractional cent rounding test precision)

## Human Decisions
- **Accepted**: 4 (RF-01, RF-02, RF-03, RF-05)
- **Modified**: 1 (RF-04: updated docstring concisely matching existing module style)
- **Rejected**: 0
- **Deferred**: 0
- **Decisions record**: `results/human-review-decisions.md`

## Re-review
- **Re-review report**: `results/re-review-report.md`
- **Resolved**: 5/5 (RF-01, RF-02, RF-03, RF-04, RF-05)
- **Partially resolved**: 0
- **Not resolved**: 0
- **New MUST FIX regressions**: 0
- **Re-review outcome**: READY FOR HUMAN REVIEW

## Traceability

| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
| AC-003-8 | CR-002: Fixed discount deduction & 2 decimal rounding | `src/calculator.py:apply_fixed_discount` | `tests/test_calculator.py:test_apply_fixed_discount_valid` | RF-05 (OPTIONAL, Resolved) |
| AC-003-9 | CR-002: Negative amount & negative fixed discount validation | `src/calculator.py:apply_fixed_discount` | `tests/test_calculator.py:test_apply_fixed_discount_negative` | RF-01 (MUST FIX, Resolved), RF-02 (MUST FIX, Resolved) |
| AC-003-10 | CR-002: Fixed discount exceeding amount validation | `src/calculator.py:apply_fixed_discount` | `tests/test_calculator.py:test_apply_fixed_discount_exceeds_amount` | None (Clean initial pass) |
| AC-003-11 | CR-002: Composite order total calculation | `src/calculator.py:calculate_order_total` | `tests/test_calculator.py:test_calculate_order_total_fixed_discount*` | RF-03 (SHOULD FIX, Resolved), RF-04 (SHOULD FIX, Resolved) |

## Remaining Risks / Technical Debt
- Floating point arithmetic is constrained to IEEE 754 64-bit float with `round(..., 2)`. While standard across this library, large enterprise financial systems may eventually consider `decimal.Decimal` if arbitrary precision is mandated in future requirements.
- No remaining MUST FIX or SHOULD FIX debts on this branch.

## Final Human Decision
[ ] NOT READY  
[x] READY FOR HUMAN MERGE  

**Approved by**: Rafael (Lead Reviewer & Human Gate Keeper)  
**Date**: 2026-11-05  
