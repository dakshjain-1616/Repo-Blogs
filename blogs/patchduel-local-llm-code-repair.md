---
title: "PatchDuel: A Local LLM Code Repair Arena with SQLite Leaderboards"
description: "NEO built a Gradio-based arena that pits two local LLMs against each other on code repair tasks, scoring each patch 0-100 and logging every duel to SQLite for persistent leaderboards."
date: 2026-03-28
tags: [llm, code-repair, gradio, ollama, benchmarking]
slug: patchduel-local-llm-code-repair
github: https://github.com/dakshjain-1616/patchduel-local-llm-code-repair
---

# PatchDuel: A Local LLM Code Repair Arena with SQLite Leaderboards

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/patchduel-local-llm-code-repair)

![Pipeline Architecture](../public/images/diagrams/patchduel-local-llm-code-repair.png)

## The Problem

> Choosing between two local models for a code repair task usually means running each one manually, reading the outputs, and making a judgment call. There is no systematic way to accumulate evidence about which model performs better across many bugs over time.

NEO built PatchDuel to make this comparison rigorous. Two models run simultaneously on the same buggy snippet, each gets a quality score, and every result is stored in SQLite. Over time you build a real leaderboard, not a one-off impression.

## The Arena Model

PatchDuel runs as a Gradio web app at `http://localhost:7860`. The interface has three tabs: arena, leaderboard, and history.

In the **arena tab**, you pick two models (called Model A and Model B), select a built-in bug scenario or paste your own code, and click Run. Both models generate fixes simultaneously. The result is a split-screen view with a git-style diff for each model, showing exactly which lines changed. Below each diff you see timing in seconds, estimated token count, and the quality score.

The **leaderboard tab** shows wins, losses, and ties per model sorted by win count. The **history tab** shows every past duel with full reproducibility data: both patches, both diffs, the winner, and any judge notes.

This structure means each duel contributes to a running evidence base. After 50 duels, the leaderboard reflects real performance data rather than vibes.

## Quality Scoring

Each patch receives a **quality score** from 0 to 100 based on how much of the file changed relative to an expected fix.

An exact match with the expected fix scores 100. A surgical fix that changes less than 5% of the file scores 90. A moderate fix at 5 to 15% scores 80. A large rewrite at 15 to 40% scores 65. A full rewrite above 40% scores 40. A model that returns the code unchanged scores 0.

A +15 bonus applies if the patch closely approximates the expected fix (within 10 characters), capped at 100. The heuristic winner is the model with the higher score. When both patches are identical, a tie is declared.

```python
from patchduel_local_llm_ import compute_quality_score, heuristic_winner

buggy    = "def add(a, b):\n    return a - b  # Bug"
expected = "def add(a, b):\n    return a + b"

patch_a = repair_code("llama3.2", buggy)
patch_b = repair_code("mistral",  buggy)

score_a = compute_quality_score(buggy, patch_a, expected)
score_b = compute_quality_score(buggy, patch_b, expected)
winner  = heuristic_winner(buggy, patch_a, patch_b, expected)
```

The scoring function is deterministic and has no LLM calls. You can run it offline to re-score historical patches if you change the expected fix.

## Eight Built-In Bug Scenarios

The tool ships eight hand-crafted Python bugs tagged by difficulty. These cover the most common categories of code repair tasks.

Easy scenarios include an arithmetic operator bug (`-` instead of `+`) and a wrong guard return. Medium scenarios cover off-by-one loop errors (`range(len+1)`), missing None checks, wrong logical operators (`and` vs `or`), string vs integer comparison, and wrong string method (`.strip()` called on a list). The hard scenario is a mutable default argument, the classic Python gotcha where a list or dict default is shared across all calls.

You can paste any custom code directly in the UI. The expected fix is optional for custom inputs. Without it, the quality score uses file change percentage only, without the exact-match bonus.

## Three Providers

**Ollama** is the primary local provider. Pull any model and point PatchDuel at it. No API cost, fully private, no data leaves the machine.

**OpenRouter** gives access to cloud models including GPT-4o, Claude, and Mistral via a single API key. You can duel a local Ollama model against a cloud model to benchmark the capability gap at a given task.

**Mock** runs with no setup. It produces deterministic patches and is the recommended provider for first-run testing and CI.

```bash
# Set up Ollama
ollama pull llama3.2
ollama pull mistral

# Set up OpenRouter (optional)
echo "OPENROUTER_API_KEY=sk-or-..." > .env

python app.py
# Open http://localhost:7860
```

## SQLite Persistence

Every duel is stored in `patchduel.db` with 18 columns: timestamp, model names, buggy code, both patches, rendered HTML diffs, winner, judge notes, latency per model, token counts, providers, and scenario ID. The schema stores everything needed to reproduce any past duel exactly.

```python
from patchduel_local_llm_ import export_runs_csv, get_leaderboard

# Export all runs to CSV
csv_data = export_runs_csv()
with open("runs.csv", "w") as f:
    f.write(csv_data)

# Print leaderboard
for row in get_leaderboard():
    print(row["model"], row["wins"], row["win_rate"])
```

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Gradio web app called PatchDuel that runs two local LLMs head-to-head on Python code repair tasks. Each model generates a fix simultaneously, show split-screen git-style diffs, and score each patch 0-100: exact match scores 100, surgical fix under 5% change scores 90, moderate fix 5-15% scores 80, large rewrite 15-40% scores 65, full rewrite above 40% scores 40, unchanged scores 0 with a +15 bonus for near-exact match capped at 100. Support Ollama, OpenRouter, and a deterministic mock provider. Store every duel in SQLite with 18 columns including both patches, HTML diffs, winner, latency, and token counts. Show a leaderboard tab sorted by win count and a history tab with full reproducibility data."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20Gradio%20web%20app%20called%20PatchDuel%20that%20runs%20two%20local%20LLMs%20head-to-head%20on%20Python%20code%20repair%20tasks.%20Each%20model%20generates%20a%20fix%20simultaneously%2C%20show%20split-screen%20git-style%20diffs%2C%20and%20score%20each%20patch%200-100%3A%20exact%20match%20scores%20100%2C%20surgical%20fix%20under%205%25%20change%20scores%2090%2C%20moderate%20fix%205-15%25%20scores%2080%2C%20large%20rewrite%2015-40%25%20scores%2065%2C%20full%20rewrite%20above%2040%25%20scores%2040%2C%20unchanged%20scores%200%20with%20a%20%2B15%20bonus%20for%20near-exact%20match%20capped%20at%20100.%20Support%20Ollama%2C%20OpenRouter%2C%20and%20a%20deterministic%20mock%20provider.%20Store%20every%20duel%20in%20SQLite%20with%2018%20columns%20including%20both%20patches%2C%20HTML%20diffs%2C%20winner%2C%20latency%2C%20and%20token%20counts.%20Show%20a%20leaderboard%20tab%20sorted%20by%20win%20count%20and%20a%20history%20tab%20with%20full%20reproducibility%20data." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add eight built-in bug scenarios tagged by difficulty (arithmetic operator bug through mutable default argument), add CSV export of the full SQLite run history, or add programmatic API access so duels can be scripted without launching the Gradio UI.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/patchduel-local-llm-code-repair
cd patchduel-local-llm-code-repair
pip install -r requirements.txt
python app.py
```

Open `http://localhost:7860`, select Mock for both models, pick a bug scenario, and run your first duel — no API key or Ollama install needed.

NEO built a local LLM code repair arena with split-screen diffs, quality scoring, and SQLite-backed leaderboards that accumulate evidence across duels over time. See what else NEO ships at [heyneo.so](https://heyneo.so()).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
