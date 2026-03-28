---
title: "LLM Consistency Monitor: Testing Whether Your Model Gives the Same Answer Twice"
description: "NEO built an LLM consistency monitoring tool that generates 20 paraphrased variants of a question, queries the model concurrently, and scores response consistency using embeddings and clustering."
date: 2026-03-09
tags: [LLM evaluation, model consistency, prompt testing, DBSCAN, sentence-transformers, AI reliability]
slug: llm-consistency-monitor
github: https://github.com/Dakshjain1604/LLM-consistency-Monitor
---

# LLM Consistency Monitor: Testing Whether Your Model Gives the Same Answer Twice

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dakshjain1604/LLM-consistency-Monitor)

![Pipeline Architecture](../public/images/diagrams/llm-consistency-monitor.png)

## The Problem

> LLMs are stochastic systems with real sensitivity to phrasing. The same question, rephrased or reworded, can produce meaningfully different answers. Most teams never test this — they write a set of example prompts, check that the responses look good, and deploy. For factual queries especially, that inconsistency is a reliability problem that only surfaces after users encounter it in production.

NEO built a tool specifically to surface it before you ship.

## What the Consistency Monitor Does

The pipeline runs four steps. First, it takes your question and generates **20 semantically identical paraphrases**. These are questions that ask the same thing but with different vocabulary, sentence structure, and phrasing. Then it sends all 20 variants to the model concurrently and collects every response. Then it analyzes those responses using embeddings and clustering to identify whether they are semantically consistent or whether the model is giving substantively different answers to what is nominally the same question.

The output is a consistency score from **0 to 100**, plus an interactive HTML report with visualizations.

## The Analysis Pipeline

### Embeddings and Clustering

Raw text comparison does not work well for semantic consistency. Two responses can be phrased completely differently and mean the same thing, or can look superficially similar while contradicting each other on key facts.

The monitor uses sentence-transformers to convert all 20 responses into embedding vectors that represent their semantic content. Then it runs DBSCAN clustering on those vectors. DBSCAN is a density-based clustering algorithm that groups responses with similar semantic content together without requiring you to specify the number of clusters upfront. The distribution of clusters tells you a great deal: a well-consistent model should produce one tight cluster. Multiple clusters indicate the model is giving categorically different answers.

### Fact Extraction and Contradiction Detection

Clustering tells you about surface-level semantic consistency. For deeper analysis, the monitor uses the Claude API to extract specific factual claims from each response and flag contradictions.

This catches a class of problem that embedding similarity misses. Two responses might be semantically similar in tone and structure but disagree on a specific fact. The fact extraction step finds that.

### Stress Testing Categories

NEO built five analytical modes that probe different dimensions of consistency:

- **Adversarial prompts**: inputs crafted to push the model toward different responses
- **Socratic questioning**: gradual reframings that approach the same question from different angles
- **Emotionally charged variations**: versions with added emotional framing or urgency
- **Ambiguous phrasing**: versions where the question could be interpreted multiple ways
- **Technical jargon**: versions using domain-specific vocabulary vs. plain language

Running all five gives you a comprehensive picture of where the model's consistency breaks down.

## Multi-Provider Support

The tool works with Claude (Sonnet 4), GPT-4, HuggingFace endpoints, and custom local models via HTTP. The configuration is straightforward: set your API keys in the environment file and specify which model to test.

Batch mode lets you test multiple questions from a JSON file in a single run, which is useful for systematic evaluation before a production release.

## Reading the Results

The HTML report includes a similarity heatmap across all 20 responses, cluster distribution charts, latency analysis, and prompt engineering suggestions based on where inconsistency was detected.

A score of **80% or above** generally indicates the model is consistent enough for production use on that question type. Below that, the report points to which phrasing variants are causing divergence, giving you concrete direction for prompt refinement.

## Who Needs This

Any team running a customer-facing LLM application on factual content. Legal research tools, medical information systems, financial advisories, customer support bots. If your application gives answers that users act on, consistency is not optional.

It is also useful during model evaluation and selection. Before you commit to a particular model or fine-tune for a specific domain, running consistency testing across your target question types tells you whether the model's reliability profile fits your requirements.

The full pipeline runs in **60 to 120 seconds** on typical hardware and uses approximately **2GB of memory**. It is fast enough to run as part of a pre-deployment evaluation workflow.

---

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python LLM consistency monitoring tool that takes a question, generates 20 semantically identical paraphrases using an LLM, sends all 20 variants to the target model concurrently, and analyzes consistency using sentence-transformers embeddings and DBSCAN clustering (density-based, no need to specify cluster count upfront). The distribution of clusters reveals whether the model gives one consistent answer or categorically different ones. Also run Claude API-based fact extraction on each response to catch contradictions that embedding similarity misses. Include five analytical modes: adversarial prompts, Socratic questioning, emotionally charged variations, ambiguous phrasing, and technical jargon vs. plain language. Output a consistency score 0-100 and an HTML report with a similarity heatmap across all 20 responses, cluster distribution chart, per-variant latency, and prompt refinement suggestions. Support Claude (Sonnet 4), [GPT-4](https://platform.openai.com/docs/models/gpt-4), HuggingFace endpoints, and custom local models via HTTP. No GPU required — CPU inference within 2 GB memory."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20Python%20LLM%20consistency%20monitoring%20tool%20that%20takes%20a%20question%2C%20generates%2020%20semantically%20identical%20paraphrases%20using%20an%20LLM%2C%20sends%20all%2020%20variants%20to%20the%20target%20model%20concurrently%2C%20and%20analyzes%20consistency%20using%20sentence-transformers%20embeddings%20and%20DBSCAN%20clustering%20%28density-based%2C%20no%20need%20to%20specify%20cluster%20count%20upfront%29.%20The%20distribution%20of%20clusters%20reveals%20whether%20the%20model%20gives%20one%20consistent%20answer%20or%20categorically%20different%20ones.%20Also%20run%20Claude%20API-based%20fact%20extraction%20on%20each%20response%20to%20catch%20contradictions%20that%20embedding%20similarity%20misses.%20Include%20five%20analytical%20modes%3A%20adversarial%20prompts%2C%20Socratic%20questioning%2C%20emotionally%20charged%20variations%2C%20ambiguous%20phrasing%2C%20and%20technical%20jargon%20vs.%20plain%20language.%20Output%20a%20consistency%20score%200-100%20and%20an%20HTML%20report%20with%20a%20similarity%20heatmap%20across%20all%2020%20responses%2C%20cluster%20distribution%20chart%2C%20per-variant%20latency%2C%20and%20prompt%20refinement%20suggestions.%20Support%20Claude%20%28Sonnet%204%29%2C%20GPT-4%2C%20HuggingFace%20endpoints%2C%20and%20custom%20local%20models%20via%20HTTP.%20No%20GPU%20required%20%E2%80%94%20CPU%20inference%20within%202%20GB%20memory." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation from that. From there you iterate — ask it to add batch mode that reads multiple questions from a JSON file and evaluates them in a single run saving results to an output directory, add the five stress-testing analytical modes with separate scores per mode, or add a score threshold flag that exits non-zero when consistency falls below a configurable value for CI/CD integration. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/Dakshjain1604/LLM-consistency-Monitor
cd LLM-consistency-Monitor
pip install -r requirements.txt
python monitor.py --question "What is the capital of France?" --model claude-sonnet-4
```

The full run completes in 60-120 seconds and opens an HTML report — a score above 80 means the model answers consistently across phrasings; below that, the report flags which paraphrase groups diverge and suggests prompt refinements.

NEO built an LLM consistency monitor where semantic clustering across 20 paraphrased variants exposes answer instability before it reaches users in production. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
