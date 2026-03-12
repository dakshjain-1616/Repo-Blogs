---
title: "Real-Time Voice Translation Pipeline with Sub-2-Second Latency"
description: "How NEO built a production voice translation system using Whisper, MarianMT, and Edge-TTS that delivers end-to-end speech-to-speech translation in 1.3 seconds across English, Spanish, French, and German."
date: "2026-03-09"
tags: ["voice translation", "speech-to-text", "Whisper", "MarianMT", "Edge-TTS", "real-time AI", "voice AI", "NLP pipeline"]
slug: "realtime-voice-translation-pipeline"
github: https://github.com/dakshjain-1616/Real-time-Voice-Translation-Pipeline
---

# Real-Time Voice Translation Pipeline with Sub-2-Second Latency

<a href="https://github.com/dakshjain-1616/Real-time-Voice-Translation-Pipeline" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">dakshjain-1616/Real-time-Voice-Translation-Pipeline</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/realtime-voice-translation-pipeline.png)

## The Problem

> Latency is everything in voice applications. Once you cross two seconds of delay between someone speaking and hearing a translated response, the interaction stops feeling natural — it becomes a transaction. The common trap in building voice translation systems is stacking components that each add meaningful delay: if your speech-to-text takes 1.5 seconds, translation takes 0.8 seconds, and TTS adds 1.2 seconds, you've already lost before users even notice the quality.

We hit **1.3 seconds** end-to-end. Here's how.

## Designing for Low Latency

We made specific model choices at each stage to keep the pipeline fast without sacrificing quality.

## Pipeline Architecture

The system chains four components: audio preprocessing, speech recognition, neural machine translation, and speech synthesis.

### Audio Preprocessing

We use Librosa for audio handling specifically because it works without an FFmpeg dependency. This matters for deployment. FFmpeg is a system-level dependency that creates friction in containerized environments. Librosa handles resampling, normalization, and format conversion entirely in Python.

The preprocessing stage also handles noise robustness. We've tested against background noise, varying microphone quality, and recordings made in non-ideal acoustic environments. The pipeline degrades gracefully rather than failing hard.

### Speech-to-Text with Whisper Tiny

We chose Whisper Tiny for the STT stage. This is a deliberate trade-off. Whisper Large produces better transcriptions, but the latency cost is too high for real-time use. Whisper Tiny completes the STT stage in **0.4 seconds** and achieves a word error rate **below 0.10** on clean audio, which is sufficient for the languages and use cases we're targeting.

For applications where accuracy matters more than latency, swapping in a larger Whisper variant is a one-line config change.

### Neural Machine Translation with MarianMT

Translation runs through MarianMT transformer models. We load a separate model per language pair, which costs some memory but keeps translation inference to 0.3 seconds per request. The models cover English, Spanish, French, and German, handling four of the most common translation pairs in business and travel contexts.

MarianMT is well-suited here because the models are compact, inference is fast on CPU, and translation quality is competitive with much larger models for common language pairs.

### Text-to-Speech with Edge-TTS

The final stage converts translated text to speech using Edge-TTS with neural voices. This is the slowest stage at 0.6 seconds, but the output quality is substantially better than older TTS systems. The voices are natural enough that the output doesn't sound robotic.

Edge-TTS runs without requiring local model weights for TTS, which keeps the deployment footprint smaller.

## End-to-End Performance

Total processing: 1.3 seconds median latency across tested audio samples.

Breakdown:
- **STT (Whisper Tiny): 0.4s**
- **Translation (MarianMT): 0.3s**
- **TTS (Edge-TTS): 0.6s**

These numbers are measured on CPU hardware. With GPU acceleration, the STT and translation stages run faster, pushing total latency lower.

## Deployment Flexibility

The pipeline supports three deployment targets:

**Local installation** via pip, straightforward for development and single-machine deployments.

**Docker containerization** for consistent environments and easy scaling. The Docker image bundles all dependencies including Librosa audio handling, so there are no system-level surprises at deployment time.

**Serverless cloud platforms** including AWS Lambda and Google Cloud Run. For serverless deployment, pre-warm model instances to avoid cold-start latency on the first request. Model loading time is the main source of variability in cold-start scenarios.

For high-volume production environments, load balancing across multiple instances with pre-loaded models is the standard approach.

## Language Support

The current four language pairs cover English-Spanish, English-French, English-German, and bidirectional translation between each. Adding a new language pair requires downloading the corresponding MarianMT model and registering it in the configuration file. The pipeline architecture doesn't change.

## Practical Use Cases

Real-time voice translation at this latency range opens up several applications that don't work well with slower systems:

**Live meetings and calls** where participants speak different languages and need near-real-time translation to follow the conversation.

**Customer service** where agents and customers speak different languages, and a translated audio feed reduces the need for bilingual agents.

**Field translation** for healthcare, legal, and social services where interpreter availability is limited.

**Travel applications** where quick conversational exchange in a foreign language is the primary use case.

## Extending the System

The architecture is modular. The main extension points are: adding WebSocket support for true streaming (rather than request-response), expanding language coverage beyond the current four, adding speaker diarization to handle multi-speaker audio, and integrating domain-specific vocabulary for technical or specialized language.

---

NEO built a real-time voice translation pipeline where deliberate model choices at every stage—Whisper Tiny, MarianMT, Edge-TTS—deliver end-to-end speech-to-speech translation in 1.3 seconds without sacrificing output quality. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)
