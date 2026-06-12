#!/usr/bin/env python3
"""Architecture diagram for the Fine-tune vs Prompt Engineering Decision Tool.

Pattern: input -> data layer -> 4 parallel experiments -> shared metrics ->
weighted decision matrix -> constraint diamond -> winner / gap explanation,
with SQLite/FastAPI/Streamlit result surfaces and a real-run evidence box.
"""
import sys

sys.path.insert(0, '/home/azureuser/blogsandDesciptions/Repo-Blogs')

import gen_3_new_diagrams as g
from gen_3_new_diagrams import (
    text, rect, ellipse, diamond, arrow, evidence_box, title_block, write,
    TITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE,
    EVIDENCE_GREEN, EVIDENCE_AMBER,
)

g.OUT = '/home/azureuser/blogsandDesciptions/Repo-Blogs/public/images/diagrams'


def build():
    g._seed[0] = 2300000
    els = []
    els += title_block(
        60, 1100,
        "Fine-tune vs Prompt Engineering — Empirical Decision Tool",
        "Four experiments on your data -> F1 / cost / latency -> weighted decision matrix -> constraint-checked winner",
    )

    # --- Row A: input + data layer + LLM backend ---
    els += ellipse(40, 100, 260, 64,
                   "Input\n--task · --data CSV/JSONL\n--target-f1 · --budget $N",
                   fill=START_FILL, stroke=START_STROKE, label_size=10)

    els += rect(340, 100, 360, 64,
                "Data Layer — loader.py · sampler.py\nparse + validate · embedding diversity\n(all-MiniLM-L6-v2)",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(300, 132, 340, 132)

    els += rect(880, 92, 280, 60,
                "LLM backend — OpenRouter\nanthropic/claude-opus-4.8\npowers experiments 1-3 + judge",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)

    # --- Row B: four experiments ---
    experiments = [
        ("1. Zero-Shot\nraw task -> Claude\nbaseline", TERTIARY_FILL, PRIMARY_STROKE),
        ("2. Few-Shot\n8 diverse examples\nmax-min embedding sampling", AI_FILL, AI_STROKE),
        ("3. Prompt Optimizer\n3 rounds: eval -> diagnose\n-> regenerate (70/30 split)", DECISION_FILL, DECISION_STROKE),
        ("4. LoRA Fine-tune\nphi-2 · PEFT r=8 alpha=16\nCPU · self-hosted inference", START_FILL, START_STROKE),
    ]
    exp_x = [40, 330, 620, 910]
    starts = [(400, 164), (470, 164), (560, 164), (660, 164)]
    for (label, fill, stroke), x, (sx, sy) in zip(experiments, exp_x, starts):
        els += rect(x, 230, 250, 84, label, fill=fill, stroke=stroke, label_size=10)
        els += arrow(sx, sy, x + 125, 230)

    # --- Row C: shared metrics ---
    els += rect(240, 370, 720, 60,
                "evaluation/metrics.py — shared base.py (timeout 120s · token accounting)\nF1 · accuracy · BLEU · latency per call · cost USD",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    metric_targets = [320, 470, 730, 880]
    for x, tx in zip(exp_x, metric_targets):
        els += arrow(x + 125, 314, tx, 370)

    # --- Result surfaces stack (right) ---
    els.append(text(1000, 356, 170, 14, "result surfaces", size=10, color=BODY, align="left"))
    els += rect(1000, 380, 170, 50, "SQLite\nexperiments.db", fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += rect(1000, 450, 170, 50, "FastAPI\n/experiment/*", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += rect(1000, 520, 170, 50, "Streamlit UI\nsrc/ui/app.py", fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(960, 398, 1000, 402)
    els += arrow(1085, 430, 1085, 450)
    els += arrow(1085, 500, 1085, 520)

    # --- Row D: decision matrix ---
    els += rect(290, 470, 620, 70,
                "Decision Matrix — evaluation/decision.py\nmin-max normalize -> F1 40% · cost 25% · latency 15% · complexity 20%\nverdicts: RECOMMENDED / Strong alternative / Viable / Not recommended",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(600, 430, 600, 470)

    # --- Row E: constraint diamond + outcomes ---
    els += diamond(470, 580, 260, 90, "meets --target-f1\n+ --budget?", label_size=11)
    els += arrow(600, 540, 600, 580)

    els += rect(790, 596, 330, 64,
                "Winner: RECOMMENDED\nranked verdicts + weighted rationale",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(730, 625, 790, 626, label="yes")

    els += rect(70, 596, 310, 64,
                "no approach qualifies ->\nbest score + gap explanation",
                fill=WARN_FILL, stroke=WARN_STROKE, label_size=10)
    els += arrow(470, 625, 380, 626, label="no")

    # --- Evidence: real run output ---
    els += evidence_box(60, 706, 1080, 132, [
        "Approach            F1       Acc      Cost       Latency      Verdict",
        "Zero-Shot           0.442    0.480    $0.4773    2018ms       RECOMMENDED",
        "Few-Shot            0.225    0.206    $0.7773    1965ms       Not recommended",
        "Optimized Prompt    0.000    0.000    $0.8132    2094ms       Not recommended",
        "",
        "Winner: Zero-Shot — 32 free-text labels too fragmented for 3 refinement rounds",
    ], line_color=EVIDENCE_GREEN,
       title="$ python -m src.cli run --task 'Classify sentiment' --data sample_data/sentiment_sample.csv --budget 10")
    els += arrow(600, 670, 600, 706)

    return els


write('finetune-vs-prompt-engineering', build())
