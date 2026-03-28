---
title: "SQL Trust Lens: Schema Validation for LLM-Generated SQL"
description: "NEO built a Python tool that validates LLM-generated SQL against a live database schema, scoring each query 0–100 and blocking unsafe execution."
date: 2026-03-28
tags: [sql, llm, validation, database, python]
slug: sql-trust-lens
github: https://github.com/dakshjain-1616/sql-trust-lens
---

# SQL Trust Lens: Schema Validation for LLM-Generated SQL

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/sql-trust-lens)

![Pipeline Architecture](../public/images/diagrams/sql-trust-lens.png)

## The Problem

> LLMs generate SQL that references tables and columns that do not exist. These queries reach the database, crash pipelines, and sometimes leak information through detailed error messages. There is no standard gate between generation and execution.

NEO built SQL Trust Lens to intercept LLM-generated SQL before it hits the database, validate every identifier against the live schema, and block any query that fails the threshold.

## How the Trust Score Works

**SQL Trust Lens** assigns each query a score from 0 to 100 using a weighted formula:

```
trust_score = (table_component × 0.5 + col_component × 0.5) × 100
```

The tool validates every table and column reference in the query against the actual database schema. Missing identifiers reduce the score. The three score bands map to actions:

- **80–100:** Safe to execute
- **50–79:** Partial validity, manual review recommended
- **0–49:** Hallucination detected, blocked

This means a query that gets one table right but references five non-existent columns will score below 50 and never reach the database.

## The EvalEngine

The core component is **EvalEngine**, which wraps the full validation and execution pipeline. It returns a `ValidationResult` struct with:

- `trust_score` — the 0–100 numeric score
- `can_execute` — boolean gate flag
- `valid_tables` and `invalid_tables` — per-identifier breakdown
- `valid_columns` and `invalid_columns` — same for columns
- `suggested_corrections` — typo fixes using `difflib` fuzzy matching
- `complexity` — counts of joins, subqueries, and aggregations

The `suggested_corrections` field is particularly useful. If a column is named `customer_name` and the query says `custmer_name`, the engine catches the edit distance and suggests the fix rather than just rejecting the query.

## Typo Correction with difflib

LLMs sometimes generate near-correct identifiers. Instead of treating all mismatches as hallucinations, **SQL Trust Lens** uses Python's `difflib` to compute similarity ratios against every schema identifier.

When the ratio exceeds a threshold, the engine classifies the mismatch as a likely typo and adds it to `suggested_corrections`. This prevents valid queries from being blocked due to minor spelling errors while still catching entirely fabricated identifiers.

## LLM Backend Priority

The tool supports three backends, tried in this order when in auto mode:

1. **llama.cpp** — local GGUF model, no API cost
2. **OpenRouter** — cloud API fallback
3. **Mock** — built-in templates for testing without any API key

This lets you run the full pipeline offline during development and switch to a cloud backend in production without changing application code.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/sql-trust-lens
cd sql-trust-lens
pip install -r requirements.txt
```

The bundled Northwind dataset provides an 8-table schema ready to query. No additional database setup is needed.

For cloud-based SQL generation, set your API key:

```bash
export OPENROUTER_API_KEY=sk-or-...
```

Use the Python API:

```python
from sql_trust_lens import EvalEngine

engine = EvalEngine()
result = engine.validate_sql("SELECT name FROM customers WHERE city = 'London'")

print(result.trust_score)        # e.g. 95.0
print(result.can_execute)        # True
print(result.suggested_corrections)  # [] if all identifiers valid

if result.can_execute:
    df = engine.execute_sql(result.sql)
    print(df.head())
```

Launch the Streamlit UI for interactive querying, schema browsing, and history export:

```bash
streamlit run app.py
```

The UI shows the trust score, per-identifier validity breakdown, suggested corrections, and query complexity metrics for every submitted query.

NEO built a SQL validation layer that stops LLM hallucinations before they hit the database. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
