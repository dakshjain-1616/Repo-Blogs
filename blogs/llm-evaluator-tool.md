---
title: "Automated LLM Evaluation: How We Built a Tool to Find the Best Model for Any Task"
description: "We built an LLM evaluator that automatically generates test cases, benchmarks candidate models, and uses a Judge LLM to rank them with an optimized system prompt for your specific task."
date: 2026-03-09
tags: ["LLM evaluation", "model selection", "benchmarking", "Judge LLM", "AI tooling", "prompt optimization", "machine learning"]
slug: llm-evaluator-tool
github: https://github.com/gauravvij/llm-evaluator
---

# Automated LLM Evaluation: How We Built a Tool to Find the Best Model for Any Task

[View the code on GitHub](https://github.com/gauravvij/llm-evaluator)

Choosing the right LLM for a production task is harder than it looks. Leaderboard rankings tell you how models perform on academic benchmarks. They tell you very little about how a model will perform on your specific task, with your input distribution, evaluated against criteria that matter to your use case.

We built a tool that answers the actual question: given a task description, which model performs best on that task?

## The Problem with Manual Evaluation

The standard approach is to pick a few models, manually write some test prompts, run them, read the outputs, and form an opinion. This works for early exploration. It doesn't scale. Manual evaluation is slow, subjective, and expensive to repeat when your task requirements change or new models are released.

You also end up with selection bias. Humans evaluate LLM outputs inconsistently, especially across multiple dimensions simultaneously. You might notice factual errors but miss subtle hallucinations. You might prefer a confident-sounding response over an accurate but hedged one.

A systematic, automated evaluation process produces better results and can be re-run cheaply.

## How the Evaluator Works

The pipeline has five steps that run automatically from a single task description.

**Test case generation.** The tool generates tailored test cases for your task. Not generic questions, but inputs designed to probe the specific capabilities and failure modes relevant to what you're building. By default it generates five test cases, configurable via CLI flag.

**Model discovery.** The tool identifies top candidate models to benchmark. Up to six candidates by default. These aren't randomly selected. The discovery step considers which models are likely to perform well given the task characteristics.

**Benchmark execution.** Every candidate model runs every test case. Responses are collected and stored.

**Judge LLM evaluation.** A Judge LLM, using Gemini Pro, evaluates each response across five dimensions: accuracy, hallucination detection, grounding, tool-calling ability, and response clarity. Each dimension is scored independently, so you can inspect the breakdown rather than just a single overall score.

**Ranking and prompt optimization.** The top three models are ranked by performance. The tool also produces an optimized system prompt tailored to your use case and the winning model's characteristics.

## Why a Judge LLM?

Human evaluation is inconsistent. Rule-based evaluation is too rigid for open-ended text. A well-prompted Judge LLM hits a useful middle ground: consistent, multi-dimensional, and flexible enough to evaluate responses that don't have a single right answer.

The key design choice is using a separate, capable model as the judge rather than having each model evaluate itself or its competitors. Self-evaluation produces obvious biases. Cross-model evaluation is cleaner.

Separating judge and candidate also means you can upgrade the judge independently as better models become available, without changing the rest of the pipeline.

## Evaluation Dimensions

The five scoring dimensions capture different aspects of response quality:

**Accuracy** measures whether the response is factually correct relative to ground truth or verifiable facts.

**Hallucination detection** looks at whether the model invents plausible-sounding but false information. This dimension is often the most important for production applications.

**Grounding** assesses whether claims are supported by the provided context or evidence rather than stated without backing.

**Tool-calling ability** matters for agentic applications where the model needs to decide when and how to use tools.

**Response clarity** evaluates whether the answer is well-organized and easy to understand, independent of its accuracy.

Getting a separate score for each dimension lets you make task-specific tradeoffs. For a fact-checking application, accuracy and hallucination scores matter most. For a customer-facing assistant, clarity might rank higher.

## Running the Tool

Setup is quick. Clone the repository, create a virtual environment, install from `requirements.txt`, and set your OpenRouter API key in a `.env` file. Then run:

```
python main.py --task "your task description here"
```

The tool handles everything from there. You get a ranked list of the top three models, per-dimension performance metrics, and an optimized system prompt ready to use.

Optional flags let you adjust the number of test cases (`--test-cases`), the maximum number of candidates (`--max-candidates`), and the output directory (`--output-dir`).

## Real Applications

**Model selection for new projects.** Before committing to a model for a production system, run the evaluator on your actual task. A few minutes of compute time will save hours of debugging later.

**Regression testing after model updates.** When a model provider releases a new version, re-run the evaluation to check whether performance changed on your task before updating.

**Cost-performance analysis.** The ranking combines with pricing information to help you decide whether a cheaper model is close enough in performance to justify the cost savings.

**Prompt engineering.** The optimized system prompt output is a starting point for prompt engineering, grounded in observed model behavior rather than intuition.

## Evaluation is Infrastructure

Good model evaluation is infrastructure, not a one-time activity. The teams that build reliable AI systems treat evaluation as a continuous process. They run it before deploying, after updating, and when their task requirements change.

The goal of this tool is to make continuous evaluation cheap and systematic enough that teams actually do it.

## Build Reliable AI Systems

If you're building production ML systems and need help with evaluation infrastructure, model selection, or end-to-end pipeline design, this is what we do at NEO.

Learn more at [heyneo.so](https://heyneo.so/).
