---
title: "LLM Consistency Monitor: Testing Whether Your Model Gives the Same Answer Twice"
description: "NEO built an LLM consistency monitoring tool that generates 20 paraphrased variants of a question, queries the model concurrently, and scores response consistency using embeddings and clustering."
date: 2026-03-09
tags: [LLM evaluation, model consistency, prompt testing, DBSCAN, sentence-transformers, AI reliability]
slug: llm-consistency-monitor
github: https://github.com/Dakshjain1604/LLM-consistency-Monitor
---

# LLM Consistency Monitor: Testing Whether Your Model Gives the Same Answer Twice

<a href="https://github.com/Dakshjain1604/LLM-consistency-Monitor" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">Dakshjain1604/LLM-consistency-Monitor</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

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

We use sentence-transformers to convert all 20 responses into embedding vectors that represent their semantic content. Then we run DBSCAN clustering on those vectors. DBSCAN is a density-based clustering algorithm that groups responses with similar semantic content together without requiring you to specify the number of clusters upfront. The distribution of clusters tells you a great deal: a well-consistent model should produce one tight cluster. Multiple clusters indicate the model is giving categorically different answers.

### Fact Extraction and Contradiction Detection

Clustering tells you about surface-level semantic consistency. For deeper analysis, we use the Claude API to extract specific factual claims from each response and flag contradictions.

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

NEO built an LLM consistency monitor where semantic clustering across 20 paraphrased variants exposes answer instability before it reaches users in production. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)

---
