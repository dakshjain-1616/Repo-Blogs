---
title: "NEO Built an AI Agent That Fills Out Job Applications End-to-End"
description: "NEO built AutoCareer, an autonomous job application agent that parses resumes, scrapes listings, scores candidate fit, generates cover letters, and fills out application forms using RAG and Selenium."
date: 2026-03-09
tags: ["autonomous agent", "job application automation", "RAG", "LangChain", "Selenium", "FAISS", "NLP"]
slug: job-application-autofiller-agent
github: https://github.com/Dakshjain1604/Job-Application-AutoFiller-Agent
---

# NEO Built an AI Agent That Fills Out Job Applications End-to-End

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dakshjain1604/Job-Application-AutoFiller-Agent)

![Pipeline Architecture](../public/images/diagrams/job-application-autofiller-agent.png)

## The Problem

> Job hunting is repetitive by design. Copy your resume details into a form. Write a cover letter. Submit. Repeat forty times. The process is structured enough that a machine should handle it — but no existing tool closes the full loop from discovery through submission, with cover letters that actually reference specific company context rather than generic templates.

NEO built AutoCareer — an autonomous job application agent that reads your resume, finds relevant listings, decides whether you're a good fit, writes a tailored cover letter, and submits the application. The whole thing runs without you sitting at a keyboard.

## How the Pipeline Works

The system is composed of six tightly integrated modules, each handling a distinct part of the workflow.

### Resume Parsing and Indexing

The pipeline starts by converting the candidate's PDF resume into vector embeddings using SentenceTransformers. Those embeddings get indexed with FAISS, which enables fast semantic retrieval when matching against job descriptions. This isn't keyword matching. It's meaning-level comparison, so a resume that mentions "model deployment" still surfaces for roles asking for "MLOps experience."

### Job Discovery

The scraper pulls listings from LinkedIn and Greenhouse. NEO built anti-bot handling in from the start using Playwright, because naive scrapers get blocked within minutes. Rate limiting, session rotation, and realistic browser fingerprinting are all part of the default configuration.

### Candidate Fit Scoring

Each listing gets a fit score from **0 to 100**. The base scoring uses keyword alignment between the job description and the resume embedding. When higher-confidence reasoning is needed, the system pipes the job description and resume into GPT-4 for structured analysis. The GPT-4 path is optional and controlled by a config flag, so you're not making API calls for every listing if you don't need to.

### Cover Letter Generation

This is where the RAG pipeline matters most. Before writing the cover letter, the system fetches the company's website and extracts relevant context. That context gets retrieved and fed into the generation prompt alongside the job description and resume. The output is a letter that references the company's actual product focus or stated values, not a generic template. LangChain handles the retrieval and prompt orchestration.

### Form Automation

Selenium handles the form-filling step. NEO built in review checkpoints so the candidate can inspect what's about to be submitted before it goes through. There's also a dry-run mode that walks through the entire flow without actually submitting anything. Both features exist because blind automation on job applications is a bad idea.

### Application History

Every submission gets logged with a timestamp and a screenshot. The logs are cryptographically secured so they can't be silently altered. If you ever need to audit what was sent to which employer, the record is there.

## The Tech Stack

The backend runs on **FastAPI** with Python 3.10+. The frontend is **React 18**. The full stack spins up with Docker Compose: frontend on port 3000, API server on port 8000 with auto-generated documentation. **SQLite** handles local persistence with no cloud storage dependency, which matters if you're cautious about where your resume data lives.

Core dependencies: LangChain for RAG workflows, OpenAI GPT-4 for fit analysis and cover letter generation, SentenceTransformers for embeddings, FAISS for vector indexing, Playwright and Selenium for web automation.

## Where This Gets Useful

The obvious use case is individual job seekers who want to apply at scale without spending hours on repetitive form entry. But there are other angles.

Recruiting platforms could run this internally to auto-populate candidate profiles. Career coaching tools could use the fit scoring module alone to help candidates identify which listings are worth pursuing. Staffing agencies managing applications across multiple clients could run parallel instances per candidate.

The modular architecture makes it straightforward to swap components. Want to replace FAISS with Pinecone for production scale? That's one module. Want to add Indeed or Lever to the scraper? Same deal.

## What NEO Paid Attention To

Two things stood out during development. First, cover letter quality depends heavily on the RAG context. A letter written with real company information reads differently than one generated from the job description alone. The retrieval step is not optional if you want output that doesn't sound generic.

Second, the review checkpoints in the form automation aren't a courtesy feature. They're load-bearing. An agent that submits without human review creates a trust problem that's hard to recover from. NEO kept those checkpoints in the default flow.

## Build Your Own Automation

AutoCareer works best as a starting point. The scoring logic is extensible, the scraper can target new boards, and the RAG pipeline is general enough to handle different document types.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build an autonomous job application agent with a FastAPI backend and React 18 frontend that run together via Docker Compose. The pipeline has six stages: parse a PDF resume into FAISS vector embeddings using SentenceTransformers; scrape LinkedIn and Greenhouse listings using Playwright with anti-bot handling (rate limiting, session rotation, realistic browser fingerprinting); score candidate fit 0-100 using keyword alignment against resume embeddings with an optional [GPT-4](https://platform.openai.com/docs/models/gpt-4) path for higher-confidence reasoning; generate tailored cover letters using LangChain RAG that fetches the company's website for context before writing; fill application forms with Selenium including a 10-second review checkpoint before any submission; and log every submission with a timestamp, screenshot, and cryptographically secured record. Include DRY_RUN=true mode that walks through the full pipeline including form filling without submitting."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20an%20autonomous%20job%20application%20agent%20with%20a%20FastAPI%20backend%20and%20React%2018%20frontend%20that%20run%20together%20via%20Docker%20Compose.%20The%20pipeline%20has%20six%20stages%3A%20parse%20a%20PDF%20resume%20into%20FAISS%20vector%20embeddings%20using%20SentenceTransformers%3B%20scrape%20LinkedIn%20and%20Greenhouse%20listings%20using%20Playwright%20with%20anti-bot%20handling%20%28rate%20limiting%2C%20session%20rotation%2C%20realistic%20browser%20fingerprinting%29%3B%20score%20candidate%20fit%200-100%20using%20keyword%20alignment%20against%20resume%20embeddings%20with%20an%20optional%20GPT-4%20path%20for%20higher-confidence%20reasoning%3B%20generate%20tailored%20cover%20letters%20using%20LangChain%20RAG%20that%20fetches%20the%20company%27s%20website%20for%20context%20before%20writing%3B%20fill%20application%20forms%20with%20Selenium%20including%20a%2010-second%20review%20checkpoint%20before%20any%20submission%3B%20and%20log%20every%20submission%20with%20a%20timestamp%2C%20screenshot%2C%20and%20cryptographically%20secured%20record.%20Include%20DRY_RUN%3Dtrue%20mode%20that%20walks%20through%20the%20full%20pipeline%20including%20form%20filling%20without%20submitting." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation from that. From there you iterate — ask it to add the fallback to keyword-based scoring when no OpenAI API key is configured, add Indeed and Lever scraper adapters using the same anti-bot Playwright setup, or add SQLite-backed application history with the cryptographic audit log. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/Dakshjain1604/Job-Application-AutoFiller-Agent
cd Job-Application-AutoFiller-Agent
docker-compose up --build
```

The frontend is at `http://localhost:3000` and the API docs at `http://localhost:8000/docs` — upload a resume PDF, search for jobs, review fit scores, generate cover letters, and submit with the 10-second review gate before anything goes out.

NEO built an end-to-end job application agent where RAG-powered cover letter generation, semantic fit scoring, and form automation close the full loop from discovery to submission. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>
