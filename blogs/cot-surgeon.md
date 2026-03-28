---
title: "CoT Surgeon: Surgical Editing for LLM Reasoning Chains"
description: "NEO built a tool that parses LLM chain-of-thought output into an editable graph, lets you fix individual reasoning steps, and recalculates all downstream conclusions."
date: 2026-03-28
tags: [llm, chain-of-thought, reasoning, graph, python]
slug: cot-surgeon
github: https://github.com/dakshjain-1616/cot-surgeon
---

# CoT Surgeon: Surgical Editing for LLM Reasoning Chains

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/cot-surgeon)

![Pipeline Architecture](../public/images/diagrams/cot-surgeon.png)

## The Problem

> LLMs produce chain-of-thought reasoning as unstructured prose. When one step is wrong, you re-run the entire prompt and hope the model self-corrects. There is no way to pinpoint the bad step, fix it, and propagate the correction without touching the rest.

NEO built CoT Surgeon to parse reasoning chains into a typed graph, expose individual nodes for editing, and recalculate only the affected downstream path.

## The ReasoningGraph Structure

**CoT Surgeon** converts LLM output into a `ReasoningGraph`, a directed acyclic graph where every node has a type and a confidence score.

Three node types cover the full reasoning structure:

- **FACT** — grounded, verifiable premises. Example: "The atmosphere contains N2, O2, and suspended particles."
- **REASONING** — inferential steps derived from facts. Example: "Rayleigh scattering causes shorter wavelengths to scatter more."
- **CONCLUSION** — the final answer derived from the reasoning chain.

Each node carries a `confidence` float between 0.0 and 1.0, estimated by the LLM during generation. Nodes below the `CONFIDENCE_THRESHOLD` (default 0.7) are flagged as low-confidence and highlighted in both the Streamlit UI and Mermaid exports.

## The Edit and Recalculate Workflow

The core operation is surgical: fix one node, regenerate only the path that depends on it.

```python
from cot_surgeon import ReasoningEngine

engine = ReasoningEngine(mode="mock")
graph = engine.generate_cot("Why is the sky blue?")

# Find low-confidence nodes
weak = graph.low_confidence_nodes(threshold=0.75)
for node in weak:
    print(f"{node.id}  conf={node.confidence:.2f}  {node.content}")

# Fix the flawed step
graph.update_node("node_3", "Rayleigh scattering causes shorter wavelengths to scatter more strongly.")

# Recalculate everything downstream — upstream nodes are untouched
graph = engine.recalculate_from_node(graph, "node_3")
```

Nodes that do not depend on `node_3` are never touched. The graph's `version` counter increments on every edit. Every mutation pushes a snapshot onto an internal history stack with a default depth of 20, so `graph.undo()` steps back through changes.

## Confidence Scoring and Graph Stats

After generation or recalculation, `graph.stats()` returns a summary:

```python
stats = graph.stats()
# {
#   "node_count": 5,
#   "avg_confidence": 0.89,
#   "low_confidence_count": 1,
#   "edit_count": 1,
#   "version": 2
# }
```

Low-confidence nodes receive a distinct color in **Mermaid** exports. Edited nodes are rendered in purple so you can see exactly which parts of a graph were modified.

## LLM Backend Priority

Three backends are supported in auto mode:

1. **OpenRouter** — used when `OPENROUTER_API_KEY` is set
2. **Local llama.cpp** — used when `LLAMA_MODEL_PATH` is set
3. **Mock** — always available, uses built-in templates, no API key needed

Pass `mode` explicitly to bypass auto-detection:

```python
engine = ReasoningEngine(mode="openrouter")  # cloud
engine = ReasoningEngine(mode="local")       # llama.cpp GGUF
engine = ReasoningEngine(mode="mock")        # no key needed
```

## How to Build This

Clone the repo and install:

```bash
git clone https://github.com/dakshjain-1616/cot-surgeon
cd cot-surgeon
pip install -r requirements.txt
```

For the Streamlit UI:

```bash
pip install streamlit
streamlit run app.py
```

For local llama.cpp inference:

```bash
pip install llama-cpp-python
export LLAMA_MODEL_PATH=/path/to/model.gguf
```

Run the CLI demo:

```bash
python scripts/demo.py          # auto-detect backend
python scripts/demo.py --local  # force local llama.cpp
python scripts/demo.py --batch  # batch comparison demo
```

The Streamlit interface has two tabs. **Single Analysis** lets you generate a reasoning graph, inspect nodes, edit content, trigger recalculation, and export Mermaid. **Batch Compare** runs multiple prompts in parallel and displays graphs side-by-side, useful for regression testing prompt changes.

Run the test suite:

```bash
pytest tests/test_reasoning.py -v
# 104 tests covering node creation, graph construction, confidence scoring,
# edit / undo / recalculate, Mermaid export, batch analysis, and error handling
```

NEO built a structured reasoning editor that treats LLM chain-of-thought as inspectable, editable, and version-controlled data. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
