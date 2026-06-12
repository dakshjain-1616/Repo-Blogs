#!/usr/bin/env python3
"""Excalidraw architecture diagram for Context Compaction Visualizer.

Story: Browser (React 18 + D3 tabs) <-> FastAPI (7 endpoints) -> 4 trace
parsers -> normalized message/compaction shape -> SQLite, with token counter
and Claude-powered info-loss analyzer services, plus a real analyzer output.
"""
import sys
sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, arrow, evidence_box, title_block, write,
    TITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'
g._seed[0] = 2600000


def build():
    els = []
    els += title_block(60, 1100, "Context Compaction Visualizer — See What Your Agent Forgot",
                       "Trace upload → 4 parsers → normalized timeline, replay, analytics → Claude-scored info loss")

    # ── Browser band ────────────────────────────────────────────────────────
    els.append(text(40, 92, 700, 18, "Browser — React 18 + D3.js + Tailwind (nginx :5173)",
                    size=13, color=TITLE, bold=True, align="left"))
    components = [
        ("TraceUploader\ndrag-drop · 4 formats", START_FILL, START_STROKE),
        ("ContextTimeline\nD3 stacked bars", TERTIARY_FILL, PRIMARY_STROKE),
        ("SessionReplay\nturn-by-turn diff", AI_FILL, AI_STROKE),
        ("TokenAnalytics\ncost + charts", DECISION_FILL, DECISION_STROKE),
        ("InfoLossDetector\nrisk scores", WARN_FILL, WARN_STROKE),
        ("ComparativeView\nside-by-side", END_FILL, END_STROKE),
    ]
    for i, (label, fill, stroke) in enumerate(components):
        els += rect(40 + i * 190, 118, 180, 55, label, fill=fill, stroke=stroke, label_size=10)

    # HTTP request / response between browser and backend
    els += arrow(570, 173, 570, 232, label="HTTP /api/*")
    els += arrow(660, 232, 660, 173, dashed=True, label="JSON")

    # ── FastAPI backend ─────────────────────────────────────────────────────
    els += rect(420, 232, 380, 62, "FastAPI Backend — main.py :8000\n7 REST endpoints · CORS · SQLAlchemy sessions",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)

    # Endpoint list (right)
    els += evidence_box(860, 215, 300, 132, [
        "POST /api/traces/upload",
        "GET  /api/traces/{id}/timeline",
        "GET  /api/traces/{id}/replay?turn=N",
        "GET  /api/traces/{id}/token-analysis",
        "POST /api/traces/{id}/analyze-info-loss",
        "POST /api/traces/compare",
    ], line_color=EVIDENCE_AMBER, title="7 endpoints (+ GET /api/traces/)")
    els += arrow(800, 263, 860, 263, stroke=BODY, dashed=True)

    # Trace file inputs (left)
    els += evidence_box(40, 225, 240, 105, [
        "langsmith_export.json",
        "otel_spans.json",
        "agentops_session.json",
        "custom_messages.json",
    ], line_color=EVIDENCE_GREEN, title="Trace formats")
    els += arrow(280, 262, 420, 262, label="upload")

    # ── Parser registry ─────────────────────────────────────────────────────
    parsers = [
        ("langsmith_parser.py\nruns + usage metadata", TERTIARY_FILL, PRIMARY_STROKE),
        ("otel_parser.py\nspan-tree traversal", AI_FILL, AI_STROKE),
        ("agentops_parser.py\nsession events → roles", DECISION_FILL, DECISION_STROKE),
        ("custom_parser.py\nmessages[] + events", START_FILL, START_STROKE),
    ]
    for i, (label, fill, stroke) in enumerate(parsers):
        els += rect(40 + i * 220, 380, 200, 50, label, fill=fill, stroke=stroke, label_size=10)

    # FastAPI fans out to the four parsers
    els += arrow(470, 294, 140, 380)
    els += arrow(530, 294, 360, 380)
    els += arrow(610, 294, 580, 380)
    els += arrow(680, 294, 800, 380)

    # ── Normalized shape + SQLite ───────────────────────────────────────────
    els += rect(260, 470, 420, 55,
                "Normalized trace\nmessages: role · tokens · turn  |  compaction: before · after · dropped",
                fill=SECONDARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(140, 430, 330, 470)
    els += arrow(360, 430, 420, 470)
    els += arrow(580, 430, 520, 470)
    els += arrow(800, 430, 610, 470)

    els += rect(760, 470, 240, 55, "SQLite — SQLAlchemy\nTrace · Message · CompactionEvent",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(680, 497, 760, 497)

    # ── Services ────────────────────────────────────────────────────────────
    els += rect(120, 565, 250, 62, "token_counter.py\ntiktoken or ~4 chars/token\n$3/M input · $15/M output",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(350, 525, 245, 565)

    els += rect(430, 565, 250, 62, "context_analyzer.py\n±5 messages per compaction event\n→ JSON risk items",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(480, 525, 555, 565)
    els += arrow(800, 525, 660, 565, stroke=BODY, dashed=True)

    els += rect(430, 660, 250, 55, "Anthropic API\nclaude-sonnet-4 · OpenRouter-compatible",
                fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(555, 627, 555, 660)

    # ── Real analyzer output ────────────────────────────────────────────────
    els += evidence_box(740, 565, 420, 175, [
        "overall_risk_score: 0.85",
        "tokens_dropped: 77,000 (security review)",
        "",
        "[0.90] 3 JWT findings lost permanently:",
        "       missing expiry check · no refresh",
        "       rotation · weak secret key",
        "[0.70] 23 tool-call exchanges of",
        "       reasoning context dropped",
    ], line_color=EVIDENCE_GREEN, title="POST /api/traces/{id}/analyze-info-loss")
    els += arrow(680, 596, 740, 596)

    return els


write("context-compaction-visualizer", build())
