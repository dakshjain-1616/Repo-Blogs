#!/usr/bin/env python3
"""Generate Excalidraw diagrams for Arch Guard, Cost Guard, and Agent Liar.

Patterns:
  - arch-guard: AST + dep-graph -> 6 detectors fan-out -> formatters -> CLI/hook/CI outputs
  - cost-guard: app -> proxy -> tiktoken estimator -> 4-tier circuit breakers -> forward/block
  - agent-liar: task+claim+diff -> async orchestrator -> 4 parallel checks -> weighted score -> report
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
# Re-use primitives from the previous batch
from gen_3_new_diagrams import (
    text, shape, rect, ellipse, diamond, arrow, line, dot, evidence_box,
    title_block, write,
    TITLE, SUBTITLE, BODY, INK,
    PRIMARY_FILL, PRIMARY_STROKE, SECONDARY_FILL, TERTIARY_FILL,
    START_FILL, START_STROKE, END_FILL, END_STROKE,
    WARN_FILL, WARN_STROKE, DECISION_FILL, DECISION_STROKE,
    AI_FILL, AI_STROKE, ERROR_FILL, ERROR_STROKE,
    EVIDENCE_BG, EVIDENCE_GREEN, EVIDENCE_AMBER,
    _seed,
)
import gen_3_new_diagrams as g


# ===== 1. arch-guard =====
def build_arch_guard():
    g._seed[0] = 800000
    els = []
    els += title_block(60, 1180, "ArchGuard — Static Analysis for Architectural Degradation",
                       "AST + dependency graph -> six detectors -> formatters -> CLI, git hooks, GitHub Actions")

    # Codebase input (left)
    els += evidence_box(40, 110, 260, 150, [
        "src/",
        "  app/services/billing.py",
        "  app/api/checkout.py",
        "  app/models/order.py",
        "  app/utils/helpers.py",
        "  ...",
        ".archguard.yml",
    ], line_color=EVIDENCE_GREEN, title="Python codebase")

    # Core engine
    els += rect(360, 110, 220, 70, "AST Parser\n(stdlib ast module)", fill=AI_FILL, stroke=AI_STROKE, label_size=11)
    els += arrow(300, 145, 360, 145)

    els += rect(360, 200, 220, 70, "Dependency Graph\n(NetworkX)", fill=AI_FILL, stroke=AI_STROKE, label_size=11)
    els += arrow(470, 180, 470, 200)

    els += rect(360, 290, 220, 60, "Core Engine\n+ severity filter", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE,
                label_color="#ffffff", label_size=11)
    els += arrow(470, 270, 470, 290)

    # Six detectors fan-out to the right
    els.append(text(660, 90, 480, 18, "Six Built-In Detectors", size=14, color=TITLE, bold=True, align="left"))
    detectors = [
        ("Circular Dependencies", "cycles in module imports", WARN_FILL, WARN_STROKE),
        ("God Classes", "size, methods, attributes thresholds", ERROR_FILL, ERROR_STROKE),
        ("Service Layer Bypass", "API directly hits models", DECISION_FILL, DECISION_STROKE),
        ("Magic Values", "unnamed literals in business logic", AI_FILL, AI_STROKE),
        ("Cyclomatic Complexity", "per-function branch count", TERTIARY_FILL, PRIMARY_STROKE),
        ("Layer Violations", "lower layer imports upper", START_FILL, START_STROKE),
    ]
    for i, (name, detail, fill, stroke) in enumerate(detectors):
        col = i % 2
        row = i // 2
        x = 660 + col * 250
        y = 115 + row * 80
        els += rect(x, y, 240, 65, f"{name}\n{detail}", fill=fill, stroke=stroke, label_size=10)
        els += arrow(580, 320, x, y + 32, stroke=BODY, dashed=True)

    # Formatter row
    els.append(text(40, 380, 600, 18, "Formatters", size=14, color=TITLE, bold=True, align="left"))
    formats = ["Table (Rich)", "JSON", "YAML", "Markdown", "HTML"]
    for i, f in enumerate(formats):
        els += rect(40 + i * 160, 410, 145, 50, f, fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=11)

    # arrow from detectors to formatter band
    els += arrow(900, 360, 400, 410, stroke=BODY, dashed=True)

    # Output consumers row
    els.append(text(40, 490, 600, 18, "Consumers", size=14, color=TITLE, bold=True, align="left"))
    consumers = [
        ("CLI", "archguard scan / trend", END_FILL, END_STROKE),
        ("Git Hooks", "pre-commit · pre-push", DECISION_FILL, DECISION_STROKE),
        ("GitHub Actions", "PR comments + status", AI_FILL, AI_STROKE),
    ]
    for i, (name, sub, fill, stroke) in enumerate(consumers):
        els += rect(40 + i * 270, 520, 250, 65, f"{name}\n{sub}", fill=fill, stroke=stroke, label_size=11)
        els += arrow(160 + i * 270, 460, 165 + i * 270, 520, stroke=BODY)

    # CLI evidence
    els += evidence_box(40, 610, 540, 160, [
        "$ archguard scan src/ --severity high",
        "",
        "[!] god_class       app/services/billing.py  Service (412 lines, 31 methods)",
        "[!] circular_dep    app.api.checkout -> app.services.billing -> app.api.checkout",
        "[ ] magic_value     app/utils/helpers.py:84  TIMEOUT = 30",
        "[!] layer_violation app/models/order.py imports app.api.checkout",
        "",
        "4 violations  |  score: 6.8 / 10  |  HTML report: ./archguard-report.html",
    ], line_color=EVIDENCE_AMBER, title="archguard scan")

    # Trend evidence
    els += rect(620, 610, 520, 160, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(640, 620, 480, 16, "archguard trend — last 10 commits", size=12, color=TITLE, bold=True, align="left"))

    # Simple bar trend
    bar_heights = [40, 55, 50, 70, 65, 80, 75, 90, 85, 100]
    for i, h in enumerate(bar_heights):
        bx = 650 + i * 48
        by = 770 - h
        color = "#22c55e" if h < 60 else ("#fbbf24" if h < 85 else "#dc2626")
        els.append({
            "type": "rectangle", "id": f"bar{g.s()}",
            "x": bx, "y": by, "width": 36, "height": h,
            "strokeColor": color, "backgroundColor": color,
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0,
            "seed": g.s(), "version": 1, "versionNonce": g.s(),
            "isDeleted": False, "groupIds": [], "boundElements": None,
            "link": None, "locked": False,
        })
    els.append(text(640, 750, 480, 14, "violations per commit -> rising trend triggers CI warning", size=10, color=BODY, align="left"))

    return els

write("arch-guard", build_arch_guard())


# ===== 2. cost-guard =====
def build_cost_guard():
    g._seed[0] = 900000
    els = []
    els += title_block(60, 1180, "CostGuard — Hard Spending Limits Before AI API Calls",
                       "Local FastAPI proxy estimates with tiktoken, enforces 4-tier circuit breakers, then forwards or blocks")

    # Application client (left)
    els += rect(40, 145, 180, 75, "Your App\nopenai.ChatCompletion\nbase_url=localhost:8088",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)

    # Proxy (FastAPI)
    els += rect(290, 130, 230, 105, "CostGuard Proxy\nFastAPI · async\nlocalhost:8088",
                fill=AI_FILL, stroke=AI_STROKE, label_size=11)
    els += arrow(220, 182, 290, 182, label="POST /v1/chat/completions")

    # Tiktoken estimator
    els += rect(590, 130, 220, 70, "Pre-Flight Estimator\ntiktoken count + price table\n(May 2026)",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(520, 165, 590, 165)

    # Decision diamond
    els += diamond(870, 125, 200, 110, "Within all\nbudgets?", fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=12)
    els += arrow(810, 165, 870, 180)

    # 4-tier budgets fan-down from estimator
    els.append(text(290, 280, 600, 18, "4-Tier Circuit Breakers (must pass ALL)", size=14, color=TITLE, bold=True, align="left"))
    tiers = [
        ("Session", "$5 cap · resets on restart", END_FILL, END_STROKE),
        ("Hourly", "$10 cap · rolling 60min", TERTIARY_FILL, PRIMARY_STROKE),
        ("Daily", "$50 cap · resets at midnight", DECISION_FILL, DECISION_STROKE),
        ("Project", "$500/mo · per-tag accounting", AI_FILL, AI_STROKE),
    ]
    for i, (name, detail, fill, stroke) in enumerate(tiers):
        x = 290 + i * 200
        els += rect(x, 310, 185, 70, f"{name}\n{detail}", fill=fill, stroke=stroke, label_size=10)
        els += arrow(700, 200, x + 90, 310, stroke=BODY, dashed=True)

    # Safe mode confirm prompt
    els += rect(40, 310, 220, 90, "Safe Mode\nif est > $0.10:\n  prompt for confirm\nelse: auto-pass",
                fill=WARN_FILL, stroke=WARN_STROKE, label_size=10)
    els += arrow(150, 235, 150, 310, stroke=WARN_STROKE, dashed=True)

    # Yes branch -> upstream
    els += rect(870, 280, 200, 60, "Forward to Upstream\nOpenAI · Anthropic ·\nOpenRouter",
                fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(970, 235, 970, 280, label="yes")

    # No branch -> blocked
    els += rect(870, 380, 200, 60, "Block + 402 Response\n{\"error\": \"budget\"}",
                fill=ERROR_FILL, stroke=ERROR_STROKE, label_size=10)
    els += arrow(870, 200, 870, 380, label="no", stroke=ERROR_STROKE, dashed=True)

    # SQLite + WebSocket + notifications
    els.append(text(40, 430, 800, 18, "Observability", size=14, color=TITLE, bold=True, align="left"))
    els += rect(40, 460, 220, 70, "SQLite Ledger\nrequest · est · actual · tag",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(405, 235, 200, 460, stroke=BODY)

    els += rect(290, 460, 220, 70, "WebSocket Stream\nlive cost updates",
                fill=AI_FILL, stroke=AI_STROKE, label_size=11)
    els += arrow(155, 495, 290, 495, stroke=BODY)

    els += rect(540, 460, 200, 70, "Notifications\nconsole · webhook · file",
                fill=WARN_FILL, stroke=WARN_STROKE, label_size=10)
    els += arrow(510, 495, 540, 495, stroke=BODY)

    # Terminal dashboard mockup (right side, large)
    els += rect(770, 460, 380, 320, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(790, 475, 340, 18, "costguard dashboard", size=13, color=TITLE, bold=True, align="left"))
    els.append(text(790, 498, 340, 14, "live · localhost:8089", size=10, color=BODY, align="left"))

    rows = [
        ("Session",  "$2.18", "$5.00", "#22c55e"),
        ("Hourly",   "$4.71", "$10.00", "#22c55e"),
        ("Daily",    "$38.20", "$50.00", "#fbbf24"),
        ("Project: prod-api", "$412", "$500/mo", "#dc2626"),
    ]
    for i, (label, used, cap, color) in enumerate(rows):
        ry = 530 + i * 56
        els.append(text(790, ry, 200, 14, label, size=11, color=INK, align="left"))
        els.append(text(990, ry, 80, 14, used, size=11, color=color, align="left", ))
        els.append(text(1075, ry, 70, 14, f"/ {cap}", size=10, color=BODY, align="left"))
        # progress bar
        used_num = float(used.replace("$", "").replace(",", ""))
        cap_num = float(cap.replace("$", "").replace("/mo", "").replace(",", ""))
        pct = min(1.0, used_num / cap_num) if cap_num else 0
        els.append({
            "type": "rectangle", "id": f"pb{g.s()}",
            "x": 790, "y": ry + 22, "width": 340, "height": 8,
            "strokeColor": "#e2e8f0", "backgroundColor": "#e2e8f0",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0,
            "seed": g.s(), "version": 1, "versionNonce": g.s(),
            "isDeleted": False, "groupIds": [], "boundElements": None,
            "link": None, "locked": False,
        })
        els.append({
            "type": "rectangle", "id": f"pbf{g.s()}",
            "x": 790, "y": ry + 22, "width": int(340 * pct), "height": 8,
            "strokeColor": color, "backgroundColor": color,
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0,
            "seed": g.s(), "version": 1, "versionNonce": g.s(),
            "isDeleted": False, "groupIds": [], "boundElements": None,
            "link": None, "locked": False,
        })

    els.append(text(790, 760, 340, 14, "↑ resize / ↓ select project / q quit", size=10, color=BODY, align="left"))

    # CLI footer
    els += evidence_box(40, 560, 700, 200, [
        "$ costguard server --port 8088",
        "$ costguard estimate --model claude-opus-4-7 \\",
        "    --prompt-file ./prompt.txt",
        "  estimated: $0.247  (in 8214 tok @ $15/M, out ~512 @ $75/M)",
        "$ costguard status --tag prod-api",
        "  session  $2.18 / $5.00",
        "  hourly   $4.71 / $10.00",
        "  daily    $38.20 / $50.00  ⚠ 76%",
        "  project  $412 / $500/mo   ⛔ 82%  -> next call may block",
    ], line_color=EVIDENCE_GREEN, title="CLI")

    return els

write("cost-guard", build_cost_guard())


# ===== 3. agent-liar =====
def build_agent_liar():
    g._seed[0] = 1000000
    els = []
    els += title_block(60, 1180, "AgentLiar — Verifying When Coding Agents Lie About Completing Tasks",
                       "task + claim + diff -> async orchestrator -> 4 parallel checks -> weighted score -> evidence report")

    # Inputs (three stacked on the left)
    inputs = [
        ("task.md", "what the agent was asked to do", START_FILL, START_STROKE),
        ("claim.md", "what the agent says it did", DECISION_FILL, DECISION_STROKE),
        ("changes.diff", "the actual file changes", TERTIARY_FILL, PRIMARY_STROKE),
    ]
    for i, (name, sub, fill, stroke) in enumerate(inputs):
        els += rect(40, 110 + i * 90, 220, 70, f"{name}\n{sub}", fill=fill, stroke=stroke, label_size=11)

    # Orchestrator
    els += rect(320, 175, 220, 100, "Async Orchestrator\nasyncio.gather(checks)\n+ weighted score",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)
    for i in range(3):
        els += arrow(260, 145 + i * 90, 320, 215)

    # 4 parallel checks fan-out
    checks = [
        ("File Check",  "missing files · placeholders\n· unexpected additions",  END_FILL, END_STROKE, 35),
        ("Test Check",  "empty tests · missing asserts\n· skipped/xfail",        TERTIARY_FILL, PRIMARY_STROKE, 30),
        ("Scope Check", "\"only\" / \"for now\" /\nnarrowing language",          DECISION_FILL, DECISION_STROKE, 20),
        ("LLM Judge",   "OpenRouter cross-model\nadjudication (optional)",       AI_FILL, AI_STROKE, 15),
    ]
    for i, (name, detail, fill, stroke, weight) in enumerate(checks):
        x = 600
        y = 110 + i * 110
        els += rect(x, y, 280, 90, f"{name}  ({weight}%)\n{detail}", fill=fill, stroke=stroke, label_size=10)
        els += arrow(540, 225, x, y + 45, stroke=BODY)

    # Evidence boxes pull from each check
    file_ev = [
        "✗ src/auth/refresh.py — claimed, file missing",
        "⚠ src/auth/login.py — `# TODO implement` body",
        "✓ tests/test_login.py — added",
    ]
    test_ev = [
        "✗ tests/test_refresh.py::test_rotates — empty body",
        "⚠ tests/test_login.py — no asserts (3 fns)",
        "✓ tests/test_user.py — 4 asserts, passes",
    ]
    scope_ev = [
        "⚠ claim: \"implemented login for now\"",
        "⚠ claim: \"only the happy path is wired\"",
        "✓ task requested full auth flow",
    ]
    judge_ev = [
        "judge: claude-sonnet-4-6 -> 42 / 100",
        "judge: gpt-4o            -> 55 / 100",
        "consensus: \"partial implementation\"",
    ]
    evidences = [(file_ev, ERROR_STROKE), (test_ev, "#fbbf24"), (scope_ev, "#fbbf24"), (judge_ev, EVIDENCE_GREEN)]
    for i, (lines, col) in enumerate(evidences):
        y = 110 + i * 110
        els += evidence_box(910, y - 8, 360, 100, lines, line_color=col)
        els += arrow(880, y + 45, 910, y + 42, stroke=BODY, dashed=True)

    # Weighted score box
    els += rect(320, 320, 220, 80, "Weighted Score\n0.35·file + 0.30·test\n+ 0.20·scope + 0.15·judge",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(430, 275, 430, 320)

    # Score gauge (visual)
    els += rect(320, 430, 220, 130, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(330, 440, 200, 14, "Confidence Score", size=12, color=TITLE, bold=True, align="left"))
    els.append(text(330, 470, 200, 28, "47 / 100", size=24, color="#dc2626", bold=True, align="left"))
    els.append(text(330, 510, 200, 14, "verdict: LIKELY OVERCLAIMED", size=11, color=ERROR_STROKE, align="left"))
    els.append(text(330, 530, 200, 12, "fail < 60  ·  warn 60-79  ·  pass ≥ 80", size=9, color=BODY, align="left"))
    els += arrow(430, 400, 430, 430)

    # Report outputs
    els.append(text(40, 410, 250, 18, "Outputs", size=14, color=TITLE, bold=True, align="left"))
    els += rect(40, 440, 240, 55, "JSON report\nscore · per-check evidence", fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += rect(40, 510, 240, 55, "Markdown report\nfor PR comment / Slack", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(320, 360, 280, 467, stroke=BODY)
    els += arrow(320, 360, 280, 537, stroke=BODY)

    # Interfaces row
    els.append(text(40, 600, 1200, 18, "Interfaces", size=14, color=TITLE, bold=True, align="left"))
    interfaces = [
        ("CLI",          "agentliar verify --task t.md --claim c.md --diff d.diff", AI_FILL, AI_STROKE),
        ("Python lib",   "from agentliar import verify",                            TERTIARY_FILL, PRIMARY_STROKE),
        ("GitHub Action","step: dakshjain-1616/AgentLiar@v1",                       DECISION_FILL, DECISION_STROKE),
        ("HTTP API",     "POST /verify  (FastAPI)",                                 END_FILL, END_STROKE),
    ]
    for i, (name, detail, fill, stroke) in enumerate(interfaces):
        els += rect(40 + i * 310, 630, 290, 80, f"{name}\n{detail}", fill=fill, stroke=stroke, label_size=10)

    # CLI evidence at bottom
    els += evidence_box(40, 730, 1230, 60, [
        "$ agentliar verify --task task.md --claim claim.md --diff changes.diff --judge claude-sonnet-4-6",
        "score: 47/100  verdict: LIKELY OVERCLAIMED  ·  file 12/35  test 8/30  scope 7/20  judge 20/15  ·  report -> report.md",
    ], line_color=EVIDENCE_AMBER, title="agentliar verify")

    return els

write("agent-liar", build_agent_liar())

print("All 3 diagrams written. Run render_pil.py next.")
