---
title: "LLM SLA Gatekeeper: Automated Deployment Gating for Language Models"
description: "NEO built a deployment gating tool that benchmarks LLMs against latency and throughput SLA profiles and returns a deterministic GO/NO-GO verdict with CI/CD exit codes."
date: 2026-03-28
tags: [llm, deployment, sla, benchmarking, ci-cd]
slug: llm-sla-gatekeeper
github: https://github.com/dakshjain-1616/llm-sla-gatekeeper
---

# LLM SLA Gatekeeper: Automated Deployment Gating for Language Models

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/llm-sla-gatekeeper)

![Pipeline Architecture](../public/images/diagrams/llm-sla-gatekeeper.png)

## The Problem

> Teams swap LLM versions, adjust hardware, or change quantization levels and have no automated check to confirm the new configuration meets latency and throughput requirements before traffic hits it. Manual spot-checks miss edge cases and are not reproducible.

NEO built LLM SLA Gatekeeper to run repeatable benchmarks against configurable SLA targets and return a deterministic PASS or FAIL with structured output and CI/CD-compatible exit codes.

## The Validation Pipeline

**LLM SLA Gatekeeper** runs a straightforward four-step process:

1. **Input** — provide a Hugging Face model ID or local path plus an SLA config with `max_latency_ms`, `min_throughput_tokens_per_sec`, and `max_cost_per_token`.
2. **Benchmark** — run `N` inference passes (default 5), collect per-token latency samples, compute p50, p95, average latency, and throughput.
3. **SLA Check** — compare results against thresholds: average latency, p95 latency (using a configurable multiplier), and throughput.
4. **Verdict** — emit PASS (exit 0) or FAIL (exit 1), with a confidence score, recommendations, and results appended to a JSONL history file.

The exit codes integrate directly with CI/CD: `0` is PASS, `1` is FAIL, `2` is ERROR.

## Built-in SLA Profiles

Five named profiles cover the common LLM deployment scenarios:

| Profile | Max Latency | Min Throughput | Use Case |
|---------|-------------|----------------|----------|
| `chatbot` | 150 ms | 10 tok/s | Interactive chat, customer support |
| `realtime` | 50 ms | 50 tok/s | Streaming, voice assistants |
| `batch` | 2000 ms | 1 tok/s | Document processing, summarization |
| `edge` | 500 ms | 2 tok/s | IoT, on-device inference |
| `dev` | 5000 ms | — | CI/CD dry runs, local development |

Every threshold is overridable via environment variable, so you can tune `SLA_PROFILE_CHATBOT_LATENCY_MS` without touching the code.

## Confidence Scoring

Every result includes a `confidence_score` between 0.0 and 1.0 that reflects how trustworthy the verdict is:

```
run_score   = min(n / 20.0, 1.0)
var_score   = max(0.0, 1.0 - (std / mean) × 2)
mode_factor = 1.0 (real hardware) | 0.75 (simulation)
confidence  = min(1.0, (run_score × 0.5 + var_score × 0.5) × mode_factor)
```

Simulation mode caps confidence at 0.75 because synthetic latency figures are estimates. Increase `--runs` to raise confidence on real hardware.

## Simulation Mode

When no GPU is available, simulation mode generates synthetic benchmark data using a linear formula:

```
latency_ms = 5 × model_size_in_B + 15
```

A 7B model yields 50 ms simulated latency. A 1.7B model yields 23.5 ms. This makes the tool practical for CI/CD pipelines on CPU-only runners.

## How to Build This

Clone the repo and install:

```bash
git clone https://github.com/dakshjain-1616/llm-sla-gatekeeper
cd llm-sla-gatekeeper
pip install -r requirements.txt
```

Validate a model against a named profile in simulation mode:

```bash
python run_validation.py --model=Qwen/Qwen3-8B --profile=chatbot --simulate
```

Use the Python API:

```python
from llm_sla_gatekeeper import validate_model, profile_to_sla_config, SLAValidator

# One-liner
result = validate_model("Qwen/Qwen3-8B", max_latency_ms=200, force_simulation=True)
print(result.status)           # "PASS" or "FAIL"
print(result.confidence_score) # 0.0–1.0

# Named profile
sla = profile_to_sla_config("chatbot")
validator = SLAValidator(force_simulation=True)
result = validator.validate("Qwen/Qwen3-8B", sla)
print(result.recommendations)
```

Add it to a GitHub Actions workflow:

```yaml
- name: SLA Gate
  run: |
    SLA_SIMULATION_MODE=1 python run_validation.py \
      --model=Qwen/Qwen3-8B \
      --profile=chatbot \
      --output=sla-result.json
```

Exit code 1 automatically blocks the merge or deployment. Save and export results:

```bash
python run_validation.py --model=Qwen/Qwen3-8B --profile=realtime --output-format=both
```

This produces JSON, CSV, and a self-contained HTML report. The JSONL history file at `outputs/history.jsonl` accumulates every run for longitudinal tracking across model versions.

Launch the Gradio UI for interactive validation:

```bash
python app.py
# → http://localhost:7860
```

The UI has four tabs: Validate, Compare (batch mode), History, and About.

NEO built a deployment gate that gives LLM teams a repeatable, CI-compatible answer to the question "is this model fast enough to ship." See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
