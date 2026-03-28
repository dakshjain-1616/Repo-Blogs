---
title: "VLouvain: Fast Scalable Clustering for High-Dimensional Embeddings"
description: "NEO built a Python clustering library that groups millions of float32 embeddings in seconds using FAISS-accelerated k-NN graphs and vectorized label propagation."
date: 2026-03-28
tags: [clustering, embeddings, faiss, machine-learning, python]
slug: vlouvain
github: https://github.com/dakshjain-1616/vlouvain
---

# VLouvain: Fast Scalable Clustering for High-Dimensional Embeddings

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/vlouvain)

![Pipeline Architecture](../public/images/diagrams/vlouvain.png)

## The Problem

> Clustering millions of high-dimensional embeddings with UMAP and HDBSCAN takes minutes to hours and becomes impractical above 100,000 vectors. Traditional Louvain clustering builds the full graph on CPU, which bottlenecks on large datasets. Most production systems need clustering results in seconds, not minutes, and without requiring specialized hardware.

NEO built VLouvain to cluster embeddings at scale using a four-stage pipeline that stays in pure Python. It handles 10,000 vectors in 33 milliseconds and 1 million vectors in 12 seconds, with memory usage that stays bounded around 2 GB.

## Four-Stage Pipeline

VLouvain runs four sequential stages to transform raw embeddings into cluster assignments.

The first stage is **L2 normalization**. Every input vector is normalized to unit length, which converts inner product similarity into cosine similarity. This matters because FAISS's IndexFlatIP (inner product index) becomes equivalent to cosine similarity after normalization, giving consistent distance semantics across all downstream steps.

The second stage builds a **k-NN graph** using FAISS. For datasets up to 500,000 points, VLouvain uses the HNSW (Hierarchical Navigable Small World) index, which provides approximate nearest neighbor search in O(log n) time with excellent recall. For larger datasets, it switches to the IVF (Inverted File Index) structure, which trades a small amount of recall for dramatically reduced memory usage. The k-NN graph stores only the k nearest neighbors for each point, represented as a sparse adjacency structure.

The third stage runs **vectorized label propagation** using NumPy operations. Each node is assigned its own label initially. The algorithm then iterates, updating each node's label to the most frequent label among its k neighbors. NumPy broadcasting lets this run over the entire graph in each iteration without Python-level loops, making it orders of magnitude faster than naive label propagation implementations.

The fourth stage, optional, applies **Louvain refinement**. For smaller datasets where modularity optimization is feasible, VLouvain runs the standard Louvain algorithm to split or merge communities based on the modularity objective. This produces tighter, more semantically meaningful clusters at a higher compute cost.

## Speed Comparison

The performance gap over UMAP + HDBSCAN widens sharply with dataset size.

At 10,000 vectors in 128 dimensions, VLouvain completes in roughly 33 milliseconds. UMAP + HDBSCAN takes about 60 seconds on the same dataset. At 100,000 vectors, VLouvain takes 0.8 seconds. UMAP becomes impractical at that scale. At 1 million vectors, VLouvain completes in 12 seconds with around 2 GB peak RAM. HDBSCAN cannot run on that input without distributed infrastructure.

The speed advantage comes from two decisions: using FAISS's approximate nearest neighbor search instead of exact search, and replacing graph-level modularity optimization (which is O(n log n) at best) with vectorized label propagation, which runs in fixed NumPy array operations per iteration.

## Configuration Options

VLouvain exposes its key parameters through constructor arguments, CLI flags, or environment variables.

**`k`** controls the number of nearest neighbors in the k-NN graph. Higher k produces coarser clusters with more inter-cluster connectivity. Lower k produces finer-grained clusters that may fragment sparse regions. The default is 15.

**`resolution`** tunes cluster granularity during optional Louvain refinement. Values above 1.0 favor more, smaller clusters. Values below 1.0 favor fewer, larger clusters.

**`similarity_threshold`** filters weak edges from the k-NN graph before label propagation. Setting this to 0.5 removes all edges with cosine similarity below 0.5, which reduces noise in sparse embedding regions but may disconnect some valid communities.

Environment variable names follow the `VLOUVAIN_` prefix convention: `VLOUVAIN_K`, `VLOUVAIN_RANDOM_STATE`, and so on.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/vlouvain
cd vlouvain
pip install -r requirements.txt
```

Python 3.8 or later is required. FAISS is included in the requirements.

Cluster a NumPy embedding file from the CLI:

```bash
vlouvain cluster --input embeddings.npy --output labels.npy --k 15
```

Or use the Python API directly in your inference pipeline:

```python
from vlouvain import VLouvain
import numpy as np

embeddings = np.load("embeddings.npy")  # shape: (N, D), float32

model = VLouvain(k=15, resolution=1.0, similarity_threshold=0.3)
labels = model.fit_predict(embeddings)

print(f"Found {len(set(labels))} clusters across {len(labels)} vectors")
```

The `labels` array is a 1D NumPy array of integer cluster IDs, one per input vector. Cluster IDs are not ordered by size or any other property, so post-processing to sort by frequency is often useful.

To run the test suite:

```bash
python -m pytest tests/ -v
```

NEO built VLouvain to cluster millions of embeddings in seconds without GPU acceleration, combining FAISS-powered k-NN graph construction with vectorized label propagation. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
