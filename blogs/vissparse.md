---
title: "VisSparse — Token Pruning Toolkit for Vision-Language Models"
description: "NEO built VisSparse, a toolkit that prunes image tokens in vision-language models using cosine-similarity scoring, keeping 10% of tokens while losing less than 5% accuracy."
date: 2026-03-28
tags: [vision-language-model, token-pruning, sparse-attention, qwen2-vl, llava]
slug: vissparse
github: https://github.com/dakshjain-1616/vissparse
---

# VisSparse — Token Pruning Toolkit for Vision-Language Models

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/vissparse)

![Pipeline Architecture](../public/images/diagrams/vissparse.png)

## The Problem

> Vision-language models like Qwen2-VL and LLaVA process images by converting them into hundreds of patch tokens. A 448x448 image produces 1024 tokens at standard patch size. Every one of those tokens participates in every attention computation, even the tokens representing uniform sky, blank margins, or other low-information regions. The compute cost scales quadratically with token count.

NEO built VisSparse to cut that token count aggressively while preserving the tokens that actually matter for the task. At 10% token retention, models achieve a 4.7x inference speedup with less than 5% accuracy loss.

## Cosine-Similarity Token Scoring

The core mechanism is **cosine-similarity token selection**. Each image patch token is compared against a query representation derived from the text prompt. Tokens with high cosine similarity to the query are semantically relevant to the current task. Tokens with low similarity represent image regions that don't relate to what the model is being asked.

VisSparse computes these similarity scores at inference time, before the expensive cross-attention computation runs. Tokens below the score threshold are masked out. The model then runs cross-attention over only the retained tokens, which is where the compute savings come from.

This approach requires no model retraining. The scoring and masking happen as a wrapper around the existing model's attention mechanism, which means it works with any HuggingFace vision-language model that exposes standard attention interfaces.

## The keep_ratio Parameter

The **`keep_ratio`** parameter controls what fraction of image tokens survive pruning. It accepts values between 0.05 and 1.0. At 1.0, all tokens are kept and the model behaves identically to baseline. At 0.1, only the top 10% most query-relevant tokens are kept.

The right value depends on the task. Tasks that require reading text in images need higher ratios because text is distributed across many patches. Tasks about a single prominent object can use aggressive ratios because the object occupies a small fraction of the image.

```python
from vissparse import VisSparse

model = VisSparse(base_model="Qwen/Qwen2-VL-7B", keep_ratio=0.10)
output = model.generate(image=img, prompt="What color is the car?")
```

At `keep_ratio=0.10`, the benchmark shows 4.7x speedup. At `keep_ratio=0.25`, the accuracy gap shrinks to under 2% while still delivering a 2.5x speedup.

## Sparse Attention Masks

Token selection produces a **sparse attention mask** that marks which tokens are active and which are pruned. This mask is built once per forward pass and applied to all attention layers. The mask is a boolean tensor with the same length as the image token sequence.

The sparse mask integrates with HuggingFace's `attention_mask` parameter, which means standard model code paths handle it correctly without modification. Pruned tokens receive zero attention weight and do not contribute to the key-value computations that dominate transformer inference time.

Building the mask at inference time means the sparsity pattern adapts to each image-prompt pair. The same image processed with two different prompts will produce different masks, because different regions of the image are relevant to different questions.

## Performance Monitoring

VisSparse records three metrics for each inference call: accuracy (compared against a reference model or ground truth), latency in milliseconds, and speedup relative to the un-pruned baseline. These are logged per call and aggregated across a benchmark run.

The toolkit includes a **mock testing mode** that generates synthetic image tokens and produces realistic metric outputs without requiring a GPU. This makes it possible to verify the scoring and masking logic on any hardware.

```python
from vissparse import VisSparse

model = VisSparse(base_model="mock", keep_ratio=0.10, mock=True)
results = model.benchmark(n_samples=100)
print(f"Speedup: {results['speedup']:.1f}x, Accuracy delta: {results['accuracy_delta']:.2%}")
```

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/vissparse
cd vissparse
pip install -r requirements.txt
```

Run a quick benchmark in mock mode:

```python
from vissparse import VisSparse

model = VisSparse(base_model="mock", keep_ratio=0.10, mock=True)
results = model.benchmark(n_samples=50)
print(results)
```

For real inference with Qwen2-VL:

```python
from vissparse import VisSparse
from PIL import Image

model = VisSparse(base_model="Qwen/Qwen2-VL-7B", keep_ratio=0.15)
img = Image.open("your-image.jpg")
output = model.generate(image=img, prompt="Describe what you see.")
print(output)
```

Adjust `keep_ratio` based on your task requirements. Start at 0.25 for general tasks and decrease toward 0.10 for object-focused queries where the target occupies a small image region.

Run the test suite:

```bash
pytest tests/ -v
# 91 passed
```

The 91-test suite covers token scoring correctness, mask generation, accuracy measurement, speedup calculation, and mock mode behavior across different keep_ratio values.

NEO built VisSparse as a zero-retraining token pruning toolkit that delivers up to 4.7x inference speedup on vision-language models by discarding image tokens that are irrelevant to the prompt. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
