# Test Strategy for the Healthcare Data Pipeline

## Objective
This repository does not yet contain a repository-level Python test suite. The strategy therefore combines the existing dbt validation model with a lightweight local pytest suite for the Python ingestion code paths and transformation-contract logic that can be validated without credentials or cloud access.

## Scope and constraints
The strategy intentionally avoids cloud-dependent execution. That means:

- We test pure Python logic and data contracts locally.
- We do not create a live Snowflake connection in automated tests.
- We do not overwrite production datasets or sample files.
- We keep all negative tests isolated in temporary directories or in-memory DataFrames.

## Test categories
### 1. Ingestion and source-file readiness
- Confirm the file can be read and parsed.
- Confirm required columns exist.
- Confirm malformed rows or missing raw files fail clearly.

### 2. Schema and column validation
- Validate required columns are present.
- Validate column casing/normalization expectations.
- Confirm metadata columns are appended.

### 3. Empty and null handling
- Empty CSVs should not crash unexpectedly.
- Missing values should stay as nulls or be normalized according to source rules.
- Duplicate metadata should not break the pipeline contract.

### 4. Duplicate and business-key validation
- Confirm duplicates are detected when expected.
- Validate the raw metadata `_row_hash` is consistent for identical rows.
- Ensure Business keys are not silently overwritten.

### 5. Date and numeric boundary validation
- Validate quarter parsing and boundary dates.
- Validate invalid date strings stay null or fail safely, depending on ingestion contract.
- Confirm numeric conversions do not silently misparse values.

### 6. Transformation correctness
- Validate renames and expected data type conversions.
- Confirm `NULLIF` and `TRY_TO_DATE` behavior is consistent with the dbt logic.
- Check that key mart columns are derived as documented.

### 7. Regression protection
- Preserve known safe behaviors for quarter parsing and DataFrame normalization.
- Guard against future schema drift and raw-file format changes.

## Assumptions and limitations
The following are assumptions requiring confirmation before treating them as business rules:

- Exact FAERS row limits are not considered an operational correctness issue; they are source API constraints.
- The raw ingest layer intentionally stores all values as strings, so type validation occurs downstream in dbt.
- The generated Synthea data is synthetic and therefore not expected to be production-grade from a statistical standpoint.

## Test execution plan
1. Run the existing repository tests first, if available.
2. Add local pytest tests for ingestion helper functions and data contracts.
3. Execute the new suite in the project `.venv`.
4. Record exits and failures.
5. If a real defect is found, fix only the narrow root cause and rerun the relevant tests.

## Expected result
The local test suite should provide repeatable evidence for the ingestion contract and helper logic, even when live Snowflake or cloud sources are unavailable.
