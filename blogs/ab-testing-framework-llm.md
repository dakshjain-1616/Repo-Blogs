---
title: "Beyond A/B: Building a Multi-Variant LLM Testing Framework with Statistical Rigor"
description: "NEO built a production-ready A/B/n testing framework for LLMs that supports 3+ model variants, uses ANOVA and Bonferroni correction for statistical analysis, and adds under 0.5ms routing overhead."
date: 2026-03-09
tags: [A/B testing, LLM evaluation, statistical analysis, model comparison, ANOVA, machine learning]
slug: ab-testing-framework-llm
github: https://github.com/dakshjain-1616/AB-testing-tool
---

# Beyond A/B: Building a Multi-Variant LLM Testing Framework with Statistical Rigor

<a href="https://github.com/dakshjain-1616/AB-testing-tool" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">dakshjain-1616/AB-testing-tool</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/ab-testing-framework-llm.png)

## The Problem

> Most A/B testing frameworks are built for binary outcomes: click or no-click, convert or bounce. LLM evaluation is fundamentally different. When testing multiple prompt templates, model sizes, and fine-tuned variants simultaneously, running pairwise t-tests inflates your false positive rate — test five variants and you have ten simultaneous tests, each with a 5% chance of a spurious result. Standard tooling simply wasn't built for this.

NEO autonomously built a multi-variant testing framework from the ground up, designed specifically for ML systems. It supports N variants simultaneously, uses proper statistical corrections for multiple comparisons, and adds **under 0.5ms** of routing overhead per request.

## How the Framework Works

The system runs four stages in sequence.

### Deterministic Routing

Incoming requests get assigned to variants using MD5-based hashing on a user or session identifier. This is deterministic. The same user always hits the same variant. That matters because it eliminates the noise you get when the same user experiences multiple variants inconsistently.

Routing overhead is under 0.5ms. It is not a bottleneck.

### Async Metric Collection

Metric logging is fully asynchronous. We use a queue-based system so logging never blocks the request path. Total logging overhead stays **under 1ms** per request. In high-throughput production environments, non-blocking collection is not optional.

We track response quality scores, latency, token usage, and any custom metrics you define per experiment.

### Statistical Analysis

This is where the framework earns its keep. For continuous metrics across N variants, we run one-way ANOVA first. If that test shows a statistically significant difference somewhere in the group, we move to pairwise comparisons with Bonferroni correction.

Bonferroni correction adjusts the significance threshold for each individual test based on the total number of comparisons being made. It keeps the family-wise error rate under control. For categorical outcomes, we use Chi-Square tests with the same correction applied.

Every result comes with confidence intervals and effect sizes, not just p-values. A statistically significant result with a tiny effect size might not be worth shipping.

### Automated Reporting

The output is a full report with publication-ready visualizations, effect size tables, and JSON export for downstream integration. Results are ready to share with a team or feed into another system without manual processing.

## Configuration and Integration

The framework is YAML-configured. You define your variants, traffic splits, metrics to track, and experiment duration. Results accumulate in CSV format for immediate analysis.

There is a FastAPI endpoint for model serving, so you can integrate this directly into an existing ML serving stack. Teams running online experiments do not need a separate infrastructure layer.

## Real Use Cases

The most common use case is prompt template comparison. You have a system prompt you wrote six months ago and a new version. You want to know if the new one actually improves response quality across a real distribution of user queries, not just the five examples you tested manually.

Other uses: **comparing model sizes** (does the 70B variant meaningfully outperform the 13B on your specific task?), **evaluating fine-tuned vs. base models**, **testing different retrieval strategies** in a RAG system.

The framework handles all of these. As long as you can define a metric, you can test it.

## What Rigorous Testing Actually Buys You

The alternative to proper statistical testing is intuition-driven decisions. Someone looks at a sample of 20 responses, decides one prompt "feels better," and ships it. That works sometimes and fails silently much of the time.

With this framework, you get confidence intervals that tell you the true effect size range. You get correction for multiple comparisons so you are not chasing noise. You get effect sizes so you know whether a statistically significant improvement is actually large enough to matter in practice.

That is the difference between shipping a hunch and shipping a measured improvement.

---

NEO built a multi-variant LLM testing framework where rigorous statistical evaluation—ANOVA, Bonferroni correction, effect sizes—is a first-class concern, not an afterthought. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)

---
