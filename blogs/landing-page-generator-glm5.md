---
title: "NEO Built a CLI That Generates Production-Ready Landing Pages Using GLM5"
description: "NEO built Ship-It, a GPU-accelerated CLI tool that uses GLM5 and a multi-agent pipeline to generate complete, self-contained landing pages from a single command, with live preview and interactive editing."
date: 2026-03-09
tags: ["landing page generator", "GLM5", "multi-agent system", "GPU inference", "code generation", "CLI tool", "transformer models"]
slug: landing-page-generator-glm5
github: https://github.com/dakshjain-1616/GLA5-Landing-Page-tool
---

# NEO Built a CLI That Generates Production-Ready Landing Pages Using GLM5

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/GLA5-Landing-Page-tool)

![Pipeline Architecture](../public/images/diagrams/landing-page-generator-glm5.png)

## The Problem

> Most code generation tools produce snippets. They give you a component, a function, a starting point you then spend an hour wiring together. For landing pages specifically, that means wrestling with CSS frameworks, JavaScript dependencies, and responsive layout issues — all before you've validated whether the idea is worth building.

NEO autonomously built Ship-It: one CLI command, one HTML file, live preview at localhost:8080. No assembly required.

## Why GLM5

GLM5 is a GPU-accelerated transformer model well-suited for structured code generation tasks. It produces coherent HTML with embedded CSS and JavaScript in a single pass, without the context fragmentation you get from smaller models. Ship-It runs it locally with CUDA, which means no API calls, no rate limits, and no data leaving your machine.

The model comes in three size configurations. The smallest requires about **512 MB of VRAM**, the medium (default) sits around **1 GB**, and the large variant uses up to **2 GB**. Most development machines with a modern GPU can run the medium configuration without issue. The tool monitors VRAM usage in real time and warns if you're approaching limits.

## The Multi-Agent Architecture

Generating a good landing page isn't a single task. It's a set of distinct tasks that benefit from focused attention. NEO split the work across six specialized agents that run in parallel where possible.

**Research Agent** analyzes the product description and identifies key selling points, target audience characteristics, and competitive context. It runs at the same time as the Copy Agent, which means the generation phase doesn't wait for research to complete sequentially.

**Copy Agent** generates the actual text content: headlines, subheadlines, feature descriptions, social proof copy, and calls to action. Good landing page copy follows specific structural patterns, and the agent is prompted with those patterns explicitly.

**Design Agent** makes layout decisions: section ordering, visual hierarchy, color palette selection, and spacing logic. It outputs a structured design spec that the Builder Agent consumes.

**Builder Agent** assembles the actual HTML. It takes the copy, the design spec, and the research output and produces a single self-contained file. No external CSS frameworks. No JavaScript dependencies. Everything is inline.

**QA Agent** validates the output across four dimensions: design consistency, responsive layout behavior, accessibility, and SEO. It checks for things like missing alt text, inadequate color contrast, and absent meta tags. If validation fails, the Builder Agent gets a correction pass.

**Deploy Agent** writes the final `index.html` and launches the local preview server.

The total output is a standalone file around **30 to 35 KB**. It requires no build process and no dependencies to serve. Drop it anywhere.

## Live Preview and Interactive Editing

Once the initial generation completes, Ship-It launches a preview at localhost:8080 with hot-reload. You can request edits to specific sections without regenerating the entire page. If the hero text doesn't land right, you tell the tool which section to revise and what to change. The other sections stay intact.

This interaction model matters because full-page regeneration takes time and often changes things you didn't want changed. Section-level editing is faster and more predictable.

## The Four-Phase Workflow

The full pipeline runs in four stages:

1. **Parallel generation**: Research and Copy agents run simultaneously, GPU inference handles both.
2. **Assembly**: Builder Agent takes all inputs and constructs the HTML file.
3. **QA validation**: The QA Agent checks design, responsiveness, accessibility, and SEO. Any failures trigger a targeted fix pass.
4. **Deployment**: Final file is written and the preview server starts.

The whole process runs end-to-end in a single CLI invocation. You watch the phases complete in the terminal, and the browser opens automatically when the preview is ready.

## Hardware Requirements

You need Python 3.8 or higher, an NVIDIA GPU with CUDA 11.8 or later, and at least 4 GB of VRAM for the default medium configuration. PyTorch with CUDA support is a dependency. CPU-only execution isn't supported because the inference speed becomes impractical for interactive use.

If you're running on a machine without a GPU, the architecture still makes sense as a reference for how to structure multi-agent code generation workflows, even if Ship-It itself isn't the right tool for your hardware.

## When This Approach Makes Sense

Ship-It is built for situations where you need a functional landing page fast. Early-stage products that need a web presence before the engineering team is ready to build one. A/B testing ideas that don't justify a full design cycle. Marketing campaigns that need a standalone page with a specific message and call to action.

The single-file output makes deployment trivial. Upload to S3, drop it in a CDN, serve it from Nginx. No framework, no build step, no dependency management.

## Code Generation That Ships

The principle behind Ship-It is that good tooling should produce complete, usable artifacts, not starting points. The multi-agent approach with GLM5 gets you there for landing pages. The same architecture applies to other structured code generation tasks where the output needs to meet multiple quality criteria simultaneously.

## How to Build This

You need Python 3.8+, an NVIDIA GPU with CUDA 11.8+, and at least 4 GB of VRAM. Clone and install:

```bash
git clone https://github.com/dakshjain-1616/GLA5-Landing-Page-tool
cd GLA5-Landing-Page-tool
python3 -m venv venv
source venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

Verify your GPU is accessible:

```bash
python3 -c "import torch; print(torch.cuda.get_device_name(0))"
```

Run the generator:

```bash
python3 ship_it.py
```

You will be prompted for four inputs: product name, tagline, description, and hero headline. After you provide them, the pipeline loads the GLM5 medium model (~1 GB VRAM), runs the Research and Copy agents in parallel using GPU inference, assembles the HTML with the Builder Agent, validates it with the QA Agent across design, responsiveness, accessibility, and SEO checks, and writes the final `index.html`. The preview server starts automatically at `http://localhost:8080`. An iteration menu then appears in the terminal where you can edit specific sections, check live VRAM stats, or run a targeted fix pass on individual parts of the page without regenerating everything. The final output file is around 30 to 35 KB and requires no build step to deploy.

NEO built a multi-agent landing page generator where a single CLI command produces a complete, self-contained HTML file—validated for accessibility, SEO, and responsive layout—with no assembly required. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
