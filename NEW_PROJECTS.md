# New Projects — May 2026

17 new blog posts added covering developer tooling, LLM evaluation, agent frameworks, and edge AI. Each post ships with a hand-crafted Excalidraw architecture diagram under `public/images/diagrams/<slug>.{excalidraw,png}` — built with the `excalidraw-diagram` skill (varied visual patterns, semantic color encoding, evidence artifacts like real CLI invocations and JSON payloads).

## Developer Tools

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Loop Anti-Pattern Linter — AST-based Python loop performance analyzer, 7 pattern detectors, auto-fix suggestions | `loop-anti-pattern-linter` | [dakshjain-1616/Loop-Anti-Pattern-Linter](https://github.com/dakshjain-1616/Loop-Anti-Pattern-Linter) | fan-out detectors → ranking engine → fan-out outputs |
| RAG Retrieval Semantic Deduplication — 5 dedup strategies, 30–50% token reduction, streaming support | `rag-retrieval-semantic-deduplication` | [dakshjain-1616/RAG-with-Retrieval-Time-Semantic-Deduplication](https://github.com/dakshjain-1616/RAG-with-Retrieval-Time-Semantic-Deduplication) | retrieval → 5-strategy convergence → reduced context |
| Low-Latency Model Router — sub-0.1ms LLM selector, 4 priority modes, Redis cache, circuit breaker, failover | `low-latency-model-router` | [dakshjain-1616/low-Latency-Model-Router](https://github.com/dakshjain-1616/low-Latency-Model-Router) | request → priority decision diamond → routed model |
| Token Budget Negotiator — greedy ablation prompt compressor, CLI + library + MCP server, 40–60% reduction | `token-budget-negotiator` | [dakshjain-1616/Token-Budget-Negotiator](https://github.com/dakshjain-1616/Token-Budget-Negotiator) | greedy ablation loop with before/after token counts |
| LLM-Powered Git Bisect — automated git bisect + Ollama local explanation, binary search, root cause report | `llm-powered-git-bisect` | [dakshjain-1616/LLM-Powered-Git-Bisect](https://github.com/dakshjain-1616/LLM-Powered-Git-Bisect) | binary-search timeline → Ollama explanation panel |
| Morph: AST-Level LLM Refactoring — typed ops (RenameSymbol, MoveFunction), NetworkX dep graph, tree-sitter apply | `morph-ast-refactoring` | [dakshjain-1616/Morph](https://github.com/dakshjain-1616/Morph) | typed-op pipeline with dep graph + tree-sitter apply |
| ContextCraft: Visual Prompt Workbench — drag-and-drop canvas, tiktoken budget tracking, semantic compression | `contextcraft-prompt-workbench` | [dakshjain-1616/ContextCraft](https://github.com/dakshjain-1616/ContextCraft) | canvas → tiktoken meter → compressed prompt artifact |
| PipelineScope: LLM Pipeline Debugger — context/RAG/agent/proxy in one tool, visual DAG, no cloud required | `pipelinescope-llm-pipeline-debugger` | [dakshjain-1616/PipelineScope](https://github.com/dakshjain-1616/PipelineScope) | DAG of stages → debugger UI mockup |

## LLM Evaluation & Testing

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Local Model Behavior Prober — YAML probe suites for Ollama, 8 probe categories, HTML reports | `local-model-behavior-prober` | [dakshjain-1616/Local-Model-Behavior-Prober](https://github.com/dakshjain-1616/Local-Model-Behavior-Prober) | YAML suite → 8-probe fan-out → HTML report |
| LLM Behavior Diff Detector — semantic diff across model versions, embedding comparison, HTML drift reports | `llm-behavior-diff-detector` | [dakshjain-1616/-LLM-Behavior-Diff-Model-Update-Detector](https://github.com/dakshjain-1616/-LLM-Behavior-Diff-Model-Update-Detector) | side-by-side v_old / v_new with embedding-diff convergence |
| Invariant: Property-Based Testing for LLMs — 7 invariants, 3 generators, auto binary-search shrinking, pytest | `invariant-property-testing-llms` | [dakshjain-1616/Invariant](https://github.com/dakshjain-1616/Invariant) | generator → 7-invariant check → shrink loop |

## Benchmarks

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Claude Opus 4.7 vs GPT-5.5 vs DeepSeek V4 Benchmark — 13-task eval: Claude 9.23, GPT 9.15, DeepSeek 7.31 | `claude-opus-vs-gpt55-vs-deepseek-v4-benchmark` | [dakshjain-1616/Claude-Opus-4.7-vs-GPT-5.5-vs-DeepSeek-V4-Pro-Reasoning-Benchmark](https://github.com/dakshjain-1616/Claude-Opus-4.7-vs-GPT-5.5-vs-DeepSeek-V4-Pro-Reasoning-Benchmark) | 3-model convergence into judge + horizontal score bars |
| Long-Horizon Agent Benchmark — 50+ tool call tasks: Opus 0.90/19 calls vs Kimi 0.90/93 calls vs DeepSeek 0.85/$0.11 | `long-horizon-agent-benchmark` | [dakshjain-1616/-Long-Horizon-Agent-Benchmark-GLM-5.1-vs-Kimi-K2.6-vs-DeepSeek-V4-Pro](https://github.com/dakshjain-1616/-Long-Horizon-Agent-Benchmark-GLM-5.1-vs-Kimi-K2.6-vs-DeepSeek-V4-Pro) | tool-call timeline per model + cost/calls comparison |
| DeepSeek V4 Million-Token Context Benchmark — NIAH: Flash 100% at $0.14 vs Scout 33%, multi-doc QA | `deepseek-v4-context-benchmark` | [dakshjain-1616/DeepSeek-V4-Context-Benchmark](https://github.com/dakshjain-1616/DeepSeek-V4-Context-Benchmark) | NIAH grid + multi-doc QA flow with accuracy bars |

## Agent Frameworks

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Synthetic Data Flywheel — 8-stage self-improving pipeline, LLM judge, diversity filter, recycling loop, A2A agent | `synthetic-data-flywheel` | [dakshjain-1616/Synthetic-Data-Flywheel](https://github.com/dakshjain-1616/Synthetic-Data-Flywheel) | cycle: generate → judge → recycle, A2A side panel |
| A2A + MCP Dual-Protocol Reference Agent — canonical Google A2A + Anthropic MCP agent, DeepSeek V4-Flash | `a2a-mcp-dual-protocol-reference-agent` | [dakshjain-1616/A2A-MCP-Dual-Protocol-Reference-Agent](https://github.com/dakshjain-1616/A2A-MCP-Dual-Protocol-Reference-Agent) | dual-rail A2A + MCP protocols meeting at agent core |

## Edge AI

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| SmolVLM2 Edge Vision Agent — offline CPU-only vision monitoring, SmolVLM2 2.2B, motion-gating, RTSP/MJPEG | `smolvlm2-edge-vision-agent` | [dakshjain-1616/SmolVLM2-Edge-Vision-Agent](https://github.com/dakshjain-1616/SmolVLM2-Edge-Vision-Agent) | RTSP stream → motion gate (decision) → VLM → alert |
