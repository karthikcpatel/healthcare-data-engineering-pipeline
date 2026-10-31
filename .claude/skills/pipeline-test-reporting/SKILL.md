---
name: pipeline-test-reporting
description: Collect test results and failure details, separate passed, failed, blocked, and skipped tests, record reproduction steps and defect severity, and produce a readable final testing report.
---

# Pipeline Test Reporting

Use this skill when creating the final evidence package for a data pipeline verification run.

## Required output
- A concise summary of executed tests.
- Exact commands and exit codes.
- Counts of passed, failed, blocked, and skipped tests.
- Defect severity and reproduction steps.
- A list of changes made, if any.
- Remaining limitations and recommended next steps.

## Reporting rules
- Report only what was actually executed.
- Distinguish environment problems from product defects.
- Call out assumptions and unverified areas separately.
- Keep the final report readable enough for engineering and QA review.

## Evidence standard
- Save command output for the final report.
- Include the relevant test names and observed behavior.
- Separate blocked checks caused by missing credentials or unavailable services from true failing assertions.
- Document whether the issue is reproducible and whether a fix was attempted.
