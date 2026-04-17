---
title: "Neural TTS: From WaveNet to Edge-Ready Speech Synthesis, Benchmarked"
description: "NEO traced Neural TTS from WaveNet to modern VITS and StyleTTS2, then benchmarked five models on RTF, size, and CPU viability to find which survive real deployment."
date: 2026-04-17
tags: [tts, speech-synthesis, benchmarking, edge-deployment, onnx]
slug: neural-tts
github: https://github.com/gauravvij/neural_tts
---

# Neural TTS: From WaveNet to Edge-Ready Speech Synthesis, Benchmarked

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/gauravvij/neural_tts)

## The Problem

> TTS model cards advertise "natural prosody" and "state-of-the-art quality" but rarely publish honest Real-Time Factor numbers on commodity hardware — so teams pick a model, discover it's GPU-bound or 900MB, and rip it out a week later.

NEO built Neural TTS to trace the evolution from WaveNet to modern efficient architectures, then benchmark five representative models on RTF, size, and CPU viability so you can pick one with open eyes.

## The Evolution Timeline

**2016 — WaveNet.** DeepMind's autoregressive vocoder predicted each audio sample conditioned on all previous samples, generating 16–24kHz waveforms one sample at a time. Quality was stunning; CPUs took minutes per second of audio. Needed a separate text-to-spectrogram model (Tacotron) to run end-to-end.

**2017–2018 — Tacotron and Tacotron 2.** Encoder-attention-decoder mapping characters to mel spectrograms, paired with a modified WaveNet vocoder. Roughly 50MB and several seconds per second of audio on CPU.

**2019–2020 — FastSpeech and FastSpeech 2.** Non-autoregressive generation using duration predictors produced entire spectrograms in a single forward pass. RTF improved from 50-100x slower than real-time to 5-10x slower, but still largely GPU-bound.

**2021–present — efficient neural TTS.** VITS-style end-to-end training without a separate vocoder, StyleTTS2 diffusion-based synthesis with style control, ONNX graphs that run efficiently on CPU, and INT8/FP16 quantization. A 5.8MB Piper model can generate speech at 1,400x RTF on a modest CPU. An 82MB Kokoro delivers near-human quality at 5x real-time.

## Real-Time Factor as the Core Metric

Every experiment anchors on Real-Time Factor — seconds of audio per second of wall-clock time. The repo inverts the convention and reports "faster-than-real-time" ratios (higher is better), because Piper numbers span three orders of magnitude. Each experiment loads a fixed `TEST_PHRASES` list covering short sentences, long sentences, numbers, and punctuation, warms the model, times synthesis, and writes a JSON artifact to `results/`:

```python
{
  "model_variant": {
    "quality": "low",
    "size_mb": 5.8,
    "average_rtf": 1409.358
  }
}
```

A `create_comparison_visualizations.py` script pulls every JSON artifact and renders matplotlib/seaborn charts for RTF across quality tiers, model sizes, and architecture families.

## Five Architectures, Five Deployment Stories

The suite covers a deliberate spread from ultra-lightweight CPU inference to GPU-only transformer models, one experiment file per model under `experiments/`:

| Model | Size | Arch | RTF (CPU) | Target |
|---|---|---|---|---|
| Piper (low) | 5.8 MB | VITS / ONNX | 1,409x | IoT, edge devices |
| Piper (medium) | 62 MB | VITS / ONNX | 2,483x | Standard servers |
| Piper (high) | 110 MB | VITS / ONNX | 7,603x | Offline high-fidelity |
| Kokoro | 82 MB | StyleTTS2 | 5x (RTF 0.21) | Natural prosody on CPU |
| MeloTTS | 162 MB | VITS + BERT | 6x (RTF 0.16) | Multilingual, 44.1kHz |
| Parler-TTS Mini | 880 MB | T5 + DAC | ~7x slower | GPU deployments |
| XTTSv2 | ~4.5 GB | GPT2 autoregressive | GPU-only | Voice cloning on GPU |

Three structural findings drop out of the numbers. Model size does not track quality linearly — the 110MB Piper-high tier is a diminishing-returns step over the 62MB medium. ONNX export collapses 100MB+ PyTorch checkpoints into 5-60MB artifacts without measurable quality loss. Transformer-based synthesis (Parler-TTS, XTTSv2) stays GPU-bound in practice; Parler runs ~7x slower than real-time on CPU, and XTTSv2 will not run at all without 8GB+ VRAM because the GPT2 decoder is inherently autoregressive.

## Per-Model Findings

**Piper dominates for speed.** All three tiers synthesize in milliseconds — the 5.8MB low tier averages 0.008s per phrase for an RTF of 1,409x. ONNX Runtime's highly optimised CPU kernels combined with VITS's parallel-friendly architecture make this possible. Piper's `synthesize_stream_raw()` returns `AudioChunk` objects; the experiment extracts `.data` from each chunk before concatenation.

**MeloTTS and Kokoro are the best quality/speed balance.** Both run 5-6x faster than real-time on CPU with noticeably more natural prosody than Piper low. MeloTTS outputs at 44.1kHz (CD-quality) with mixed Chinese-English support via BERT embeddings. Kokoro's generator API returns `(graphemes, phonemes, audio)` tuples — the experiment consumes the generator and concatenates audio arrays before saving.

**Parler-TTS trades speed for control.** T5 encoder + DAC audio codec at 880MB produces excellent quality with fine-grained style control through natural-language descriptions, but needs nearly 7 seconds of CPU compute per second of audio. Memory management mattered — careful batching and cleanup were required to finish the run without OOM.

**XTTSv2 is GPU-only, honestly documented.** Rather than silent failure, the repo documents why: the GPT2 decoder's sequential dependency prevents CPU parallelization, and the 2.3B parameters exceed practical CPU throughput. Additionally, the `TTS` library pins Python <3.12, blocking installation on 3.12.3 environments. Use it when you have 8GB+ VRAM and need zero-shot voice cloning.

## Running the Experiments

```bash
git clone https://github.com/gauravvij/neural_tts.git
cd neural_tts
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python experiments/piper_experiment.py
python experiments/kokoro_experiment.py
python experiments/create_comparison_visualizations.py
```

Each experiment downloads its own weights on first run into the gitignored `models/` directory. Results land in `results/` as JSON plus PNG comparison charts. Extending the suite follows one convention — drop a new `experiments/<model>_experiment.py` that initialises the model, times it across `TEST_PHRASES`, and writes a JSON artifact with the same `{quality, size_mb, average_rtf}` shape so the visualiser picks it up automatically. Optional extras are isolated per experiment (`torch` for Kokoro, `melotts-onnx` for MeloTTS, `parler-tts` for Parler) so base setup stays lean.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a reproducible TTS benchmarking suite with one experiment file per model under experiments/, each loading a fixed TEST_PHRASES list and measuring Real-Time Factor across quality tiers, writing JSON artifacts with quality/size_mb/average_rtf fields to results/, plus a create_comparison_visualizations.py that renders matplotlib/seaborn charts comparing Piper, Kokoro, MeloTTS, Parler-TTS and XTTSv2 on RTF and model size."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20reproducible%20TTS%20benchmarking%20suite%20with%20one%20experiment%20file%20per%20model%20under%20experiments%2F%2C%20each%20loading%20a%20fixed%20TEST_PHRASES%20list%20and%20measuring%20Real-Time%20Factor%20across%20quality%20tiers%2C%20writing%20JSON%20artifacts%20with%20quality%2Fsize_mb%2Faverage_rtf%20fields%20to%20results%2F%2C%20plus%20a%20create_comparison_visualizations.py%20that%20renders%20matplotlib%2Fseaborn%20charts%20comparing%20Piper%2C%20Kokoro%2C%20MeloTTS%2C%20Parler-TTS%20and%20XTTSv2%20on%20RTF%20and%20model%20size." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a MOS-estimation quality scorer using UTMOS, add GPU-vs-CPU side-by-side RTF measurement with device auto-detection, wire in a streaming-latency experiment measuring time-to-first-audio-chunk, or ship a FastAPI service that exposes the best-performing tier with streaming output and caching. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/gauravvij/neural_tts
cd neural_tts
pip install -r requirements.txt
python experiments/piper_experiment.py
```

Results land in `results/` as JSON and PNG charts, and the comparison visualizer renders a single plot of RTF against model size across every architecture you benchmark.

NEO built a reproducible TTS benchmark suite that turns "which model should we deploy" into a chart grounded in measured RTF and model-size numbers. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
