#!/usr/bin/env python3
"""Architecture diagram for Tool Permission Matrix Builder & Validator.

Story: six React tabs -> axios -> async FastAPI -> SQLite matrix +
three services (policy generator, agent validator, sprawl analyzer)
-> policy artifacts + Claude-backed validation report.
"""
import sys
sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, ellipse, diamond, arrow, line, dot, evidence_box, title_block, write,
    TITLE, SUBTITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE, ERROR_FILL, ERROR_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'
g._seed[0] = 3100000


def build():
    els = []
    els += title_block(60, 1100, "Tool Permission Matrix Builder & Validator",
                       "Drag-and-drop roles × tools policy matrix → JSON / YAML / Python artifacts → Claude-validated agents")

    # ── Frontend column (left) ──────────────────────────────────────────
    els.append(text(40, 92, 200, 16, "React 18 + Zustand (nginx :80)", size=11, color=TITLE, bold=True, align="left"))
    tabs = [
        ("ToolRegistry\n6 risk categories", TERTIARY_FILL, PRIMARY_STROKE),
        ("RoleManager\ninheritance", TERTIARY_FILL, PRIMARY_STROKE),
        ("PermissionMatrix\n@dnd-kit grid", PRIMARY_FILL, PRIMARY_STROKE),
        ("PolicyExporter\ndownload", TERTIARY_FILL, PRIMARY_STROKE),
        ("AgentValidator\npaste code", AI_FILL, AI_STROKE),
        ("SprawlAnalysis\nscore + issues", DECISION_FILL, DECISION_STROKE),
    ]
    for i, (label, fill, stroke) in enumerate(tabs):
        y = 115 + i * 58
        lc = "#ffffff" if fill == PRIMARY_FILL else INK
        els += rect(40, y, 200, 46, label, fill=fill, stroke=stroke, label_color=lc, label_size=10)

    # ── FastAPI backend (center) ────────────────────────────────────────
    els += rect(330, 210, 210, 110, "FastAPI Backend\nmain.py — async routes\n/api/tools /api/roles\n/api/permissions /api/matrix",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    for i in range(6):
        yc = 115 + i * 58 + 23
        lbl = "axios · 20 methods" if i == 2 else None
        els += arrow(240, yc, 330, 265, label=lbl)

    # SQLite below backend
    els += rect(330, 380, 210, 70, "SQLite (aiosqlite)\nTool · Role · Permission\n3-state cells",
                fill="#f0fdf4", stroke=END_STROKE, label_size=10)
    els += arrow(435, 320, 435, 380)

    # ── Services column ─────────────────────────────────────────────────
    els.append(text(610, 122, 230, 16, "backend/services/", size=11, color=TITLE, bold=True, align="left"))
    els += rect(610, 150, 230, 55, "policy_generator.py\nJSON · YAML · py_compile gate",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += rect(610, 240, 230, 55, "agent_validator.py\nregex extract + Claude",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += rect(610, 330, 230, 55, "sprawl_analyzer.py\nover-exposure + Claude",
                fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=10)
    els += arrow(540, 240, 610, 180)
    els += arrow(540, 265, 610, 267)
    els += arrow(540, 290, 610, 357)

    # ── Outputs (right) ─────────────────────────────────────────────────
    els += rect(900, 140, 240, 60, "Policy Artifacts\npolicy.json · policy.yaml\npermissions.py (check_permission)",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(840, 175, 900, 170)

    els += rect(900, 260, 240, 70, "Anthropic API\nclaude-sonnet-4\n(heuristic fallback if no key)",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(840, 267, 900, 285)
    els += arrow(840, 357, 900, 310)

    # ── Matrix evidence (left bottom) ───────────────────────────────────
    els += evidence_box(40, 490, 480, 120, [
        "                  analyst  operator  admin",
        "query_db   [ro]      ✓        ✓       ✓",
        "send_email [ext]     ✕        ✓       ✓",
        "delete_res [destr]   ✕        ●       ✓",
        "✓ allowed   ✕ denied   ● inherited from parent",
    ], line_color=EVIDENCE_GREEN, title="GET /api/matrix — 3-state grid (roles × tools)")

    # ── Validation evidence (right bottom) ──────────────────────────────
    els += evidence_box(610, 430, 530, 170, [
        "security_score: 62/100   tool_calls_detected: 7",
        "[critical] delete_resource   missing_permission",
        "[high]     execute_code      high_risk_tool_usage",
        "[medium]   fetch_url         unknown_tool",
        "recommendation: gate destructive calls behind approval",
        "",
        "sprawl_score: 80/100 — 9 issues (2 critical)",
        "over_exposed_role: admin holds execute_code + delete_resource",
    ], line_color=EVIDENCE_AMBER, title="POST /api/validate · POST /api/sprawl/analysis")
    els += arrow(725, 385, 725, 430)
    els += arrow(1020, 330, 1020, 430, dashed=True)

    # ── Deploy footer ───────────────────────────────────────────────────
    els += evidence_box(40, 650, 1100, 40, [
        "$ docker compose up --build    backend :8000 /api/health (healthcheck)  →  frontend nginx :80 waits for healthy",
    ], line_color=EVIDENCE_AMBER)

    return els


write('tool-permission-matrix-builder', build())
