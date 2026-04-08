---
title: "Mobile LLM Benchmark Suite: Evaluating LLMs on Resource-Constrained Hardware"
description: "NEO built a benchmark suite that evaluates quantized LLMs on mobile and edge hardware across tokens per second, memory footprint, battery drain, and accuracy to produce hardware-specific deployment recommendations."
date: 2026-04-08
tags: [benchmarking, mobile, llm, inference, edge]
slug: mobile-llm-benchmark-suite
github: https://github.com/dakshjain-1616/mobile-llm-benchmark-suite
---

# Mobile LLM Benchmark Suite: Evaluating LLMs on Resource-Constrained Hardware

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/mobile-llm-benchmark-suite)

![Pipeline Architecture](../public/images/diagrams/mobile-llm-benchmark-suite.png)

## The Problem

> Quantized LLM benchmarks almost always run on server hardware. When you try to deploy a "mobile-ready" model on an actual Android device or Raspberry Pi, the numbers fall apart — thermal throttling kicks in, memory swapping destroys latency, and battery drain is disqualifying. There is no standard test harness for this.

NEO built Mobile LLM Benchmark Suite to bring structured, reproducible evaluation to the hardware tiers where on-device LLM deployment actually happens.

## Target Hardware and Model Formats

**Mobile LLM Benchmark Suite** targets three hardware tiers. **Android** devices are connected via ADB; the benchmark runner pushes the model binary and executor to the device, runs inference remotely, and pulls back metrics. **Raspberry Pi** (3B+ and 4B) and other ARM Linux boards run the benchmark agent natively over SSH. **ARM Macs** (M1/M2/M3) run locally using Metal Performance Shaders via `llama.cpp`'s Metal backend.

The suite supports GGUF-quantized models (Q4_K_M, Q5_K_M, Q8_0, and full F16 baseline) loaded via `llama.cpp`, and ONNX models for the Android execution path via ONNX Runtime Mobile. A model manifest YAML registers each model variant with its quantization level, file path, and expected accuracy tier:

```yaml
models:
  - name: qwen2.5-0.5b-q4
    format: gguf
    path: models/qwen2.5-0.5b-q4_k_m.gguf
    quantization: Q4_K_M
    baseline: qwen2.5-0.5b-f16
  - name: phi-3-mini-q5
    format: gguf
    path: models/phi-3-mini-q5_k_m.gguf
    quantization: Q5_K_M
    baseline: phi-3-mini-f16
```

## Metrics: From Tokens Per Second to Thermal Behavior

The suite collects five metrics per (model, hardware) pair. **Tokens per second** is measured as median throughput over 20 generation runs at a fixed prompt length (256 tokens) and fixed output length (128 tokens), with a 2-run warmup discarded. **Memory footprint** is the peak RSS reported by `/proc/self/status` on Linux targets or `ActivityManager` on Android during inference. **Battery drain** is measured as percentage of battery capacity consumed over a 10-minute continuous inference workload, sampled via `dumpsys battery` on Android or `upower` on Linux. **Thermal throttling** is detected by monitoring CPU frequency via `/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq` and flagging runs where frequency dropped more than 20% below the baseline clock. **Accuracy delta** compares model output against the full-precision baseline using BERTScore on a 100-sample evaluation set drawn from MMLU and HellaSwag.

```
Model               Hardware     TPS    Mem(MB)  Battery/hr  Throttled  Acc-Delta
──────────────────────────────────────────────────────────────────────────────────
qwen2.5-0.5b-q4    RPi 4B       4.2    312      11.4%       No         -1.8%
qwen2.5-0.5b-q4    Android 12   6.8    298      8.9%        Yes        -1.8%
phi-3-mini-q5      M2 Mac       47.3   1840     2.1%        No         -0.9%
phi-3-mini-q5      RPi 4B       2.1    1792     18.2%       Yes        -0.9%
```

## Mobile Readiness Score and Recommendations

After all metrics are collected, the suite computes a **composite mobile-readiness score** (0–100) per (model, hardware) pair using a weighted formula:

- Tokens per second (normalized to hardware class baseline): 35%
- Memory footprint vs. available RAM: 25%
- Battery drain rate: 20%
- Accuracy delta vs. baseline: 15%
- Thermal throttling penalty: 5% deduction if triggered

Scores are binned into tiers: **Deploy** (80+), **Acceptable** (60–79), **Marginal** (40–59), **Avoid** (<40). The report generator produces a hardware-specific recommendations section that lists the highest-scoring model for each target device and flags any models that triggered thermal throttling on more than 50% of runs.

Reports are written as JSON (for programmatic consumption), Markdown (for README embedding), and an interactive HTML page with sortable tables and a radar chart per hardware tier.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python benchmark suite for evaluating quantized LLMs on mobile and edge hardware — Android via ADB, Raspberry Pi via SSH, and ARM Macs locally. Measure tokens per second, peak memory, battery drain, thermal throttling, and accuracy delta vs. full-precision baseline. Compute a composite mobile-readiness score and generate JSON, Markdown, and HTML reports with hardware-specific deployment recommendations."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20Python%20benchmark%20suite%20for%20evaluating%20quantized%20LLMs%20on%20mobile%20and%20edge%20hardware%20%E2%80%94%20Android%20via%20ADB%2C%20Raspberry%20Pi%20via%20SSH%2C%20and%20ARM%20Macs%20locally.%20Measure%20tokens%20per%20second%2C%20peak%20memory%2C%20battery%20drain%2C%20thermal%20throttling%2C%20and%20accuracy%20delta%20vs.%20full-precision%20baseline.%20Compute%20a%20composite%20mobile-readiness%20score%20and%20generate%20JSON%2C%20Markdown%2C%20and%20HTML%20reports%20with%20hardware-specific%20deployment%20recommendations." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add support for a new hardware target, extend the accuracy evaluation with task-specific benchmarks, or build a CI integration that runs the suite on a connected device fleet after each model release. Each request builds on what's already there without re-explaining the context.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/mobile-llm-benchmark-suite
cd mobile-llm-benchmark-suite
pip install -r requirements.txt
python benchmark.py --config config.yaml --target rpi --output reports/
```

Point the config at your model files, specify the target hardware, and the suite produces a full benchmark report including a per-device readiness score and deployment recommendation.

NEO built a reproducible benchmark harness that evaluates quantized LLMs on real mobile and edge hardware, measuring five performance dimensions and producing a composite readiness score with deployment recommendations. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
