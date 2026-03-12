---
title: "Carbon-Aware Model Training: Cutting CO2 by 43% Without Sacrificing Accuracy"
description: "NEO built a PyTorch training pipeline that schedules workloads around real-time grid carbon intensity, achieving a 43.2% CO2 reduction while keeping model accuracy within 0.3% of baseline."
date: 2026-03-09
tags: [carbon-aware computing, sustainable ML, green AI, gradient accumulation, emissions tracking, PyTorch]
slug: carbon-aware-model-training
github: https://github.com/dakshjain-1616/CarbonAwareModelTraining
---

# Carbon-Aware Model Training: Cutting CO2 by 43% Without Sacrificing Accuracy

<a href="https://github.com/dakshjain-1616/CarbonAwareModelTraining" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">dakshjain-1616/CarbonAwareModelTraining</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/carbon-aware-model-training.png)

## The Problem

> Training machine learning models is expensive — not just in compute costs, but in carbon. Large training runs can produce hundreds of kilograms of CO2 depending on where and when they run, and most teams simply ignore this. There's no standard tooling to schedule training around cleaner energy windows or to measure emissions as a first-class metric alongside accuracy and loss.

The result is a PyTorch training pipeline that monitors real-time grid carbon intensity, schedules training during cleaner energy windows, and tracks emissions throughout the run. On MNIST with an RTX 3090, we achieved a **43.2% CO2 reduction** while keeping accuracy **within 0.3%** of baseline.

## The Core Insight: Timing Matters

Electrical grids are not constant. Carbon intensity varies based on what energy sources are feeding the grid at any given moment. Wind and solar generation push intensity down. Coal and gas push it up. In some regions, the difference between the cleanest and dirtiest hours of the day can exceed **300%**.

Training a model at the right time costs the same compute but produces significantly less carbon. The problem is that most training pipelines do not know or care about grid state. They run whenever you submit the job.

NEO built a scheduler that checks carbon intensity before starting a training run and can delay the start until conditions improve.

## Three Optimization Strategies Working Together

### Carbon-Aware Scheduling

The scheduler pulls real-time carbon intensity data from an electricity grid API. If the current intensity exceeds a configurable threshold, the run waits. If the API is unavailable, the system falls back to realistic mock patterns that approximate typical grid behavior for the configured region.

This alone accounts for most of the emissions reduction. Shifting training from a high-carbon window to a low-carbon window does not change the amount of compute you use. It changes what that compute costs the atmosphere.

### Gradient Accumulation

We combined carbon-aware scheduling with gradient accumulation, a memory optimization that lets you train with effectively larger batch sizes without proportionally larger GPU memory requirements.

The technique processes smaller mini-batches sequentially, accumulates their gradients, and only performs the weight update after accumulating gradients across what would have been the full batch. This reduces peak GPU memory usage by **45-60%** in our tests, without meaningfully affecting the loss landscape the optimizer sees.

This matters for carbon efficiency in a practical way. A smaller memory footprint means you can train on less expensive, more power-efficient hardware without degrading accuracy. It also enables mixed precision (FP16) training more reliably, which reduces power draw further.

### Continuous Emissions Tracking

We integrated CodeCarbon throughout the training loop. It monitors CO2 emissions, energy consumption, and power draw in real time. At the end of each run, it generates a JSON-formatted report comparing the optimized run against a baseline.

This is the piece most sustainability-focused teams are missing. You cannot improve what you do not measure. CodeCarbon makes the carbon cost of a training run a first-class metric alongside accuracy and loss.

## Results

Training on MNIST with an RTX 3090:

- **CO2 reduction: 43.2%**
- **Accuracy delta vs. baseline: within 0.3%**
- **GPU memory reduction: 45-60%**

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

<a href="https://youtu.be/71Se6aNaWTM" target="_blank" style="display:block;max-width:560px;margin:20px 0;border-radius:12px;overflow:hidden;border:1px solid #30363d;position:relative;cursor:pointer;text-decoration:none;">
  <img src="https://img.youtube.com/vi/71Se6aNaWTM/maxresdefault.jpg" alt="Watch on YouTube" style="width:100%;display:block;">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.72);border-radius:50%;width:68px;height:68px;display:flex;align-items:center;justify-content:center;">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>
  </div>
  <div style="position:absolute;bottom:12px;left:16px;background:rgba(0,0,0,0.7);color:#fff;font-size:12px;padding:4px 10px;border-radius:4px;font-family:sans-serif;">▶ Watch on YouTube</div>
</a>

---

NEO built a carbon-aware model training pipeline where grid carbon intensity and emissions tracking are first-class training metrics, not afterthoughts—delivering a 43% CO2 reduction without sacrificing accuracy. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)
