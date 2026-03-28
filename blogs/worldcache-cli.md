---
title: "WorldCache CLI: Perceptual Frame Deduplication for World Models"
description: "NEO built a CLI preprocessing tool that uses perceptual hashing to skip redundant video frames before they reach world models, cutting processing load by up to 90%."
date: 2026-03-28
tags: [video, preprocessing, hashing, world-models, performance]
slug: worldcache-cli
github: https://github.com/dakshjain-1616/worldcache-cli
---

# WorldCache CLI: Perceptual Frame Deduplication for World Models

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/worldcache-cli)

![Pipeline Architecture](../public/images/diagrams/worldcache-cli.png)

## The Problem

> World models like Genie, UniSim, and WorldDreamer are computationally expensive to run. Real video footage is brutally redundant — consecutive frames in a static scene can differ by less than 1% of pixels. Running every frame through a world model wastes resources on information that hasn't changed.

NEO built WorldCache CLI to filter out duplicate and near-duplicate frames before they hit the model. It sits in front of your inference pipeline as a perceptual cache layer, requiring no GPU and no model modifications.

## How Perceptual Hashing Works

**Perceptual hashing** converts an image into a compact fingerprint that stays stable across minor pixel-level noise but changes when the image content changes meaningfully. Unlike cryptographic hashes, two frames that look nearly identical to a human eye will produce similar perceptual hashes with a small Hamming distance.

WorldCache computes a hash for each incoming frame and checks it against a cache of previously seen hashes. If the Hamming distance between the new frame's hash and the closest cached hash falls below a configurable threshold, the frame is classified as a duplicate and skipped. This single comparison replaces a full model forward pass.

The threshold you set determines the trade-off between deduplication aggressiveness and recall. A low threshold only skips frames that are pixel-for-pixel identical. A higher threshold skips frames that are perceptually similar, which is useful for slow-moving scenes but may miss subtle motion in fast-action sequences.

## Four Hash Algorithms

WorldCache ships four **hash algorithms**, each with different performance and sensitivity characteristics.

**DHASH** (difference hash) is the default. It encodes horizontal gradient information, making it robust to lighting changes and minor color shifts. It runs fast and handles general motion detection well. **PHASH** (perceptual hash) uses a discrete cosine transform over a downsampled grayscale image, giving it more resistance to JPEG artifacts and noise at the cost of slightly higher compute. **AHASH** (average hash) is the simplest: it averages pixel values and encodes which pixels are above the mean. It is the fastest option but most sensitive to global brightness changes. **WHASH** (wavelet hash) applies a Haar wavelet decomposition and captures multi-scale frequency content, making it best suited for scenes with high-frequency texture detail.

Run `benchmark` to compare all four on your specific video content before committing to one algorithm for production.

## CLI Commands

WorldCache exposes four commands through its CLI.

`process` is the primary command. It takes a directory of frame images or an MP4 file and outputs a deduplicated set of frames, along with a JSON report of which frames were skipped and why.

`demo` generates a synthetic frame sequence and runs deduplication against it. Use this to verify installation and get a feel for threshold behavior without needing real footage.

`inspect` reads the JSON output from a previous `process` run and prints a human-readable summary: total frames, frames skipped, deduplication rate, and the hash algorithm used.

`benchmark` runs all four hash algorithms over the same input and reports throughput (frames per second) and cache hit rate for each. This is the right starting point when tuning for a new video domain.

## Python API Integration

For embedding WorldCache directly into an inference loop, the **Python API** gives you fine-grained control. You instantiate a `WorldCache` object with your chosen algorithm and threshold, then call `.is_duplicate(frame)` on each frame before passing it to the model.

```python
from worldcache import WorldCache

cache = WorldCache(algorithm="dhash", threshold=10)

for frame in video_frames:
    if not cache.is_duplicate(frame):
        world_model.predict(frame)
```

This pattern integrates cleanly with any existing pipeline. The cache stores only the hash fingerprints, not the full frame data, so memory usage stays flat regardless of how much footage you process.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/worldcache-cli
cd worldcache-cli
pip install -r requirements.txt
```

For MP4 video file support, install OpenCV:

```bash
pip install opencv-python
```

Run the demo to verify everything works without needing real footage:

```bash
python -m worldcache demo
```

To process a directory of frames:

```bash
python -m worldcache process --input ./frames/ --algorithm dhash --threshold 10 --output ./deduplicated/
```

To process an MP4 file directly:

```bash
python -m worldcache process --input ./video.mp4 --threshold 8
```

The tool prints a live progress bar during processing and writes a `cache_report.json` to the output directory. That report contains the full list of skipped frame indices and the computed Hamming distances, which you can feed into `inspect` for a formatted summary.

NEO built WorldCache CLI to cut redundant frame processing in world model pipelines by up to 90%, using perceptual hashing instead of expensive model inference. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
