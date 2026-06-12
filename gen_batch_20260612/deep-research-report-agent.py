#!/usr/bin/env python3
"""Excalidraw architecture diagram for Deep Research Report Agent.

Pattern: multi-stage pipeline with a parallel fan-out band.
  topic input -> Stage 1 Decomposer -> [asyncio.gather band: Search -> Fetch -> Synthesize]
  -> Stage 5 Report Builder -> SQLite store -> CLI / FastAPI / Streamlit consumers.
"""
import sys

sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, arrow, evidence_box, title_block, write,
    TITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    DECISION_FILL, DECISION_STROKE, AI_FILL, AI_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'


def build():
    g._seed[0] = 2200000
    els = []
    els += title_block(60, 1080, "Deep Research Report Agent — Topic In, Cited Report Out",
                       "Decompose -> parallel search/fetch/synthesize per sub-question -> report builder -> SQLite -> CLI / API / UI")

    # ── Row 1: input, decomposer, depth configs ──
    els += evidence_box(40, 110, 320, 100, [
        "$ python -m src.cli research \\",
        "    --topic 'AI agents in enterprise' \\",
        "    --depth analyst_report",
    ], line_color=EVIDENCE_AMBER, title="Input: topic + depth")

    els += rect(420, 110, 240, 100,
                "Stage 1 — Decomposer\nClaude Opus 4.8 + thinking\ntopic -> N sub-questions\n(JSON: question + context)",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(360, 160, 420, 160)

    els += evidence_box(740, 110, 400, 100, [
        "overview         5q x 2src   2k-5k words",
        "analyst_report   7q x 3src   8k-15k words",
        "due_diligence   10q x 5src  20k-40k +risk",
        "academic_survey 10q x 5src  40k-80k +method",
    ], line_color=EVIDENCE_GREEN, title="DepthConfig (src/models/config.py)")
    els += arrow(740, 160, 660, 160, stroke=BODY, dashed=True)

    # ── Row 2: parallel band ──
    els += rect(40, 280, 1100, 160, "", fill="#f8fafc", stroke=PRIMARY_STROKE, dashed=True)
    els.append(text(60, 292, 620, 16,
                    "asyncio.gather() — all N sub-questions processed in parallel",
                    size=12, color=TITLE, bold=True, align="left"))
    els += arrow(540, 210, 540, 280, label="N sub-questions")

    els += rect(80, 330, 280, 85,
                "Stage 2 — Searcher\nDuckDuckGo via asyncio.to_thread\ntop K sources per question",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(440, 330, 280, 85,
                "Stage 3 — Fetcher\nhttpx (3 retries) -> Playwright\nBeautifulSoup + markdownify",
                fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=10)
    els += rect(800, 330, 280, 85,
                "Stage 4 — Synthesizer\nClaude Opus 4.8\nper-question finding + [N] cites",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(360, 372, 440, 372)
    els += arrow(720, 372, 800, 372)

    # ── Row 3: evidence + report builder ──
    els += evidence_box(40, 480, 340, 190, [
        "Decomposed into 7 sub-questions",
        "[1] Searching: enterprise use cases...",
        "[1] Found 3 sources",
        "[1] Fetching content...",
        "[1] Synthesizing...",
        "[1] Synthesis complete",
        "Report generated: ~9,400 words",
        "Saved: output/report_AI_agents_...md",
    ], line_color=EVIDENCE_GREEN, title="CLI progress (stderr)")

    els += rect(440, 500, 360, 90,
                "Stage 5 — Report Builder\nClaude Opus 4.8\nexec summary · ToC · cited sections\nconclusion · bibliography",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(620, 440, 620, 500, label="N Synthesis objects")

    # ── Row 4: store + consumers ──
    els += rect(480, 640, 280, 60,
                "SQLite (aiosqlite)\nsessions · sources · reports",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(620, 590, 620, 640)

    els += rect(110, 750, 280, 60,
                "CLI\npython -m src.cli research",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += rect(470, 750, 300, 60,
                "FastAPI\nPOST /research/start · GET .../report",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(850, 750, 280, 60,
                "Streamlit UI\nstreamlit run src/ui/app.py",
                fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(545, 700, 280, 750)
    els += arrow(620, 700, 620, 750)
    els += arrow(695, 700, 960, 750)

    return els


write('deep-research-report-agent', build())
