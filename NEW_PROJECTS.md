# New Projects — Added 2026-05-14

5 new blog posts covering agent governance, context-window observability, AI config sync, and ASR benchmarking. Each post ships with a hand-crafted Excalidraw architecture diagram under `public/images/diagrams/<slug>.{excalidraw,png}` — built with the `excalidraw-diagram` skill (varied visual patterns, semantic color encoding, evidence artifacts like real CLI invocations and JSON payloads).

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| Agent Constitution — YAML policy + AST-restricted evaluator + regex/Ollama PII detection + JSONL audit + FastAPI/React dashboard | `agent-constitution` | [dakshjain-1616/Agent-Constitution](https://github.com/dakshjain-1616/Agent-Constitution) | tool call → AST evaluator → 3-way decision (allow/block/approve) + audit log + dashboard mockup |
| ContextTimeMachine — post-hoc replay of an agent's context window at any turn, fact tracker, divergence finder | `context-time-machine` | [dakshjain-1616/ContextTimeMachine](https://github.com/dakshjain-1616/ContextTimeMachine) | vertical turn timeline + three investigation-mode panels |
| LiveContext — transparent OpenAI/Anthropic/Ollama proxy with real-time context, token, eviction, attention dashboard | `livecontext` | [dakshjain-1616/LiveContext](https://github.com/dakshjain-1616/LiveContext) | agent ↔ proxy ↔ provider + WebSocket/REST + five live panel mockups |
| agentsync — git-backed AI config sync, tree-level 3-way merge, 52-point security/compliance audit | `agentsync` | [dakshjain-1616/agentsync](https://github.com/dakshjain-1616/agentsync) | 7-command top bar → merge engine ↔ git → 52-point audit fan-out by category |
| ASR Evaluation Framework — 5 ASR models × 15+ scenarios × WER/CER/RTF, stable JSON schema | `asr-evaluation-framework` | [dakshjain-1616/Asr-Evaluation](https://github.com/dakshjain-1616/Asr-Evaluation) | sequential model load → metric engine → per-scenario score bars |

# New Projects — Added 2026-05-15

3 new blog posts covering AI tool config sync, cross-session knowledge persistence, and multi-tool proxy context management. Each post ships with a hand-crafted Excalidraw architecture diagram under `public/images/diagrams/<slug>.{excalidraw,png}`.

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| RuleSync — single RULES.yaml synced to 6 AI tool config formats, 5-dimension quality audit, file watcher | `rulesync` | [dakshjain-1616/RuleSync](https://github.com/dakshjain-1616/RuleSync) | RULES.yaml hub → Pydantic parser → 6-adapter fan-out (Claude/Cursor/Gemini/Codex/Windsurf/Kiro) + audit dimension bar |
| ContextCarry — local proxy captures AI sessions, extracts 5 knowledge types into graph, injects Context Brief | `context-carry` | [dakshjain-1616/Context-Carry-](https://github.com/dakshjain-1616/Context-Carry-) | pipeline: AI tools → proxy → 5 detectors → SQLite knowledge graph → relevance scorer → brief injected |
| ToolRouter — shared session state across AI tools, Handoff Briefs on tool switch, real token spend tracking | `tool-router` | [dakshjain-1616/Tool-Router](https://github.com/dakshjain-1616/Tool-Router) | multi-tool input → proxy → state store (file tracker + decision extractor) → handoff brief + spend dashboard |
