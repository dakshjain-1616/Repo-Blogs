---
title: "Building a Low-Latency CPU-Based Voice Assistant with Streaming TTS"
description: "How NEO built a sub-1.3-second voice assistant that runs entirely on CPU using KittenML's TTS model, sub-sentence streaming, and a multi-threaded producer-consumer pipeline."
date: 2026-03-09
tags: ["voice AI", "TTS", "streaming", "CPU inference", "low latency", "ONNX", "LLM assistant"]
slug: cpu-tts-streaming-llm-assistant
github: https://github.com/abhishekgandhi-neo/Low-Latency-CPU-Based-Voice-Assistant
---

# Building a Low-Latency CPU-Based Voice Assistant with Streaming TTS

<a href="https://github.com/abhishekgandhi-neo/Low-Latency-CPU-Based-Voice-Assistant" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">abhishekgandhi-neo/Low-Latency-CPU-Based-Voice-Assistant</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

![Pipeline Architecture](../public/images/diagrams/cpu-tts-streaming-llm-assistant.png)

## The Problem

> Most voice assistants feel sluggish. You ask a question, wait two or three seconds, and then speech finally starts playing. That gap is the difference between a system that feels alive and one that feels like a demo. The problem is architectural: most TTS pipelines wait for a complete sentence before synthesizing audio, stacking sequential delays that compound into noticeable lag — especially on CPU hardware where GPU acceleration isn't available.

NEO autonomously built a CPU-based voice assistant that achieves **1.25 seconds** time-to-first-audio (TTFA) without a GPU.

## Why CPU-Only?

GPU-based inference has real advantages, but also real constraints: cost, availability, driver complexity, and portability. Many production deployments run on CPU instances. Edge deployments almost always do. If you want a voice assistant that works reliably across diverse hardware, you need to solve the CPU performance problem.

That's the design constraint we started from. Everything in this system is optimized for CPU execution.

## The Core Insight: Sub-Sentence Streaming

Most TTS pipelines wait for a complete sentence before synthesizing audio. That seems logical, but it introduces unnecessary latency. The sentence has to finish generating, then synthesis starts, then audio plays. Each step is sequential.

We changed this by triggering audio synthesis at punctuation boundaries, specifically commas and semicolons, rather than waiting for full stops. Combined with a 25-character look-ahead buffer, the system can start producing audio mid-sentence without the output sounding choppy or unnatural. The look-ahead gives enough context to preserve natural prosody even when working with partial text.

This single architectural decision pushes TTFA down to **1.25 seconds**. Without it, you're looking at **1.8 to 2.5 seconds** under comparable conditions.

## Architecture Overview

The system runs a multi-threaded producer-consumer pipeline:

- **LLM inference** calls an OpenRouter-hosted model and streams tokens as they arrive
- **Chunking logic** watches the token stream for punctuation triggers and packages chunks for synthesis
- **TTS synthesis** runs KittenML's model on each chunk as soon as it's ready
- **Audio playback** queues synthesized audio and plays it continuously

These stages run concurrently. Synthesis starts on the first chunk while the LLM is still generating the rest of the response. Playback starts while synthesis is still running. The pipeline keeps all cores busy rather than stalling at each stage.

## KittenML and ONNX Tuning

The TTS model itself is **under 100MB**. That compares favorably with alternatives like **Piper** and **Sherpa-ONNX**, which frequently exceed 150MB. Smaller models load faster, use less memory, and have lower inference overhead per chunk.

We run inference through ONNX Runtime, tuned specifically for Windows systems with high core counts. Thread affinity and parallelism settings matter significantly here. Default ONNX configurations are often conservative. After benchmarking different thread configurations, we settled on settings that keep CPU utilization high and cache misses low during the hot synthesis loop.

## Getting It Running

The setup is straightforward. You need Python 3.12 or higher, an OpenRouter API key in a `.env` file, and the dependencies installed. The main entry point is `voice_assistant_true_streaming.py`.

Configuration is minimal by design. Point it at your preferred LLM via OpenRouter, run the script, and speak. The system handles the rest.

## Where This Fits

This system is well-suited for any context where voice interaction is needed without GPU hardware:

- **Embedded systems and edge devices** where attaching a GPU isn't an option
- **Developer laptops** for prototyping voice-first applications
- **Cost-sensitive deployments** where GPU instances are overkill
- **Offline environments** where cloud GPU APIs aren't available

The 1.25-second TTFA is fast enough that users perceive the response as immediate. That threshold matters. Below roughly 1.5 seconds, interaction feels conversational. Above it, it feels like waiting.

## What We Learned

Building this exposed several things we didn't anticipate. Windows-specific ONNX compatibility issues required significant debugging. Audio queue management under high CPU load needed careful tuning to avoid pops and dropouts. The 25-character look-ahead value wasn't arbitrary; it came from empirical testing across a range of TTS edge cases where prosody broke down at smaller values.

Performance benchmarking across hardware configurations was part of the process throughout. The numbers we cite (1.25s TTFA, sub-100MB model) are measured, not estimated.

## Build Voice AI That Actually Responds

NEO built a CPU-based voice assistant where sub-sentence streaming and a multi-threaded pipeline deliver 1.25-second time-to-first-audio without any GPU hardware. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)

---
