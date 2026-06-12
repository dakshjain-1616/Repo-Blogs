#!/usr/bin/env python3
"""Excalidraw architecture diagram for Data Pipeline Debugger.

Story: React browser components -> FastAPI backend -> investigation engine
       -> pipeline adapters (context) + Claude (streaming) -> SQLite
       -> SSE stream back to the browser -> findings + report.
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
g._seed[0] = 2700000


def build():
    els = []
    els += title_block(60, 1100, "Data Pipeline Debugger — AI Investigation for Failed Pipelines",
                       "Evidence upload → FastAPI → adapter-grounded Claude investigation → SSE stream → findings + remediation")

    # ── Browser column (left) ────────────────────────────────────────
    els.append(text(40, 88, 210, 16, "Browser — React 18 + Vite (Nginx :80)", size=11, color=TITLE, bold=True, align="left"))
    components = [
        ("SessionCreator", "name · pipeline type"),
        ("ArtifactUploader", "log / schema / trace / dataset"),
        ("InvestigationStream", "EventSource — live steps"),
        ("FindingsDashboard", "root cause · confidence"),
        ("RemediationPanel", "fix · prevention · monitoring"),
    ]
    for i, (name, sub) in enumerate(components):
        y = 115 + i * 56
        els += rect(40, y, 210, 44, f"{name}\n{sub}", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=9)

    # ── FastAPI backend ──────────────────────────────────────────────
    els += rect(330, 150, 230, 120,
                "FastAPI Backend :8000\nsessions · artifacts ·\ninvestigate · stream · report\nSQLAlchemy ORM",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)
    els += arrow(250, 190, 330, 182, label="HTTP")
    els += arrow(330, 238, 250, 246, dashed=True, label="SSE")

    # ── Investigation engine ─────────────────────────────────────────
    els += rect(630, 140, 220, 80,
                "Investigation Engine\nbuild prompt → stream model\nparse steps → save findings",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(560, 170, 630, 165)
    els += arrow(630, 205, 560, 205, dashed=True)

    # ── Pipeline adapters (below engine) ─────────────────────────────
    adapters = [
        ("Airflow Adapter", "DAGs · tasks · pools · airflow CLI", START_FILL, START_STROKE),
        ("dbt Adapter", "models · tests · compilation", DECISION_FILL, DECISION_STROKE),
        ("Spark Adapter", "stages · executors · shuffle", WARN_FILL, WARN_STROKE),
    ]
    for i, (name, sub, fill, stroke) in enumerate(adapters):
        y = 264 + i * 54
        els += rect(630, y, 220, 44, f"{name}\n{sub}", fill=fill, stroke=stroke, label_size=9)
    els += arrow(740, 264, 740, 220)
    els.append(text(758, 232, 170, 12, "context + diagnostic cmds", size=9, color=BODY, align="left"))

    # ── Claude (right of engine) ─────────────────────────────────────
    els += rect(920, 140, 220, 80, "Claude API\nclaude-sonnet-4\nmessages.stream",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(850, 170, 920, 170)
    els.append(text(852, 148, 70, 12, "stream", size=9, color=BODY, align="left"))

    # No-API-key fallback note
    els += rect(920, 250, 220, 50, "No API key →\nsimulated investigation", fill="#f8fafc",
                stroke=BODY, dashed=True, label_size=9)

    # ── SQLite ───────────────────────────────────────────────────────
    els += rect(920, 330, 220, 90, "SQLite\nDebugSession · Artifact\nInvestigationStep · Finding",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(850, 210, 920, 350)
    els.append(text(856, 258, 90, 12, "save each step", size=9, color=BODY, align="left"))

    # ── SSE evidence box (bottom left) ───────────────────────────────
    els += evidence_box(40, 470, 620, 185, [
        'data: {"event":"status","status":"investigating"}',
        'data: {"event":"step","step_type":"hypothesis","step_number":1}',
        '      H1 resource exhaustion 75% · H2 data skew 60% · H3 config 40%',
        'data: {"event":"step","step_type":"evidence","step_number":2}',
        '      OOM at Stage 3 Task 42 — partition 8.5 GB vs 200 MB median',
        'data: {"event":"step","step_type":"root_cause","step_number":3}',
        '      Data skew on unsalted join key — confidence 85%',
        'data: {"event":"step","step_type":"remediation","step_number":4}',
        'data: {"event":"done","step_count":4,"finding_count":3}',
    ], line_color=EVIDENCE_GREEN, title="GET /api/sessions/7/investigation/stream — Server-Sent Events")
    els += arrow(430, 270, 380, 470)

    # ── Findings / report evidence (bottom right) ────────────────────
    els += evidence_box(700, 470, 440, 185, [
        "finding_type   conf   title",
        "root_cause      85%   Data skew on unsalted join key",
        "dismissed        0%   Config error — 50 identical runs",
        "remediation    100%   salt join · AQE · memory flag",
        "",
        "report.md — all 4 steps + findings ranked",
        "by confidence, ready for the incident channel",
    ], line_color=EVIDENCE_AMBER, title="GET /findings · GET /report")
    els += arrow(1030, 420, 1010, 470)

    # ── Footer ───────────────────────────────────────────────────────
    els.append(text(40, 675, 1100, 16,
                    "docker compose up --build  —  backend :8000 (healthcheck /api/health) · frontend Nginx :80 · 32 backend tests with mocked model calls",
                    size=11, color=BODY, align="left"))

    return els


write('data-pipeline-debugger', build())
