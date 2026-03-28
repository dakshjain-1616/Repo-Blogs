---
title: "Qwen2.5-VL-7B Nike LoRA — GGUF Q8_0 Vision Quantization Pipeline"
description: "NEO built a merge-quantize-benchmark pipeline for a Nike-fine-tuned Qwen2.5-VL-7B vision model, producing a 4.5 GB Q8_0 GGUF that fits in 8 GB VRAM."
date: 2026-03-28
tags: [gguf, vision-language-model, lora, quantization, qwen2-5-vl]
slug: qwen25-vl-7b-nike-lora-gguf
github: https://github.com/dakshjain-1616/erichflam-hkust-qwen2-5-vl-7b
huggingface: https://huggingface.co/daksh-neo/Qwen2.5-VL-7B-Nike-LoRA-GGUF
---

# Qwen2.5-VL-7B Nike LoRA — GGUF Q8_0 Vision Quantization Pipeline

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/erichflam-hkust-qwen2-5-vl-7b)
[![View on HuggingFace](https://img.shields.io/badge/View_on_HuggingFace-FF9D00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/daksh-neo/Qwen2.5-VL-7B-Nike-LoRA-GGUF)

![Pipeline Architecture](../public/images/diagrams/qwen25-vl-7b-nike-lora-gguf.png)

## The Problem

> Thousands of Vision-Language LoRA adapters are published on HuggingFace for tasks like product recognition, brand identification, and medical imaging. Almost none of them ship an official GGUF quantization. Running a merged Qwen2.5-VL-7B model in bfloat16 needs 15+ GB VRAM, which rules out most consumer GPUs.

NEO built this pipeline to close that gap. It merges a Nike-fine-tuned LoRA adapter into the [Qwen2.5-VL-7B](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) base, quantizes the result to Q8_0 GGUF at 4.5 GB, and benchmarks it on a Nike visual reasoning suite, all in one command.

## The Three-Stage Architecture

The pipeline runs three sequential stages. Each stage produces a concrete artifact that feeds into the next.

**Stage 1: LoRA Merge.** The `LoRAMerger` class loads the Qwen2.5-VL-7B-Instruct base and the Nike LoRA adapter via PEFT, then merges them into a single full-weight bfloat16 model. This step is necessary before quantization because GGUF tools cannot handle separate base-plus-adapter setups. The merged model is written to disk as a standard HuggingFace checkpoint.

**Stage 2: GGUF Quantization.** The `GGUFQuantizer` calls llama.cpp's `convert_hf_to_gguf.py` on the merged model directory, producing an intermediate float16 GGUF. It then runs `llama-quantize` to compress to Q8_0, which stores weights at 8 bits with block-level scaling. The final file is 4.5 GB and fits in 8 GB VRAM.

**Stage 3: Benchmark.** The `VLBenchmark` class runs the model against eight Nike visual reasoning tasks, covering logo recognition, product description, colorway identification, and sport classification. It records accuracy, confidence scores per task, and VRAM delta. Results are written in JSON, CSV, and Markdown formats.

## Why Q8_0 for Vision Models

Vision-language models have a more complex architecture than pure text models. The visual encoder processes image patches separately from the language decoder, and the two share cross-attention layers. Aggressive quantization (Q4 and below) can cause visual grounding to degrade noticeably because the cross-attention weights are particularly sensitive to precision loss.

Q8_0 keeps 8 bits per weight, which preserves visual reasoning accuracy at 93.75% on the Nike benchmark suite while cutting memory from 15+ GB to 8 GB. This is a practical choice for fine-tuned vision models where the LoRA training has introduced task-specific weight patterns that 4-bit rounding can distort.

## Nike Visual Reasoning Benchmark

The benchmark suite tests eight distinct visual tasks, each with its own category, prompt, and ground truth answer. Categories include logo recognition, product description, colorway identification, and sport classification.

```json
{
  "model_id": "erichflam-hkust/Qwen2.5-VL-7B-Nike-LoRA",
  "quant_type": "Q8_0",
  "accuracy_pct": 93.75,
  "benchmarks": [
    {
      "id": "nike_logo_001",
      "category": "logo_recognition",
      "prompt": "What brand logo is shown in this image?",
      "answer": "Nike",
      "score": 1.0
    }
  ]
}
```

The benchmark runs in mock mode without a GPU, producing realistic synthetic results for integration testing. Real inference requires an OpenRouter API key or a local GPU with 8+ GB VRAM.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a three-stage pipeline for vision-language LoRA models: Stage 1 — a LoRAMerger class that loads [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) base and a PEFT LoRA adapter, merges them into a single bfloat16 HuggingFace checkpoint; Stage 2 — a GGUFQuantizer class that calls llama.cpp's convert_hf_to_gguf.py on the merged model then runs llama-quantize to produce a Q8_0 GGUF at ~4.5GB that fits in 8GB VRAM; Stage 3 — a VLBenchmark class that runs the model against eight visual reasoning tasks (logo recognition, product description, colorway identification, sport classification), records accuracy and confidence per task and VRAM delta, and writes results as JSON, CSV, and Markdown. Include mock mode that runs without a GPU for integration testing."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20three-stage%20pipeline%20for%20vision-language%20LoRA%20models%3A%20Stage%201%20%E2%80%94%20a%20LoRAMerger%20class%20that%20loads%20Qwen2.5-VL-7B-Instruct%20base%20and%20a%20PEFT%20LoRA%20adapter%2C%20merges%20them%20into%20a%20single%20bfloat16%20HuggingFace%20checkpoint%3B%20Stage%202%20%E2%80%94%20a%20GGUFQuantizer%20class%20that%20calls%20llama.cpp%27s%20convert_hf_to_gguf.py%20on%20the%20merged%20model%20then%20runs%20llama-quantize%20to%20produce%20a%20Q8_0%20GGUF%20at%20~4.5GB%20that%20fits%20in%208GB%20VRAM%3B%20Stage%203%20%E2%80%94%20a%20VLBenchmark%20class%20that%20runs%20the%20model%20against%20eight%20visual%20reasoning%20tasks%20%28logo%20recognition%2C%20product%20description%2C%20colorway%20identification%2C%20sport%20classification%29%2C%20records%20accuracy%20and%20confidence%20per%20task%20and%20VRAM%20delta%2C%20and%20writes%20results%20as%20JSON%2C%20CSV%2C%20and%20Markdown.%20Include%20mock%20mode%20that%20runs%20without%20a%20GPU%20for%20integration%20testing." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add VRAM delta measurement per inference call using pynvml, add Q4 quantization as a second format alongside Q8_0 for comparison, or add a regression check that fails the pipeline if accuracy drops below a configurable threshold.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/erichflam-hkust-qwen2-5-vl-7b
cd erichflam-hkust-qwen2-5-vl-7b
pip install -r requirements.txt
python scripts/demo.py
```

The demo runs in mock mode with no GPU required. Set `OPENROUTER_API_KEY` for real inference against the 4.5GB GGUF on 8GB VRAM hardware.

NEO built a full merge-quantize-benchmark pipeline for the Nike-fine-tuned Qwen2.5-VL-7B vision model, producing a 4.5 GB GGUF with 93.75% benchmark accuracy on 8 GB VRAM. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
