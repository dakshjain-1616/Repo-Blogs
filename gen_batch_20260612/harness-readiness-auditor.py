#!/usr/bin/env python3
"""Excalidraw architecture diagram for Harness Readiness Auditor.

Story: agent codebase -> file scanner -> prompt builder -> (Claude | heuristic
fallback) -> 8 audit categories -> score aggregator -> 3 reporters -> report,
with the FastAPI backend + React frontend reusing the same audit modules.
"""
import sys

sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, ellipse, diamond, arrow, line, dot, evidence_box,
    title_block, write,
    TITLE, SUBTITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE, ERROR_FILL, ERROR_STROKE,
    EVIDENCE_BG, EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'


def build():
    g._seed[0] = 2800000
    els = []
    els += title_block(60, 1100, "Harness Readiness Auditor — Is Your AI Agent Production-Ready?",
                       "Scan agent code -> Claude or heuristic scoring across 8 maturity categories -> color-coded report + web dashboard")

    # --- Row 1: scan pipeline ---
    els += evidence_box(40, 110, 250, 145, [
        "my-agent/",
        "  agent.py",
        "  tools.py",
        "  memory.py",
        "  config.py",
        "  workflows.yaml",
    ], line_color=EVIDENCE_GREEN, title="Agent codebase (input)")

    els += rect(350, 125, 200, 65, "File Scanner\n.py .ts .js .json .yaml\n500 KB/file cap", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(290, 180, 350, 160)

    els += rect(620, 125, 210, 65, "build_audit_prompt\ncode <= 80k chars\n+ 8 category checklists", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(550, 157, 620, 157)

    els += diamond(900, 115, 180, 85, "ANTHROPIC_\nAPI_KEY set?", label_size=10)
    els += arrow(830, 157, 900, 157)

    # --- Row 2: two scoring paths ---
    els += rect(880, 250, 250, 65, "Claude API — temp 0\nclaude-sonnet-4-20250514\nJSON: scores + line-level findings", fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(990, 200, 1000, 250, label="yes")

    els += rect(600, 250, 230, 65, "Heuristic Fallback\nkeyword pattern scoring\n(works offline / in CI)", fill=WARN_FILL, stroke=WARN_STROKE, label_size=10)
    els += arrow(955, 197, 745, 250, stroke=WARN_STROKE, dashed=True, label="no key")

    # --- Row 3: 8 audit categories band ---
    els.append(text(40, 344, 760, 18, "8 Audit Categories — cli/categories/ · each exports CHECKLIST + assess()", size=14, color=TITLE, bold=True, align="left"))
    cats = [
        ("Context & Memory", "window budget · persistence", TERTIARY_FILL, PRIMARY_STROKE),
        ("Tool Permissions", "allowlist · arg validation", END_FILL, END_STROKE),
        ("Budget & Cost Controls", "token tracking · hard limits", DECISION_FILL, DECISION_STROKE),
        ("Context Compaction", "summarize, don't truncate", AI_FILL, AI_STROKE),
        ("Observability & Tracing", "structured logs · tool traces", START_FILL, START_STROKE),
        ("Human Approval", "confirm destructive calls", ERROR_FILL, ERROR_STROKE),
        ("Reliability Safeguards", "retry · backoff · circuit breaker", WARN_FILL, WARN_STROKE),
        ("Failure Recovery", "checkpoints · cleanup on exit", SECONDARY_FILL, PRIMARY_STROKE),
    ]
    for i, (name, detail, fill, stroke) in enumerate(cats):
        col = i % 4
        row = i // 4
        x = 40 + col * 285
        y = 375 + row * 70
        els += rect(x, y, 260, 55, f"{name}\n{detail}", fill=fill, stroke=stroke, label_size=10)

    els += arrow(1005, 315, 1025, 375)                       # Claude -> band
    els += arrow(715, 315, 740, 375, stroke=WARN_STROKE, dashed=True)  # heuristic -> band

    # --- Row 4: aggregator + reporters ---
    els += rect(40, 595, 230, 70, "Score Aggregator\noverall = mean of 8\nfindings + recommendations", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(170, 500, 155, 595)

    els += rect(330, 540, 230, 50, "terminal_reporter\nRich table, color-coded", fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += rect(330, 605, 230, 50, "json_reporter\nmachine-readable, for CI", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(330, 670, 230, 50, "html_reporter\nself-contained, shareable", fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(270, 612, 330, 568)
    els += arrow(270, 630, 330, 630)
    els += arrow(270, 648, 330, 692)

    # --- Audit output evidence ---
    els += evidence_box(630, 540, 530, 185, [
        "Overall Maturity Score: 61/100",
        "",
        "Context & Memory       78   no persistence layer",
        "Tool Permissions       85   allowlist + validation OK",
        "Budget & Cost          40   no hard cost limit",
        "Reliability            45   no retry w/ backoff",
        "Failure Recovery       52   checkpoints missing",
        "",
        ">=80 green · 50-79 yellow · <50 red",
    ], line_color=EVIDENCE_AMBER, title="$ harness-audit scan ./my-agent")
    els += arrow(560, 565, 630, 580)
    els += arrow(560, 630, 630, 640, dashed=True, stroke=BODY)

    # --- Web stack (reuses the same audit modules) ---
    els += rect(40, 745, 250, 70, "FastAPI Backend\nPOST /audit · GET /reports/{id}\nSQLite: Report + Finding", fill=SECONDARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(165, 745, 158, 665, stroke=BODY, dashed=True, label="same modules")

    els += rect(340, 750, 270, 60, "React Frontend (Vite)\nScoreCard · RadarChart\nFindingsList · CategoryDrilldown", fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(340, 780, 290, 780, label="HTTP")

    return els


write('harness-readiness-auditor', build())
