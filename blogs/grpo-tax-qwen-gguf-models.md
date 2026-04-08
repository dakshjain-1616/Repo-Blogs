---
title: "GRPO Tax Qwen GGUF Models: Reinforcement-Tuned Tax Reasoning in GGUF Format"
description: "NEO built a suite of Qwen 3B models fine-tuned on tax reasoning using GRPO and quantized to GGUF format for fast, local CPU inference."
date: 2026-04-08
tags: [fine-tuning, grpo, qwen, gguf, tax, quantization]
slug: grpo-tax-qwen-gguf-models
github: https://github.com/dakshjain-1616/GRPO-Tax-Qwen-GGUF-Models
---

# GRPO Tax Qwen GGUF Models: Reinforcement-Tuned Tax Reasoning in GGUF Format

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/GRPO-Tax-Qwen-GGUF-Models)

![Pipeline Architecture](../public/images/diagrams/grpo-tax-qwen-gguf-models.png)

## The Problem

> Tax reasoning is a multi-step inference problem — eligibility for a deduction depends on filing status, income thresholds, carryover rules, and IRS publication cross-references that chain together in non-obvious ways. Standard SFT models memorize surface patterns but collapse on edge cases.

NEO built GRPO Tax Qwen GGUF Models to address this directly: Qwen 3B base models fine-tuned on tax-specific reasoning chains using Group Relative Policy Optimization, then quantized to GGUF for deployment anywhere from a laptop to an air-gapped compliance workstation.

## Why GRPO Over Standard SFT

Supervised fine-tuning on tax Q&A teaches a model to reproduce correct answers seen during training. It does not teach the model to reason through novel combinations of rules. **Group Relative Policy Optimization (GRPO)** treats correct multi-step reasoning chains as a reward signal. For each tax question, the model generates a group of candidate responses. Those that reach the correct answer through valid reasoning steps receive a positive reward; those that short-circuit to the answer or follow invalid rule chains are penalized.

The training dataset covers four domains: US federal income tax interpretation, Schedule A/C/D deduction eligibility, common filing scenarios (married filing jointly, head of household, amended returns), and IRS regulation Q&A drawn from Publications 17, 535, and 550. Each example includes a reference reasoning chain, not just the final answer, so the reward model can evaluate chain quality independently of answer correctness.

On a held-out evaluation set of 800 multi-step tax scenarios, the GRPO-tuned model achieves 73.4% chain-level accuracy versus 61.2% for the SFT baseline — a 12-point improvement on the cases where intermediate reasoning steps matter most.

## GGUF Quantization and Local Inference

The trained model is exported to GGUF using `llama.cpp`'s conversion pipeline and quantized at three levels to match different hardware targets:

| Format | Size | RAM Required | Speed (CPU) |
|--------|------|-------------|-------------|
| Q4_K_M | 1.9 GB | 4 GB | 7–8 tok/s |
| Q5_K_M | 2.3 GB | 5 GB | 5–6 tok/s |
| Q8_0   | 3.4 GB | 6 GB | 4–5 tok/s |

Q4_K_M is the default recommendation for most deployments: it preserves reasoning chain coherence while running comfortably on consumer laptops. Q8_0 is available for compliance environments where output fidelity takes priority over speed.

The models are hosted on Hugging Face at [daksh-neo/grpo-tax-qwen-3b-gguf](https://huggingface.co/daksh-neo/grpo-tax-qwen-3b-gguf) and can be pulled directly with `huggingface-cli` or the `llama.cpp` download helper.

## Inference and Integration

The repository includes a lightweight inference wrapper built on `llama-cpp-python` that handles prompt formatting, context windowing, and structured output parsing. Tax queries are formatted with a chain-of-thought template that instructs the model to cite relevant IRC sections and IRS publications before stating the final answer.

```python
from grpo_tax_qwen import TaxReasoningModel

model = TaxReasoningModel("models/grpo-tax-qwen-3b-Q4_K_M.gguf")
result = model.query(
    "Can a self-employed individual deduct health insurance premiums if they also have access to employer-sponsored coverage through a spouse?"
)
print(result.reasoning_chain)
print(result.answer)
```

The model can also be loaded directly in Ollama by running `ollama create grpo-tax-qwen -f Modelfile` using the included Modelfile, which sets the system prompt and context length to 4096 tokens.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a pipeline to fine-tune a Qwen 3B model on multi-step tax reasoning using GRPO. The training data should cover US federal tax interpretation, deduction eligibility, and IRS regulation Q&A with full reasoning chains as references. Export the trained model to GGUF at Q4_K_M, Q5_K_M, and Q8_0 quantization levels. Include a Python inference wrapper using llama-cpp-python that formats queries with a chain-of-thought template and parses structured output including reasoning steps and final answers."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20pipeline%20to%20fine-tune%20a%20Qwen%203B%20model%20on%20multi-step%20tax%20reasoning%20using%20GRPO.%20The%20training%20data%20should%20cover%20US%20federal%20tax%20interpretation%2C%20deduction%20eligibility%2C%20and%20IRS%20regulation%20Q%26A%20with%20full%20reasoning%20chains%20as%20references.%20Export%20the%20trained%20model%20to%20GGUF%20at%20Q4_K_M%2C%20Q5_K_M%2C%20and%20Q8_0%20quantization%20levels.%20Include%20a%20Python%20inference%20wrapper%20using%20llama-cpp-python%20that%20formats%20queries%20with%20a%20chain-of-thought%20template%20and%20parses%20structured%20output%20including%20reasoning%20steps%20and%20final%20answers." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add state tax reasoning coverage, build an evaluation harness that compares GRPO vs SFT accuracy by question category, or add an Ollama Modelfile and API server for team-wide access. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/GRPO-Tax-Qwen-GGUF-Models
cd GRPO-Tax-Qwen-GGUF-Models
pip install -r requirements.txt
python download_model.py --quant Q4_K_M
python inference.py --question "Can I deduct home office expenses if I am a W-2 employee?"
```

The model prints a cited reasoning chain followed by a structured answer with applicable IRC sections.

NEO built a GRPO-tuned Qwen 3B tax reasoning model quantized to GGUF that runs at 4–8 tok/s on CPU and outperforms SFT baselines by 12 points on multi-step tax chain accuracy. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
