---
title: "PyForge: Generate, Refactor, and Debug Python from the Terminal with Natural Language"
description: "NEO built PyForge, an AI-powered CLI that generates, refactors, and debugs Python code from natural language commands directly in the terminal workflow."
date: 2026-03-23
tags: [CLI tools, code generation, Python, developer tools, AI coding, terminal workflow]
slug: pyforge-ai-python-cli
github: https://github.com/dakshjain-1616/PyForge-AI-powered-Python-CLI
---

# PyForge: Generate, Refactor, and Debug Python from the Terminal with Natural Language

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/PyForge-AI-powered-Python-CLI)

![Pipeline Architecture](../public/images/diagrams/pyforge-ai-python-cli.png)

## The Problem

> Python developers spend a disproportionate amount of time on mechanical tasks: writing boilerplate for a new CLI tool, refactoring a function to use a newer API, or tracing a stack trace back to its root cause. These tasks require Python knowledge but not creative thought. Switching to a browser or chat interface to ask an AI breaks the terminal flow that most developers work hardest to stay in.

NEO built PyForge to keep AI-assisted coding inside the terminal, where the code actually runs.

## Core Command Modes

PyForge exposes four primary command modes, each optimized for a different stage of the development workflow.

### `pyforge gen` — One-Shot Code Generation

The `gen` command takes a natural language description and produces runnable Python. The output is not pseudocode or a skeleton — it is executable code with imports, error handling, and sensible defaults. PyForge makes opinionated choices about style (type hints, f-strings, dataclasses over raw dicts) and documents them in inline comments so the developer understands what was generated and can override it.

The generated code is written directly to a file if a path is specified, or piped to stdout for integration with other shell tools. This means `pyforge gen "parse CSV and compute per-column statistics" | pbcopy` works exactly as expected.

For longer generation tasks, PyForge uses streaming output so the terminal shows progress as the code is produced rather than hanging until completion.

### `pyforge refactor` — Targeted Code Transformation

The `refactor` command takes an existing Python file and a natural language instruction. Instructions can be specific ("replace all `print` statements with `logging.info` calls") or high-level ("modernize this to use pathlib instead of os.path"). The command produces a diff preview before writing changes, requiring explicit confirmation by default.

Under the hood, PyForge parses the target file into an AST before passing it to the model. This gives the model structural context — it knows which functions exist, what they call, and what the imports are — without requiring the full source text to be in the context window for large files. The AST summary is passed alongside the relevant source sections identified by the instruction.

### `pyforge debug` — Stack Trace Analysis

The `debug` command accepts a Python stack trace (from stdin or a file) and a description of what the code was supposed to do. It identifies the root cause, explains what went wrong, and produces a specific fix. For common error patterns — `KeyError` on dict access, `AttributeError` on None, off-by-one in slice operations — it also identifies whether the fix should be defensive (add a check) or corrective (fix the underlying logic).

PyForge does not guess. If the stack trace is ambiguous without seeing the source code, it asks for the relevant file before producing a diagnosis. This interactive mode is intentional — a confident wrong answer is worse than a clarifying question.

### `pyforge scaffold` — Project Structure Generation

The `scaffold` command generates a complete project structure from a high-level description. "A FastAPI service with PostgreSQL, JWT auth, and a pytest test suite" produces a directory tree with `pyproject.toml`, a Dockerfile, environment variable templates, a database migration setup, and test fixtures. The scaffold follows community conventions — it does not invent its own project layout.

## Iterative Refinement

The most underrated feature is iterative refinement. After any `gen` or `refactor` operation, PyForge stores the result in a session buffer. Follow-up commands like `pyforge refine "add input validation"` or `pyforge refine "make it async"` apply to the buffered result without re-reading the file. This creates a conversational loop inside the terminal where each command builds on the last.

Session state is stored in a lightweight SQLite database in the user's home directory. Sessions are named automatically by timestamp and the first few words of the initial generation prompt, making it easy to resume a previous session with `pyforge resume`.

## Integration with the Shell

PyForge is designed to compose with standard shell tools. Generated code can be piped to `black` for formatting, `mypy` for type checking, or `pytest` for immediate test execution. Exit codes follow Unix conventions — zero for success, non-zero for any error — so PyForge steps can be embedded in shell scripts and CI pipelines without special handling.

The tool also reads from `.pyforge.toml` in the project root for project-specific configuration: preferred style, common imports, module naming conventions. This means the generated code fits the existing codebase rather than starting from PyForge's own defaults.

## Performance and Local vs. Cloud Models

PyForge supports both cloud API backends (OpenAI, Anthropic) and local models via Ollama. For one-shot scripts and small refactors, local models with quantization are fast enough to feel responsive. For complex scaffolding or multi-file refactors, cloud models produce substantially better results. The backend is configurable per command type, so a developer can route simple generations to a local model and complex tasks to a cloud API, balancing speed and capability.

## How to Build This

Clone the repo and install:

```bash
git clone https://github.com/dakshjain-1616/PyForge-AI-powered-Python-CLI
cd PyForge-AI-powered-Python-CLI
pip install -e .
```

Installing with `-e` makes the `pyforge` command available globally. Set your API key for the provider you want to use:

```bash
OPENAI_API_KEY=sk-...
# or for Anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

For local model support, install Ollama and pull a model before using the `--backend ollama` flag. Generate a Python script from a natural language description:

```bash
pyforge gen "read a CSV file, compute per-column statistics, and write a summary to stdout"
```

PyForge writes the generated code to stdout by default. Pipe it to a file or to `black` for formatting:

```bash
pyforge gen "parse command-line args with argparse and validate required fields" > cli.py
```

Refactor an existing file with a natural language instruction:

```bash
pyforge refactor utils.py "replace all os.path calls with pathlib equivalents"
```

PyForge shows a diff preview and prompts for confirmation before writing. Debug a stack trace by piping it in:

```bash
cat traceback.txt | pyforge debug --context "this function is supposed to process a CSV row"
```

Scaffold a full project:

```bash
pyforge scaffold "FastAPI service with PostgreSQL, JWT auth, and pytest test suite" --output ./my-service
```

Session state is stored automatically, so follow-up refinements apply to the last generated output without re-reading anything.

NEO built PyForge to eliminate the context switch between writing code and asking for help with it. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
