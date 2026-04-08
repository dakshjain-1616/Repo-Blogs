---
title: "Routing Sanity: Validation and Testing for LLM Router Configurations"
description: "NEO built a testing and validation suite that runs 200+ categorized prompts through an LLM routing configuration and produces a routing audit report with misrouting examples and accuracy scores."
date: 2026-04-08
tags: [routing, llm, testing, validation, infrastructure]
slug: routing-sanity
github: https://github.com/dakshjain-1616/routing-sanity
---

# Routing Sanity: Validation and Testing for LLM Router Configurations

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/routing-sanity)

![Pipeline Architecture](../public/images/diagrams/routing-sanity.png)

## The Problem

> LLM router configurations are written once and trusted forever — but nobody verifies that math questions actually reach the math-strong model or that cheap queries aren't silently getting routed to GPT-4.

NEO built Routing Sanity to run a structured test suite against any LLM router and produce a routing audit report showing exactly where the configuration breaks down.

## The Test Prompt Suite

**Routing Sanity** ships with 200+ hand-labeled test prompts across six routing categories: `math`, `code`, `simple`, `complex`, `creative`, and `factual`. Each prompt has an expected routing target defined as a model capability class rather than a specific model name — this keeps the test suite portable across different provider configurations.

The test manifest is a YAML file that maps prompts to expected routing outcomes:

```yaml
test_cases:
  - id: math_001
    prompt: "What is the eigenvalue decomposition of a 3x3 symmetric matrix?"
    expected_capability: math_strong
    expected_tier: capable
  - id: simple_003
    prompt: "What is the capital of France?"
    expected_capability: general
    expected_tier: cheap
  - id: code_017
    prompt: "Write a Rust implementation of a lock-free queue using atomics."
    expected_capability: code_strong
    expected_tier: capable
```

The runner sends each prompt through the configured router and intercepts the routing decision before the LLM call completes (using a mock completion layer), so the test suite runs in seconds without incurring full inference costs.

## Routing Validation Engine

The validation engine compares the router's actual routing decision against the expected capability class and tier. It supports four router integration modes: LiteLLM router configs, RouteLLM configurations, custom HTTP routers via a webhook spec, and OpenRouter model selection via API logging.

For each test case, the engine records the routed model, the capability class of that model (looked up from a configurable model registry), whether it matches the expected class, and the latency of the routing decision itself:

```bash
python routing_sanity.py \
  --router litellm \
  --config ./router_config.yaml \
  --test_suite ./suites/standard_200.yaml \
  --model_registry ./registries/openai_anthropic.yaml \
  --output report.html
```

Misrouting examples are extracted and grouped by failure type: `wrong_capability` (math question routed to a general model), `wrong_tier` (simple question hitting a capable/expensive model), and `routing_failure` (the router returned an error or timeout).

## Routing Audit Report

The audit report leads with a top-level routing accuracy score broken down by category:

| Category | Total | Correctly Routed | Accuracy |
|---|---|---|---|
| math | 40 | 31 | 77.5% |
| code | 45 | 42 | 93.3% |
| simple | 38 | 28 | 73.7% |
| complex | 35 | 33 | 94.3% |
| creative | 22 | 18 | 81.8% |
| factual | 30 | 27 | 90.0% |
| **overall** | **210** | **179** | **85.2%** |

Below the summary, each misrouted test case is listed with the prompt, the expected model class, the actual routed model, and a suggested fix. The fix suggestions are rule-based: if a math prompt routes to a general model, the report recommends adding a keyword-based routing rule for math terminology or adjusting the classifier's confidence threshold.

The report also flags **tier leakage** — simple queries routing to expensive models — and estimates the monthly cost impact based on configurable token volume assumptions.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build an LLM router testing suite that loads 200+ categorized test prompts from a YAML manifest, sends each through a LiteLLM or custom router configuration using a mock completion layer, compares routing decisions against expected capability classes and cost tiers, and generates an HTML audit report with per-category accuracy scores, misrouting examples, and cost impact estimates."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20an%20LLM%20router%20testing%20suite%20that%20loads%20200%2B%20categorized%20test%20prompts%20from%20a%20YAML%20manifest%2C%20sends%20each%20through%20a%20LiteLLM%20or%20custom%20router%20configuration%20using%20a%20mock%20completion%20layer%2C%20compares%20routing%20decisions%20against%20expected%20capability%20classes%20and%20cost%20tiers%2C%20and%20generates%20an%20HTML%20audit%20report%20with%20per-category%20accuracy%20scores%2C%20misrouting%20examples%2C%20and%20cost%20impact%20estimates." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a CI mode that fails the build if routing accuracy drops below a threshold, extend the test suite with domain-specific prompts for your use case, or build a live monitoring mode that samples production traffic and flags routing drift over time. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/routing-sanity
cd routing-sanity
pip install -r requirements.txt
python routing_sanity.py \
  --router litellm \
  --config ./examples/router_config.yaml \
  --test_suite ./suites/standard_200.yaml
```

Open `report.html` to see your routing accuracy breakdown, misrouting examples, and estimated cost leakage from tier violations.

NEO built a structured test harness that validates LLM router configurations against 200+ categorized prompts and surfaces misrouting patterns with actionable fix suggestions. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
