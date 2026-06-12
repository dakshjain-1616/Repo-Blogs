#!/usr/bin/env python3
"""Architecture diagram for Harness Template Library.

Story: 10 CLI entry points -> template harness package -> 15 shared core
modules -> infra (SQLite + Anthropic API), with a run-output evidence box.
"""
import sys
sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, ellipse, diamond, arrow, line, dot, evidence_box, title_block,
    write, TITLE, SUBTITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE, ERROR_FILL, ERROR_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'


def build():
    g._seed[0] = 2900000
    els = []
    els += title_block(60, 1100, "Harness Template Library — 10 Agent Harnesses, One Shared Core",
                       "Pick a template, get all 15 infrastructure modules pre-wired: permissions, budgets, approval, state, audit")

    # ===== 10 CLI entry points (two rows of 5) =====
    els += rect(30, 88, 1150, 132, "", fill="#f8fafc", stroke=BODY, dashed=True)
    els.append(text(45, 94, 500, 14, "10 CLI entry points — pyproject.toml [project.scripts] (click)",
                    size=11, color=TITLE, bold=True, align="left"))
    clis = [
        "coding-agent", "research-agent", "customer-support", "data-engineering", "browser-automation",
        "multi-agent-orchestrator", "rag-agent", "finance-operations", "document-analysis", "long-horizon-task",
    ]
    for i, name in enumerate(clis):
        col, row = i % 5, i // 5
        x = 50 + col * 225
        y = 116 + row * 50
        els += rect(x, y, 205, 40, name, fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)

    # ===== Template harness package =====
    els += arrow(605, 220, 605, 262, label="task / query")
    els += rect(345, 262, 520, 90,
                "Template Harness — templates/<name>/\nharness.py wires all 15 core modules\ntools.py · config.py · system_prompt.txt",
                fill=AI_FILL, stroke=AI_STROKE, label_size=11)

    # Left note: what varies per template
    els += rect(40, 272, 260, 70, "Templates differ only in\ntools · prompts · workflows\n· permission policies",
                fill="#f8fafc", stroke=BODY, label_size=10, dashed=True)
    els += arrow(300, 307, 345, 307, stroke=BODY, dashed=True)

    # Right note: Docker per template
    els += rect(910, 272, 260, 70, "Docker per template\ndocker compose up --build\n(DeploymentConfig generates)",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(865, 307, 910, 307, stroke=END_STROKE, dashed=True)

    # ===== 15 core modules grid =====
    els += arrow(605, 352, 605, 396)
    els += rect(30, 396, 1150, 232, "", fill="#ffffff", stroke=PRIMARY_STROKE, dashed=True)
    els.append(text(45, 402, 500, 14, "15 shared core modules (core/) — written once, used by all 10 templates",
                    size=11, color=TITLE, bold=True, align="left"))
    modules = [
        ("InstructionManager", "prompt load + {var} interp", TERTIARY_FILL, PRIMARY_STROKE),
        ("ContextBuilder", "token-budget messages", TERTIARY_FILL, PRIMARY_STROKE),
        ("MemoryLayer", "SQLite keyword memory", END_FILL, END_STROKE),
        ("ModelAdapter", "AsyncAnthropic + backoff", AI_FILL, AI_STROKE),
        ("ToolRegistry", "name + schema + handler", TERTIARY_FILL, PRIMARY_STROKE),
        ("PermissionResolver", "allowlist + wildcards", WARN_FILL, WARN_STROKE),
        ("BudgetManager", "BudgetExceededError", WARN_FILL, WARN_STROKE),
        ("WorkflowEngine", "steps + branching", TERTIARY_FILL, PRIMARY_STROKE),
        ("StateManager", "SQLite resume state", END_FILL, END_STROKE),
        ("HumanApprovalLayer", "CLI confirm gate", WARN_FILL, WARN_STROKE),
        ("ObservabilityLayer", "structlog + OTEL spans", DECISION_FILL, DECISION_STROKE),
        ("EvaluationFramework", "rubric via 2nd Claude call", AI_FILL, AI_STROKE),
        ("RetryRecoverySystem", "backoff + checkpoints", DECISION_FILL, DECISION_STROKE),
        ("AuditLogger", "append-only SQLite log", END_FILL, END_STROKE),
        ("DeploymentConfig", "Dockerfile + compose gen", START_FILL, START_STROKE),
    ]
    for i, (name, detail, fill, stroke) in enumerate(modules):
        col, row = i % 5, i // 5
        x = 50 + col * 225
        y = 424 + row * 64
        els += rect(x, y, 205, 52, f"{name}\n{detail}", fill=fill, stroke=stroke, label_size=9)

    # ===== Infrastructure =====
    els += arrow(280, 628, 280, 672)
    els += arrow(620, 628, 620, 672)
    els += rect(130, 672, 300, 64, "SQLite (aiosqlite)\nmemory.db · state.db · audit.db",
                fill=END_FILL, stroke=END_STROKE, label_size=11)
    els += rect(470, 672, 300, 64, "Anthropic API\nclaude-sonnet-4-20250514",
                fill=START_FILL, stroke=START_STROKE, label_size=11)

    # ===== Evidence: real CLI run output =====
    els += arrow(990, 628, 990, 656, stroke=BODY, dashed=True)
    els += evidence_box(820, 656, 360, 124, [
        "Model: claude-sonnet-4-20250514",
        "Input tokens: 1284 · Output tokens: 412",
        "Cost: $0.010032  (budget $5.00)",
        "audit.db <- model_call logged",
        "workflow: understand -> ... -> commit  [ok]",
    ], line_color=EVIDENCE_GREEN, title='$ coding-agent "check if a string is a palindrome"')

    return els


write('harness-template-library', build())
