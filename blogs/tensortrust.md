---
title: "TensorTrust — Visual Integrity Auditor for AI Model Weights"
description: "NEO built TensorTrust, a local auditing tool that verifies AI model weights via SHA256 hashing, structural analysis, and weight distribution checks before you load them."
date: 2026-03-28
tags: [model-security, safetensors, gguf, integrity-check, gradio]
slug: tensortrust
github: https://github.com/dakshjain-1616/tensortrust
---

# TensorTrust — Visual Integrity Auditor for AI Model Weights

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/tensortrust)

![Pipeline Architecture](../public/images/diagrams/tensortrust.png)

## The Problem

> Every time you download a model from HuggingFace, a torrent, or a third-party mirror, you are running an untrusted binary on your hardware. Model weights can be backdoored, silently modified to trigger specific outputs on specific inputs, or corrupted during transfer. There is no standard tooling to verify a model file before loading it.

NEO built TensorTrust to give you a verifiable answer before you run the model. It computes SHA256 hashes, validates layer counts, scans for hidden parameters, and produces a structured health report, all locally, without uploading your weights anywhere.

## Hash Verification

The first check TensorTrust runs is **SHA256 hash verification**. Each file in the model directory gets a computed hash that is compared against a registry of known-good checksums. A single bit flip anywhere in the weights file will produce a completely different hash, so this check catches both intentional tampering and silent data corruption from failed downloads.

The registry ships as `mock_registry.json` for offline testing. In a production setup you populate it with hashes from the original model publisher's release notes or the HuggingFace model card. Any mismatch produces a `TAMPERED` status with the list of affected files.

## Structural Analysis

Hash verification catches file-level tampering, but a modified model can still pass a hash check if the attacker controls the published hash. **Structural analysis** provides a second independent check.

TensorTrust validates the layer count and tensor shapes against the declared architecture. It knows expected tensor counts for common model families and flags deviations as suspicious. It also scans for unexpected tensor names that don't match the declared architecture, which is the pattern used by most backdoor injection techniques: an attacker adds hidden weight tensors that activate on specific trigger inputs.

```python
from auditor import ModelAuditor

auditor = ModelAuditor()
report = auditor.scan("mistral-7b-instruct-v0.1.Q4_K_M.safetensors")
print(report.get_health_status())
# → "HEALTHY"
```

The scan returns a structured report with tensor-level detail: name, shape, dtype, parameter count, and whether the tensor is flagged as suspicious.

## Weight Distribution Analysis

Even a structurally correct model can carry a backdoor through unusual weight magnitudes. **Weight distribution visualization** plots per-layer histograms and computes basic statistics: mean, standard deviation, min, max, NaN count, and infinity count.

Normal transformer weights follow approximately Gaussian distributions centered near zero. Injected backdoor triggers often appear as isolated weight clusters far from zero, or as NaN/infinity values that cause specific numerical behaviors. The visualizer flags layers where the distribution is a statistical outlier compared to the rest of the model.

## Format Support and the Gradio Dashboard

TensorTrust handles `.safetensors`, `.bin` (PyTorch), and `.gguf` files through the same `ModelAuditor` interface. The scan logic is format-aware and extracts tensors correctly from each container format.

For users who prefer a visual workflow, the **Gradio dashboard** provides a browser-based interface at `http://127.0.0.1:7860`. Upload any supported file and get an interactive health report with per-tensor details, status indicators, and weight distribution plots.

```bash
python app.py
# Running on http://127.0.0.1:7860
```

Status values are explicit:

| Status | Meaning |
|--------|---------|
| `HEALTHY` | Hash matches, architecture correct, no anomalies |
| `SUSPICIOUS` | Architecture deviates or weight distribution is unusual |
| `TAMPERED` | SHA256 mismatch or hidden parameters detected |

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/tensortrust
cd tensortrust
pip install -r requirements.txt
```

Run the Gradio dashboard for interactive auditing:

```bash
python app.py
```

Or use the Python API to integrate into an existing pipeline:

```python
from auditor import ModelAuditor

auditor = ModelAuditor()
report = auditor.scan("your-model.safetensors")

print(report.get_health_status())
print(report.summary())
```

Run the test suite to verify your setup:

```bash
pytest tests/ -q
# 36 passed in 2.47s
```

The report JSON includes hash check results, structural analysis, per-tensor statistics, and any detected anomalies. Scan duration for a typical 7B safetensors file is under 100ms for the structural pass, with hash computation scaling linearly with file size.

NEO built TensorTrust as a local-first model integrity auditor that catches backdoored, tampered, or corrupted weights before they reach your hardware. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
