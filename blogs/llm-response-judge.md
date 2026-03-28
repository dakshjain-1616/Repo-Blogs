---
title: "LLM Response Judge: Automated Quality Evaluation with Customizable Rubrics"
description: "NEO built a web app for automated LLM response evaluation using customizable weighted rubrics, multi-provider support, and per-criterion scoring with justifications. React frontend, FastAPI backend."
date: 2026-03-09
tags: [LLM evaluation, response quality, rubric scoring, FastAPI, React, automated evaluation]
slug: llm-response-judge
github: https://github.com/Dakshjain1604/LLM-response-Judge
---

# LLM Response Judge: Automated Quality Evaluation with Customizable Rubrics

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dakshjain1604/LLM-response-Judge)

![Pipeline Architecture](../public/images/diagrams/llm-response-judge.png)

## The Problem

> Manual evaluation of LLM responses does not scale. You might review 50 responses carefully and build a good intuition for quality. But when you have 500, or 5,000, or you want to run evaluation continuously as part of a deployment pipeline, manual review breaks down. The standard alternatives — ROUGE or BLEU scores — measure surface overlap and miss semantic quality entirely, while human annotation pipelines are slow and expensive.

NEO built a better option: an automated evaluation system that uses an LLM as a judge, with customizable weighted rubrics, per-criterion scoring, and justifications you can actually inspect.

## How the Evaluation System Works

The core idea is to evaluate responses against explicit quality criteria rather than comparing them to reference answers. You define what good looks like for your specific use case, weight the criteria by importance, and the judge scores each response against that rubric.

For customer support responses, you might care about accuracy, empathy, clarity, and completeness. For technical documentation, you might weight precision and completeness more heavily than tone. The rubric is yours to configure.

Each criterion gets an individual score with a written justification explaining why that score was assigned. This is the part that makes the system actionable. An aggregate score of 6.2 out of 10 does not tell you what to fix. A breakdown showing that accuracy scored 8 and empathy scored 4, with a note explaining what was missing, gives you a concrete direction.

## The Architecture

The stack is a React frontend with a FastAPI backend. The frontend handles file uploads, rubric configuration, and report display. The backend handles LLM calls, scoring logic, and result formatting.

NEO built it with Docker from the start, so deployment is straightforward in containerized environments.

### Model Provider Flexibility

The system supports **Anthropic Claude** (recommended for evaluation tasks due to its instruction-following reliability), **OpenAI GPT-4**, **Google Gemini**, **OpenRouter** for access to a wider model selection, and local **Ollama** deployments for teams that need fully on-premises evaluation.

Provider selection happens in the interface. You can switch models mid-experiment to compare how different judges score the same responses, which is useful for understanding judge reliability.

### Input Format

The application accepts CSV and JSON files. Required fields are `question` and `response`. An optional `category` field lets you tag responses by type and filter analysis by category, which is useful when your dataset spans multiple task types with different quality requirements.

## Getting Started

Demo mode starts in **under a minute** without any API keys. It uses mock scores to demonstrate the interface and report format. Full setup with real evaluation takes about **three minutes** once you have API credentials.

The interface walks you through uploading your data, configuring the rubric weights, selecting a model, and running the evaluation. Progress tracking is real-time. A batch of **100 responses** processes in roughly **three minutes** depending on the provider and rate limits.

## Security Considerations

API keys are stored client-side only. Nothing is persisted on the server. CORS protection, rate limiting, and input validation are in place across all backend endpoints.

For teams with strict data governance requirements, the Ollama integration means you can run the entire system on your own infrastructure with no data leaving your environment.

## AI-Powered Response Improvement

Beyond scoring, the system can generate improved versions of low-scoring responses. This is not a generic rewrite. It uses the rubric scores and per-criterion justifications as input, so the improvement targets the specific dimensions that scored poorly.

For teams running continuous evaluation, this creates a feedback loop. Evaluate a batch of responses, identify the worst performers, generate improved versions, and use those to refine your prompts or fine-tuning data.

## Use Cases

Customer support quality assurance is the primary use case NEO designed around. You have agents and responses, and you want to know if the quality meets your standards across the full distribution. This handles that at scale.

It also fits well into model evaluation workflows. Before deploying a new model or fine-tune, run your evaluation dataset through the judge and compare the score distributions against your current production model.

Content moderation and compliance review are adjacent uses. Configure the rubric to evaluate for specific compliance criteria and you have an automated screening layer.

---

## How to Build This

You need Python 3.10 or later for the backend and Node.js 18+ for the frontend. Docker is the recommended path because it handles both together in one command.

Clone and install:

```bash
git clone https://github.com/Dakshjain1604/LLM-response-Judge
cd LLM-response-Judge
```

With Docker:

```bash
docker-compose up --build
```

Without Docker, start each service manually:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser. The interface starts in demo mode with mock scores, so you can explore the report format before adding API keys. To enable real evaluation, go to the settings panel and enter your API key for whichever provider you want to use as the judge (Anthropic, OpenAI, Google, or OpenRouter). For on-premises use with no data leaving your environment, point it at a local Ollama instance instead.

Prepare your data as a CSV with `question` and `response` columns, then upload it through the interface. Set your rubric criteria and weights, pick a judge model, and click Run. A batch of 100 responses processes in roughly three minutes. The output report shows an aggregate score, a per-criterion breakdown for every response, and written justifications explaining each score. Responses flagged as low-scoring can be sent through the improvement generator directly from the report view.

NEO built an LLM response judge where customizable weighted rubrics and per-criterion justifications make automated quality evaluation actionable, not just a score. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
