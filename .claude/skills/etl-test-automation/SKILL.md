---
name: etl-test-automation
description: Generate and maintain automated tests using the existing compatible testing framework, covering positive, negative, boundary, and regression scenarios for extraction, transformation, and loading logic.
---

# ETL Test Automation

Use this skill to add repeatable Python tests for pipeline logic.

## Standards
- Prefer the repository's existing framework when it is already in use.
- If no framework exists, use pytest as the lightweight default for Python.
- Keep tests deterministic, isolated, and independent of external services.
- Use temporary directories, temporary files, and synthetic fixtures for negative tests.
- Verify both success and failure behavior.

## Coverage areas
- Extraction and file-read validation.
- Schema normalization and column reindexing.
- Empty input, malformed input, and missing fields.
- Duplicate inputs and duplicate keys.
- Boundary values and date logic.
- Regression paths for previously detected defects.

## Execution guidance
1. Write the smallest test that reproduces the behavior.
2. Confirm that the test fails before a code change when the bug is real.
3. Implement the narrowest valid fix.
4. Re-run the relevant tests and then the broader suite.
5. Preserve original behavior when the expected rule is not confirmed.

## Safety rules
- Never overwrite the original sample datasets.
- Avoid production writes during tests.
- Keep assertions specific and meaningful.
- No weakening of assertions to make a red test green.
