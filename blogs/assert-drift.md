---
title: "AssertDrift: Detecting Behavioral Drift in LLM Outputs Over Time"
description: "NEO built a tool that runs a fixed prompt test suite against an LLM at regular intervals, flags semantic drift beyond a configurable threshold, and tracks output stability across model updates."
date: 2026-04-08
tags: [llm, testing, drift, evaluation, regression]
slug: assert-drift
github: https://github.com/dakshjain-1616/AssertDrift
---

# AssertDrift: Detecting Behavioral Drift in LLM Outputs Over Time

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/AssertDrift)

![Pipeline Architecture](../public/images/diagrams/assert-drift.png)

## The Problem

> LLM APIs change underneath you. A model update, a silent prompt caching change, or a new RLHF round can shift outputs in ways that break downstream behavior without throwing a single error. By the time users notice, the drift has been in production for weeks.

NEO built AssertDrift to give teams a continuous regression test for LLM behavior — not just a one-time evaluation, but an ongoing measurement that catches drift the moment it exceeds an acceptable threshold.

## Test Suite Design and Baseline Capture

**AssertDrift** is built around a fixed prompt test suite stored in `prompts/`. Each prompt is a YAML file that specifies the input, any system prompt, and optional metadata tags for grouping:

```yaml
id: summarization-001
tags: [summarization, factual]
system: "You are a concise assistant."
prompt: "Summarize the water cycle in two sentences."
```

On the first run, AssertDrift captures a **baseline snapshot**: it runs every prompt against the target model, records the full response, and stores the embedding of that response alongside the raw text in `baselines/<model_id>/<run_id>.json`. All subsequent runs are measured against this baseline.

Embeddings are generated using a local sentence-transformer model (`all-MiniLM-L6-v2` by default, swappable via config). Using a local embedding model rather than the same API being tested ensures that embedding drift does not confound behavioral drift measurement.

## Drift Detection and Threshold Configuration

Each scheduled run re-runs every prompt and computes the **cosine distance** between the current response embedding and the baseline embedding. Distance values range from 0 (identical semantic content) to 2 (maximally different). A configurable `drift_threshold` (default: 0.15) separates acceptable variation from flagged drift.

When a prompt crosses the threshold, AssertDrift records the drift event with the before-and-after responses, the cosine distance, and a semantic diff that highlights which concepts appeared, disappeared, or changed emphasis:

```
DRIFT DETECTED: summarization-001
  Distance: 0.23 (threshold: 0.15)
  Baseline: "Water evaporates from surfaces and rises as vapor; it then condenses into clouds and falls as precipitation."
  Current:  "The water cycle involves evaporation, cloud formation, and rainfall, driven by solar energy and gravity."
  Δ concepts: +[solar energy, gravity] -[surfaces, rises as vapor]
```

**Prompt sensitivity analysis** runs automatically: prompts are ranked by their average drift distance across all runs. This identifies which prompts are most sensitive to model changes — useful for building a minimal canary test set that catches drift early without running the full suite.

## Model Version Comparison and Dashboard

AssertDrift supports **model version comparison**: point it at two different model endpoints (or two API keys routing to different model versions) and it runs the full test suite against both simultaneously, producing a side-by-side drift report showing which prompts diverge between versions and by how much.

The **drift dashboard** (`dashboard/index.html`) renders an interactive time-series chart for each prompt tag group, showing average drift distance per run over time. Drift events are marked as vertical bands. The dashboard reads directly from the `runs/` directory — no backend required, just open the HTML file after each run.

Scheduling is handled externally (cron or CI pipeline). AssertDrift provides a `--ci-mode` flag that exits with code 1 when any prompt exceeds threshold, making it straightforward to gate deployments:

```bash
# In CI pipeline
python assert_drift.py --suite prompts/ --model gpt-4o --ci-mode --threshold 0.15
```

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python tool called AssertDrift that runs a fixed YAML prompt test suite against an LLM at regular intervals, captures response embeddings using a local sentence-transformer, computes cosine distance from baseline to detect drift, flags prompts exceeding a configurable threshold, ranks prompts by sensitivity, supports model version comparison, and generates an interactive HTML drift dashboard with time-series charts per prompt group."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20Python%20tool%20called%20AssertDrift%20that%20runs%20a%20fixed%20YAML%20prompt%20test%20suite%20against%20an%20LLM%20at%20regular%20intervals%2C%20captures%20response%20embeddings%20using%20a%20local%20sentence-transformer%2C%20computes%20cosine%20distance%20from%20baseline%20to%20detect%20drift%2C%20flags%20prompts%20exceeding%20a%20configurable%20threshold%2C%20ranks%20prompts%20by%20sensitivity%2C%20supports%20model%20version%20comparison%2C%20and%20generates%20an%20interactive%20HTML%20drift%20dashboard%20with%20time-series%20charts%20per%20prompt%20group." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add Slack alerting when drift events are detected, build a prompt editor UI for managing the test suite, or extend version comparison to diff across three or more model checkpoints. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/AssertDrift
cd AssertDrift
pip install -r requirements.txt
python assert_drift.py --suite prompts/ --model gpt-4o --capture-baseline
python assert_drift.py --suite prompts/ --model gpt-4o --threshold 0.15
```

Run the first command once to capture the baseline, then schedule the second command on a cron job or in your CI pipeline.

NEO built AssertDrift, a continuous LLM behavioral regression tool that detects semantic drift in model outputs using embedding cosine distance, tracks drift over time on a per-prompt basis, and integrates into CI pipelines with a single flag. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
