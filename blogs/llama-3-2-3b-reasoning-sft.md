---
title: "Llama 3.2 3B Reasoning SFT: On-Device Chain-of-Thought via LoRA Distillation"
description: "NEO built a supervised fine-tuning pipeline that adds DeepSeek-R1-style reasoning to Llama 3.2 3B, exporting a 2 GB GGUF that runs at 12 tok/s on a Raspberry Pi 5."
date: 2026-03-28
tags: [llm, fine-tuning, lora, gguf, reasoning]
slug: llama-3-2-3b-reasoning-sft
github: https://github.com/dakshjain-1616/llama-3-2-3b-reasoning-sft
---

# Llama 3.2 3B Reasoning SFT: On-Device Chain-of-Thought via LoRA Distillation

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/llama-3-2-3b-reasoning-sft)
[![View on HuggingFace](https://img.shields.io/badge/View_on_HuggingFace-FF9D00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/daksh-neo/llama-3-2-3b-reasoning-sft)

![Pipeline Architecture](../public/images/diagrams/llama-3-2-3b-reasoning-sft.png)

## The Problem

> Edge devices like phones and Raspberry Pi cannot run cloud LLMs due to latency or privacy constraints. Existing 3B models produce single-shot answers without structured reasoning, making outputs hard to audit or verify.

NEO built this pipeline to add `<think>` reasoning traces to Llama 3.2 3B via knowledge distillation, then export the result as a 2 GB GGUF that runs locally on any device with 4 GB RAM.

## The Distillation Pipeline

**Response-Only Training** is the central technique. The model trains only on the assistant's response tokens. User prompt tokens are masked with `labels = -100`, so no gradient flows through them.

The label mask looks like this:

```
<|start_header_id|>user<|end_header_id|>     → labels = -100
What is 17 × 24?                             → labels = -100
<|eot_id|>                                   → labels = -100
<|start_header_id|>assistant<|end_header_id|> → labels = -100

<think>                                      → labels = token_id ✅
17 × 24 = 17×20 + 17×4 = 340 + 68           → labels = token_id ✅
</think>                                     → labels = token_id ✅
17 × 24 = **408**                            → labels = token_id ✅
```

This teaches the model how to reason rather than how to echo prompts.

## LoRA Configuration

**Unsloth** handles the LoRA injection. The adapter targets the attention projection layers only:

| Parameter | Value |
|-----------|-------|
| Rank (r) | 16 |
| Alpha | 32 |
| Target modules | q_proj, v_proj, k_proj, o_proj |
| Dropout | 0.05 |
| Max sequence length | 4096 |
| Quantization (training) | 4-bit NF4 |
| Optimizer | AdamW 8-bit |
| Epochs | 3 |

The base model runs in 4-bit NF4 during training, so the full pipeline fits in 8 GB GPU VRAM. The LoRA adapter itself is approximately 80 MB. After training, `merge_and_unload()` merges adapter weights into the base model for export.

## GGUF Export and Quantization

The merged model passes through llama.cpp's converter and quantizer to produce a `Q4_K_M` file:

| Quantization | Size | RAM Needed | Speed |
|--------------|------|------------|-------|
| Q4_K_M | ~1.6 GB | 4 GB | ~12 tok/s on Pi 5 |
| Q5_K_M | ~1.96 GB | 4 GB | slightly slower |
| Q8_0 | ~2.89 GB | 6 GB | best quality |

Q4_K_M hits the practical sweet spot. It runs on a Raspberry Pi 5, any Android phone with 4 GB RAM, and Apple M1 Macs.

## What the Reasoning Output Looks Like

```
Input: Why does ice float on water?

<think>
Water molecules form hydrogen bonds. In ice they arrange into a
hexagonal lattice — more space between molecules than liquid water.
Ice density = 0.917 g/cm³ vs liquid water 1.0 g/cm³ → floats.
</think>

Ice floats because it is less dense (0.917 g/cm³) than liquid water
(1.0 g/cm³). The hexagonal hydrogen-bond lattice in ice creates more
space between molecules than the compact liquid structure.
```

The `<think>` block is auditable. You can verify the reasoning steps before trusting the conclusion.

## How to Build This

**To run training yourself**, clone the repo and install:

```bash
git clone https://github.com/dakshjain-1616/llama-3-2-3b-reasoning-sft
cd llama-3-2-3b-reasoning-sft
pip install -r requirements.txt
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

Set your HuggingFace token and run training:

```bash
export HF_TOKEN=hf_your_token_here
python -m llama32_reasoning_sft train
```

Export to GGUF and push to Hub:

```bash
export HF_REPO_ID=your-hf-username/your-repo-name
python -m llama32_reasoning_sft export
```

**To use the released model directly**, pull it from HuggingFace:

```bash
pip install huggingface_hub transformers
huggingface-cli download daksh-neo/llama-3-2-3b-reasoning-sft --local-dir ./model
```

Load and run inference:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("daksh-neo/llama-3-2-3b-reasoning-sft")
tokenizer = AutoTokenizer.from_pretrained("daksh-neo/llama-3-2-3b-reasoning-sft")
inputs = tokenizer("What is 15% of 240?", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0]))
```

For llama.cpp inference directly:

```bash
./llama-cli -m model-q4_k_m.gguf \
  -p "<|start_header_id|>user<|end_header_id|>

Why is the sky blue?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

<think>" -n 256
```

Try a dry run without GPU or API key:

```bash
python demo.py
# Completes in ~0.12s, shows config, dataset validation, and GGUF size estimates
```

NEO built a distillation pipeline that gives a 3B model structured reasoning traces while keeping inference under 2 GB and fully offline. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
