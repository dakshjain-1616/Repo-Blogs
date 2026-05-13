---
title: "VLouvain: O(n log n) Clustering for Millions of Embeddings"
description: "NEO built high-performance clustering library that clusters millions of high-dimensional embeddings in seconds using FAISS-accelerated k-NN graphs and vectorized label propagation with <2GB memory."
date: 2026-05-13
tags: [clustering, embeddings, FAISS, high-dimensional data, scalable algorithms]
slug: vlouvain-fast-scalable-clustering
github: https://github.com/dakshjain-1616/vlouvain
---

# VLouvain: O(n log n) Clustering for Embeddings

Traditional clustering breaks on large-scale embeddings. UMAP+HDBSCAN impractical beyond 10k vectors. Tree-based approaches O(n²) clustering.

NEO built VLouvain replacing O(n²) bottleneck with O(n log n). Clusters 1M 128-dimensional vectors in ~12 seconds, <2GB RAM.

## Three-Stage Algorithm

**Sparse k-NN Graph**: FAISS constructs sparse nearest-neighbor graph (not dense n×n). Up to 500k: HNSW. Larger: IVF. Both logarithmic complexity.

**Vectorized Label Propagation**: Each point starts with unique label. Iteratively updates based on most frequent neighbor label using NumPy (no Python loops, vectorized).

**Optional Louvain Refinement**: Apply modularity optimization for smaller datasets. Configurable resolution parameter.

## Performance

Clusters 1M float32 128-dim vectors in ~12 seconds, <2GB peak memory.

UMAP+HDBSCAN: Impractical beyond 10k. Hours for 1M (if completes).

## Semantic Search Integration

VLouvain clusters stable/consistent, ideal for semantic search indexing. Cluster representatives serve as routing hubs, drastically speed lookup in large embedding DBs.

## Build with NEO

> "Build clustering library (VLouvain): (1) sparse k-NN via FAISS (HNSW <500k, IVF larger), (2) vectorized label propagation NumPy (no loops), (3) optional Louvain modularity optimization, (4) 1M 128-dim in <12s <2GB, (5) GPU when available, efficient CPU, (6) cluster labels + stability metrics."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20high-performance%20clustering%20library" style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

**Architecture Diagram**: `vlouvain-fast-scalable-clustering.png`
