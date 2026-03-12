---
title: "Building a Drug Repurposing Research Platform with AI and Live Reasoning Traces"
description: "NEO built BioScript, an AI-powered drug repurposing platform that mines PubMed abstracts, extracts FDA-approved candidates, scores them against fibrotic disease pathways, and generates full research reports with 3D molecular visualization."
date: 2026-03-09
tags: ["drug repurposing", "biomedical NLP", "PubMed", "GPT-4o", "molecular visualization", "AI research tools", "pathway analysis"]
slug: ai-powered-drug-repurposing-platform
github: https://github.com/Dakshjain1604/AI-Powered-Drug-Repurposing-Platform
---

# Building a Drug Repurposing Research Platform with AI and Live Reasoning Traces

<a href="https://github.com/Dakshjain1604/AI-Powered-Drug-Repurposing-Platform" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">Dakshjain1604/AI-Powered-Drug-Repurposing-Platform</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/ai-powered-drug-repurposing-platform.png)

## The Problem

> Drug discovery is slow and expensive. Developing a new drug from scratch takes over a decade and billions of dollars. Repurposing approved drugs sidesteps the safety profile problem — those candidates are already validated. But identifying which approved drugs might work against a new disease context requires mining hundreds of recent abstracts, cross-referencing pathway databases, and synthesizing evidence that no single researcher can track manually.

NEO autonomously built BioScript to do exactly that: mine current scientific literature, extract viable drug candidates, score them against known disease pathways, and generate structured research reports. The focus is fibrotic diseases, but the architecture generalizes.

## What the Platform Does

BioScript pulls **50 to 100 recent abstracts** from PubMed, parses them for drug mentions, validates each candidate against an FDA approval database, and then scores them across a curated set of biological pathways. The output is a full report with visualizations, experimental protocols, and a live log of every reasoning step the system took.

That last part deserves attention. The live reasoning trace is a real-time, timestamped log of the AI's decision-making process. You can watch it work. Each extraction, each scoring decision, each hypothesis gets surfaced as it happens. That's not just useful for debugging. It's useful for building trust in a domain where treating the system as a black box is not an option.

## The Architecture

The platform breaks into seven core modules.

**Literature Retrieval** handles PubMed queries using Biopython. We pull structured abstracts with metadata so downstream modules have clean input to work with.

**Candidate Extraction** uses GPT-4o-mini with a structured prompting approach. The model reads each abstract and identifies drug mentions, then flags which ones are worth tracking based on disease relevance. FDA validation runs against a local cache of **30+ approved drugs**, which keeps API calls down during repeated analysis sessions.

**Pathway Scoring** is where the core scientific judgment happens. NEO built a set of **eight curated fibrotic pathways**, things like TGF-beta signaling, inflammation cascades, and collagen synthesis pathways. Each candidate gets scored **0 to 100** based on how many relevant pathway interactions appear in the literature. This is a weighted scoring system informed by what the abstracts actually say, not a rigid rule engine.

**Molecular Visualization** uses stmol and PubChem's API to render interactive 3D structures. You can rotate, zoom, and inspect property details for each candidate directly in the browser. This matters for researchers who need to think about binding geometry, not just pathway scores.

**Report Generation** produces comprehensive PDF documents via ReportLab. The reports include executive summaries, full scoring breakdowns, and suggested experimental protocols for the top candidates. These are designed to be shareable with wet-lab teams without any additional formatting work.

## Three External APIs, One Coherent Interface

BioScript integrates PubMed, OpenAI, and PubChem. Coordinating three external APIs in a single research workflow creates obvious failure points. We handled this by building local caching for FDA drug data and structuring API calls to fail gracefully rather than halting the pipeline. If PubChem is slow, the visualization degrades but the scoring still runs.

The Streamlit interface ties everything together into a dashboard that doesn't require any ML background to operate. A bench researcher who has never touched a transformer model can run a query, read the reasoning trace, and interpret the results.

## What 35 Development Cycles Produces

This project took **35 iterative development cycles** to reach production quality. That number is worth mentioning not as a boast but as a data point: roughly **3,500 lines of code** covering seven distinct modules, three API integrations, and a complete reporting pipeline. Each cycle tightened the scoring logic, improved the prompt structure, or hardened the error handling.

The iterative process is how you get a system that handles edge cases. Abstracts with ambiguous drug names. PubChem lookups that return multiple compound matches. Pathway scores that need normalization across different abstract volumes. These aren't problems you anticipate on day one.

## Who Uses This

The primary audience is biomedical researchers looking for an accelerated first-pass analysis. Instead of manually reviewing hundreds of abstracts and cross-referencing pathway databases, BioScript produces a ranked list with supporting evidence in minutes.

Secondary use cases include pharmaceutical analysts tracking the competitive landscape, academic labs building systematic literature reviews, and anyone doing exploratory work on fibrosis-adjacent mechanisms who needs a structured starting point.

## AI Research Tools Should Show Their Work

The design principle we returned to throughout development was transparency. An AI system making biomedical claims needs to be interrogable. The live reasoning trace isn't a nice-to-have. It's a requirement for any context where a researcher needs to know why the system ranked a particular candidate.

NEO built a drug repurposing research platform where live reasoning traces and transparent AI decision-making are built into the system, not bolted on as an afterthought. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)
