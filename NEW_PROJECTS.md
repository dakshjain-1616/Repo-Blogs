# New Projects — Added 2026-05-15

3 new blog posts covering AI tool config sync, cross-session knowledge persistence, and multi-tool proxy context management. Each post ships with a hand-crafted Excalidraw architecture diagram under `public/images/diagrams/<slug>.{excalidraw,png}`.

| Blog | Slug | GitHub | Diagram |
|------|------|--------|---------|
| RuleSync — single RULES.yaml synced to 6 AI tool config formats, 5-dimension quality audit, file watcher | `rulesync` | [dakshjain-1616/RuleSync](https://github.com/dakshjain-1616/RuleSync) | RULES.yaml hub → Pydantic parser → 6-adapter fan-out (Claude/Cursor/Gemini/Codex/Windsurf/Kiro) + audit dimension bar |
| ContextCarry — local proxy captures AI sessions, extracts 5 knowledge types into graph, injects Context Brief | `context-carry` | [dakshjain-1616/Context-Carry-](https://github.com/dakshjain-1616/Context-Carry-) | pipeline: AI tools → proxy → 5 detectors → SQLite knowledge graph → relevance scorer → brief injected |
| ToolRouter — shared session state across AI tools, Handoff Briefs on tool switch, real token spend tracking | `tool-router` | [dakshjain-1616/Tool-Router](https://github.com/dakshjain-1616/Tool-Router) | multi-tool input → proxy → state store (file tracker + decision extractor) → handoff brief + spend dashboard |
