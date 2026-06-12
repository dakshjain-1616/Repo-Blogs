#!/usr/bin/env python3
"""Excalidraw diagram for the Multi-Service System Design & Implementation Agent.

Story: four-screen React flow -> FastAPI backend (9 endpoints + SSE bus)
-> design generator + parallel impl generator -> Claude (AsyncAnthropic)
-> per-service scaffolds persisted to SQLite. Evidence: live SSE stream
and the docker-compose runtime.
"""
import sys

sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, arrow, evidence_box, title_block, write,
    TITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    DECISION_FILL, DECISION_STROKE, AI_FILL, AI_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'


def build():
    g._seed[0] = 3000000
    els = []
    els += title_block(40, 1120, "Multi-Service System Design Agent — Idea to Scaffolds",
                       "React four-screen flow -> FastAPI + SSE -> Claude design + asyncio.gather parallel codegen -> SQLite")

    # ---- Top row: browser flow ------------------------------------------
    els.append(text(40, 92, 420, 16, "Browser — React + Tailwind (Vite)", size=12, color=TITLE, bold=True, align="left"))

    screens = [
        ("IdeaInput\nPOST /api/design", START_FILL, START_STROKE),
        ("DesignReview\ninline edit · approve / regen", TERTIARY_FILL, PRIMARY_STROKE),
        ("ProgressStream\nSSE /api/stream/{id}", TERTIARY_FILL, PRIMARY_STROKE),
        ("ProjectExplorer\nfile tree · ZIP download", END_FILL, END_STROKE),
    ]
    xs = [40, 320, 600, 880]
    for (label, fill, stroke), x in zip(screens, xs):
        els += rect(x, 115, 240, 55, label, fill=fill, stroke=stroke, label_size=10)
    for x in (280, 560, 840):
        els += arrow(x, 142, x + 40, 142)

    # ---- Middle: FastAPI core --------------------------------------------
    els += rect(430, 260, 340, 80, "FastAPI main.py\n9 REST endpoints + SSE broadcast bus",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=12)

    # frontend -> backend arrows
    els += arrow(160, 170, 480, 260, label="POST /api/design")
    els += arrow(440, 170, 560, 260, label="approve -> generate")
    els += arrow(640, 260, 700, 170, dashed=True, label="SSE events")
    els += arrow(980, 170, 700, 260, label="GET files")

    # SQLite (left of backend)
    els += rect(40, 280, 180, 80, "SQLite (SQLAlchemy)\nprojects · designs\n· generated_files",
                fill="#f0fdf4", stroke=END_STROKE, label_size=10)
    els += arrow(430, 300, 220, 310, label="ORM")

    # ---- Generators row ---------------------------------------------------
    els += rect(300, 390, 230, 70, "design_generator.py\nidea -> strict JSON design",
                fill=SECONDARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(640, 390, 230, 70, "impl_generator.py\nasyncio.gather — one task\nper service",
                fill=SECONDARY_FILL, stroke=PRIMARY_STROKE, label_size=10)

    els += arrow(500, 340, 430, 390, label="product idea")
    els += arrow(700, 340, 740, 390, label="approved design")

    # ---- Claude -----------------------------------------------------------
    els += rect(470, 520, 260, 80, "Anthropic API\nclaude-sonnet-4 (AsyncAnthropic)\nfence-strip -> json.loads",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(415, 460, 530, 520, label="1 call · temp 0.3")
    els += arrow(755, 460, 670, 520, label="N calls · temp 0.2")

    # ---- Scaffold fan-out (right) ----------------------------------------
    els.append(text(950, 325, 210, 14, "Generated scaffolds (per service)", size=11, color=TITLE, bold=True, align="left"))
    scaffolds = ["auth-service", "pr-service", "ai-service", "notification-service"]
    for i, name in enumerate(scaffolds):
        y = 350 + i * 60
        els += rect(950, y, 210, 45, f"{name}\nmain · routes · Dockerfile · tests",
                    fill=END_FILL, stroke=END_STROKE, label_size=9)
        els += arrow(870, 405 + i * 10, 950, y + 22)

    # ---- Evidence: SSE stream --------------------------------------------
    els += evidence_box(40, 630, 560, 130, [
        'event: connected  {"message": "Connected"}',
        'event: status     "Starting code generation for 4 services..."',
        'event: progress   "Generating auth-service implementation..."',
        'event: progress   "Generated 9 files for auth-service"',
        'event: complete   "Generated 38 files across 4 services"',
    ], line_color=EVIDENCE_GREEN, title="GET /api/stream/{project_id} — live progress, 30s keepalive pings")

    # ---- Evidence: docker compose ----------------------------------------
    els += evidence_box(640, 630, 520, 100, [
        "$ docker compose up --build",
        "backend   :8000  healthcheck /health gates frontend",
        "frontend  :5173  nginx · VITE_API_BASE=http://backend:8000/api",
    ], line_color=EVIDENCE_AMBER, title="docker-compose.yml")

    return els


write('multi-service-system-design-agent', build())
