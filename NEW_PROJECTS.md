# New Projects — Added 2026-05-14

5 new blog posts covering agent governance, context-window observability, AI config sync, and ASR benchmarking. Each post ships with a hand-crafted Excalidraw architecture diagram under `public/images/diagrams/<slug>.{excalidraw,png}` — built with the `excalidraw-diagram` skill (varied visual patterns, semantic color encoding, evidence artifacts like real CLI invocations and JSON payloads).

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Agent Constitution — YAML policy + AST-restricted evaluator + regex/Ollama PII detection + JSONL audit + FastAPI/React dashboard | `agent-constitution` | [dakshjain-1616/Agent-Constitution](https://github.com/dakshjain-1616/Agent-Constitution) | tool call → AST evaluator → 3-way decision (allow/block/approve) + audit log + dashboard mockup |
| ContextTimeMachine — post-hoc replay of an agent's context window at any turn, fact tracker, divergence finder | `context-time-machine` | [dakshjain-1616/ContextTimeMachine](https://github.com/dakshjain-1616/ContextTimeMachine) | vertical turn timeline + three investigation-mode panels |
| LiveContext — transparent OpenAI/Anthropic/Ollama proxy with real-time context, token, eviction, attention dashboard | `livecontext` | [dakshjain-1616/LiveContext](https://github.com/dakshjain-1616/LiveContext) | agent ↔ proxy ↔ provider + WebSocket/REST + five live panel mockups |
| agentsync — git-backed AI config sync, tree-level 3-way merge, 52-point security/compliance audit | `agentsync` | [dakshjain-1616/agentsync](https://github.com/dakshjain-1616/agentsync) | 7-command top bar → merge engine ↔ git → 52-point audit fan-out by category |
| ASR Evaluation Framework — 5 ASR models × 15+ scenarios × WER/CER/RTF, stable JSON schema | `asr-evaluation-framework` | [dakshjain-1616/Asr-Evaluation](https://github.com/dakshjain-1616/Asr-Evaluation) | sequential model load → metric engine → per-scenario score bars |
