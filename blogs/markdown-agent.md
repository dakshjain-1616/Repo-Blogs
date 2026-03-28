---
title: "Markdown Agent: An AI Agent That Lives in Three Plain Text Files"
description: "NEO built a stateful AI agent that reads its goal from plan.md, writes results to output.md, and accumulates memory in memory.md across sessions, with no server or database required."
date: 2026-03-28
tags: [ai-agent, markdown, local-llm, automation, plaintext]
slug: markdown-agent
github: https://github.com/dakshjain-1616/markdown-agent
---

# Markdown Agent: An AI Agent That Lives in Three Plain Text Files

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/markdown-agent)

![Pipeline Architecture](../public/images/diagrams/markdown-agent.png)

## The Problem

> Most AI agent frameworks require a database for state, a server for the API, and a proprietary dashboard to inspect what the agent is doing. Debugging a LangChain agent means reading logs. Editing its memory means writing code. None of this is necessary.

NEO built Markdown Agent to reduce an AI agent to its minimal form: three plain text files and one command. The entire lifecycle is readable and editable in any text editor.

## The Three-File Architecture

The agent operates on three Markdown files. You write to one, the agent writes to the other two.

**`plan.md`** is your input. Write your goal in `## Goal`, add a checklist in `## Tasks`, and optionally add `## Context` with background information and `## Constraints` with limits on format or scope. Only the Goal section is required.

**`output.md`** is the agent's response. It writes structured results here after each run, including completed task items and session metadata. You read this file to see what the agent produced.

**`memory.md`** is the agent's persistent state. It reads this at the start of every run and appends a new session block at the end. Each block records the timestamp, goal, completed tasks, and a summary of what was done. This file is how the agent remembers previous sessions without any database.

The memory format is the key design decision. Because it is plain Markdown, you can `git diff memory.md` to see what changed between sessions, hand-edit any session block to correct the agent's understanding, or `cat memory.md | grep goal` to find a previous run. There is no proprietary format to decode.

## Backend Auto-Detection

The agent auto-detects the best available LLM backend based on environment variables, in priority order.

**Dry-run** mode (`--dry-run` flag) prints the full prompt and token count without calling any model. Use this to verify your `plan.md` is parsed correctly before spending tokens.

**Local GGUF** activates when `LLAMA_MODEL_PATH` points to a `.gguf` file. The agent loads the model via `llama-cpp-python` and runs entirely offline. This is the option for air-gapped machines or when you want zero API cost.

**Anthropic Claude** activates when `ANTHROPIC_API_KEY` is set. The default model is `claude-sonnet-4-6`. Override with `ANTHROPIC_MODEL`.

**OpenAI** activates when `OPENAI_API_KEY` is set. Set `OPENAI_BASE_URL` to point at any OpenAI-compatible server, including Ollama and LM Studio running locally.

**Mock** is the fallback when no key is set. It produces deterministic output, which makes it useful for CI pipelines and testing.

```bash
# Local GGUF model, fully offline
LLAMA_MODEL_PATH=~/models/llama-3-8b.gguf python run_agent.py

# Any OpenAI-compatible local server
OPENAI_API_KEY=ollama OPENAI_BASE_URL=http://localhost:11434/v1 python run_agent.py
```

## Built-in Templates

The agent ships six `plan.md` templates for common use cases: `research` for structured literature reviews, `code-review` for PR analysis with severity ratings, `brainstorm` for idea generation, `bug-report` for root cause analysis, `data-analysis` for dataset exploration, and `weekly-review` for recurring team reviews.

```python
from markdown_agent_3_fil import get_template, list_templates

print(list_templates())
# ['brainstorm', 'bug-report', 'code-review', 'data-analysis', 'research', 'weekly-review']

template = get_template("code-review")
# Write to plan.md and run
```

These templates pre-fill the Goal, Tasks, Context, and Constraints sections with sensible defaults for each use case. They are starting points, not fixed formats.

## Why Not LangChain

The practical difference is inspectability. With LangChain or AutoGPT, the agent's state lives in a vector database or managed service. You cannot `cat` it, `grep` it, or `git diff` it. Changing what the agent remembers requires writing code and redeploying.

With Markdown Agent, the state is `memory.md`. Open it in any editor. Change what the agent should remember. Run the agent again. The agent reads the file at startup, so your edit is immediately effective.

The dependency surface is also smaller. The core library needs only Python. Adding a local GGUF backend requires `llama-cpp-python`. Adding cloud backends requires `anthropic` or `openai`. No vector database, no graph database, no embedded Redis.

## How to Build This

Clone and install:

```bash
git clone https://github.com/dakshjain-1616/markdown-agent
cd markdown-agent
pip install -r requirements.txt
```

Write a goal and run the agent with the mock backend (no API key needed):

```bash
cat > plan.md << 'EOF'
# Plan

## Goal
List the five most important principles of clean code

## Tasks
- [ ] Name each principle
- [ ] Give a one-line example for each
EOF

python run_agent.py
cat output.md
```

To use Claude:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python run_agent.py
```

To use a local GGUF model:

```bash
LLAMA_MODEL_PATH=~/models/mistral-7b-q4.gguf python run_agent.py
```

After multiple runs, inspect the accumulated memory:

```bash
cat memory.md
git diff memory.md  # if memory.md is tracked in git
```

Run the test suite:

```bash
pytest tests/ -q
# 89 passed
```

NEO built a three-file AI agent that accumulates memory across sessions in plain Markdown, with backend auto-detection from local GGUF files to Claude to OpenAI. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
