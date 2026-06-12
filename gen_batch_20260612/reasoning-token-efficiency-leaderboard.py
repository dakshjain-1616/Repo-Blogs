#!/usr/bin/env python3
"""Excalidraw architecture diagram for the Reasoning Token Efficiency Leaderboard.

Story: 6 models x 20 tasks -> async BenchmarkRunner -> OpenRouter (completions +
generation stats) -> four graders -> metrics engine (efficiency score) ->
SQLite / FastAPI / HTML leaderboard, with a live-results leaderboard panel.
"""
import sys

sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, arrow, evidence_box, title_block, write,
    TITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'
g._seed[0] = 2500000


def build():
    els = []
    els += title_block(60, 1100,
                       "Reasoning Token Efficiency Leaderboard",
                       "6 thinking models x 20 tasks -> async runner -> OpenRouter token accounting -> efficiency = accuracy / reasoning_tokens x 1000")

    # ---- Inputs: models and tasks ----
    els += evidence_box(40, 100, 320, 150, [
        "openai/gpt-4.1        effort: high",
        "claude-opus-4.8       adaptive",
        "gemini-2.5-pro        enabled",
        "x-ai/grok-4.3         native",
        "deepseek-r1           native",
        "moonshotai/kimi-k2    native",
    ], line_color=EVIDENCE_GREEN, title="6 thinking models (config.MODELS)")

    els += evidence_box(400, 100, 320, 150, [
        "AIME Math (5)       exact match",
        "Logic Puzzles (5)   boolean T/F",
        "Code Debug (5)      subprocess tests",
        "Formal Proofs (5)   LLM judge rubric",
    ], line_color=EVIDENCE_AMBER, title="20 tasks in 4 categories")

    # ---- Runner ----
    els += rect(215, 320, 330, 70,
                "BenchmarkRunner\nasyncio - Semaphore(8) - httpx AsyncClient",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)
    els += arrow(190, 250, 310, 320)
    els += arrow(570, 250, 460, 320)
    els.append(text(310, 276, 140, 16, "120 combinations", size=10, color=BODY))

    # ---- OpenRouter (right of runner) ----
    els += rect(770, 300, 360, 100,
                "OpenRouter API\nPOST /chat/completions + thinking params\nGET /generation?id -> native_tokens_reasoning",
                fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(545, 330, 770, 330, label="request")
    els += arrow(770, 375, 545, 375, stroke=BODY, dashed=True, label="tokens + cost")

    # ---- Graders ----
    els.append(text(40, 412, 400, 16, "Four graders, one per task category",
                    size=12, color=TITLE, bold=True, align="left"))
    graders = [
        ("Math\nexact match", END_FILL, END_STROKE),
        ("Logic\nboolean True/False", TERTIARY_FILL, PRIMARY_STROKE),
        ("Code\nsubprocess test suite", DECISION_FILL, DECISION_STROKE),
        ("Proofs\nLLM judge (Opus 4.8)", AI_FILL, AI_STROKE),
    ]
    for i, (label, fill, stroke) in enumerate(graders):
        x = 40 + i * 165
        els += rect(x, 440, 150, 65, label, fill=fill, stroke=stroke, label_size=10)
        els += arrow(380, 390, x + 75, 440)

    # ---- Metrics engine ----
    els += rect(40, 570, 645, 80,
                "Metrics Engine\nefficiency = accuracy / avg_reasoning_tokens x 1000\ncost per correct answer - latency p50 / p95",
                fill=WARN_FILL, stroke=WARN_STROKE, label_size=11)
    for i in range(4):
        x = 115 + i * 165
        els += arrow(x, 505, x, 570)

    # ---- Outputs ----
    els += rect(40, 710, 190, 60, "SQLite Store\naiosqlite - run history",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(270, 710, 200, 60, "FastAPI + CLI\nPOST /run - GET /leaderboard",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += rect(510, 710, 200, 60, "Leaderboard HTML\nJinja2 - sorted by efficiency",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(135, 650, 135, 710)
    els += arrow(370, 650, 370, 710)
    els += arrow(610, 650, 610, 710)

    # ---- Live leaderboard panel (right column) ----
    els += evidence_box(770, 460, 400, 200, [
        "#  model              acc   r-tok    eff",
        "1  gemini-2.5-pro     80%   1,900   0.421",
        "2  claude-opus-4.8    65%   adaptive    -",
        "2  deepseek-r1        65%   -           -",
        "2  kimi-k2            65%   -           -",
        "5  grok-4.3           60%   216      2.78",
        "6  gpt-4.1            40%   -           -",
        "",
        "grok leads efficiency - gemini leads accuracy",
    ], line_color=EVIDENCE_GREEN, title="Live run - 2026-06-09 - 6 models x 20 tasks")
    els += arrow(710, 730, 770, 640)

    return els


write('reasoning-token-efficiency-leaderboard', build())
