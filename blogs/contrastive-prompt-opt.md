---
title: "Contrastive Prompt Optimizer: Learning Better Prompts from Success and Failure"
description: "NEO built a prompt optimization tool that uses contrastive learning to iteratively improve prompts by analyzing what separates successful outputs from failing ones."
date: 2026-04-08
tags: [prompt-engineering, optimization, llm, contrastive-learning, evaluation]
slug: contrastive-prompt-opt
github: https://github.com/dakshjain-1616/contrastive-prompt-opt
---

# Contrastive Prompt Optimizer: Learning Better Prompts from Success and Failure

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/contrastive-prompt-opt)

![Pipeline Architecture](../public/images/diagrams/contrastive-prompt-opt.png)

## The Problem

> Most prompt optimization approaches treat prompts as independent experiments — try one, score it, try another. They miss the signal hiding in the relationship between successes and failures.

NEO built Contrastive Prompt Optimizer to exploit that signal directly: by collecting pairs of prompts and outputs, identifying the contrastive patterns between what worked and what failed, and using those patterns to steer gradient-free optimization toward better prompts.

## Contrastive Pair Collection and Scoring

**Contrastive Prompt Optimizer** begins by running automatic A/B scoring over a prompt pool. Each candidate prompt is executed against a shared evaluation dataset and scored using a configurable metric — exact match accuracy, ROUGE-L, semantic similarity, or a custom LLM-as-judge rubric. The outputs are then sorted into a positive set (high-scoring) and a negative set (low-scoring) based on a configurable threshold.

The core data structure is a `ContrastivePair`: a tuple of `(positive_prompt, positive_output, negative_prompt, negative_output, task_input)`. Pairs are only valid when the two prompts received meaningfully different scores on the same input — a delta of at least `min_score_gap` (default 0.15). This filtering step ensures the optimizer is learning from genuinely informative contrasts rather than noisy variation.

```python
pair = ContrastivePair(
    positive_prompt="You are a precise JSON extractor...",
    negative_prompt="Extract the JSON from the following:",
    task_input="Order details: name=Alice, qty=3",
    score_delta=0.42,
)
```

Pairs are stored in a local SQLite database and deduplicated by prompt hash before being passed to the optimizer.

## Gradient-Free Optimization via Contrastive Analysis

With a library of contrastive pairs, the optimizer runs a meta-analysis step using an Analyzer LLM. The Analyzer reads a batch of positive/negative pairs and produces a structured report: which elements of positive prompts are absent from negative ones, what phrasing patterns correlate with high scores, and which constraints or examples appear to be load-bearing.

This report becomes the rewrite instruction for the next candidate generation step. The Generator LLM produces `n_candidates` (default 5) new prompt variants, each required to incorporate the identified positive patterns while avoiding the negative ones. This is gradient-free — no backpropagation, no differentiable loss — just structured reasoning about what distinguishes good outputs from bad ones.

The loop runs for a configurable number of rounds. Each round extends the pair library with new high/low examples, giving the Analyzer more signal. Score progression and pair library growth are logged to `optimization_run.json` after every round.

## DSPy-Compatible Interface

The optimizer exposes a DSPy-compatible `ContrastiveOptimizer` class that drops into any DSPy pipeline as a teleprompter-style optimizer. It wraps the pair collection and meta-analysis steps behind the standard `compile()` interface, so teams already using DSPy can adopt contrastive optimization without restructuring their codebase.

```python
from contrastive_prompt_opt import ContrastiveOptimizer

optimizer = ContrastiveOptimizer(
    metric=my_metric,
    n_rounds=4,
    n_candidates=5,
    min_score_gap=0.15,
)
compiled_program = optimizer.compile(my_dspy_program, trainset=trainset)
```

Outside of DSPy, the `StandaloneOptimizer` class accepts a plain Python callable as the prompt executor, making integration with LangChain, direct API calls, or local models equally straightforward.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a contrastive prompt optimization tool in Python. Collect pairs of high-scoring and low-scoring prompt outputs on a shared evaluation dataset, use an Analyzer LLM to identify what patterns separate the successful prompts from the failing ones, and use those patterns to generate improved prompt candidates. Support gradient-free optimization across multiple rounds, store contrastive pairs in SQLite, log score progression to JSON, and expose a DSPy-compatible compile interface."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20contrastive%20prompt%20optimization%20tool%20in%20Python.%20Collect%20pairs%20of%20high-scoring%20and%20low-scoring%20prompt%20outputs%20on%20a%20shared%20evaluation%20dataset%2C%20use%20an%20Analyzer%20LLM%20to%20identify%20what%20patterns%20separate%20the%20successful%20prompts%20from%20the%20failing%20ones%2C%20and%20use%20those%20patterns%20to%20generate%20improved%20prompt%20candidates.%20Support%20gradient-free%20optimization%20across%20multiple%20rounds%2C%20store%20contrastive%20pairs%20in%20SQLite%2C%20log%20score%20progression%20to%20JSON%2C%20and%20expose%20a%20DSPy-compatible%20compile%20interface." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add support for LLM-as-judge scoring, build a dashboard that visualizes pair library growth across rounds, or extend the DSPy interface with teleprompter chaining. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/contrastive-prompt-opt
cd contrastive-prompt-opt
pip install -r requirements.txt
python main.py --task sentiment --rounds 4
```

Point it at your own evaluation dataset and initial prompt candidates to run contrastive optimization on any classification or generation task.

NEO built a contrastive prompt optimizer that learns from success/failure pairs and uses structured meta-analysis to iteratively generate better prompts without gradient computation. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
