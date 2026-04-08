---
title: "Context Audit: Analyzing What Your LLM Actually Uses from Its Context Window"
description: "NEO built a tool that uses attention weight analysis and ablation testing to score which segments of a context window actually influence an LLM's output."
date: 2026-04-08
tags: [llm, context, interpretability, analysis, optimization]
slug: context-audit
github: https://github.com/dakshjain-1616/Context-Audit
---

# Context Audit: Analyzing What Your LLM Actually Uses from Its Context Window

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/Context-Audit)

![Pipeline Architecture](../public/images/diagrams/context-audit.png)

## The Problem

> Teams stuff 32K-token context windows with system prompts, retrieved chunks, conversation history, and tool outputs — then pay for every token whether the model reads it or not.

NEO built Context Audit to quantify exactly which segments of a context window influence the model's output, so teams can cut the dead weight.

## Attention-Based Influence Scoring

**Context Audit** begins by segmenting the context window into named spans: `system_prompt`, `retrieved_chunk_N`, `conversation_turn_N`, and `tool_output_N`. Each span boundary is tracked by token offset. The tool then runs a forward pass through the model with `output_attentions=True` and aggregates attention weights from every layer and head over the output token positions.

For each context segment, the influence score is the mean attention mass flowing from output tokens back to that segment's token range, averaged across all layers and heads:

```python
from context_audit import ContextAuditor

auditor = ContextAuditor(model="meta-llama/Llama-3.1-8B-Instruct")

segments = {
    "system_prompt": "You are a helpful assistant...",
    "retrieved_chunk_1": "Our refund policy states...",
    "retrieved_chunk_2": "Shipping typically takes 3-5 days...",
    "user_query": "Can I return my order?"
}

report = auditor.analyze(segments, query=segments["user_query"])
print(report.influence_scores)
# {'system_prompt': 0.08, 'retrieved_chunk_1': 0.61, 'retrieved_chunk_2': 0.04, 'user_query': 0.27}
```

Segments with influence scores below a configurable threshold (default 0.05) are flagged as candidates for removal.

## Ablation Testing for Causal Confirmation

Attention weights reveal correlation, not causation — a segment can receive high attention without changing the output. Context Audit follows up with targeted ablation tests: it replaces each segment with a same-length noise span, re-runs inference, and measures output divergence using token-level KL divergence between the original and ablated output distributions.

This produces a second metric, the **ablation sensitivity score**, that captures true causal influence. Segments that score high on attention but low on ablation sensitivity are labeled `attended_but_ignorable` — a common pattern for boilerplate system prompt text that the model reads but ignores for the specific query type.

The combined audit report ranks segments by a weighted average of both scores:

| Segment | Attention Score | Ablation Sensitivity | Final Rank |
|---|---|---|---|
| retrieved_chunk_1 | 0.61 | 0.78 | 1 |
| user_query | 0.27 | 0.91 | 2 |
| system_prompt | 0.08 | 0.12 | 3 |
| retrieved_chunk_2 | 0.04 | 0.03 | 4 |

## Cost Reduction Recommendations

After scoring, Context Audit generates a context optimization report with concrete token-count savings. For each `zero_influence` segment it produces a removal recommendation; for long segments with partial influence it identifies the specific sub-spans that matter using a sliding-window ablation at sentence granularity.

Teams running RAG pipelines have used the tool to discover that 40-60% of their retrieved chunks contribute nothing to the final answer on a typical query. Removing those chunks cuts latency and cost without measurable accuracy loss:

```bash
python audit.py \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --context context.json \
  --output report.html \
  --ablation_samples 10
```

The HTML report includes an interactive token heatmap, the ranked segment table, and a projected cost savings estimate based on the current model's per-token price.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a context window analysis tool that segments a prompt into named spans, runs attention weight extraction across all layers and heads to score each segment's influence, then runs ablation tests by replacing segments with noise and measuring KL divergence on output distributions, producing a ranked influence report and HTML heatmap."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20context%20window%20analysis%20tool%20that%20segments%20a%20prompt%20into%20named%20spans%2C%20runs%20attention%20weight%20extraction%20across%20all%20layers%20and%20heads%20to%20score%20each%20segment%27s%20influence%2C%20then%20runs%20ablation%20tests%20by%20replacing%20segments%20with%20noise%20and%20measuring%20KL%20divergence%20on%20output%20distributions%2C%20producing%20a%20ranked%20influence%20report%20and%20HTML%20heatmap." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add support for closed-source models via proxy attention approximation, build a CLI for batch-auditing entire eval datasets, or integrate cost projections for specific model pricing tables. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/Context-Audit
cd Context-Audit
pip install -r requirements.txt
python audit.py --model meta-llama/Llama-3.1-8B-Instruct --context examples/rag_context.json
```

Open `report.html` to see the interactive token heatmap and segment rankings with cost savings projections.

NEO built an interpretability tool that measures exactly which parts of a context window an LLM reads and which it ignores, enabling data-driven context pruning. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
