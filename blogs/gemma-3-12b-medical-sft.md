---
title: "Gemma 3 12B Medical SFT: Offline Clinical Reasoning via LoRA Fine-Tuning"
description: "NEO built a supervised fine-tuning pipeline that adapts Gemma-3-12B for medical reasoning across symptom triage, drug interactions, and lab interpretation, exporting a 7.8 GB GGUF for fully offline clinical decision support."
date: 2026-03-28
tags: [llm, fine-tuning, medical, lora, gguf]
slug: gemma-3-12b-medical-sft
github: https://github.com/dakshjain-1616/gemma3-medical-sft
---

# Gemma 3 12B Medical SFT: Offline Clinical Reasoning via LoRA Fine-Tuning

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/gemma3-medical-sft)
[![View on HuggingFace](https://img.shields.io/badge/View_on_HuggingFace-FF9D00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/daksh-neo/gemma-3-12b-medical-sft)

![Pipeline Architecture](../public/images/diagrams/gemma-3-12b-medical-sft.png)

> **Important:** This model is for research and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

## The Problem

> Clinicians in resource-limited settings need decision-support tools that work without internet connectivity and cannot transmit patient data to cloud APIs. General-purpose LLMs are not trained on clinical reasoning formats and cannot be used where HIPAA or GDPR apply to patient data.

NEO built this fine-tuning pipeline to adapt Gemma-3-12B for structured medical reasoning, then export the result as a 7.8 GB GGUF that runs fully offline on a standard 16 GB laptop.

## Three Medical Domains

**Gemma-3-12B Medical SFT** handles three clinical reasoning tasks:

1. **Symptom triage** — given a set of presenting symptoms, the model produces a differential diagnosis with risk stratification (LOW / MEDIUM / HIGH).
2. **Drug interaction checking** — given a medication list, the model identifies known interactions and severity levels.
3. **Lab result interpretation** — given lab values with reference ranges, the model flags abnormalities and suggests clinical context.

All three use the same `<think>` block structure, which shows a five-step differential reasoning chain before the final answer. This makes the output auditable: you can inspect the reasoning steps before accepting the conclusion.

## The Training Pipeline

The pipeline follows four stages:

1. **Synthetic data generation** — 1,000 medical cases generated with seeded randomization for reproducibility. Each case is tagged with domain, severity, and reasoning step count.
2. **4-bit model loading** — Gemma-3-12B loads in 4-bit NF4 to fit GPU VRAM during training.
3. **Response-Only LoRA training** — user turns and reasoning prefixes are masked. Loss flows only through the model's response tokens.
4. **LoRA merge and GGUF export** — the 200 MB adapter merges into the base weights, then llama.cpp quantizes to Q4_K_M.

The **Response-Only Training** approach is critical. Without masking user tokens, the model wastes training capacity memorizing prompts instead of learning how to reason through clinical presentations.

## LoRA Configuration

| Parameter | Value |
|-----------|-------|
| Rank (r) | 32 |
| Alpha | 64 |
| Max sequence length | 4096 |
| Training epochs | 3 |
| Learning rate | 2e-4 |
| Quantization (training) | 4-bit NF4 |
| Adapter size | ~200 MB |

The training format uses Gemma-3 chat syntax:

```
<start_of_turn>user
Patient presents with chest pain, shortness of breath, diaphoresis.<end_of_turn>
<start_of_turn>model
<think>
Step 1: Identify cardinal symptoms...
Step 2: Consider differential diagnoses...
Step 3: Evaluate risk factors...
Step 4: Apply clinical decision rules...
Step 5: Determine risk stratification...
</think>
Primary consideration: ACS. Risk level: HIGH.
Immediate ECG and troponin indicated.<end_of_turn>
```

## GGUF Quantization Options

| Quantization | Size | RAM Needed |
|--------------|------|------------|
| Q4_K_M | 7.8 GB | 16 GB |
| Q5_K_M | 9.1 GB | 16 GB |
| Q8_0 | ~15 GB | 32 GB |

Q4_K_M fits on any MacBook M2 or standard laptop with 16 GB RAM. No GPU is required for inference.

## How to Build This

**To run training yourself**, clone the repo and install:

```bash
git clone https://github.com/dakshjain-1616/gemma3-medical-sft
cd gemma3-medical-sft
pip install -r requirements.txt
```

Set your HuggingFace token and configure training parameters via environment variables, then run:

```bash
export HF_TOKEN=hf_your_token_here
python -m gemma3_medical_sft train
```

Generate the synthetic dataset separately:

```bash
python -m gemma3_medical_sft generate-dataset
```

Export to GGUF:

```bash
python -m gemma3_medical_sft export
```

**To use the released model directly**, pull it from HuggingFace:

```bash
pip install huggingface_hub transformers
huggingface-cli download daksh-neo/gemma-3-12b-medical-sft --local-dir ./model
```

Load and run inference:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("daksh-neo/gemma-3-12b-medical-sft")
tokenizer = AutoTokenizer.from_pretrained("daksh-neo/gemma-3-12b-medical-sft")
inputs = tokenizer("Patient presents with fever, productive cough, and pleuritic chest pain.", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0]))
```

Try the dry run without any GPU or API key:

```bash
python demo.py
```

All environment variables are configurable: `LORA_R`, `LORA_ALPHA`, `MAX_SEQ_LENGTH`, `NUM_TRAIN_EPOCHS`, `BATCH_SIZE`, `LEARNING_RATE`, `GGUF_QUANT`. Set `DRY_RUN=1` to run two mock training steps without downloading the model.

NEO built a medical reasoning model that runs entirely on-device, keeps patient data local, and shows its differential diagnosis reasoning in auditable `<think>` blocks. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
