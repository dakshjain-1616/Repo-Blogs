---
title: "Carbon-Aware Model Training: Cutting CO2 by 43% Without Sacrificing Accuracy"
description: "NEO built a PyTorch training pipeline that schedules workloads around real-time grid carbon intensity, achieving a 43.2% CO2 reduction while keeping model accuracy within 0.3% of baseline."
date: 2026-03-09
tags: [carbon-aware computing, sustainable ML, green AI, gradient accumulation, emissions tracking, PyTorch]
slug: carbon-aware-model-training
github: https://github.com/dakshjain-1616/CarbonAwareModelTraining
---

# Carbon-Aware Model Training: Cutting CO2 by 43% Without Sacrificing Accuracy

[View the code on GitHub](https://github.com/dakshjain-1616/CarbonAwareModelTraining)

![Pipeline Architecture](/images/diagrams/carbon-aware-model-training.png)


Training machine learning models is expensive. Not just in compute costs, but in carbon. Large training runs can produce hundreds of kilograms of CO2 depending on where and when they run. Most teams simply ignore this. We decided to take it seriously and build tooling around it.

The result is a PyTorch training pipeline that monitors real-time grid carbon intensity, schedules training during cleaner energy windows, and tracks emissions throughout the run. On MNIST with an RTX 3090, we achieved a 43.2% CO2 reduction while keeping accuracy within 0.3% of baseline.

## The Core Insight: Timing Matters

Electrical grids are not constant. Carbon intensity varies based on what energy sources are feeding the grid at any given moment. Wind and solar generation push intensity down. Coal and gas push it up. In some regions, the difference between the cleanest and dirtiest hours of the day can exceed 300%.

Training a model at the right time costs the same compute but produces significantly less carbon. The problem is that most training pipelines do not know or care about grid state. They run whenever you submit the job.

We built a scheduler that checks carbon intensity before starting a training run and can delay the start until conditions improve.

## Three Optimization Strategies Working Together

### Carbon-Aware Scheduling

The scheduler pulls real-time carbon intensity data from an electricity grid API. If the current intensity exceeds a configurable threshold, the run waits. If the API is unavailable, the system falls back to realistic mock patterns that approximate typical grid behavior for the configured region.

This alone accounts for most of the emissions reduction. Shifting training from a high-carbon window to a low-carbon window does not change the amount of compute you use. It changes what that compute costs the atmosphere.

### Gradient Accumulation

We combined carbon-aware scheduling with gradient accumulation, a memory optimization that lets you train with effectively larger batch sizes without proportionally larger GPU memory requirements.

The technique processes smaller mini-batches sequentially, accumulates their gradients, and only performs the weight update after accumulating gradients across what would have been the full batch. This reduces peak GPU memory usage by 45-60% in our tests, without meaningfully affecting the loss landscape the optimizer sees.

This matters for carbon efficiency in a practical way. A smaller memory footprint means you can train on less expensive, more power-efficient hardware without degrading accuracy. It also enables mixed precision (FP16) training more reliably, which reduces power draw further.

### Continuous Emissions Tracking

We integrated CodeCarbon throughout the training loop. It monitors CO2 emissions, energy consumption, and power draw in real time. At the end of each run, it generates a JSON-formatted report comparing the optimized run against a baseline.

This is the piece most sustainability-focused teams are missing. You cannot improve what you do not measure. CodeCarbon makes the carbon cost of a training run a first-class metric alongside accuracy and loss.

## Results

Training on MNIST with an RTX 3090:

- CO2 reduction: 43.2%
- Accuracy delta vs. baseline: within 0.3%
- GPU memory reduction: 45-60%

Training time increased. That is the honest tradeoff. If you delay a run waiting for a cleaner grid window, it does not start immediately. For many workloads, that is an acceptable cost. Nightly retraining jobs, batch fine-tuning runs, evaluation pipelines. These are all schedulable.

For jobs that need to start immediately, the system can run without the scheduling delay and still benefit from gradient accumulation and emissions tracking.

## Technical Setup

The stack is Python 3.8+ with PyTorch 2.0+ and CodeCarbon. Configuration is YAML-based, so you specify your training parameters, carbon intensity threshold, target region, and gradient accumulation steps in a single file. CUDA is detected automatically with CPU fallback.

The codebase is split into clean modules: the scheduler handles carbon monitoring, the tracker handles emissions measurement, and the trainer handles the optimization loop. They are independently testable and composable.

## Who This Is For

The most immediate audience is ML teams with regular retraining workflows who want to reduce environmental impact without switching infrastructure. If you are retraining models daily or weekly, carbon-aware scheduling compounds over time.

It is also useful for any organization with emissions reporting requirements. The CodeCarbon integration produces structured, quantified emissions data that sustainability reports actually need, not estimates or rough calculations.

Longer term, as energy costs and carbon pricing become more significant factors in infrastructure decisions, building carbon awareness into your ML pipeline from the start is good engineering practice.

## Watch It in Action

We put together a video walkthrough of the pipeline in action, showing the carbon intensity scheduler, gradient accumulation, and the live CodeCarbon emissions readout.

**[Watch on YouTube](https://youtu.be/71Se6aNaWTM)**

---

NEO builds ML systems that account for the full cost of what they do. Carbon is part of that cost.

See more at [heyneo.so](https://heyneo.so).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [NEO in Cursor](cursor:extension/NeoResearchInc.heyneo)
