---
title: "Building a Drug Repurposing Research Platform with AI and Live Reasoning Traces"
description: "NEO built BioScript, an AI-powered drug repurposing platform that mines PubMed abstracts, extracts FDA-approved candidates, scores them against fibrotic disease pathways, and generates full research reports with 3D molecular visualization."
date: 2026-03-09
tags: ["drug repurposing", "biomedical NLP", "PubMed", "GPT-4o", "molecular visualization", "AI research tools", "pathway analysis"]
slug: ai-powered-drug-repurposing-platform
github: https://github.com/Dakshjain1604/AI-Powered-Drug-Repurposing-Platform
---

# Building a Drug Repurposing Research Platform with AI and Live Reasoning Traces

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dakshjain1604/AI-Powered-Drug-Repurposing-Platform)

![Pipeline Architecture](../public/images/diagrams/ai-powered-drug-repurposing-platform.png)

## The Problem

> Drug discovery is slow and expensive. Developing a new drug from scratch takes over a decade and billions of dollars. Repurposing approved drugs sidesteps the safety profile problem — those candidates are already validated. But identifying which approved drugs might work against a new disease context requires mining hundreds of recent abstracts, cross-referencing pathway databases, and synthesizing evidence that no single researcher can track manually.

NEO autonomously built BioScript to do exactly that: mine current scientific literature, extract viable drug candidates, score them against known disease pathways, and generate structured research reports. The focus is fibrotic diseases, but the architecture generalizes.

## What the Platform Does

BioScript pulls **50 to 100 recent abstracts** from PubMed, parses them for drug mentions, validates each candidate against an FDA approval database, and then scores them across a curated set of biological pathways. The output is a full report with visualizations, experimental protocols, and a live log of every reasoning step the system took.

That last part deserves attention. The live reasoning trace is a real-time, timestamped log of the AI's decision-making process. You can watch it work. Each extraction, each scoring decision, each hypothesis gets surfaced as it happens. That's not just useful for debugging. It's useful for building trust in a domain where treating the system as a black box is not an option.

## The Architecture

The platform breaks into seven core modules.

**Literature Retrieval** handles PubMed queries using Biopython. The pipeline pulls structured abstracts with metadata so downstream modules have clean input to work with.

**Candidate Extraction** uses GPT-4o-mini with a structured prompting approach. The model reads each abstract and identifies drug mentions, then flags which ones are worth tracking based on disease relevance. FDA validation runs against a local cache of **30+ approved drugs**, which keeps API calls down during repeated analysis sessions.

**Pathway Scoring** is where the core scientific judgment happens. NEO built a set of **eight curated fibrotic pathways**, things like TGF-beta signaling, inflammation cascades, and collagen synthesis pathways. Each candidate gets scored **0 to 100** based on how many relevant pathway interactions appear in the literature. This is a weighted scoring system informed by what the abstracts actually say, not a rigid rule engine.

**Molecular Visualization** uses stmol and PubChem's API to render interactive 3D structures. You can rotate, zoom, and inspect property details for each candidate directly in the browser. This matters for researchers who need to think about binding geometry, not just pathway scores.

**Report Generation** produces comprehensive PDF documents via ReportLab. The reports include executive summaries, full scoring breakdowns, and suggested experimental protocols for the top candidates. These are designed to be shareable with wet-lab teams without any additional formatting work.

## Three External APIs, One Coherent Interface

BioScript integrates PubMed, OpenAI, and PubChem. Coordinating three external APIs in a single research workflow creates obvious failure points. NEO handled this by building local caching for FDA drug data and structuring API calls to fail gracefully rather than halting the pipeline. If PubChem is slow, the visualization degrades but the scoring still runs.

The Streamlit interface ties everything together into a dashboard that doesn't require any ML background to operate. A bench researcher who has never touched a transformer model can run a query, read the reasoning trace, and interpret the results.

## What 35 Development Cycles Produces

This project took **35 iterative development cycles** to reach production quality. That number is worth mentioning not as a boast but as a data point: roughly **3,500 lines of code** covering seven distinct modules, three API integrations, and a complete reporting pipeline. Each cycle tightened the scoring logic, improved the prompt structure, or hardened the error handling.

The iterative process is how you get a system that handles edge cases. Abstracts with ambiguous drug names. PubChem lookups that return multiple compound matches. Pathway scores that need normalization across different abstract volumes. These aren't problems you anticipate on day one.

## Who Uses This

The primary audience is biomedical researchers looking for an accelerated first-pass analysis. Instead of manually reviewing hundreds of abstracts and cross-referencing pathway databases, BioScript produces a ranked list with supporting evidence in minutes.

Secondary use cases include pharmaceutical analysts tracking the competitive landscape, academic labs building systematic literature reviews, and anyone doing exploratory work on fibrosis-adjacent mechanisms who needs a structured starting point.

## AI Research Tools Should Show Their Work

The design principle NEO returned to throughout development was transparency. An AI system making biomedical claims needs to be interrogable. The live reasoning trace isn't a nice-to-have. It's a requirement for any context where a researcher needs to know why the system ranked a particular candidate.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a drug repurposing research platform in Python using Streamlit, Biopython, [GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini), and PubChem. Pull 50-100 recent PubMed abstracts for a given disease query, extract drug candidates with [GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini), validate them against an FDA-approved drug cache, and score each candidate 0-100 across eight curated fibrotic disease pathways. Show a live timestamped reasoning trace as each step executes. Render interactive 3D molecular structures with stmol and generate a PDF research report with ReportLab including executive summary, scoring breakdowns, and experimental protocols."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20drug%20repurposing%20research%20platform%20in%20Python%20using%20Streamlit%2C%20Biopython%2C%20GPT-4o-mini%2C%20and%20PubChem.%20Pull%2050-100%20recent%20PubMed%20abstracts%20for%20a%20given%20disease%20query%2C%20extract%20drug%20candidates%20with%20GPT-4o-mini%2C%20validate%20them%20against%20an%20FDA-approved%20drug%20cache%2C%20and%20score%20each%20candidate%200-100%20across%20eight%20curated%20fibrotic%20disease%20pathways.%20Show%20a%20live%20timestamped%20reasoning%20trace%20as%20each%20step%20executes.%20Render%20interactive%203D%20molecular%20structures%20with%20stmol%20and%20generate%20a%20PDF%20research%20report%20with%20ReportLab%20including%20executive%20summary%2C%20scoring%20breakdowns%2C%20and%20experimental%20protocols." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation from that. From there you iterate — ask it to add the PubChem 3D visualization tab with rotation and property details, build out the eight fibrotic pathway scoring weights, or add graceful API fallback so the pipeline continues when PubChem is slow. Each request builds on what's already there without re-explaining the context.

To run the finished project:

```bash
git clone https://github.com/Dakshjain1604/AI-Powered-Drug-Repurposing-Platform.git
cd AI-Powered-Drug-Repurposing-Platform
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`, set a disease focus, and click Start Analysis. The live reasoning trace appears on the left while results populate across the Literature, Candidates, Visualization, and Report Export tabs over 60-105 seconds.

NEO built a drug repurposing research platform where live reasoning traces and transparent AI decision-making are built into the system, not bolted on as an afterthought. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>
