---
title: "9x Model Compression with Quantization-Aware Training for Edge Deployment"
description: "How we compressed MobileNetV2 from 23.5MB to 2.6MB using INT8 quantization-aware training, achieving 9x size reduction with only a 3.8% accuracy drop, ready for deployment on Android, iOS, and Raspberry Pi."
date: "2026-03-09"
tags: ["quantization", "quantization-aware training", "MobileNetV2", "edge AI", "TensorFlow Lite", "model compression", "INT8", "mobile ML"]
slug: "quantization-aware-training"
github: https://github.com/dakshjain-1616/Quantisation-Awareness-training
---

# 9x Model Compression with Quantization-Aware Training for Edge Deployment

<a href="https://github.com/dakshjain-1616/Quantisation-Awareness-training" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">dakshjain-1616/Quantisation-Awareness-training</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/quantization-aware-training.png)

## The Problem

> Deploying neural networks to edge devices is a genuine engineering challenge. The model that works great on your training server is often too large and too slow for a mobile device or a Raspberry Pi. Naive post-training quantization can cause accuracy drops of 10-20% on some models, leaving teams stuck between a model that's too big to deploy and one that's too degraded to use.

Quantization-aware training (QAT) addresses this by simulating quantization during training, so the model learns to be robust to the precision reduction before it's actually applied. We compressed a **23.5MB** model down to **2.6MB** — a **9.08x reduction** — with only a **3.8% accuracy drop**.

## Why Quantization Works

Neural networks are typically trained with 32-bit floating point weights (4 bytes per parameter). Research has consistently shown that you can represent weights with much lower precision, 8-bit integers instead of 32-bit floats, without losing much predictive capability.

INT8 quantization cuts the memory footprint by roughly 4x on weights alone. It also enables faster inference on hardware with optimized INT8 compute paths, which includes most modern mobile chips and microcontrollers. Reduced memory bandwidth requirements matter significantly on constrained devices.

## The Implementation

### Data and Model Setup

We work with CIFAR-10 resized to 224x224 pixels to match MobileNetV2's expected input dimensions. MobileNetV2 is initialized with ImageNet pretrained weights, giving the model a strong starting point before fine-tuning on CIFAR-10.

Fine-tuning runs for 8 epochs. This is enough to adapt the pretrained weights to the new dataset while preserving the general visual features learned from ImageNet.

### Calibration

Quantization-aware training requires a calibration dataset: a representative sample of input data used to determine the optimal scaling factors for mapping floating-point values to the INT8 range. We use **200 representative samples** for calibration.

The calibration step is critical. The scaling factors it produces determine how well the quantized model approximates the full-precision model's behavior. Too few calibration samples and the scaling is poorly estimated. Too many and you're spending compute on diminishing returns. 200 samples is a reliable default for most vision tasks.

### INT8 Quantization with TFLite

We convert the calibrated model to TensorFlow Lite format with full INT8 quantization. "Full INT8" means both weights and activations are quantized, as opposed to weight-only quantization which leaves activations in floating point.

The output is a `.tflite` file at 2.59MB.

### A Practical Note on Tooling

During development, we initially tried TensorFlow's native quantization toolkit for the conversion step and hit API compatibility issues with the specific TF version in use. We pivoted to post-training quantization instead, which proved more stable and produced comparable results. This kind of tooling friction is common in the quantization space, where APIs are still evolving. The lesson is to have a fallback approach ready and to test the output model thoroughly regardless of which conversion path you use.

## Results

| Metric | Original | Quantized |
|--------|----------|-----------|
| Model size | 23.52 MB | 2.59 MB |
| Compression ratio | 1x | 9.08x |
| Test accuracy | 81.0% | 77.2% |
| Accuracy drop | - | 3.8% |
| Format | .h5 | .tflite |

A 3.8% accuracy drop is acceptable for most edge applications. If your baseline accuracy is 81% and your quantized model hits 77.2%, you're still within the performance range needed for practical classification tasks.

The total training and quantization process takes **15-40 minutes** depending on hardware.

## Deployment Targets

The `.tflite` model deploys to three main targets:

**Android and iOS** via the native TensorFlow Lite APIs. Mobile apps can bundle the model file and run inference on-device without network connectivity. This matters for latency and privacy.

**Raspberry Pi and edge devices** via the Python TFLite runtime. The compressed model loads fast and runs inference efficiently on ARM processors.

**Docker containers** for edge server deployments where you want containerization but still need CPU-optimized inference.

## When to Use QAT vs. Post-Training Quantization

Post-training quantization (PTQ) is faster to apply and works well when the base model has a large capacity relative to the task. QAT takes longer because it requires a training pass, but it typically recovers more accuracy for smaller models where PTQ degrades performance significantly.

For MobileNetV2, which is already a compact architecture, QAT is worth the extra training time. For very large models like ResNet-50 or larger, PTQ often works well enough and saves significant compute.

## Where This Fits in a Production ML Pipeline

Quantization is usually one of the last steps before deployment, but it should be planned for early. The model architecture, training data, and fine-tuning regime all affect how well quantization works. Building quantization into your training pipeline from the start, rather than treating it as an afterthought, leads to better results.

This pipeline integrates naturally into CI/CD workflows: train, quantize, evaluate, and if accuracy meets your threshold, deploy. If it doesn't, adjust the calibration or fine-tuning and repeat.

## Watch It in Action

We recorded a full walkthrough of the quantization pipeline, showing the training run, conversion step, and the final model size comparison live.

<a href="https://youtu.be/Z9W2gTu-Ekc" target="_blank" style="display:block;max-width:560px;margin:20px 0;border-radius:12px;overflow:hidden;border:1px solid #30363d;position:relative;cursor:pointer;text-decoration:none;">
  <img src="https://img.youtube.com/vi/Z9W2gTu-Ekc/maxresdefault.jpg" alt="Watch on YouTube" style="width:100%;display:block;">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.72);border-radius:50%;width:68px;height:68px;display:flex;align-items:center;justify-content:center;">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>
  </div>
  <div style="position:absolute;bottom:12px;left:16px;background:rgba(0,0,0,0.7);color:#fff;font-size:12px;padding:4px 10px;border-radius:4px;font-family:sans-serif;">▶ Watch on YouTube</div>
</a>

---

NEO built a quantization-aware training pipeline where MobileNetV2 is compressed 9x for edge deployment—from 23.5MB to 2.6MB—with only a 3.8% accuracy drop, ready to run on Android, iOS, and Raspberry Pi. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)

---
