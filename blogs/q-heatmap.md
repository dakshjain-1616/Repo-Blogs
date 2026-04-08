---
title: "Q-Heatmap: Visualizing Quantization Error Across Model Layers"
description: "NEO built a tool that computes per-layer quantization error across a model and renders an interactive heatmap showing which layers lose the most precision at different bit depths."
date: 2026-04-08
tags: [quantization, visualization, llm, interpretability, gguf]
slug: q-heatmap
github: https://github.com/dakshjain-1616/q-heatmap
---

# Q-Heatmap: Visualizing Quantization Error Across Model Layers

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/q-heatmap)

![Pipeline Architecture](../public/images/diagrams/q-heatmap.png)

## The Problem

> Quantizing a model to 4-bit cuts memory in half, but uniform quantization silently destroys accuracy in a handful of sensitive layers while leaving most layers nearly lossless.

NEO built Q-Heatmap to identify exactly which layers cannot survive aggressive compression and which can be pushed further without measurable degradation.

## Per-Layer Error Metrics

**Q-Heatmap** loads both the full-precision model and its quantized counterpart and computes three complementary error signals for each layer. This multi-metric approach matters because different layers fail in different ways — some show large weight distance but survive functionally, while others show small weight shift but produce dramatically different activations.

The three metrics computed per layer are:

- **Weight distance (L2)**: Frobenius norm of the difference between the full-precision and dequantized weight matrices, normalized by weight magnitude.
- **Activation MSE**: Mean squared error between full-precision and quantized activations on a 512-sample calibration set drawn from the model's training distribution.
- **KL divergence**: KL divergence between the full-precision and quantized output distributions on calibration inputs, measured at the layer's output logits before the next layer's transformation.

```python
from q_heatmap import QuantizationAuditor

auditor = QuantizationAuditor(
    fp16_model="meta-llama/Llama-3.1-8B",
    quantized_model="./models/llama-3.1-8b-Q4_K_M.gguf",
    format="gguf",
    calibration_data="./calib/c4_512samples.jsonl"
)

results = auditor.compute_layer_errors()
auditor.render_heatmap(results, output="heatmap.html")
```

## Interactive Heatmap Rendering

The heatmap renders as a Plotly HTML file with layers on the Y-axis and bit-depth configurations on the X-axis (Q2, Q3, Q4, Q5, Q6, Q8). Each cell is colored by the composite error score — the weighted average of normalized weight distance, activation MSE, and KL divergence. Hovering a cell shows the raw values for all three metrics.

Typical output reveals a clear pattern: the first two and last two transformer layers are consistently high-error under aggressive quantization, while middle layers tolerate Q3-Q4 with near-zero activation drift. Attention projection layers (q_proj, k_proj) tend to be more sensitive than MLP layers (gate_proj, down_proj):

| Layer | Q4 Activation MSE | Q4 KL Div | Q8 Activation MSE | Q8 KL Div |
|---|---|---|---|---|
| layer.0 (embed) | 0.0041 | 0.089 | 0.0002 | 0.004 |
| layer.1 (attn) | 0.0312 | 0.241 | 0.0008 | 0.011 |
| layer.16 (attn) | 0.0019 | 0.017 | 0.0001 | 0.002 |
| layer.31 (final) | 0.0298 | 0.198 | 0.0007 | 0.009 |

## Mixed-Precision Recommendations

Q-Heatmap goes beyond visualization and outputs a mixed-precision configuration file compatible with llama.cpp's `--tensor-type` argument and AutoGPTQ's per-layer bit assignment. High-error layers are assigned Q6 or Q8; low-error layers drop to Q3 or Q2.

In practice, mixed-precision configurations produced by Q-Heatmap recover 80-90% of the perplexity lost in uniform Q4 quantization while adding only 5-8% to the total model size:

```bash
python q_heatmap.py \
  --fp16 meta-llama/Llama-3.1-8B \
  --quantized ./models/llama-3.1-8b-Q4_K_M.gguf \
  --format gguf \
  --calibration ./calib/c4_512samples.jsonl \
  --output heatmap.html \
  --export_config mixed_precision.json
```

The exported `mixed_precision.json` maps each tensor name to its recommended bit depth and can be passed directly to `llama-quantize` for re-quantization.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a quantization error analysis tool that loads a full-precision model and its GGUF or GPTQ quantized counterpart, computes per-layer weight distance, activation MSE, and KL divergence on a calibration dataset, then renders an interactive Plotly heatmap with layers on one axis and bit depths on the other, and exports a mixed-precision configuration file."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20quantization%20error%20analysis%20tool%20that%20loads%20a%20full-precision%20model%20and%20its%20GGUF%20or%20GPTQ%20quantized%20counterpart%2C%20computes%20per-layer%20weight%20distance%2C%20activation%20MSE%2C%20and%20KL%20divergence%20on%20a%20calibration%20dataset%2C%20then%20renders%20an%20interactive%20Plotly%20heatmap%20with%20layers%20on%20one%20axis%20and%20bit%20depths%20on%20the%20other%2C%20and%20exports%20a%20mixed-precision%20configuration%20file." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add AWQ format support, integrate perplexity benchmarking against Wikitext-2, or build a CLI batch mode that audits an entire model zoo and compares quantization sensitivity across architectures. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/q-heatmap
cd q-heatmap
pip install -r requirements.txt
python q_heatmap.py --fp16 meta-llama/Llama-3.1-8B --quantized ./models/model-Q4_K_M.gguf --format gguf
```

Open `heatmap.html` to explore per-layer quantization sensitivity and download the mixed-precision config for re-quantization.

NEO built a per-layer quantization error visualizer that identifies which transformer layers break under compression and generates mixed-precision configurations to recover accuracy. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
