#!/usr/bin/env python3
"""Architecture diagram for LLM Real-World Benchmark.

Story: triggers (cron / CLI / API) -> async runner -> OpenRouter models,
task suite feeds the runner, responses flow to a Claude Opus judge,
scores land in SQLite, leaderboard renders from snapshots, FastAPI serves it.
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
    AI_FILL, AI_STROKE, EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'
g._seed[0] = 2400000


def build():
    els = []
    els += title_block(60, 1100,
                       "LLM Real-World Benchmark — Weekly Harness, Real Engineering Tasks",
                       "7 models x 4 tasks via OpenRouter -> Claude Opus judge -> SQLite -> ranked leaderboard with latency + cost")

    # ── Triggers row ────────────────────────────────────────────────
    els += rect(330, 90, 170, 45, "APScheduler\nMon 03:00 UTC", fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += rect(530, 90, 140, 45, "CLI run-now", fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += rect(700, 90, 140, 45, "POST /api/run", fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(415, 135, 470, 185)
    els += arrow(600, 135, 590, 185)
    els += arrow(770, 135, 700, 185)

    # ── Task suite (left column) ────────────────────────────────────
    tasks = [
        ("fastapi_jwt", "/login + JWT + 5 pytest tests"),
        ("debug_traceback", "3-level exception chain"),
        ("refactor_async", "200-line sync -> asyncio"),
        ("schema_pydantic", "SQL schema -> Pydantic v2"),
    ]
    for i, (name, desc) in enumerate(tasks):
        yt = 110 + i * 60
        els += rect(40, yt, 240, 50, f"{name}\n{desc}", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
        els += arrow(280, yt + 25, 330, 200 + i * 15)

    # ── Async runner ────────────────────────────────────────────────
    els += rect(330, 185, 510, 80,
                "Async Runner — httpx\nSemaphore(10) · 60s timeout · 3x backoff · cost per call",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)

    # ── OpenRouter models (right) ───────────────────────────────────
    els += rect(900, 130, 250, 190,
                "OpenRouter\n7 models under test\n\nGPT-4.1 · Claude Opus 4.8\nGemini 2.5 Pro · Grok 3\nDeepSeek V3 · Kimi K2\nGLM-4 32B",
                fill="#f8fafc", stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(840, 205, 900, 190)
    els.append(text(835, 162, 60, 14, "28 calls", size=10, color=BODY, align="left"))
    els += arrow(900, 265, 840, 248, stroke=BODY, dashed=True)
    els.append(text(848, 272, 80, 14, "responses", size=10, color=BODY, align="left"))

    # ── Judge ───────────────────────────────────────────────────────
    els += rect(330, 330, 510, 80,
                "LLM Judge — claude-opus-4.8\ncorrectness 35% · completeness 25% · code quality 20%\nerror handling 10% · instructions 10%",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(585, 265, 585, 330, label="model responses")

    # Judge JSON evidence (left)
    els += evidence_box(40, 380, 250, 120, [
        '{"score": 87,',
        ' "rationale": "...",',
        ' "breakdown": {',
        '   "correctness": 90,',
        '   "completeness": 85, ...}}',
    ], line_color=EVIDENCE_GREEN, title="judge returns strict JSON")
    els += arrow(330, 372, 292, 400, stroke=BODY, dashed=True)

    # ── SQLite ──────────────────────────────────────────────────────
    els += rect(330, 460, 510, 60,
                "SQLite — runs · results · leaderboard_snapshots",
                fill="#f0fdf4", stroke=END_STROKE, label_size=11)
    els += arrow(585, 410, 585, 460, label="score 0-100")

    # ── Leaderboard ─────────────────────────────────────────────────
    els += rect(330, 570, 510, 70,
                "Leaderboard — Jinja2 + Chart.js\nsortable · medals · score badges · 6-run trend line",
                fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=11)
    els += arrow(585, 520, 585, 570)

    # ── FastAPI serve (right of leaderboard) ────────────────────────
    els += rect(900, 565, 250, 80,
                "FastAPI serve\nGET /  ·  /api/leaderboard\n/api/results  ·  /api/runs",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(840, 605, 900, 605)

    # ── CLI run evidence ────────────────────────────────────────────
    els += evidence_box(40, 675, 600, 130, [
        "Collected 28 results  (7 models x 4 tasks)",
        "Scored 28 results  (judge: claude-opus-4.8)",
        "1. gpt-4.1           91.8   11.0s   $0.0115",
        "2. kimi-k2           89.0   67.7s   $0.0034",
        "3. claude-opus-4.8   87.0   39.0s   $0.1019",
        "Leaderboard written to leaderboard/index.html",
    ], line_color=EVIDENCE_GREEN, title="$ python -m src.cli run-now")

    # ── Env footer ──────────────────────────────────────────────────
    els += evidence_box(680, 675, 470, 40, [
        "OPENROUTER_API_KEY=sk-or-...   one key covers models + judge",
    ], line_color=EVIDENCE_AMBER)

    return els


write('llm-real-world-benchmark', build())
