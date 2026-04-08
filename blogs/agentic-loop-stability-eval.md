---
title: "Agentic Loop Stability Evaluator: Detecting Drift and Loops in Autonomous Agents"
description: "NEO built an evaluation framework that runs agentic loops for a configurable number of steps and detects instability patterns including infinite loops, goal drift, context collapse, and action oscillation."
date: 2026-04-08
tags: [agents, evaluation, stability, llm, safety]
slug: agentic-loop-stability-eval
github: https://github.com/dakshjain-1616/agentic-loop-stability-eval
---

# Agentic Loop Stability Evaluator: Detecting Drift and Loops in Autonomous Agents

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/agentic-loop-stability-eval)

![Pipeline Architecture](../public/images/diagrams/agentic-loop-stability-eval.png)

## The Problem

> Autonomous agents fail in ways that unit tests cannot catch. A loop that looks productive after 10 steps may be spinning in circles after 30, silently dropping the original goal, or oscillating between two contradictory actions without making progress.

NEO built the Agentic Loop Stability Evaluator to instrument agent execution at each step and detect these failure patterns before they reach production.

## Four Instability Patterns and How They Are Detected

**The evaluator** monitors four distinct failure modes during a live agent run. Each has its own detection logic that operates on the step trace in real time.

**Infinite loops** are detected by hashing each tool call — the function name plus a normalized representation of its arguments — and checking against a rolling window of the last N calls. If the same hash appears more than `loop_threshold` times (default: 3) within `loop_window` steps (default: 10), the step is flagged as a loop and the agent is halted or warned depending on the configured action.

**Goal drift** is detected using semantic similarity between the agent's current stated objective (extracted from each step's reasoning trace) and the original task description. The evaluator embeds both strings using a sentence-transformer model and computes cosine distance. If distance exceeds `drift_threshold` (default: 0.35) for two consecutive steps, the step is annotated with a drift warning.

**Context collapse** is detected by tracking which key facts from the original task are still referenced in the agent's active context window. A set of anchor phrases is extracted from the original task at initialization. At each step, the evaluator checks whether those anchors appear in the last K tokens of context. Missing anchors trigger a collapse annotation.

**Action oscillation** is detected by comparing the last four actions for an ABAB alternation pattern. If the agent switches between two semantically similar action clusters more than `oscillation_threshold` times in a row, the step is flagged.

## Step Trace and Stability Score

Every agent run produces a **step-by-step trace** in `traces/run_<timestamp>.json`. Each step entry records the action taken, tool calls made, reasoning text, and any instability annotations:

```json
{
  "step": 14,
  "action": "search_web",
  "args": { "query": "Python async event loop" },
  "annotations": [
    { "type": "loop", "detail": "Repeated call #4 within window of 10" }
  ],
  "stability_flags": ["loop"]
}
```

At the end of each run, the evaluator computes a **stability score** from 0 to 1. The score starts at 1.0 and is penalized for each flagged step, with heavier penalties for loop and collapse events (0.15 each) than for drift and oscillation (0.08 each). A score above 0.85 is considered stable; below 0.6 triggers a critical warning in the summary report.

## Configuration and Integration

The evaluator wraps any agent loop through a simple callback interface. Pass your step function to the `StabilityEvaluator` wrapper and it instruments each call transparently:

```python
from stability_eval import StabilityEvaluator

evaluator = StabilityEvaluator(
    original_task="Summarize the top 5 papers on attention mechanisms from 2024",
    max_steps=50,
    loop_threshold=3,
    drift_threshold=0.35,
)

with evaluator.run() as ctx:
    for step in agent_loop(task):
        ctx.record(step)

print(evaluator.stability_score())
evaluator.save_trace("traces/")
```

Thresholds are fully configurable via YAML or constructor arguments. The evaluator supports early stopping on critical instability, or passive monitoring mode where it records without intervening.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python evaluation framework that wraps agentic loops and detects four instability patterns: infinite loops via tool-call hashing, goal drift via cosine similarity between current objective and original task, context collapse via anchor-phrase tracking, and action oscillation via ABAB pattern detection. Produce a per-step annotated trace JSON and a final stability score from 0 to 1 with configurable thresholds."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20Python%20evaluation%20framework%20that%20wraps%20agentic%20loops%20and%20detects%20four%20instability%20patterns%3A%20infinite%20loops%20via%20tool-call%20hashing%2C%20goal%20drift%20via%20cosine%20similarity%20between%20current%20objective%20and%20original%20task%2C%20context%20collapse%20via%20anchor-phrase%20tracking%2C%20and%20action%20oscillation%20via%20ABAB%20pattern%20detection.%20Produce%20a%20per-step%20annotated%20trace%20JSON%20and%20a%20final%20stability%20score%20from%200%20to%201%20with%20configurable%20thresholds." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a real-time dashboard that visualizes the trace as the agent runs, build a replay mode for inspecting past traces interactively, or add integration tests for each instability detector. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/agentic-loop-stability-eval
cd agentic-loop-stability-eval
pip install -r requirements.txt
python eval.py --agent examples/research_agent.py --task "Summarize 2024 attention papers" --max-steps 50
```

The evaluator runs the agent, annotates every step, prints a stability score, and writes the full trace to `traces/`.

NEO built an agentic loop stability evaluator that detects infinite loops, goal drift, context collapse, and action oscillation in real time and produces a scored, annotated step trace for every run. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
