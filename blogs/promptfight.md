---
title: "PromptFight: Statistical A/B Testing for LLM Prompts"
description: "NEO built a lightweight Python tool that runs two prompts head-to-head across any LLM and reports win rates, latency, cost, and token counts with statistical validation."
date: 2026-03-28
tags: [prompts, llm, evaluation, a-b-testing, python]
slug: promptfight
github: https://github.com/dakshjain-1616/promptfight
---

# PromptFight: Statistical A/B Testing for LLM Prompts

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/promptfight)

![Pipeline Architecture](../public/images/diagrams/promptfight.png)

## The Problem

> Choosing between two prompt formulations usually comes down to intuition or a handful of manual tests. That process produces no statistical confidence and misses latency and cost differences that matter in production. Running a proper A/B test requires either a framework with significant overhead or custom evaluation infrastructure that takes time to build.

NEO built PromptFight to run prompt comparisons with statistical rigor and no framework overhead. It calls OpenAI and Anthropic APIs directly through Python's `urllib` module, tracks win rates using the Mann-Whitney U test, and reports latency, cost, and token counts per run.

## No SDK Overhead

PromptFight's core design decision is to avoid importing openai, anthropic, or any other large SDK at runtime. All API calls go through Python's standard library `urllib.request`, with JSON payloads and response parsing handled manually.

This keeps the install size small and makes the HTTP layer visible and auditable. The request format for each provider is a thin wrapper in the codebase. If a provider changes their API schema, the fix is a one-line change to a dictionary, not a version bump of a transitive dependency.

The only optional dependencies are `scipy` and `numpy`, used for the Mann-Whitney U test. If those are absent, PromptFight skips statistical significance reporting and returns raw win counts.

## Running a Fight

The `fight()` function is the primary entry point. It takes two prompt templates with an `{input}` placeholder, a list of models to test against, and a number of runs.

```python
from promptfight import fight

results = fight(
    prompt_a="Summarize: {input}",
    prompt_b="TL;DR: {input}",
    user_input="Your text here",
    models=["mock"],
    runs=5
)
```

Each run sends both prompts to the specified model and scores the responses using the configured judge. Scores are collected across all runs and passed to the Mann-Whitney U test to determine whether the difference in win rates is statistically significant at the p < 0.05 level.

The `mock` model runs offline with no API key and returns synthetic responses in milliseconds. It is the right starting point when verifying prompt logic before spending on live API calls.

## Multi-Model Testing and Judging

**Multi-model support** runs both prompts against every model in the list and reports separate results per model. This is useful when the same prompt pair behaves differently across providers. A prompt optimized for GPT-5.4 Nano may perform worse than the baseline on Claude 3.5 Sonnet, where longer context and different tokenization change the output distribution.

The **judge** is the component that scores each response. PromptFight supports two judge modes. The heuristic judge scores responses based on configurable criteria: length, keyword presence, structural elements like lists and headers, and absence of refusals. The LLM judge sends each response to a separate model evaluation call, asking the judge model to rate response quality on a fixed rubric. The LLM judge produces more nuanced scores but costs more and adds latency.

For most prompt iteration workflows, the heuristic judge is accurate enough to distinguish meaningful prompt differences across 10 to 20 runs.

## Output Formats

PromptFight reports results in three formats.

The **table** format prints a formatted comparison to stdout: win rates, average score per prompt, average latency, total token count, and estimated cost per run. This is the default output for interactive use.

The **JSON** format writes a structured object with the full run-by-run breakdown. Each entry includes the prompt used, model response, score, latency in milliseconds, token count, and cost in USD. JSON output is the right choice for downstream analysis or logging to a metrics system.

The **CSV** format produces a flat table compatible with spreadsheet tools and Pandas. Column names are stable across versions, making it safe to use as input to a recurring comparison pipeline.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/promptfight
cd promptfight
pip install -r requirements.txt
```

For statistical significance testing, also install scipy and numpy if not already present:

```bash
pip install scipy numpy
```

Run a comparison with the mock model to verify the setup:

```bash
python -m promptfight \
  --prompt-a "Summarize: {input}" \
  --prompt-b "TL;DR: {input}" \
  --input "The quick brown fox jumps over the lazy dog." \
  --model mock \
  --runs 5
```

To test against a real model, set the API key and switch the model flag:

```bash
export OPENAI_API_KEY=sk-...
python -m promptfight \
  --prompt-a "Summarize: {input}" \
  --prompt-b "Give a one-sentence summary of: {input}" \
  --input "Your production text here" \
  --model gpt-4o-mini \
  --runs 20 \
  --output json > results.json
```

With 20 runs and a real model, PromptFight has enough data to run the Mann-Whitney U test and report a p-value alongside the win rates. A p-value below 0.05 means the observed win rate difference is unlikely to be random noise at that sample size.

NEO built PromptFight to make rigorous prompt comparison as fast as running a single test, using direct API calls and statistical validation without framework overhead. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
