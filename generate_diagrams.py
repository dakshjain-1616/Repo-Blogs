"""Generate architecture diagram PNGs for the 17 new blog posts."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

OUT_DIR = "/root/blogs/public/images/diagrams"

# ── colour palette ───────────────────────────────────────────────────────────
BLUE   = "#1e40af"
LBLUE  = "#dbeafe"
SBLU   = "#3b82f6"
GREEN  = "#065f46"
LGRN   = "#d1fae5"
RED    = "#991b1b"
LRED   = "#fee2e2"
PURP   = "#6d28d9"
LPURP  = "#ede9fe"
AMBE   = "#92400e"
LAMB   = "#fef3c7"
GREY   = "#475569"
LGREY  = "#f1f5f9"
TEAL   = "#0f766e"
LTEAL  = "#ccfbf1"
TITLE_C = BLUE
SUB_C   = "#64748b"

def fig(w=18.2, h=9.8, dpi=400):
    f, ax = plt.subplots(figsize=(w, h), dpi=dpi)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    f.patch.set_facecolor('white')
    return f, ax

def title_row(ax, title, subtitle, w=18.2, h=9.8):
    ax.text(w/2, h-0.35, title, ha='center', va='top', fontsize=13,
            color=TITLE_C, fontfamily='monospace', fontweight='bold')
    ax.text(w/2, h-0.72, subtitle, ha='center', va='top', fontsize=7,
            color=SUB_C, fontfamily='monospace')

def box(ax, x, y, w, h, label, color=LBLUE, edge=SBLU, fontsize=8, center=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                 facecolor=color, edgecolor=edge, linewidth=1.5))
    tx = x + w/2 if center else x + 0.12
    ty = y + h/2
    ha = 'center' if center else 'left'
    ax.text(tx, ty, label, ha=ha, va='center', fontsize=fontsize,
            color='#1e293b', fontfamily='monospace', wrap=True)

def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def label(ax, x, y, text, fontsize=7, color=SUB_C, ha='left'):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fontsize,
            color=color, fontfamily='monospace')

def save(fig, name):
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, bbox_inches='tight', facecolor='white', dpi=400)
    plt.close(fig)
    print(f"  saved {name}.png")

# ─────────────────────────────────────────────────────────────────────────────
# 1. loop-anti-pattern-linter
# ─────────────────────────────────────────────────────────────────────────────
def d_loop_linter():
    f, ax = fig()
    W, H = 18.2, 9.8
    title_row(ax, "Loop Anti-Pattern Linter · AST Detection · Slowdown Ranking · LLM Explain",
              "5 NodeVisitor detectors · estimated slowdown % · --min-slowdown filter · --explain via OpenRouter")
    # input
    box(ax, 0.4, 7.0, 2.2, 0.9, "Python file /\ndirectory", LAMB, AMBE)
    arrow(ax, 2.6, 7.45, 3.2, 7.45)
    box(ax, 3.2, 7.0, 2.2, 0.9, "AST Parser\n(ast.parse)", LBLUE, SBLU)
    arrow(ax, 5.4, 7.45, 6.0, 7.45)

    # detectors
    label(ax, 6.0, 8.1, "5 NodeVisitor Detectors", fontsize=8, color=RED)
    dx = [6.0, 8.0, 10.0, 12.0, 14.0]
    labels = ["Nested loops\nover same iter\n≥50% slowdown",
              "String concat\nin loop\n≥40% slowdown",
              "list.append\nin loop\n≥30% slowdown",
              "Membership test\n`x in list`\n≥20% slowdown",
              "len() inside\nloop guard\n≥10% slowdown"]
    for i, (x, lbl) in enumerate(zip(dx, labels)):
        box(ax, x, 6.3, 1.8, 1.0, lbl, LRED, RED, fontsize=7)
        arrow(ax, x + 0.9, 6.3, x + 0.9, 5.6)

    # ranker
    box(ax, 7.5, 4.8, 4.0, 0.7, "Ranking Engine  (sort by estimated slowdown ↓)", LGRN, GREEN)
    [arrow(ax, dx[i]+0.9, 5.6, dx[i]+0.9, 5.5) for i in range(5)]
    for i in range(5):
        arrow(ax, dx[i]+0.9, 5.5, 9.5, 5.5)
    arrow(ax, 9.5, 5.5, 9.5, 5.5)

    # outputs
    box(ax, 3.0, 3.2, 3.5, 0.8, "Rich Table output\n(terminal)", LPURP, PURP, fontsize=8)
    box(ax, 7.2, 3.2, 3.5, 0.8, "JSON output\n(--json for CI/CD)", LBLUE, SBLU, fontsize=8)
    box(ax, 11.2, 3.2, 3.5, 0.8, "LLM Explain\n(--explain via OpenRouter)", LAMB, AMBE, fontsize=8)
    arrow(ax, 8.0, 4.8, 4.75, 4.0)
    arrow(ax, 9.0, 4.8, 8.95, 4.0)
    arrow(ax, 10.0, 4.8, 12.95, 4.0)

    # filter note
    box(ax, 0.4, 3.2, 2.4, 0.8, "--min-slowdown\nfilter threshold", LGREY, GREY, fontsize=8)
    arrow(ax, 2.8, 3.6, 3.0, 3.6)

    label(ax, 0.4, 2.2, "CLI:  loop-linter src/  ·  loop-linter src/ --min-slowdown 30  ·  loop-linter src/ --explain --model anthropic/claude-opus-4.7", fontsize=7, color=GREY)
    save(f, "loop-anti-pattern-linter")

# ─────────────────────────────────────────────────────────────────────────────
# 2. rag-retrieval-semantic-deduplication
# ─────────────────────────────────────────────────────────────────────────────
def d_rag_dedup():
    f, ax = fig()
    title_row(ax, "RAG with Retrieval-Time Semantic Deduplication · 30–50% Token Reduction",
              "ChromaDB retrieval → local CPU embedding → pairwise cosine similarity → greedy filter → LLM generation")
    steps = [
        (0.4,  "① Documents\n(.txt / .md)", LAMB,  AMBE),
        (3.0,  "② ChromaDB\nTop-K retrieval", LBLUE, SBLU),
        (5.6,  "③ Local Embedding\nall-MiniLM-L6-v2\n(CPU, no GPU)", LGRN,  GREEN),
        (8.2,  "④ Pairwise\nCosine Similarity\nmatrix", LPURP, PURP),
        (10.8, "⑤ Greedy Filter\nthreshold 0.70–0.99\nremove near-dupes", LRED,  RED),
        (13.4, "⑥ LLM Generation\n(diverse context\nfewer tokens)", LTEAL, TEAL),
    ]
    for x, lbl, fc, ec in steps:
        box(ax, x, 6.0, 2.4, 1.2, lbl, fc, ec, fontsize=8)
    for i in range(len(steps)-1):
        arrow(ax, steps[i][0]+2.4, 6.6, steps[i+1][0], 6.6)

    # metrics
    box(ax, 3.5, 3.8, 4.5, 1.0, "Metrics logged per query\n• deduplication ratio\n• tokens before / after\n• retrieval latency", LGREY, GREY, fontsize=8)
    arrow(ax, 10.8+1.2, 6.0, 10.8+1.2, 4.8)

    # threshold knob
    box(ax, 9.0, 2.4, 3.5, 1.0, "Similarity Threshold\n0.70 aggressive ← → 0.99 conservative\nconfigure per corpus type", LAMB, AMBE, fontsize=8)
    arrow(ax, 10.8+1.2, 6.0, 10.75, 3.4)

    # token saving callout
    ax.add_patch(mpatches.FancyBboxPatch((14.5, 5.5), 3.2, 1.6,
                  boxstyle="round,pad=0.1", fc=LGRN, ec=GREEN, lw=2))
    ax.text(16.1, 6.3, "30–50%\ntoken reduction\nno quality loss", ha='center', va='center',
            fontsize=10, color=GREEN, fontweight='bold', fontfamily='monospace')

    label(ax, 0.4, 1.8, "python ingest.py --docs ./documents/    ·    python query.py --question \"What is X?\" --threshold 0.85", fontsize=7, color=GREY)
    save(f, "rag-retrieval-semantic-deduplication")

# ─────────────────────────────────────────────────────────────────────────────
# 3. low-latency-model-router
# ─────────────────────────────────────────────────────────────────────────────
def d_model_router():
    f, ax = fig()
    title_row(ax, "Low-Latency Model Router · <0.1ms Routing · 4 Priority Modes · Redis Cache · Failover",
              "Score = w_latency×(1−norm_lat) + w_cost×(1−norm_cost) + w_quality×quality_score")
    # request
    box(ax, 0.4, 6.5, 2.0, 1.0, "Incoming\nRequest", LBLUE, SBLU)
    arrow(ax, 2.4, 7.0, 3.2, 7.0)

    # priority modes
    label(ax, 3.2, 8.1, "Priority Mode", fontsize=8, color=BLUE)
    modes = [("speed\n0.70/0.20/0.10", LGRN, GREEN),
             ("cost\n0.20/0.70/0.10", LAMB, AMBE),
             ("quality\n0.10/0.20/0.70", LPURP, PURP),
             ("balanced\n0.33/0.33/0.33", LBLUE, SBLU)]
    for i, (lbl, fc, ec) in enumerate(modes):
        box(ax, 3.2 + i*2.3, 6.5, 2.0, 1.0, lbl, fc, ec, fontsize=7)
    for i in range(4):
        arrow(ax, 3.2 + i*2.3 + 1.0, 6.5, 12.0, 5.8)

    # scoring engine
    box(ax, 10.2, 4.8, 3.8, 0.9, "Scoring Engine\n<0.1ms decision overhead", LRED, RED, fontsize=9)
    arrow(ax, 14.0, 5.25, 15.0, 5.25)

    # model catalogue
    box(ax, 15.0, 4.8, 2.8, 0.9, "OpenRouter\nModel Catalogue", LTEAL, TEAL, fontsize=8)
    arrow(ax, 16.4, 4.8, 16.4, 3.8)
    box(ax, 15.0, 3.0, 2.8, 0.7, "Selected Model\n+ Failover Candidate", LGRN, GREEN, fontsize=8)

    # redis cache
    box(ax, 10.2, 3.0, 3.8, 0.7, "Redis Cache\n(in-memory fallback)", LAMB, AMBE, fontsize=8)
    arrow(ax, 12.1, 4.8, 12.1, 3.7)
    arrow(ax, 14.0, 3.35, 15.0, 3.35)

    # api
    box(ax, 3.2, 3.0, 6.0, 1.8,
        "FastAPI REST Server\n/route · /complete · /models\n/metrics · /health\nSwagger docs at /docs", LGREY, GREY, fontsize=8)
    arrow(ax, 12.1, 3.0, 9.2, 3.9)

    label(ax, 0.4, 1.9, "router explore --mode quality  ·  router benchmark --requests 100  ·  POST /complete  {priority: 'speed'}", fontsize=7, color=GREY)
    save(f, "low-latency-model-router")

# ─────────────────────────────────────────────────────────────────────────────
# 4. local-model-behavior-prober
# ─────────────────────────────────────────────────────────────────────────────
def d_behavior_prober():
    f, ax = fig()
    title_row(ax, "Local Model Behavior Prober · YAML Probe Suites · Baseline Capture · Regression Diffs",
              "Ollama backend · property-based scoring (not exact outputs) · pip-installable · CLI + Python library")
    # YAML suite
    box(ax, 0.4, 6.5, 3.0, 2.4,
        "YAML Probe Suite\n─────────────────\n• instruction_following\n• factual_accuracy\n• refusal_calibration\n• format_compliance\n• edge_case_handling",
        LAMB, AMBE, fontsize=8)
    arrow(ax, 3.4, 7.7, 4.2, 7.7)
    # probe runner
    box(ax, 4.2, 6.5, 3.0, 2.4, "Probe Runner\n─────────────────\nfor each probe:\n  send to Ollama\n  receive response\n  apply scorer", LBLUE, SBLU, fontsize=8)
    arrow(ax, 7.2, 7.7, 8.0, 7.7)
    # property scorer
    box(ax, 8.0, 6.5, 3.0, 2.4, "Property Scorer\n─────────────────\ncheck behavioral\nproperties:\n(not exact strings)", LGRN, GREEN, fontsize=8)
    arrow(ax, 11.0, 7.7, 11.8, 7.7)
    # baseline
    box(ax, 11.8, 6.5, 2.5, 1.1, "Baseline\nCapture\n(first run)", LPURP, PURP, fontsize=8)
    box(ax, 11.8, 7.8, 2.5, 1.1, "Regression\nDiff Report\n(subsequent)", LRED, RED, fontsize=8)

    # diff output
    box(ax, 5.0, 3.5, 6.0, 2.0,
        "Diff Output\n─────────────────────────────\n  REGRESSED: format_compliance (q4-run)\n  IMPROVED:  factual_accuracy (+3%)\n  STABLE:    instruction_following (9/10)",
        LGREY, GREY, fontsize=8)
    arrow(ax, 11.8+1.25, 6.5, 8.0, 5.5)

    # interfaces
    box(ax, 0.4, 3.2, 2.2, 0.8, "CLI\nprober baseline\nprober run --compare", LBLUE, SBLU, fontsize=7)
    box(ax, 2.8, 3.2, 2.2, 0.8, "Python Library\nfrom local_model_prober\nimport Prober", LGRN, GREEN, fontsize=7)

    label(ax, 0.4, 2.1, "prober baseline --model llama3.2:3b  ·  prober run --model llama3.2:3b-q4 --compare baseline  ·  prober diff baseline.json q4.json", fontsize=7, color=GREY)
    save(f, "local-model-behavior-prober")

# ─────────────────────────────────────────────────────────────────────────────
# 5. token-budget-negotiator
# ─────────────────────────────────────────────────────────────────────────────
def d_token_negotiator():
    f, ax = fig()
    title_row(ax, "Token Budget Negotiator · Greedy Ablation · Quality Gating · CLI / Library / MCP Server",
              "Split prompt → baseline score → remove sections iteratively → restore if quality drops → stop at target savings")
    # prompt sections
    box(ax, 0.4, 7.2, 2.8, 2.0,
        "Prompt Sections\n──────────────\n[system_prompt]\n[few_shot_examples]\n[context]\n[constraints]\n[task]",
        LAMB, AMBE, fontsize=8)
    arrow(ax, 3.2, 8.2, 4.0, 8.2)
    # baseline
    box(ax, 4.0, 7.7, 2.5, 1.0, "① Baseline\nScore\n(full prompt)", LGRN, GREEN, fontsize=8)
    arrow(ax, 6.5, 8.2, 7.3, 8.2)
    # loop
    box(ax, 7.3, 7.2, 4.0, 2.0,
        "② Greedy Ablation Loop\n──────────────────────\nfor each section:\n  remove → rescore\n  quality ≥ threshold?\n    keep removed\n  else restore",
        LBLUE, SBLU, fontsize=8)
    arrow(ax, 11.3, 8.2, 12.1, 8.2)
    # stop condition
    box(ax, 12.1, 7.7, 2.5, 1.0, "③ Stop\nWhen savings\nreach target", LRED, RED, fontsize=8)
    arrow(ax, 14.6, 8.2, 15.4, 8.2)
    box(ax, 15.4, 7.7, 2.4, 1.0, "Compressed\nPrompt +\nAblation Log", LGRN, GREEN, fontsize=8)

    # scoring backends
    label(ax, 2.0, 6.5, "Scoring Backends", fontsize=8, color=BLUE)
    box(ax, 0.4, 5.5, 2.4, 0.8, "Local Ollama\n(free, offline)", LGRN, GREEN, fontsize=8)
    box(ax, 3.0, 5.5, 2.4, 0.8, "OpenRouter\n(cloud models)", LBLUE, SBLU, fontsize=8)
    box(ax, 5.6, 5.5, 2.4, 0.8, "Built-in Rubrics\n(QA, coding, summary)", LAMB, AMBE, fontsize=8)
    for x in [1.6, 4.2, 6.8]:
        arrow(ax, x, 7.2, x, 6.3)

    # interfaces
    label(ax, 0.4, 4.5, "Interfaces", fontsize=8, color=BLUE)
    box(ax, 0.4, 3.5, 2.8, 0.8, "CLI\nnegotiate --prompt f.txt\n--target-savings 30%", LBLUE, SBLU, fontsize=7)
    box(ax, 3.4, 3.5, 2.8, 0.8, "Python Library\nNegotiator(...)\n.negotiate(prompt)", LGRN, GREEN, fontsize=7)
    box(ax, 6.4, 3.5, 2.8, 0.8, "MCP Server\nnegotiate_prompt tool\nfor Claude Code", LPURP, PURP, fontsize=7)

    label(ax, 0.4, 2.4, "negotiate --prompt my_prompt.txt --target-savings 30% --quality-threshold 0.85 --backend ollama", fontsize=7, color=GREY)
    save(f, "token-budget-negotiator")

# ─────────────────────────────────────────────────────────────────────────────
# 6. llm-behavior-diff-detector
# ─────────────────────────────────────────────────────────────────────────────
def d_behavior_diff():
    f, ax = fig()
    title_row(ax, "LLM Behavior Diff · Detect Output Changes Across Model Updates",
              "YAML prompt suite → Model A + Model B → embedding similarity → none/minor/moderate/major → HTML report")
    # input
    box(ax, 0.4, 6.8, 2.8, 1.2, "YAML Prompt Suite\n(categorized prompts\nfor your use case)", LAMB, AMBE, fontsize=8)
    arrow(ax, 3.2, 7.4, 4.0, 7.4)

    # two model paths
    box(ax, 4.0, 7.8, 2.8, 0.8, "Model A\n(e.g. gpt-4o)", LGRN, GREEN, fontsize=8)
    box(ax, 4.0, 6.8, 2.8, 0.8, "Model B\n(e.g. gpt-4o-mini)", LRED, RED, fontsize=8)
    arrow(ax, 6.8, 8.2, 8.0, 8.2)
    arrow(ax, 6.8, 7.2, 8.0, 7.2)

    # scoring
    box(ax, 8.0, 7.0, 3.5, 1.8,
        "Scoring\n─────────────────\n① Embedding cosine sim\n   (all-MiniLM-L6-v2)\n② Jaccard fallback\n③ LLM-as-judge (optional)",
        LBLUE, SBLU, fontsize=8)
    arrow(ax, 11.5, 7.9, 12.3, 7.9)

    # classifier
    box(ax, 12.3, 7.0, 3.0, 1.8,
        "Change Classifier\n─────────────────\n• none  (≥0.95)\n• minor (0.85-0.95)\n• moderate (0.70-0.85)\n• major (<0.70)",
        LRED, RED, fontsize=8)
    arrow(ax, 15.3, 7.9, 16.1, 7.9)
    box(ax, 16.1, 7.4, 1.8, 1.0, "HTML\nReport +\nStats", LGRN, GREEN, fontsize=8)

    # summary stats
    box(ax, 5.0, 4.5, 7.5, 1.8,
        "Summary Statistics\n────────────────────────────────────────\ntotal prompts: 42  ·  changes detected: 7  ·  change rate: 16.7%\navg similarity: 0.88  ·  major changes: 2  ·  minor: 5",
        LGREY, GREY, fontsize=8)
    arrow(ax, 13.8, 7.0, 8.75, 6.3)

    # interfaces
    box(ax, 0.4, 3.5, 2.8, 0.8, "CLI\nllm-diff run\n--suite prompts.yaml", LBLUE, SBLU, fontsize=7)
    box(ax, 3.4, 3.5, 2.8, 0.8, "Python API\nBehaviorDiff(...)\n.compare(A, B, suite)", LGRN, GREEN, fontsize=7)
    box(ax, 6.4, 3.5, 2.8, 0.8, "MCP Server\nmodel comparison\ntool for agents", LPURP, PURP, fontsize=7)
    box(ax, 9.4, 3.5, 2.8, 0.8, "Stub Provider\noffline testing\nno API keys", LAMB, AMBE, fontsize=7)

    label(ax, 0.4, 2.4, "llm-diff run --suite prompts.yaml --model-a gpt-4o --model-b gpt-4o-mini --provider openrouter", fontsize=7, color=GREY)
    save(f, "llm-behavior-diff-detector")

# ─────────────────────────────────────────────────────────────────────────────
# 7. synthetic-data-flywheel
# ─────────────────────────────────────────────────────────────────────────────
def d_flywheel():
    f, ax = fig()
    title_row(ax, "Synthetic Data Flywheel · 8-Stage Pipeline · LLM Judge · Recycling Loop · A2A Agent",
              "seed prompts → generate → validate → judge → calibrate → label → compare → export → recycle failures")
    stages = [
        (0.4,  7.0, "① Seed\nPrompts", LAMB, AMBE),
        (2.4,  7.0, "② Generate\n(OpenRouter)", LBLUE, SBLU),
        (4.4,  7.0, "③ Validate\nschema/PII/dedup", LGRN, GREEN),
        (6.4,  7.0, "④ Judge\n(LLM score)", LPURP, PURP),
        (8.4,  7.0, "⑤ Calibrate\nvs human labels", LAMB, AMBE),
        (10.4, 7.0, "⑥ Label\ninteract/bulk/auto", LRED, RED),
        (12.4, 7.0, "⑦ Compare\n& stats", LBLUE, SBLU),
        (14.4, 7.0, "⑧ Export\ntraining data", LGRN, GREEN),
    ]
    for x, y, lbl, fc, ec in stages:
        box(ax, x, y, 1.8, 1.2, lbl, fc, ec, fontsize=7)
    for i in range(len(stages)-1):
        arrow(ax, stages[i][0]+1.8, stages[i][1]+0.6, stages[i+1][0], stages[i+1][1]+0.6)

    # recycling loop
    ax.annotate('', xy=(2.4+0.9, 7.0), xytext=(6.4+0.9, 5.2),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2, connectionstyle='arc3,rad=0.1'))
    label(ax, 4.0, 5.8, "Failures recycled\nas seeds (flywheel)", fontsize=8, color=RED, ha='center')

    # scoring backends
    box(ax, 4.0, 3.8, 3.5, 1.5,
        "Judge Backends\n──────────────\n• Ollama (local, free)\n• OpenRouter (cloud)\n• Anthropic\n  (with caching)",
        LPURP, PURP, fontsize=8)
    arrow(ax, 7.3+0.9, 7.0+0.6, 5.75, 5.3)

    # A2A agent
    box(ax, 11.0, 3.8, 3.5, 1.5,
        "A2A Protocol Agent\n──────────────────\nFastAPI endpoint\ndispatch jobs\npoll status\nretrieve exports",
        LBLUE, SBLU, fontsize=8)

    label(ax, 0.4, 2.4, "python flywheel.py --rounds 3    ·    python judge.py --backend ollama    ·    python export.py --output training.jsonl", fontsize=7, color=GREY)
    save(f, "synthetic-data-flywheel")

# ─────────────────────────────────────────────────────────────────────────────
# 8. llm-powered-git-bisect
# ─────────────────────────────────────────────────────────────────────────────
def d_git_bisect():
    f, ax = fig()
    title_row(ax, "LLM-Powered Git Bisect · Automated Binary Search · Local Ollama Explanation · 4 Interfaces",
              "validate SHAs → binary search → checkout + run test → first bad commit → diff + output → Ollama → JSON explanation")
    # inputs
    box(ax, 0.4, 7.2, 2.2, 1.0, "good SHA\nbad SHA\ntest command", LAMB, AMBE, fontsize=8)
    arrow(ax, 2.6, 7.7, 3.4, 7.7)

    # validation
    box(ax, 3.4, 7.2, 2.5, 1.0, "Validate\ngood is ancestor\nof bad", LBLUE, SBLU, fontsize=8)
    arrow(ax, 5.9, 7.7, 6.7, 7.7)

    # binary search loop
    box(ax, 6.7, 6.5, 4.0, 2.5,
        "Binary Search Loop\n───────────────────\nlist commits between SHAs\ncheckout midpoint\nrun test command\n  ✓ exit 0 → GOOD\n  ✗ exit 1 → BAD\nrepeat until isolated",
        LRED, RED, fontsize=8)
    arrow(ax, 10.7, 7.7, 11.5, 7.7)

    # first bad commit
    box(ax, 11.5, 7.2, 2.5, 1.0, "First Bad\nCommit\nisolated", LGRN, GREEN, fontsize=8)
    arrow(ax, 14.0, 7.7, 14.8, 7.7)

    # prompt construction
    box(ax, 14.8, 6.5, 3.0, 2.5,
        "Prompt Construction\n───────────────────\n• commit message\n• file diff (git diff)\n• test stdout/stderr\n→ structured prompt\n  for Ollama",
        LPURP, PURP, fontsize=8)

    # ollama
    box(ax, 8.0, 4.0, 3.5, 1.5, "Local Ollama\nModel\n(all inference local\nno code leaves machine)", LGRN, GREEN, fontsize=9)
    arrow(ax, 16.3, 6.5, 16.3, 5.0)
    arrow(ax, 16.3, 5.0, 11.5, 5.0)
    arrow(ax, 11.5, 5.0, 11.5, 5.5)

    # output
    box(ax, 4.0, 4.0, 3.5, 1.5,
        "JSON Explanation\n────────────────\n• explanation\n• severity (high)\n• confidence 0.92\n• suggested_fix",
        LAMB, AMBE, fontsize=8)
    arrow(ax, 8.0, 4.75, 7.5, 4.75)

    # interfaces
    ifs = [("CLI", "git-bisect-ai find\n--good --bad --test", LBLUE, SBLU),
           ("Git subcommand", "git bisect-ai\n--good HEAD~20", LGRN, GREEN),
           ("MCP Server", "find_breaking_commit\nexplain_commit", LPURP, PURP),
           ("Python Library", "BisectAI().find(\n  good, bad, test)", LAMB, AMBE)]
    for i, (title, lbl, fc, ec) in enumerate(ifs):
        box(ax, 0.4 + i*3.5, 2.0, 3.2, 1.2, f"{title}\n─────────\n{lbl}", fc, ec, fontsize=7)

    label(ax, 0.4, 1.2, "git-bisect-ai find --good HEAD~30 --bad HEAD --test 'pytest tests/'  (runs fully locally via Ollama)", fontsize=7, color=GREY)
    save(f, "llm-powered-git-bisect")

# ─────────────────────────────────────────────────────────────────────────────
# 9. claude-opus-vs-gpt55-vs-deepseek-v4-benchmark
# ─────────────────────────────────────────────────────────────────────────────
def d_three_model_bench():
    f, ax = fig()
    title_row(ax, "Claude Opus 4.7 vs GPT-5.5 vs DeepSeek V4 Pro · 13-Task Reasoning Benchmark",
              "6 domains · competition math · graduate science · multistep logic · coding · expert analysis · abstract reasoning")
    # task suite
    box(ax, 0.3, 6.0, 3.0, 3.5,
        "13-Task Suite\n─────────────────\n• Competition Math (2)\n• Graduate Science (3)\n  (GPQA-style)\n• Multistep Logic (2)\n• Advanced Coding (2)\n• Expert Analysis (2)\n• Abstract Reasoning (1)\n  (ARC-AGI style)",
        LAMB, AMBE, fontsize=8)
    for y in [7.0, 7.5, 8.0]:
        arrow(ax, 3.3, y, 4.1, y)

    # three models
    models = [
        (4.1, 7.7, "Claude\nOpus 4.7\n(Anthropic)", LBLUE, SBLU),
        (4.1, 6.5, "GPT-5.5\n(OpenAI)", LGRN, GREEN),
        (4.1, 5.3, "DeepSeek\nV4 Pro\n(DeepSeek)", LPURP, PURP),
    ]
    for x, y, lbl, fc, ec in models:
        box(ax, x, y, 2.5, 1.0, lbl, fc, ec, fontsize=8)
        arrow(ax, x+2.5, y+0.5, x+3.3, y+0.5)

    # judge
    box(ax, 9.6, 6.0, 2.5, 2.5,
        "Independent\nJudge\n─────────────\nGPT-5.5\n(anonymized\nA/B/C labels)\n\n{scores,\nwinner,\nreasoning}",
        LRED, RED, fontsize=8)
    arrow(ax, 12.1, 7.25, 12.9, 7.25)

    # results
    box(ax, 12.9, 5.5, 5.0, 3.5,
        "Results\n─────────────────────────────\n🥇 Claude Opus 4.7  →  9.23 / 10\n   most efficient · zero errors\n   ~2,800 tokens avg\n\n🥈 GPT-5.5          →  9.15 / 10\n   leads abstract reasoning\n\n🥉 DeepSeek V4 Pro  →  7.31 / 10\n   3 / 13 timeouts\n   competitive on science",
        LGRN, GREEN, fontsize=8)

    # key finding
    box(ax, 0.3, 3.5, 12.0, 1.5,
        "Key Findings: Claude dominates multistep logic (9.5 vs GPT 8.0) · GPT leads abstract reasoning · DeepSeek competitive on science but unreliable on long-horizon tasks",
        LGREY, GREY, fontsize=8)

    label(ax, 0.3, 2.4, "python run_benchmark.py  ·  --only math_001  ·  --rejudge-only  ·  --skip-judge  (full run ~45 min, ~$5-10)", fontsize=7, color=GREY)
    save(f, "claude-opus-vs-gpt55-vs-deepseek-v4-benchmark")

# ─────────────────────────────────────────────────────────────────────────────
# 10. a2a-mcp-dual-protocol-reference-agent
# ─────────────────────────────────────────────────────────────────────────────
def d_a2a_mcp():
    f, ax = fig()
    title_row(ax, "A2A + MCP Dual Protocol Reference Agent · DeepSeek V4-Flash · Gradio Dashboard",
              "A2A: inter-agent coordination (horizontal) · MCP: tool access (vertical) · canonical reference implementation")
    # a2a layer
    label(ax, 0.4, 8.8, "A2A LAYER  (horizontal coordination)", fontsize=9, color=BLUE)
    box(ax, 0.4, 7.8, 3.0, 0.9, "GET /.well-known/agent.json\ncapability discovery", LBLUE, SBLU, fontsize=8)
    box(ax, 4.0, 7.8, 3.0, 0.9, "POST /tasks/send\ntask delivery", LBLUE, SBLU, fontsize=8)
    box(ax, 7.6, 7.8, 3.0, 0.9, "GET /tasks/{id}\nstatus polling", LBLUE, SBLU, fontsize=8)

    # agent core
    box(ax, 5.0, 6.0, 5.0, 1.5,
        "Agent Core\n────────────────────\nDeepSeek V4-Flash\nreasoning loop",
        LRED, RED, fontsize=9)
    arrow(ax, 5.5, 7.8, 5.5, 7.5)
    arrow(ax, 7.5, 7.8, 7.5, 7.5)

    # mcp layer
    label(ax, 0.4, 5.5, "MCP LAYER  (vertical tool access)", fontsize=9, color=TEAL)
    mcps = [
        (0.4,  "Web Search MCP\n────────────\nDuckDuckGo\nquery refinement\nresult parsing"),
        (5.0,  "File System MCP\n────────────\nread / write / list\nsearch local files\npersist artifacts"),
        (9.6,  "GitHub MCP\n────────────\nrepo metadata\nfile contents\nissues & PRs"),
    ]
    for x, lbl in mcps:
        box(ax, x, 3.8, 4.2, 1.5, lbl, LTEAL, TEAL, fontsize=8)
        arrow(ax, x+2.1, 6.0, x+2.1, 5.3)

    # gradio dashboard
    box(ax, 11.5, 6.0, 6.3, 2.5,
        "Gradio Dashboard\n─────────────────────────────\n📋 A2A Request Log\n   task · status · requester · timing\n\n🔧 MCP Tool-Call Timeline\n   server · tool · args · result · latency\n\n🧠 Agent Reasoning\n   thinking trace between tool calls",
        LPURP, PURP, fontsize=8)
    arrow(ax, 10.0, 6.75, 11.5, 6.75)

    # mock mode
    box(ax, 11.5, 3.8, 6.3, 1.0, "Mock Mode  (MOCK_MODE=true)\nall external calls → deterministic responses\nlearn protocols without API keys", LGREY, GREY, fontsize=8)

    label(ax, 0.4, 2.8, "python agent.py  ·  MOCK_MODE=true python agent.py  (offline)  ·  uses DeepSeek V4-Flash for cost efficiency", fontsize=7, color=GREY)
    save(f, "a2a-mcp-dual-protocol-reference-agent")

# ─────────────────────────────────────────────────────────────────────────────
# 11. long-horizon-agent-benchmark
# ─────────────────────────────────────────────────────────────────────────────
def d_long_horizon():
    f, ax = fig()
    title_row(ax, "Long-Horizon Agent Benchmark · GLM 5.1 vs Kimi K2.6 vs DeepSeek V4 Pro · 50+ Tool Calls",
              "quality vs tool-call count curves · cost per run · GPT-5.5 independent judge on final answers")
    # task types
    box(ax, 0.3, 7.0, 3.5, 2.5,
        "Task Types\n──────────────────\n• Multi-source research\n  synthesis\n  (10+ sources)\n• Multi-file code\n  planning refactor\n• Conflicting evidence\n  analysis",
        LAMB, AMBE, fontsize=8)
    for y in [7.5, 8.0, 8.5]:
        arrow(ax, 3.8, y, 4.6, y)

    # three agents
    agents = [
        (4.6, 8.3, "Claude\nOpus 4.7\n200K ctx", LBLUE, SBLU, "19 tool calls\n$1.49"),
        (4.6, 7.0, "Kimi K2.6\n256K ctx\nextended think", LGRN, GREEN, "93 tool calls\n$0.92"),
        (4.6, 5.7, "DeepSeek\nV4 Pro\n1M ctx", LPURP, PURP, "43 tool calls\n$0.11"),
    ]
    for x, y, lbl, fc, ec, stats in agents:
        box(ax, x, y, 2.5, 1.0, lbl, fc, ec, fontsize=7)
        box(ax, 7.3, y, 1.8, 1.0, stats, LGREY, GREY, fontsize=7)
        arrow(ax, x+2.5, y+0.5, 7.3, y+0.5)
        arrow(ax, 9.1, y+0.5, 9.9, y+0.5)

    # judge
    box(ax, 9.9, 6.0, 2.5, 2.5,
        "GPT-5.5\nJudge\n────────────\nanonymized\nA/B/C labels\n\nscores:\n• correctness\n• completeness\n• quality",
        LRED, RED, fontsize=8)
    arrow(ax, 12.4, 7.25, 13.2, 7.25)

    # results table
    box(ax, 13.2, 5.5, 4.8, 3.5,
        "Results\n───────────────────────────\nModel     Quality  Tools  Cost\nOpus 4.7   0.90     19    $1.49\nKimi K2.6  0.90     93    $0.92\nDeepSeek   0.85     43    $0.11\n\nOpus = Kimi quality\nat 1/5 the tool calls\n\nDeepSeek: 14× cheaper",
        LGRN, GREEN, fontsize=8)

    label(ax, 0.3, 2.4, "python run_benchmark.py  ·  --max-steps 30  ·  --only task_01  (tracks quality degradation curve vs tool-call count)", fontsize=7, color=GREY)
    save(f, "long-horizon-agent-benchmark")

# ─────────────────────────────────────────────────────────────────────────────
# 12. smolvlm2-edge-vision-agent
# ─────────────────────────────────────────────────────────────────────────────
def d_smolvlm2():
    f, ax = fig()
    title_row(ax, "SmolVLM2 Edge Vision Agent · Offline CPU-Only · Motion-Gated Processing · SQLite + FastAPI",
              "2.2B param model · 16GB RAM · frame-difference gating · no GPU · no internet · no images leave device")
    # inputs
    box(ax, 0.4, 7.5, 2.0, 0.8, "Webcam\n(live feed)", LBLUE, SBLU, fontsize=8)
    box(ax, 0.4, 6.5, 2.0, 0.8, "Image Folder\n(batch mode)", LBLUE, SBLU, fontsize=8)
    box(ax, 0.4, 5.5, 2.0, 0.8, "Mock Mode\n(offline test)", LBLUE, SBLU, fontsize=8)
    for y in [7.9, 6.9, 5.9]:
        arrow(ax, 2.4, y, 3.2, y)

    # frame diff
    box(ax, 3.2, 6.0, 3.0, 2.5,
        "Level 1\nFrame-Diff\nDetector\n─────────────\npixel delta\n< threshold?\n→ DROP frame\n(CPU ~0%)",
        LGRN, GREEN, fontsize=8)

    # diamond decision
    ax.add_patch(mpatches.FancyBboxPatch((7.0, 7.0), 2.0, 1.0,
                  boxstyle="round,pad=0.1", fc=LAMB, ec=AMBE, lw=2))
    ax.text(8.0, 7.5, "Motion\nDetected?", ha='center', va='center', fontsize=8, fontfamily='monospace')
    arrow(ax, 6.2, 7.25, 7.0, 7.5)
    label(ax, 7.2, 6.5, "NO → drop frame", fontsize=7, color=GREY)
    ax.annotate('', xy=(7.0, 6.3), xytext=(8.0, 7.0),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))

    # smolvlm2
    arrow(ax, 9.0, 7.5, 9.8, 7.5)
    box(ax, 9.8, 6.8, 3.5, 1.8,
        "SmolVLM2\n2.2B parameters\n────────────────\n• object description\n• text reading (OCR)\n• scene classification\n• confidence scores\nauto-download first run",
        LPURP, PURP, fontsize=8)
    arrow(ax, 13.3, 7.7, 14.1, 7.7)

    # sqlite
    box(ax, 14.1, 7.0, 3.0, 1.8,
        "SQLite\nObservation Store\n──────────────────\n• timestamp (ms)\n• thumbnail JPEG\n• description text\n• confidence score\n• motion delta",
        LGRN, GREEN, fontsize=8)

    # fastapi
    box(ax, 4.0, 3.5, 6.0, 2.0,
        "FastAPI Dashboard  :8000\n──────────────────────────────────\n• Live feed (MJPEG stream)\n• Searchable observation log\n• /observations · /search · /export\n• /health",
        LBLUE, SBLU, fontsize=8)
    arrow(ax, 15.6, 7.0, 15.6, 6.0)
    arrow(ax, 15.6, 6.0, 10.0, 5.5)

    label(ax, 0.4, 2.4, "python agent.py --source webcam  ·  --source ./images/  ·  --source mock  (model auto-downloads on first run)", fontsize=7, color=GREY)
    save(f, "smolvlm2-edge-vision-agent")

# ─────────────────────────────────────────────────────────────────────────────
# 13. deepseek-v4-context-benchmark
# ─────────────────────────────────────────────────────────────────────────────
def d_deepseek_ctx():
    f, ax = fig()
    title_row(ax, "DeepSeek V4 Context Benchmark · Million-Token Performance · Flash vs Pro vs Llama 4 Scout",
              "NIAH at 10K/100K/500K/900K · multi-hop reasoning · codebase analysis · structured extraction · validated 2026-05-01")
    # models
    models = [
        (0.4, 7.8, "DeepSeek\nV4 Flash\n$0.14/1M tokens", LGRN, GREEN),
        (0.4, 6.5, "DeepSeek\nV4 Pro\n$0.32/1M tokens", LBLUE, SBLU),
        (0.4, 5.2, "Llama 4\nScout\n(low cost)", LPURP, PURP),
    ]
    for x, y, lbl, fc, ec in models:
        box(ax, x, y, 2.5, 1.0, lbl, fc, ec, fontsize=8)
        arrow(ax, 2.9, y+0.5, 3.7, y+0.5)

    # 4 task types
    tasks = [
        (3.7, 8.2, "NIAH\n(Needle in Haystack)\npositions:\n10K / 100K\n500K / 900K", LRED, RED),
        (6.5, 8.2, "Multi-Hop\nReasoning\n3-5 linked\npassages\nchain logic", LAMB, AMBE),
        (9.3, 8.2, "Codebase\nAnalysis\n300K–800K\ntokens\nbug finding", LTEAL, TEAL),
        (12.1, 8.2, "Structured\nExtraction\nfinancial\ndocs / research\npapers", LBLUE, SBLU),
    ]
    for x, y, lbl, fc, ec in tasks:
        box(ax, x, y-1.8, 2.4, 2.2, lbl, fc, ec, fontsize=7)
    for x in [3.7+1.2, 6.5+1.2, 9.3+1.2, 12.1+1.2]:
        arrow(ax, 2.9, 7.25, x, 7.5)

    # accuracy table
    box(ax, 0.4, 3.0, 10.0, 2.8,
        "Results (validated 2026-05-01)\n──────────────────────────────────────────────────────────────────\nModel              NIAH     MultiHop   Cost/1M    Latency\n─────────────────────────────────────────────────────────────────\nDeepSeek V4 Flash  100%     100%       $0.14      1× (baseline)\nDeepSeek V4 Pro    100%     100%       $0.32      2.3×\nLlama 4 Scout       33%     100%       low        variable",
        LGREY, GREY, fontsize=8)

    # verdict
    box(ax, 11.0, 3.0, 6.5, 2.8,
        "Verdict\n──────────────────────────────────────\n✓ Flash = Pro accuracy at 2.3× less\n  cost + 2× faster\n\n✓ Multi-hop reasoning solved at\n  frontier scale (all 3: 100%)\n\n✗ Llama 4 Scout 33% NIAH:\n  not reliable for deep retrieval\n  workloads",
        LGRN, GREEN, fontsize=8)

    label(ax, 0.4, 2.0, "python run_benchmark.py --task niah --positions 10000,100000,500000,900000  ·  --task all", fontsize=7, color=GREY)
    save(f, "deepseek-v4-context-benchmark")

# ─────────────────────────────────────────────────────────────────────────────
# 14. morph-ast-refactoring
# ─────────────────────────────────────────────────────────────────────────────
def d_morph():
    f, ax = fig()
    title_row(ax, "Morph · AST-Level LLM Refactoring · Typed Plans · Dependency Validation · Auto Rollback",
              "LLM declares intent (not code) · NetworkX dep graph · tree-sitter AST apply · pytest + git rollback")
    # user input
    box(ax, 0.4, 7.5, 2.5, 0.8, "Natural Language\nRefactoring Goal\n(user input)", LAMB, AMBE, fontsize=8)
    arrow(ax, 2.9, 7.9, 3.7, 7.9)

    # llm planner
    box(ax, 3.7, 7.2, 3.0, 1.5,
        "LLM Planner\n(temp=0.1)\n────────────\nOllama / OpenAI\nAnthropic\nOpenRouter",
        LPURP, PURP, fontsize=8)
    arrow(ax, 6.7, 7.9, 7.5, 7.9)

    # typed operations
    box(ax, 7.5, 6.5, 4.0, 2.5,
        "Typed Operation Plan\n─────────────────────────\nRenameSymbol\n  from: processData\n  to: transform_batch\nExtractFunction\n  lines: 45-67 → validate_input\nMoveFunction\n  format_output → formatters.py",
        LRED, RED, fontsize=8)
    arrow(ax, 11.5, 7.75, 12.3, 7.75)

    # dep graph
    box(ax, 12.3, 7.2, 3.0, 1.5,
        "NetworkX\nDep Graph\n────────────\n• import conflicts\n• topological sort\n• call site discovery",
        LBLUE, SBLU, fontsize=8)
    arrow(ax, 15.3, 7.9, 16.1, 7.9)

    # tree-sitter
    box(ax, 16.1, 7.2, 1.8, 1.5, "tree-sitter\nAST\nApply", LGRN, GREEN, fontsize=8)

    # pytest + rollback
    box(ax, 5.0, 4.5, 4.0, 1.5,
        "pytest\n────────────────\npass → git stage\nfail → auto rollback\nworkspace always clean",
        LGRN, GREEN, fontsize=8)
    arrow(ax, 16.1+0.9, 7.2, 16.1+0.9, 5.5)
    arrow(ax, 16.1+0.9, 5.5, 9.0, 5.5)
    arrow(ax, 9.0, 5.5, 9.0, 6.0)

    # clash detection
    box(ax, 11.0, 4.5, 4.5, 1.5,
        "Conflict Report (if any)\n─────────────────────────────\n• circular import detected\n• missing call site at src/x.py:42\nFix the plan, not the code",
        LRED, RED, fontsize=8)
    arrow(ax, 12.3+1.5, 7.2, 13.25, 6.0)

    label(ax, 0.4, 2.4, "morph \"extract validation logic into its own module\" --backend ollama  ·  morph --plan-only \"rename processData\"", fontsize=7, color=GREY)
    save(f, "morph-ast-refactoring")

# ─────────────────────────────────────────────────────────────────────────────
# 15. invariant-property-testing-llms
# ─────────────────────────────────────────────────────────────────────────────
def d_invariant():
    f, ax = fig()
    title_row(ax, "Invariant · Property-Based Testing for LLMs · 7 Invariants · Auto Shrinking · pytest",
              "declare properties → generate variations → hunt for violations → binary-search shrink to minimal case")
    # prompt input
    box(ax, 0.4, 7.0, 2.2, 1.0, "Original\nPrompt", LAMB, AMBE, fontsize=9)
    arrow(ax, 2.6, 7.5, 3.4, 7.5)

    # 3 generators
    label(ax, 3.4, 8.5, "Input Generators", fontsize=8, color=BLUE)
    gens = [("LLM\nParaphraser", LPURP, PURP), ("Rule-based\nMutator", LBLUE, SBLU), ("Adversarial\nLLM", LRED, RED)]
    for i, (lbl, fc, ec) in enumerate(gens):
        box(ax, 3.4 + i*2.4, 6.5, 2.0, 1.0, lbl, fc, ec, fontsize=8)
        arrow(ax, 4.4 + i*2.4, 6.5, 4.4 + i*2.4, 5.8)

    # variants
    box(ax, 3.4, 4.8, 6.4, 0.9, "Variant Prompts  (hundreds per invariant)", LGREY, GREY, fontsize=8)
    arrow(ax, 6.6, 4.8, 6.6, 4.1)

    # llm under test
    box(ax, 4.8, 3.1, 3.8, 0.9, "LLM Under Test\n(Ollama / OpenAI / OpenRouter)", LGRN, GREEN, fontsize=8)
    arrow(ax, 8.6, 3.55, 9.4, 3.55)

    # 7 invariants / checkers
    label(ax, 9.4, 8.5, "7 Built-in Invariants", fontsize=8, color=BLUE)
    invs = ["consistency\n(semantic rephrase)", "instruction_following", "json_output\n(+ schema validation)",
            "no_self_contradiction", "improves_with_context", "confidence_calibration", "language_matching"]
    colors = [LBLUE, LGRN, LPURP, LRED, LAMB, LTEAL, LBLUE]
    edges  = [SBLU, GREEN, PURP, RED, AMBE, TEAL, SBLU]
    for i, (lbl, fc, ec) in enumerate(zip(invs, colors, edges)):
        box(ax, 9.4, 7.8 - i*0.85, 4.5, 0.7, lbl, fc, ec, fontsize=7)
        if i == 0:
            arrow(ax, 9.4+2.25, 3.55, 9.4+2.25, 7.8)

    arrow(ax, 13.9, 5.8, 14.7, 5.8)

    # shrinking
    box(ax, 14.7, 5.2, 3.2, 1.5,
        "Auto Shrinking\n────────────────────\nbinary search\nminimal failing case\n→ immediately\n  actionable",
        LRED, RED, fontsize=8)
    arrow(ax, 16.3, 5.2, 16.3, 4.2)
    box(ax, 14.7, 3.2, 3.2, 0.9, "Violation Report\n+ pytest failure", LGREY, GREY, fontsize=8)

    label(ax, 0.4, 1.8, "invariant run --model gemma4:e4b --backend ollama --invariants consistency \"Explain quantum entanglement\"", fontsize=7, color=GREY)
    save(f, "invariant-property-testing-llms")

# ─────────────────────────────────────────────────────────────────────────────
# 16. contextcraft-prompt-workbench
# ─────────────────────────────────────────────────────────────────────────────
def d_contextcraft():
    f, ax = fig()
    title_row(ax, "ContextCraft · Visual Prompt Workbench · Token Counting · Semantic Compression · Version Control",
              "FastAPI + React · drag-and-drop canvas · tiktoken · Ollama/OpenRouter testing · SQLite versions · multi-format export")
    # canvas
    box(ax, 0.4, 6.0, 4.0, 3.5,
        "Drag-and-Drop Canvas\n──────────────────────────\n[system_prompt]\n  role: system\n  tokens: 847\n\n[few_shot_examples]\n  role: user/assistant × 3\n  tokens: 1,240\n\n[context]  ← over budget!\n  tokens: 3,180\n\n[constraints]\n  tokens: 210",
        LGREY, GREY, fontsize=7)

    # token counter
    box(ax, 5.2, 8.0, 3.5, 1.3,
        "Token Counter (tiktoken)\n──────────────────────────\nGPT-4o: 5,477 / 8,192\nClaude:  5,477 / 200,000\n🟡 within 90% of GPT limit",
        LAMB, AMBE, fontsize=8)
    arrow(ax, 4.4, 7.75, 5.2, 8.3)

    # compression
    box(ax, 5.2, 6.2, 3.5, 1.5,
        "AI Compression\n──────────────────\nrewrite via LLM\nsemantic similarity\ncheck quality floor",
        LPURP, PURP, fontsize=8)
    arrow(ax, 4.4, 7.0, 5.2, 7.0)

    # test runner
    box(ax, 9.7, 7.5, 3.5, 1.8,
        "LLM Test Runner\n──────────────────\n• Ollama (local)\n• OpenRouter (cloud)\nresponse renders inline\nno format switching",
        LGRN, GREEN, fontsize=8)
    arrow(ax, 8.7, 7.6, 9.7, 8.0)

    # version control
    box(ax, 9.7, 5.5, 3.5, 1.8,
        "Version Control\n──────────────────\nSQLite history\nsave canvas state\nrestore any version\ndiff between versions",
        LBLUE, SBLU, fontsize=8)
    arrow(ax, 8.7, 6.6, 9.7, 6.4)

    # export
    box(ax, 14.5, 6.5, 3.3, 2.5,
        "Multi-Format Export\n──────────────────────────\n• OpenAI\n  [{role, content}]\n• Anthropic\n  system/human/assistant\n• LangChain\n  ChatPromptTemplate\n• JSON (raw blocks)",
        LTEAL, TEAL, fontsize=8)
    arrow(ax, 13.2, 7.5, 14.5, 7.5)

    # stack
    box(ax, 0.4, 3.5, 6.0, 1.8,
        "Stack:  FastAPI backend  ·  React frontend\ntiktoken (GPT-4o + Claude tokenizers)\nSQLite persistence  ·  Ollama + OpenRouter integration",
        LGREY, GREY, fontsize=8)

    label(ax, 0.4, 2.4, "python server.py  →  http://localhost:8000  (canvas + token counter + test panel + version history)", fontsize=7, color=GREY)
    save(f, "contextcraft-prompt-workbench")

# ─────────────────────────────────────────────────────────────────────────────
# 17. pipelinescope-llm-pipeline-debugger
# ─────────────────────────────────────────────────────────────────────────────
def d_pipelinescope():
    f, ax = fig()
    title_row(ax, "PipelineScope · LLM Pipeline Debugger · Context · RAG · Agent · API Proxy",
              "FastAPI + React · token heatmaps · RAG failure detection · DAG graphs · production API capture")
    # 4 modes
    modes = [
        (0.4,  7.0, "Context Window\nExplorer\n──────────────\n• token distribution\n  breakdown\n• semantic relevance\n  heatmap\n• config simulation", LBLUE, SBLU),
        (5.1,  7.0, "RAG Pipeline\nExplorer\n──────────────\n• configurable chunking\n• reranking comparison\n• failure detection:\n  embed/rank/assemble", LGRN, GREEN),
        (9.8,  7.0, "Agent Execution\nTracer\n──────────────\n• visual DAG graph\n• failure attribution\n• replay from checkpoint\n• LangChain/AutoGPT", LPURP, PURP),
        (14.5, 7.0, "LLM Proxy\n: 8001\n──────────────\n• intercepts calls\n• OpenAI/Anthropic\n  /Ollama\n• SQLite storage\n• WebSocket live", LRED, RED),
    ]
    for x, y, lbl, fc, ec in modes:
        box(ax, x, y, 4.2, 2.5, lbl, fc, ec, fontsize=7.5)

    # fastapi + react
    box(ax, 3.0, 4.5, 10.0, 1.5,
        "FastAPI Backend  +  React Frontend\n─────────────────────────────────────────────────────────────────\ntoken waterfall charts · semantic heatmaps · DAG with hover details · production call log table",
        LGREY, GREY, fontsize=8)
    for x in [2.5, 7.2, 11.9, 16.6]:
        arrow(ax, x, 7.0, 8.0, 6.0)

    # sqlite
    box(ax, 0.4, 3.0, 4.0, 1.2, "SQLite\nAll captured data\nlocal storage only\nno cloud required", LTEAL, TEAL, fontsize=8)
    arrow(ax, 8.0, 4.5, 2.4, 4.2)

    # use cases
    box(ax, 5.5, 3.0, 12.0, 1.2,
        "Use cases:  diagnose wrong RAG answers  ·  find agent loop cause  ·  audit prompt reaching LLM  ·  capture production patterns without code changes",
        LAMB, AMBE, fontsize=8)

    label(ax, 0.4, 1.8, "python server.py  →  :8000 (explorer)  +  :8001 (proxy — point your app here to capture all API calls)", fontsize=7, color=GREY)
    save(f, "pipelinescope-llm-pipeline-debugger")

# ─────────────────────────────────────────────────────────────────────────────
# run all
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating diagrams...")
    d_loop_linter()
    d_rag_dedup()
    d_model_router()
    d_behavior_prober()
    d_token_negotiator()
    d_behavior_diff()
    d_flywheel()
    d_git_bisect()
    d_three_model_bench()
    d_a2a_mcp()
    d_long_horizon()
    d_smolvlm2()
    d_deepseek_ctx()
    d_morph()
    d_invariant()
    d_contextcraft()
    d_pipelinescope()
    print("Done — 17 PNGs written to", OUT_DIR)
