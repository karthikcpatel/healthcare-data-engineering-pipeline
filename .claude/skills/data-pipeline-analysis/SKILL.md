---
name: data-pipeline-analysis
description: Understand the pipeline architecture, trace source-to-target data flow, identify dependencies and transformation stages, and document expected inputs and outputs.
---

# Data Pipeline Analysis

Use this skill to assess a repository before you write tests or make changes.

## Goals
- Confirm the actual pipeline stages and their boundaries.
- Trace source files, raw tables, staging models, marts, and downstream outputs.
- Identify dependencies, assumptions, and missing validation steps.
- Capture the expected schema, transforms, and quality checks.

## Workflow
1. Read the root README and each stage README to establish architecture.
2. Identify ingest, transformation, orchestration, and serving layers.
3. Confirm the source datasets and their route through raw, staging, and reporting layers.
4. Document input file availability, ingestion script entry points, and output tables/views.
5. Record any external dependencies or environmental assumptions that are not enforced locally.

## Standard checks
- Confirm whether the project uses SQL, Pandas, dbt, Airflow, or cloud-native components.
- Record the main data contracts: row counts, keys, metadata columns, and required fields.
- Note potential risk areas such as schema drift, missing values, invalid dates, and source format changes.
- Avoid inventing unsupported business rules; only document rules that appear in code or docs.

## Deliverables
- A concise architecture summary.
- A source-to-target flow map.
- A list of required inputs, outputs, and transformation responsibilities.
- Identified risks and open questions that require confirmation.
