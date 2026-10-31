# Test Coverage Matrix

| Requirement | Test case | Status | Evidence |
|---|---|---:|---|
| Input file availability and readability | Synthetic CSV created in temp directory and read with pandas | Pass | Local pytest case |
| Required columns and schema validation | Reindex a DataFrame with missing columns and assert required ones are present | Pass | Local pytest case |
| Empty datasets and empty files | Empty DataFrame and CSV handling are exercised as safe no-op or expected error path | Pass | Local pytest case |
| Null and missing values | Assert missing values remain null and are preserved through metadata step | Pass | Local pytest case |
| Duplicate records and business keys | Duplicate-row fixtures and hash stability tests | Pass | Local pytest case |
| Invalid data types and malformed values | Invalid input strings remain as strings or are safely rejected by the helper path | Pass | Local pytest case |
| Date and numeric boundary cases | Quarter parsing for q1-q4 and invalid permutations | Pass | Local pytest case |
| Business rule validation | QA checks for allowed value mapping and expected output contracts | Pass | Local contract tests |
| Transformation correctness | Renaming, metadata append, and DataFrame normalization | Pass | Local pytest case |
| Row-count reconciliation | Validate row count after fixture generation and metadata append | Pass | Local pytest case |
| Aggregation accuracy | dbt-level aggregation rules are documented and should be validated in Snowflake-backed dbt tests | Not executed locally | Cloud/dbt dependency |
| Join correctness and unmatched records | dbt relationships tests are part of the project design | Not executed locally | Cloud/dbt dependency |
| Referential integrity | dbt relationship tests exist conceptually | Not executed locally | Cloud/dbt dependency |
| Output schema and output file validation | DataFrame schema contract and metadata columns validated in tests | Pass | Local pytest case |
| Error handling and invalid inputs | Negative fixtures for invalid quarter or missing file path | Pass | Local pytest case |
| Regression testing | Core helper regressions retained in pytest | Pass | Local pytest case |
| Idempotency | Raw ingestion design states that tables are truncated; test contract verifies metadata/hash behavior is repeatable | Assumption documented | Local verification of deterministic hash behavior |
| Data leakage or unintended modification | Repository strategy avoids production writes; tests use temp directories only | Pass | Local testing discipline |
| Performance checks | Not applicable for this repository local validation stage | Not run | No baseline described |

## Notes
- The dbt project includes a stronger production-quality validation layer for Snowflake-backed relationships, uniqueness, and accepted values.
- Because Snowflake credentials are not available in this environment, a subset of the project-level checks remains blocked rather than failed.
