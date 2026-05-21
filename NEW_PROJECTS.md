# New blogs added 2026-05-21

Three new blog posts. Diagrams generated via `gen_3_more_diagrams.py` then rendered to PNG via `render_pil.py`.

| Project | Blog | Diagram | GitHub |
|---|---|---|---|
| ArchGuard | [blogs/arch-guard.md](blogs/arch-guard.md) | `public/images/diagrams/arch-guard.png` | https://github.com/dakshjain-1616/Arch-Guard |
| CostGuard | [blogs/cost-guard.md](blogs/cost-guard.md) | `public/images/diagrams/cost-guard.png` | https://github.com/dakshjain-1616/cost-Guard |
| AgentLiar | [blogs/agent-liar.md](blogs/agent-liar.md) | `public/images/diagrams/agent-liar.png` | https://github.com/dakshjain-1616/AgentLiar |

## Descriptions and keywords

### ArchGuard
**Description:** A Python static analysis CLI that scans codebases for six architectural-degradation patterns (circular dependencies, god classes, service-layer bypass, magic values, cyclomatic complexity, layer violations), supports per-PR comparison and 10-commit trend tracking, and plugs into pre-commit hooks and GitHub Actions.
**Keywords:** static analysis, python, architecture, code quality, AST, NetworkX, CLI, technical debt, dependency graph, git hooks, GitHub Actions, code review, refactoring, codebase health, pre-commit

### CostGuard
**Description:** A local FastAPI proxy that sits between your application and OpenAI / Anthropic / OpenRouter, estimates request cost with tiktoken before forwarding, and enforces session, hourly, daily, and project-level spending caps with a HTTP 402 circuit breaker plus a live terminal dashboard.
**Keywords:** LLM cost control, FastAPI proxy, OpenAI, Anthropic, OpenRouter, tiktoken, budget enforcement, circuit breaker, AI observability, WebSocket dashboard, SQLite, pre-flight estimation, token counting, safe mode, spend tracking

### AgentLiar
**Description:** A verification system for coding agents that takes the task, the agent's claim, and the produced diff, then runs four parallel checks (file integrity, test quality, scope narrowing, optional LLM judge) and returns a weighted 0-100 confidence score with per-check evidence, available as a CLI, Python library, GitHub Action, and FastAPI service.
**Keywords:** agent verification, coding agents, AI evaluation, LLM judge, OpenRouter, FastAPI, GitHub Actions, async orchestration, test quality, scope detection, agent overclaim, code review automation, asyncio, Pydantic, confidence scoring
