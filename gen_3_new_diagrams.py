#!/usr/bin/env python3
"""Generate Excalidraw diagrams for RuleSync, ContextCarry, and ToolRouter.

Patterns:
  - rulesync: RULES.yaml hub -> 6-adapter fan-out -> quality audit dimensions (hub-and-spoke)
  - context-carry: pipeline: AI tool -> proxy -> 5 detectors -> knowledge graph -> relevance scorer -> brief
  - tool-router: multi-tool input -> proxy interceptor -> state store pipeline -> handoff brief + spend dashboard
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "images", "diagrams")

TITLE = "#1e40af"
SUBTITLE = "#3b82f6"
BODY = "#64748b"
INK = "#374151"

PRIMARY_FILL, PRIMARY_STROKE = "#3b82f6", "#1e3a5f"
SECONDARY_FILL = "#60a5fa"
TERTIARY_FILL = "#93c5fd"
START_FILL, START_STROKE = "#fed7aa", "#c2410c"
END_FILL, END_STROKE = "#a7f3d0", "#047857"
WARN_FILL, WARN_STROKE = "#fee2e2", "#dc2626"
DECISION_FILL, DECISION_STROKE = "#fef3c7", "#b45309"
AI_FILL, AI_STROKE = "#ddd6fe", "#6d28d9"
ERROR_FILL, ERROR_STROKE = "#fecaca", "#b91c1c"

EVIDENCE_BG = "#1e293b"
EVIDENCE_GREEN = "#22c55e"
EVIDENCE_AMBER = "#fbbf24"

_seed = [50000]
def s():
    _seed[0] += 1
    return _seed[0]

def text(x, y, w, h, txt, size=12, color=INK, bold=False, align="center"):
    return {
        "type": "text", "id": f"t{s()}",
        "x": x, "y": y, "width": w, "height": h,
        "text": txt, "originalText": txt,
        "fontSize": size, "fontFamily": 3,
        "fontStyle": "bold" if bold else "normal",
        "textAlign": align, "verticalAlign": "middle",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "lineHeight": 1.25
    }

def shape(kind, x, y, w, h, label, fill, stroke, label_color=INK, dashed=False, label_size=12, rounded=True):
    sid = f"r{s()}"
    tid = f"rt{s()}"
    el = {
        "type": kind, "id": sid,
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": [{"type": "text", "id": tid}],
        "link": None, "locked": False,
    }
    if kind == "rectangle" and rounded:
        el["roundness"] = {"type": 3}
    lbl = {
        "type": "text", "id": tid,
        "x": x, "y": y, "width": w, "height": h,
        "text": label, "originalText": label,
        "fontSize": label_size, "fontFamily": 3,
        "fontStyle": "normal", "textAlign": "center", "verticalAlign": "middle",
        "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "lineHeight": 1.25,
        "containerId": sid,
    }
    return [el, lbl]

def rect(x, y, w, h, label, fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color=INK, dashed=False, label_size=12):
    return shape("rectangle", x, y, w, h, label, fill, stroke, label_color, dashed, label_size)

def ellipse(x, y, w, h, label, fill=START_FILL, stroke=START_STROKE, label_color=INK, label_size=12):
    return shape("ellipse", x, y, w, h, label, fill, stroke, label_color, label_size=label_size)

def diamond(x, y, w, h, label, fill=DECISION_FILL, stroke=DECISION_STROKE, label_color=INK, label_size=11):
    return shape("diamond", x, y, w, h, label, fill, stroke, label_color, label_size=label_size)

def arrow(x1, y1, x2, y2, stroke=PRIMARY_STROKE, dashed=False, label=None):
    el = {
        "type": "arrow", "id": f"a{s()}",
        "x": x1, "y": y1, "width": x2-x1, "height": y2-y1,
        "points": [[0, 0], [x2-x1, y2-y1]],
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1.5,
        "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "startBinding": None, "endBinding": None,
        "lastCommittedPoint": None, "startArrowhead": None, "endArrowhead": "arrow",
        "elbowed": False,
    }
    elements = [el]
    if label:
        mx, my = (x1+x2)/2 - 40, (y1+y2)/2 - 14
        elements.append(text(mx, my, 80, 16, label, size=10, color=BODY))
    return elements

def line(x1, y1, x2, y2, stroke=BODY, dashed=False, width=1):
    return [{
        "type": "line", "id": f"l{s()}",
        "x": x1, "y": y1, "width": x2-x1, "height": y2-y1,
        "points": [[0, 0], [x2-x1, y2-y1]],
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width,
        "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "startBinding": None, "endBinding": None,
        "lastCommittedPoint": None,
    }]

def dot(x, y, color=PRIMARY_STROKE, r=8):
    return [{
        "type": "ellipse", "id": f"d{s()}",
        "x": x-r, "y": y-r, "width": r*2, "height": r*2,
        "strokeColor": color, "backgroundColor": color,
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
    }]

def evidence_box(x, y, w, h, lines, line_color=EVIDENCE_GREEN, title=None):
    elements = [{
        "type": "rectangle", "id": f"ev{s()}",
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": EVIDENCE_BG, "backgroundColor": EVIDENCE_BG,
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s(), "version": 1, "versionNonce": s(),
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "roundness": {"type": 3},
    }]
    py = y + 10
    if title:
        elements.append(text(x+12, py, w-24, 14, title, size=10, color="#94a3b8", align="left"))
        py += 18
    for ln in lines:
        elements.append(text(x+12, py, w-24, 14, ln, size=10, color=line_color, align="left"))
        py += 16
    return elements

def title_block(x, w, t, sub):
    return [
        text(x, 12, w, 32, t, size=22, color=TITLE, bold=True),
        text(x, 48, w, 20, sub, size=12, color=BODY),
    ]

def write(name, elements, bg="#ffffff"):
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": bg, "gridSize": 20},
        "files": {},
    }
    path = os.path.join(OUT, f"{name}.excalidraw")
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"wrote {path}")


# ===== 1. rulesync =====
# Pattern: hub-and-spoke fan-out
# RULES.yaml (center) -> Parser/Validator -> 6 adapter outputs fan right
# Quality audit dimensions stack on the left
def build_rulesync():
    _seed[0] = 500000
    els = []
    els += title_block(60, 1100, "RuleSync — One RULES.yaml, Six AI Tool Configs",
                       "Single source of truth syncs to Claude Code, Cursor, Gemini CLI, Codex, Windsurf, Kiro")

    # RULES.yaml source (left center)
    els += evidence_box(40, 110, 280, 170, [
        "conventions:",
        "  - category: naming",
        "    description: use snake_case",
        "    priority: high",
        "donts:",
        "  - rule: no hardcoded secrets",
        "    severity: critical",
        "    reason: security policy",
    ], line_color=EVIDENCE_GREEN, title="RULES.yaml")

    # Parser / Pydantic validator
    els += rect(380, 155, 200, 70, "Parser\nPydantic Validation", fill=AI_FILL, stroke=AI_STROKE)
    els += arrow(320, 195, 380, 190)

    # Diff engine and watcher
    els += rect(380, 245, 200, 55, "Diff Engine + Watch", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=11)

    # Command bar evidence
    els += evidence_box(40, 310, 280, 120, [
        "$ rulesync push",
        "$ rulesync pull --merge",
        "$ rulesync diff",
        "$ rulesync watch",
        "$ rulesync status",
    ], line_color=EVIDENCE_AMBER, title="7 commands")
    els += arrow(320, 365, 380, 270, stroke=BODY, dashed=True)

    # Hub box in the middle
    els += rect(640, 155, 180, 155, "Adapter\nLayer", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=16)
    els += arrow(580, 190, 640, 190)

    # 6 tool outputs fan out to the right
    tools = [
        ("Claude Code", "CLAUDE.md", END_FILL, END_STROKE),
        ("Cursor", ".cursor/rules/*.mdc", TERTIARY_FILL, PRIMARY_STROKE),
        ("Gemini CLI", ".gemini/config.json", AI_FILL, AI_STROKE),
        ("Codex CLI", ".codex/config.json", DECISION_FILL, DECISION_STROKE),
        ("Windsurf", ".windsurf/rules", START_FILL, START_STROKE),
        ("Kiro", "kirodocs/", WARN_FILL, WARN_STROKE),
    ]
    for i, (tool, cfg, fill, stroke) in enumerate(tools):
        yt = 90 + i * 65
        els += rect(890, yt, 240, 50, f"{tool}\n{cfg}", fill=fill, stroke=stroke, label_size=10)
        els += arrow(820, 232, 890, yt + 25)

    # Quality audit section below
    els.append(text(40, 470, 600, 20, "rulesync audit — 5-Dimension Quality Score", size=14, color=TITLE, bold=True, align="left"))
    audit_dims = [
        ("Specificity 25%", "always / never / must vs. vague language", END_FILL, END_STROKE),
        ("Coverage 20%", "style, testing, docs, naming, security, perf", TERTIARY_FILL, PRIMARY_STROKE),
        ("Actionability 20%", "examples + reasons make rules followable", AI_FILL, AI_STROKE),
        ("Contradictions 20%", "conflicting rules detected and flagged", DECISION_FILL, DECISION_STROKE),
        ("Freshness 15%", "decays at 30 / 90 / 180 days without review", START_FILL, START_STROKE),
    ]
    for i, (dim, detail, fill, stroke) in enumerate(audit_dims):
        x = 40 + i * 225
        els += rect(x, 500, 210, 70, f"{dim}\n{detail}", fill=fill, stroke=stroke, label_size=10)

    # Score legend
    els += evidence_box(40, 590, 740, 40, [
        "8–10 Excellent   6–7.9 Good   4–5.9 Fair   <4 Needs Work",
    ], line_color=EVIDENCE_AMBER)

    return els

if __name__ == "__main__":
    write("rulesync", build_rulesync())


# ===== 2. context-carry =====
# Pattern: pipeline with fan-out detectors + knowledge graph + relevance scoring
def build_context_carry():
    _seed[0] = 600000
    els = []
    els += title_block(60, 1100, "ContextCarry — Persistent Knowledge Across AI Sessions",
                       "Proxy captures every session → 5 detectors → knowledge graph → relevance-scored Context Brief")

    # AI Tools on the left
    tools = ["Claude Code", "Cursor", "Gemini CLI", "Codex CLI"]
    for i, t in enumerate(tools):
        els += rect(40, 110 + i * 65, 160, 50, t, fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=11)

    # Proxy
    els += rect(280, 175, 180, 80, "ContextCarry Proxy\nlocalhost:7862", fill=AI_FILL, stroke=AI_STROKE)
    for i in range(4):
        els += arrow(200, 135 + i * 65, 280, 215, stroke=PRIMARY_STROKE)

    # Session parser
    els += rect(280, 295, 180, 60, "Session Parser\n+ Storage", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)
    els += arrow(370, 255, 370, 295)

    # 5 pattern detectors fan down
    els.append(text(520, 270, 580, 18, "Pattern Detectors (run on every AI response)", size=12, color=TITLE, bold=True, align="left"))
    detectors = [
        ("Decisions", '"let\'s use", "we\'ll go with"', END_FILL, END_STROKE),
        ("Discoveries", '"found that", "turns out"', TERTIARY_FILL, PRIMARY_STROKE),
        ("Mistakes", '"doesn\'t work because"', ERROR_FILL, ERROR_STROKE),
        ("Conventions", '"always", "from now on"', AI_FILL, AI_STROKE),
        ("Work in Progress", '"still need to", "next step"', DECISION_FILL, DECISION_STROKE),
    ]
    for i, (det, phrase, fill, stroke) in enumerate(detectors):
        xd = 520 + i * 215
        els += rect(xd, 298, 200, 65, f"{det}\n{phrase}", fill=fill, stroke=stroke, label_size=10)
        els += arrow(460, 340, xd, 330, stroke=BODY, dashed=True)

    # Knowledge graph
    els += rect(550, 420, 500, 80, "SQLite Knowledge Graph\nnode: type · content · file_path · confidence · timestamp",
                fill="#f0fdf4", stroke=END_STROKE, label_size=11)
    for i in range(5):
        els += arrow(620 + i * 215, 363, 720 + i * 40, 420, stroke=BODY)

    # Relevance scorer
    els += rect(550, 540, 500, 70, "Relevance Scorer\nrecency 30% · file overlap 30% · node type 20% · semantic similarity 20%",
                fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=10)
    els += arrow(800, 500, 800, 540)

    # Context Brief output (right)
    els += evidence_box(620, 640, 500, 170, [
        "[ContextCarry] Previous Context",
        "",
        "Decisions: Use FastAPI not Flask",
        "Lessons: persistent_workers=True hangs",
        "Discoveries: all-MiniLM-L6-v2 works on CPU",
        "Conventions: always use Path() for paths",
        "WIP: refresh token logic still needed",
    ], line_color=EVIDENCE_GREEN, title="Context Brief injected at session start")
    els += arrow(800, 610, 800, 640)

    # Upstream provider
    els += rect(280, 175 - 120, 180, 60, "Upstream API\n(Anthropic / OpenAI / Ollama)", fill=START_FILL, stroke=START_STROKE, label_size=10)
    els += arrow(370, 175, 370, 115, stroke=BODY, dashed=True, label="forwarded")

    return els

if __name__ == "__main__":
    write("context-carry", build_context_carry())


# ===== 3. tool-router =====
# Pattern: multi-tool input -> proxy state machine -> handoff + spend dashboard
def build_tool_router():
    _seed[0] = 700000
    els = []
    els += title_block(60, 1150, "ToolRouter — Shared Session State Across AI Coding Tools",
                       "Transparent proxy maintains context across tool switches + real token spend tracking per model")

    # AI tools input row
    input_tools = ["Claude Code", "Cursor", "Gemini CLI", "Codex CLI"]
    for i, t in enumerate(input_tools):
        xi = 40 + i * 200
        els += rect(xi, 110, 170, 55, t, fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=12)

    # Proxy center
    els += rect(340, 220, 240, 80, "ToolRouter Proxy\nlocalhost:7863\n(OpenAI · Anthropic · Ollama)",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    for i in range(4):
        els += arrow(125 + i * 200, 165, 400 + i * 10, 220)

    # State store
    els += rect(150, 360, 240, 80, "SQLite State Store\n(WAL mode)\nsessions · files · decisions",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=10)
    els += arrow(370, 300, 270, 360)

    # File tracker
    els += rect(150, 490, 180, 60, "File Tracker\nwatchdog + MD5 hashes", fill=END_FILL, stroke=END_STROKE, label_size=10)
    els += arrow(230, 440, 230, 490)

    # Partial state detector
    els += rect(150, 590, 180, 55, "Partial-State Detector\nsyntax errors · conflict markers", fill=WARN_FILL, stroke=WARN_STROKE, label_size=10)
    els += arrow(230, 550, 230, 590)

    # Decision extractor
    els += rect(430, 360, 200, 80, "Decision Extractor\n\"let's use\" / \"done\" /\n\"still need to\"",
                fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=10)
    els += arrow(460, 300, 480, 360)

    # Handoff generator
    els += rect(290, 490, 200, 65, "Handoff Generator\npriority: partial → WIP\n→ decisions → done",
                fill=AI_FILL, stroke=AI_STROKE, label_size=10)
    els += arrow(270, 440, 350, 490)
    els += arrow(430, 405, 390, 490, stroke=DECISION_STROKE, dashed=True)

    # Handoff brief evidence
    els += evidence_box(40, 600, 450, 155, [
        "[ToolRouter Handoff — claude-code, 5min ago]",
        "",
        "✓ src/auth.py — JWT validation done",
        "⚠ src/api.py — PARTIALLY MODIFIED",
        "→ Implementing refresh token logic",
        "• bcrypt for passwords · JWT 24h expiry",
        "⚠ Do not touch: src/api.py (syntax errors)",
    ], line_color=EVIDENCE_GREEN, title="Handoff Brief injected into next session")
    els += arrow(390, 555, 250, 600)

    # Spend tracker (right side)
    els += rect(680, 360, 200, 80, "Spend Tracker\ntoken counts per response\n→ cost = tokens × rate",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=10)
    els += arrow(590, 300, 700, 360)

    # Spend dashboard mockup
    els += rect(680, 490, 450, 260, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(700, 500, 410, 18, "Spend Dashboard — localhost:7864", size=13, color=TITLE, bold=True, align="left"))
    els.append(text(700, 522, 410, 14, "toolrouter spend  |  toolrouter spend --week  |  toolrouter dashboard", size=10, color=BODY, align="left"))

    spend_rows = [
        ("claude-opus-4-7", "$15/$75 per M", "128k tokens", "$2.18"),
        ("claude-sonnet-4-6", "$3/$15 per M", "340k tokens", "$1.47"),
        ("gpt-4o", "$2.50/$10 per M", "80k tokens", "$0.42"),
        ("gemini-2.5-pro", "$1.25/$5 per M", "200k tokens", "$0.31"),
        ("ollama/*", "$0 / $0", "1.2M tokens", "$0.00"),
    ]
    for i, (model, rate, usage, cost) in enumerate(spend_rows):
        yr = 550 + i * 36
        col = EVIDENCE_AMBER if i < 2 else (EVIDENCE_GREEN if i == 4 else INK)
        els.append(text(700, yr, 160, 14, model, size=10, color=col, align="left"))
        els.append(text(860, yr, 130, 14, rate, size=10, color=BODY, align="left"))
        els.append(text(990, yr, 80, 14, usage, size=10, color=BODY, align="left"))
        els.append(text(1075, yr, 50, 14, cost, size=10, color=col, align="left"))

    els += arrow(780, 440, 830, 490)

    # CLI footer
    els += evidence_box(40, 780, 1100, 40, [
        "$ toolrouter start   $ toolrouter handoff   $ toolrouter spend --week   $ toolrouter config set injection true",
    ], line_color=EVIDENCE_AMBER)

    return els

if __name__ == "__main__":
    write("tool-router", build_tool_router())

print("All 3 diagrams written. Run render_pil.py to generate PNGs.")
