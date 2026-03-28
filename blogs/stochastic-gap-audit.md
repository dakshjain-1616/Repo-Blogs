---
title: "Stochastic Gap Audit: Pre-Deployment Reliability Scoring for LLMs"
description: "NEO built a local reliability auditing tool that scores any LLM's trustworthiness before deployment using Markovian simulation and stochastic gap analysis."
date: 2026-03-28
tags: [llm, reliability, testing, markov, pre-deployment]
slug: stochastic-gap-audit
github: https://github.com/dakshjain-1616/stochastic-gap-audit
---

# Stochastic Gap Audit: Pre-Deployment Reliability Scoring for LLMs

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/stochastic-gap-audit)

![Pipeline Architecture](../public/images/diagrams/stochastic-gap-audit.png)

## The Problem

> Shipping an LLM without a reliability baseline is a bet on hope. Existing evaluation tools require dashboards, cloud services, or manual inspection of outputs. There is no single offline command that gives you a numeric risk score before the model touches production.

NEO built Stochastic Gap Audit to fill that gap. It runs 100 prompts across five difficulty tiers, models response transitions as a Markov chain, and outputs a `reliability_score.csv` in under five minutes with no internet connection required.

## What the Stochastic Gap Measures

The **stochastic gap** is the difference between an ideal pass rate (95%) and the observed pass rate on your specific model. A gap of 0.12 means the model fails or hedges 12% more often than a production-grade system should.

Every response is classified as one of three states: PASS (correct, confident), UNCERTAIN (needs human review), or FAIL (wrong or refused). The tool treats consecutive responses as transitions in a Markov chain and builds a 3x3 **empirical transition matrix** from the data. From this matrix it derives:

- **Steady-state distribution** via eigendecomposition of the transposed matrix
- **Mean first passage time to FAIL** (MFPT), the average number of steps before a PASS state degrades to a FAIL
- **Oversight cost**, the fraction of prompts requiring human review

The MFPT metric is particularly useful in production contexts. A model with MFPT of 4 will degrade to failure roughly every four consecutive prompts, which is a concrete number you can compare against your expected request volume.

## The Five Prompt Tiers

The audit runs 100 curated prompts across five tiers, each weighted differently in the final score.

**Math and reasoning** (25 prompts, weight 1.0) covers arithmetic, algebra, probability, and geometry. These have unambiguous ground-truth answers that keyword matching can verify exactly.

**Code and logic** (25 prompts, weight 1.0) tests Python functions, SQL queries, complexity analysis, and architecture explanations. Expected keywords must appear in the response for a PASS.

**Factual knowledge** (25 prompts, weight 0.9) covers capitals, chemistry, history, and general science. These are the easiest tier but expose models that hallucinate common facts.

**Instruction following** (25 prompts, weight 0.8) asks for recipes, cover letters, poems, and how-to guides. The scorer checks for content-specific keywords rather than exact answers.

The weighting scheme means math and code failures penalize the score more heavily than instruction failures, which matches the cost profile of most production applications.

## Output Format

Every run writes a `reliability_score.csv` where each row is one prompt result. Key columns include `state`, `state_label`, `latency_ms`, `keyword_hits`, `keyword_total`, `hit_rate`, `weighted_score`, and `stochastic_gap`.

The CLI also prints a Rich-formatted summary table:

```
╭──────────────────────────────╮
│       Audit Summary          │
├─────────────────┬────────────┤
│ Reliability Score│ 82.0%     │
│ Pass Rate        │ 82.0%     │
│ Oversight Cost   │ 18.0%     │
│ Stochastic Gap   │ 13.0%     │
│ MFPT to Fail     │ 20.0 steps│
╰─────────────────┴────────────╯
```

The `--html` flag generates a self-contained HTML report with charts. The `--history` flag appends each run to `.audit_history.jsonl` and detects regressions between runs, useful for tracking whether a fine-tune improved or degraded the baseline.

## Comparing Two Models

The `--compare` flag runs both models and prints a side-by-side table. This is the fastest way to choose between two candidates before committing to one.

```bash
python audit.py --compare mistralai/mistral-small-2603 openai/gpt-5.4-nano
```

The `ModelComparator` runs each model through the same 100 prompts in sequence, building independent transition matrices and reliability scores. You get per-tier breakdowns for both models, so you can see whether one model is weak on code but strong on factual knowledge.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/stochastic-gap-audit
cd stochastic-gap-audit
pip install -r requirements.txt
```

Run a dry-run audit with no API key to verify everything works:

```bash
python audit.py --dry-run --model mistralai/mistral-small-2603
```

This uses the mock client, which simulates Markovian responses with realistic transition probabilities. For a real model audit via OpenRouter:

```bash
export OPENROUTER_API_KEY=sk-or-...
python audit.py --model mistralai/mistral-small-2603 --output-dir results/
```

To compare two models and save the CSV:

```bash
python audit.py --compare mistralai/mistral-small-2603 openai/gpt-5.4-nano --output-dir results/
```

To generate an HTML report and enable regression tracking:

```bash
python audit.py --model mistralai/mistral-small-2603 --html --history
```

The tool writes `outputs/reliability_score.csv` and optionally `outputs/audit_report.html`. The regression detector compares the current run against `.audit_history.jsonl` and prints a warning if any metric degrades beyond a threshold.

NEO built a five-minute, fully offline LLM reliability auditor that gives pre-deployment teams a numeric risk score with no dashboard required. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
