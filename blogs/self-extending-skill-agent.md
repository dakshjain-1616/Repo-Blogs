---
title: "Self-Extending Skill Agent: An Agent That Grows Its Own Capabilities"
description: "NEO built an agent that detects capability gaps, writes new skill modules to fill them, tests them, and registers them for future use — without human intervention."
date: 2026-04-08
tags: [agents, skills, self-improvement, llm, automation]
slug: self-extending-skill-agent
github: https://github.com/dakshjain-1616/self-extending-skill-agent
---

# Self-Extending Skill Agent: An Agent That Grows Its Own Capabilities

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/self-extending-skill-agent)

![Pipeline Architecture](../public/images/diagrams/self-extending-skill-agent.png)

## The Problem

> Tool-using agents are only as capable as their predefined tool list. When a task falls outside what's registered, the agent fails or hallucinates. Every new capability requires a developer to write and deploy a new tool manually — the agent cannot help itself.

NEO built Self-Extending Skill Agent to close that gap: an agent that writes, tests, and registers new Python skill modules on demand when it detects it cannot complete a task with existing capabilities.

## Skill Registry and Routing

**Self-Extending Skill Agent** maintains a local skill registry — a directory of Python modules, each exposing a typed function signature and a docstring description. At startup the agent indexes the registry by embedding each skill's description using a sentence-transformer model, storing the vectors in a FAISS index for fast semantic lookup.

When a task arrives, the agent runs a **routing step**: it embeds the task description and retrieves the top-K most similar skills from the index. A confidence scorer evaluates whether any retrieved skill is a strong match, using cosine similarity against a configurable threshold (default 0.82). If a skill clears the threshold, the agent dispatches the task directly to it. If no skill does, the agent enters the extension loop.

Skills follow a strict interface contract — each is a Python function with typed parameters, a return type annotation, and a docstring:

```python
def fetch_rss_feed(url: str, max_items: int = 10) -> list[dict]:
    """Fetch and parse an RSS feed, returning a list of article dicts with title, link, and published date."""
    ...
```

This structure lets the router embed descriptions accurately and lets the LLM generate compliant new skills reliably.

## The Self-Extension Loop

When the confidence scorer finds no matching skill, the agent enters a four-step extension loop. First, the **gap analyzer** constructs a prompt describing the task, the existing registry (as a list of function signatures and docstrings), and the gap detected. The LLM is asked to write a new Python skill function that would handle the task, following the registry's interface contract.

Second, the generated code is written to a sandboxed temp directory and executed against a set of **auto-generated unit tests**. The test generator asks the LLM to produce three input-output pairs for the new function based on its docstring, then runs them using `pytest`. If all three pass, the skill is accepted. If any fail, the failure trace is fed back to the LLM for one revision attempt.

Third, a passing skill is moved into the live registry directory and its embedding is added to the FAISS index — making it immediately available for future tasks without restarting the agent.

Fourth, the original task is re-routed through the updated registry, now with a matching skill, and completes normally.

```
Task received
  └─ Router: confidence 0.61 < 0.82 → gap detected
      └─ Gap Analyzer: generate skill module
          └─ Test Runner: 3/3 tests pass
              └─ Registry: skill registered + indexed
                  └─ Router: confidence 0.94 → dispatch
```

## Skill Registry Management

The registry ships with a CLI for inspection and maintenance:

```bash
# List all registered skills with similarity scores for a query
python cli.py list --query "parse structured data from HTML"

# Force-remove a skill (e.g., after a bad registration)
python cli.py remove fetch_rss_feed

# Re-index the registry after manual edits
python cli.py reindex
```

The `--query` flag on `list` runs a live similarity search against the current FAISS index, making it easy to audit what the router would find for a given task description. A `--dry-run` flag on the agent's main loop logs routing decisions and confidence scores without executing any skill — useful for debugging coverage gaps in an existing registry.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python agent that maintains a local skill registry of typed Python functions indexed with FAISS embeddings. Route incoming tasks to existing skills by semantic similarity with a confidence threshold. When no skill matches, use an LLM to generate a new skill module, auto-generate and run unit tests to validate it, then register it in the live registry and re-route the original task. Include a CLI for registry inspection and management."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20Python%20agent%20that%20maintains%20a%20local%20skill%20registry%20of%20typed%20Python%20functions%20indexed%20with%20FAISS%20embeddings.%20Route%20incoming%20tasks%20to%20existing%20skills%20by%20semantic%20similarity%20with%20a%20confidence%20threshold.%20When%20no%20skill%20matches%2C%20use%20an%20LLM%20to%20generate%20a%20new%20skill%20module%2C%20auto-generate%20and%20run%20unit%20tests%20to%20validate%20it%2C%20then%20register%20it%20in%20the%20live%20registry%20and%20re-route%20the%20original%20task.%20Include%20a%20CLI%20for%20registry%20inspection%20and%20management." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a skill versioning system that tracks which version of a skill handled each task, build a web UI for browsing the registry, or extend the test generator to cover edge cases with property-based testing. Each request builds on what's already there without re-explaining the context.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/self-extending-skill-agent
cd self-extending-skill-agent
pip install -r requirements.txt
python agent.py --task "fetch the top 5 headlines from BBC News RSS"
```

The agent checks its registry, finds no matching skill, writes and tests a new RSS fetcher, registers it, and completes the original task — all in one run.

NEO built an agent that detects its own capability gaps, writes and validates new Python skill modules to fill them, and registers them live so every future task benefits without manual developer intervention. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
