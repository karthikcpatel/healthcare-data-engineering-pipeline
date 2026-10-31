---
name: data-quality-testing
description: Check missing and null values, identify duplicate records and duplicate business keys, validate data types and schema, confirm allowed values and business rules, and detect invalid dates, malformed records, and inconsistent formats.
---

# Data Quality Testing

Use this skill when validating raw, staged, and mart datasets.

## Core checks
- Null and missing values by column.
- Duplicate business keys and duplicate rows.
- Required columns, schema drift, and unexpected file layout.
- Invalid dates, malformed strings, and conversion failures.
- Domain rules such as allowed values and expected code sets.
- Referential integrity between parent and child tables when applicable.
- Row count reconciliation and transformation result checks.

## Test design
1. Establish the expected schema from source docs or transformation logic.
2. Build a small deterministic fixture that violates one rule at a time.
3. Validate the failure mode with explicit assertions and clear error messages.
4. Confirm the clean path still succeeds.
5. Record any business assumptions as assumptions requiring confirmation.

## Constraints
- Do not modify production data during testing.
- Prefer temp files, temp tables, or in-memory DataFrames.
- Keep synthetic test data isolated from sample datasets.
- Document any rule that is only inferred and not confirmed by repository code.
