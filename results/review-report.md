# Independent Review Report

## Review Context
- **Change ID**: CR-002
- **Branch / PR**: `ada09/cr-002`
- **Commit reviewed**: `cbef67d` (`feat: implement CR-002`)
- **Reviewer agent**: Independent Code Review Subagent (`research`)
- **Model**: Gemini 3.8 Flash
- **Tools / permissions**: Read-only codebase tools, deterministic test and contract execution

## Requirements Reviewed
- FR-003 / REQ-003: Percentage & Promotional Discounts
- AC-003-8: `apply_fixed_discount` calculation and rounding to 2 decimals
- AC-003-9: Negative `amount` or negative `fixed_discount` raises `ValueError`
- AC-003-10: `fixed_discount` exceeding `amount` raises `ValueError`
- AC-003-11: `fixed_discount` optional parameter in `calculate_order_total`, sequencing subtotal -> discount % -> fixed discount -> tax

## Verification Evidence Reviewed
- Automated test output: 31 tests passing (exit code 0)
- Lint output: `compileall` clean (exit code 0)
- Repo contract: `check_repo_contract.py` PASS
- Security / protected paths: `check_protected_paths.py` PASS
- Candidate diff: `results/pr.diff` (7 files changed, +149, -2)

## Findings

### RF-01 — MUST FIX
- **Category**: Input Validation / Requirement Violation
- **Requirement / AC**: AC-003-9, ARCHITECTURE.md (descriptive ValueError)
- **File / Line**: `src/calculator.py:21-27`
- **Evidence**:
  ```python
  def apply_fixed_discount(amount: float, fixed_discount: float) -> float:
      """Apply fixed discount amount to an amount."""
      if fixed_discount < 0:
          raise ValueError("Fixed discount cannot be negative")
      if fixed_discount > amount:
          raise ValueError("Fixed discount cannot exceed amount")
      return round(amount - fixed_discount, 2)
  ```
- **Problem**:
  `apply_fixed_discount` lacks an explicit check for `amount < 0`. Unlike `apply_discount` (`if subtotal < 0: raise ValueError("Subtotal cannot be negative")`) and `apply_tax` (`if amount < 0: raise ValueError("Amount cannot be negative")`), passing a negative amount (e.g. `apply_fixed_discount(-50.0, 0.0)`) fails into `if fixed_discount > amount`, raising a misleading `ValueError: Fixed discount cannot exceed amount`.
- **Risk**:
  Violates AC-003-9 and architectural error handling conventions. Masks invalid domain inputs with confusing error messages.
- **Recommended next step**:
  Add `if amount < 0: raise ValueError("Amount cannot be negative")` as the first validation check in `apply_fixed_discount`.

### RF-02 — MUST FIX
- **Category**: Test Quality / False Confidence
- **Requirement / AC**: AC-003-9, CHANGE_REQUEST.md Verification
- **File / Line**: `tests/test_calculator.py:78-81`
- **Evidence**:
  ```python
  def test_apply_fixed_discount_negative(self):
      with self.assertRaises(ValueError):
          apply_fixed_discount(100.0, -10.0)
  ```
- **Problem**:
  The coder report claims full coverage of negative inputs, but `test_apply_fixed_discount_negative` only tested negative `fixed_discount`, omitting negative `amount`. This test gap gave false confidence that all aspects of AC-003-9 were verified when they were not.
- **Risk**:
  False confidence in green test suite; regressions or invalid inputs go undetected in automated pipelines.
- **Recommended next step**:
  Add assertions in `test_apply_fixed_discount_negative` testing `apply_fixed_discount(-50.0, 10.0)` and `apply_fixed_discount(-50.0, 0.0)`.

### RF-03 — SHOULD FIX
- **Category**: Integration Test Coverage
- **Requirement / AC**: AC-003-11
- **File / Line**: `tests/test_calculator.py:86-92`
- **Evidence**:
  Only one positive test case was added for `calculate_order_total` with `fixed_discount`.
- **Problem**:
  No tests verify that `calculate_order_total` raises `ValueError` when given a negative `fixed_discount` or when `fixed_discount` exceeds the discounted subtotal (e.g., subtotal 100 with 50% discount leaves 50; fixed discount of 60 exceeds remaining balance).
- **Risk**:
  Edge cases in the multi-stage discount pipeline could fail unexpectedly or behave inconsistently.
- **Recommended next step**:
  Add unit tests for `calculate_order_total` with negative fixed discount and fixed discount exceeding post-percentage discounted subtotal.

### RF-04 — SHOULD FIX
- **Category**: Documentation & Technical Debt
- **Requirement / AC**: AC-003-11, ARCHITECTURE.md
- **File / Line**: `src/calculator.py:45-49`
- **Evidence**:
  ```python
  def calculate_order_total(
      prices: list[float],
      discount_percent: float = 0.0,
      tax_rate: float = 0.0,
      fixed_discount: float = 0.0,
  ) -> float:
      """Calculate the final order total.

      The discount (0-100) is applied to the subtotal first; the tax rate is then
      applied to the discounted amount.
      """
  ```
- **Problem**:
  Docstring does not mention `fixed_discount` or explain the 4-step sequence (subtotal -> percentage discount -> fixed discount -> tax).
- **Risk**:
  Developers using the library will not have accurate documentation of function parameters and execution order.
- **Recommended next step**:
  Update docstring to document `fixed_discount` and the complete pipeline.

### RF-05 — OPTIONAL
- **Category**: Precision Testing
- **Requirement / AC**: AC-003-8
- **File / Line**: `tests/test_calculator.py:73-77`
- **Evidence**:
  All test inputs in `test_apply_fixed_discount_valid` use round numbers without fractional cents.
- **Problem**:
  Test cases do not exercise boundary floating-point cent rounding (e.g., `apply_fixed_discount(100.0, 15.556)`).
- **Risk**:
  Low; `round(..., 2)` is present in code, but explicit rounding test ensures future refactors preserve 2-decimal rounding.
- **Recommended next step**:
  Add an assertion with fractional cents to `test_apply_fixed_discount_valid`.

## Missing Evidence / Open Questions
None. The code and test diff is compact and fully auditable.

## Summary
- **MUST FIX**: 2 (RF-01, RF-02)
- **SHOULD FIX**: 2 (RF-03, RF-04)
- **OPTIONAL**: 1 (RF-05)

## Reviewer Recommendation
[ ] NOT READY  
[x] READY AFTER MUST FIX  
[ ] READY FOR HUMAN REVIEW  

This recommendation is not a merge approval.
