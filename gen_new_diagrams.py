#!/usr/bin/env python3
"""Generate Excalidraw diagrams for 5 new blog posts using the excalidraw-diagram skill methodology.
Patterns chosen per blog:
  - agent-constitution: fan-in (tool call) -> AST evaluator -> three-way decision -> audit log + dashboard
  - context-time-machine: vertical timeline of turns + three-mode panels on the right
  - livecontext: proxy in the middle, agent on left, provider on right, dashboard panels below
  - agentsync: 7-command top bar -> merge engine -> 52-point audit fan-out by category
  - asr-evaluation-framework: 5-model parallel columns -> metrics convergence -> result JSON
"""
import json, os

OUT = "/home/daksh/description_And_blogs/public/images/diagrams"

# Color palette (from excalidraw-diagram skill)
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

_seed = [10000]
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
    elif kind == "ellipse":
        pass
    elif kind == "diamond":
        pass
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
        # midpoint label
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

def title(x, w, t, sub):
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

# ===== 1. agent-constitution =====
def build_agent_constitution():
    _seed[0] = 100000
    els = []
    els += title(60, 1080, "Agent Constitution - Policy Layer Outside the Prompt",
                 "Tool call -> AST-evaluated rule -> allow / block / require_approval, every decision auditable")

    # Tool call source
    els += ellipse(60, 180, 160, 80, "Agent Tool Call\nrm(path, recursive)", label_size=11)

    # Constitution YAML on top
    els += evidence_box(260, 100, 340, 130, [
        "- name: block_destructive_rm",
        "  tool: rm",
        "  condition: \"args.recursive == True",
        "    or args.path.startswith('/etc')\"",
        "  action: block",
        "  message: \"Recursive delete blocked\"",
    ], line_color=EVIDENCE_GREEN, title="constitution.yaml")

    # AST evaluator
    els += rect(280, 280, 290, 90, "AST-Restricted Evaluator\nast.parse + whitelist (no eval)",
                fill=AI_FILL, stroke=AI_STROKE)

    # PII detector branch
    els += rect(640, 100, 220, 70, "PII Detector\nregex (email/phone/SSN)",
                fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=11)
    els += rect(640, 185, 220, 70, "Ollama PII Pass\n(names, addresses)",
                fill=AI_FILL, stroke=AI_STROKE, label_size=11)

    # Arrow from tool call to evaluator
    els += arrow(220, 220, 280, 320)
    # Arrow from constitution to evaluator
    els += arrow(430, 230, 425, 280, stroke=BODY)
    # Optional PII calls
    els += arrow(570, 310, 640, 220, stroke=AI_STROKE, dashed=True)
    els += arrow(570, 330, 640, 220, stroke=AI_STROKE, dashed=True)

    # Decision diamond (3-way action)
    els += diamond(640, 290, 200, 110, "action?", label_size=14)
    els += arrow(570, 325, 640, 345)

    # Three outcomes
    els += ellipse(920, 220, 170, 70, "ALLOW", fill=END_FILL, stroke=END_STROKE, label_size=14)
    els += ellipse(920, 310, 170, 70, "BLOCK", fill=ERROR_FILL, stroke=ERROR_STROKE, label_size=14)
    els += ellipse(920, 400, 170, 70, "REQUIRE\nAPPROVAL", fill=DECISION_FILL, stroke=DECISION_STROKE, label_size=12)
    els += arrow(840, 320, 920, 255, stroke=END_STROKE)
    els += arrow(840, 345, 920, 345, stroke=ERROR_STROKE)
    els += arrow(840, 370, 920, 435, stroke=DECISION_STROKE)

    # JSONL audit log
    els += evidence_box(60, 490, 540, 130, [
        "{\"ts\":\"2026-05-14T10:22:01Z\", \"tool\":\"rm\",",
        " \"args\":{\"path\":\"/etc/passwd\",\"recursive\":true},",
        " \"rule\":\"block_destructive_rm\", \"action\":\"block\",",
        " \"message\":\"Recursive delete blocked\"}",
        "{\"ts\":\"...\", \"tool\":\"curl\", \"action\":\"allow\"} ...",
    ], line_color=EVIDENCE_AMBER, title="audit.jsonl (rotated at 50MB)")

    # Arrow from diamond/outcomes into audit
    els += arrow(740, 470, 350, 490, stroke=BODY, dashed=True)

    # Dashboard mockup
    els += rect(640, 490, 450, 130, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(660, 500, 410, 20, "FastAPI + WebSocket + React Dashboard",
                    size=13, color=TITLE, bold=True, align="left"))
    els.append(text(660, 525, 410, 16, "Live event feed  |  Top-fired rules  |  Filter by tool",
                    size=11, color=BODY, align="left"))
    # tiny rule rows
    for i, (r, c) in enumerate([
        ("block_destructive_rm", "12 fires"),
        ("require_approval_for_external_curl", "4 fires"),
        ("block_pii_in_response", "1 fire"),
    ]):
        els.append(text(660, 555+i*18, 280, 14, f"- {r}", size=10, color=INK, align="left"))
        els.append(text(960, 555+i*18, 120, 14, c, size=10, color=END_STROKE, align="left"))

    # CLI footer
    els += evidence_box(60, 640, 1030, 50, [
        "$ agent-constitution check rm --arg path=/etc --arg recursive=true   # exit code 1, rule fired: block_destructive_rm",
    ], line_color=EVIDENCE_GREEN)

    return els

write("agent-constitution", build_agent_constitution())

# ===== 2. context-time-machine =====
def build_ctm():
    _seed[0] = 200000
    els = []
    els += title(60, 1080, "ContextTimeMachine - Replay an Agent's Context Window at Any Turn",
                 "Vertical turn timeline (left) + three investigation modes: Timeline, Fact Tracker, Divergence Finder")

    # Vertical timeline
    els.append(text(60, 90, 240, 18, "Session Timeline (40 turns)", size=13, color=TITLE, bold=True, align="left"))
    els += line(110, 130, 110, 640, stroke=PRIMARY_STROKE, width=2)
    turn_labels = [
        (0, "T0  user input         12k"),
        (3, "T3  user instruction   18k"),
        (5, "T5  decision           24k"),
        (12, "T12 decision (key!)    47k"),
        (15, "T15 doc retrieval      61k"),
        (20, "T20 tool result        78k"),
        (28, "T28 eviction begins    92k"),
        (34, "T34 -- fact left ctx   105k"),
        (38, "T38 wrong answer       119k"),
    ]
    for i, (tn, lbl) in enumerate(turn_labels):
        y = 145 + i*55
        color = ERROR_STROKE if tn in (34, 38) else (END_STROKE if tn == 12 else PRIMARY_STROKE)
        els += dot(110, y, color=color, r=7)
        els.append(text(125, y-9, 200, 18, lbl, size=11, color=INK, align="left"))

    # Vertical divider
    els += line(330, 90, 330, 700, stroke=BODY, dashed=True)

    # Mode 1: Timeline Navigator + reconstructed context
    els.append(text(355, 95, 380, 18, "Mode 1 - Timeline Navigator (turn 38)", size=12, color=TITLE, bold=True, align="left"))
    els += rect(355, 120, 380, 220, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    snippets = [
        ("system", "You are a careful agent...", "1.2k"),
        ("user", "Compute total revenue for Q3", "0.3k"),
        ("tool", "sql_query(...) -> 8 rows", "2.1k"),
        ("assistant", "I'll use the cached table.", "0.4k"),
        ("tool", "fetch_doc(invoices.csv)", "14.0k"),
        ("[evicted]", "T12 decision: use cached SQL", "-"),
    ]
    py = 132
    for role, body, tok in snippets:
        color = ERROR_STROKE if role == "[evicted]" else INK
        els.append(text(365, py, 260, 14, f"{role}: {body}", size=10, color=color, align="left"))
        els.append(text(645, py, 80, 14, tok, size=10, color=BODY, align="left"))
        py += 18
    # Truncation line
    els += line(360, 305, 730, 305, stroke=ERROR_STROKE, dashed=True, width=2)
    els.append(text(365, 310, 250, 14, "<-- context truncation line at 128k", size=10, color=ERROR_STROKE, align="left"))

    # Mode 2: Fact Tracker - presence bar
    els.append(text(355, 360, 380, 18, "Mode 2 - Fact Tracker", size=12, color=TITLE, bold=True, align="left"))
    els.append(text(355, 380, 380, 14, "query: \"use cached SQL (decided T12)\"", size=10, color=BODY, align="left"))
    # Presence bar: green from T12 to T33, red from T34 onward
    els += rect(355, 405, 200, 30, "PRESENT", fill="#bbf7d0", stroke=END_STROKE, label_size=11, label_color=END_STROKE)
    els += rect(555, 405, 180, 30, "ABSENT", fill="#fecaca", stroke=ERROR_STROKE, label_size=11, label_color=ERROR_STROKE)
    els.append(text(355, 440, 380, 14, "entered: T12     left: T34     ^ root cause of T38 failure",
                    size=10, color=INK, align="left"))

    # Mode 3: Divergence Finder
    els.append(text(355, 475, 380, 18, "Mode 3 - Divergence Finder", size=12, color=TITLE, bold=True, align="left"))
    els.append(text(355, 495, 380, 14, "session_A (success) vs session_B (failure)", size=10, color=BODY, align="left"))
    els += rect(355, 515, 185, 90, "session_A @ T17\ndoc.invoices loaded",
                fill="#bbf7d0", stroke=END_STROKE, label_size=10)
    els += rect(550, 515, 185, 90, "session_B @ T17\ndoc.invoices missing",
                fill="#fecaca", stroke=ERROR_STROKE, label_size=10)
    els.append(text(355, 615, 380, 14, "earliest divergence: T17  (highlighted as root cause)",
                    size=10, color=ERROR_STROKE, align="left"))

    # Right column: backend
    els.append(text(770, 95, 320, 18, "Backend (FastAPI + SQLite)", size=12, color=TITLE, bold=True, align="left"))
    els += evidence_box(770, 120, 320, 220, [
        "POST /api/session/load",
        "GET  /api/session/{id}/profile",
        "GET  /api/session/{id}/turn/{n}",
        "POST /api/session/{id}/fact",
        "POST /api/divergence",
        "",
        "Embeddings: all-MiniLM-L6-v2 (CPU)",
        "Storage:    SQLite snapshot per turn",
        "Replay:     deterministic eviction",
    ], line_color=EVIDENCE_GREEN, title="API + Core Modules")

    # Footer CLI
    els += evidence_box(770, 360, 320, 100, [
        "$ timemachine serve",
        "$ timemachine load --file session.db",
        "  -> 40 turns indexed in 2.1s",
        "$ open http://localhost:8000",
    ], line_color=EVIDENCE_AMBER, title="CLI")

    return els

write("context-time-machine", build_ctm())

# ===== 3. livecontext =====
def build_livecontext():
    _seed[0] = 300000
    els = []
    els += title(60, 1080, "LiveContext - Real-Time Stream View of an Agent's Context Window",
                 "Transparent proxy intercepts every LLM call; dashboard streams context, tokens, evictions, attention live")

    # Top: agent -> proxy -> provider
    els += ellipse(60, 130, 180, 80, "Your LLM Agent\nbase_url=localhost:7860",
                   fill=START_FILL, stroke=START_STROKE, label_size=11)
    els += rect(310, 130, 280, 80, "LiveContext Proxy\nHTTP intercept + forward",
                fill=AI_FILL, stroke=AI_STROKE, label_size=12)
    els += ellipse(660, 130, 180, 80, "LLM Provider\nOpenAI / Anthropic / Ollama",
                   fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=11)
    els += arrow(240, 170, 310, 170, label="HTTP")
    els += arrow(590, 170, 660, 170, label="forward")
    els += arrow(660, 195, 590, 195, stroke=BODY, label="response")
    els += arrow(310, 195, 240, 195, stroke=BODY, label="response")

    # Down arrow from proxy to event store
    els += arrow(450, 210, 450, 260)

    # Event store
    els += rect(290, 260, 320, 80, "Event Store (SQLite)\nmessages | snapshots | evictions | embeddings",
                fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_color="#ffffff", label_size=11)

    # WebSocket + REST
    els += rect(120, 380, 220, 60, "WebSocket (real-time)", fill=END_FILL, stroke=END_STROKE, label_size=12)
    els += rect(560, 380, 220, 60, "REST API (export, replay)", fill=END_FILL, stroke=END_STROKE, label_size=12)
    els += arrow(380, 340, 230, 380)
    els += arrow(520, 340, 670, 380)

    # Dashboard region label
    els.append(text(60, 470, 1030, 20, "React Dashboard (http://localhost:7861) - five live panels",
                    size=13, color=TITLE, bold=True))

    # Panel 1: Live context stream
    els += rect(60, 500, 200, 180, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(70, 508, 180, 16, "Context Stream", size=11, color=TITLE, bold=True, align="left"))
    for i, (role, txt_, color) in enumerate([
        ("system", "You are...", PRIMARY_FILL),
        ("user", "Compute...", SECONDARY_FILL),
        ("assistant", "I'll fetch...", AI_FILL),
        ("tool", "rows[42]", TERTIARY_FILL),
        ("user", "More?", SECONDARY_FILL),
        ("[evicted]", "old system", "#fecaca"),
    ]):
        els += rect(70, 528+i*22, 180, 18, f"{role}: {txt_}", fill=color, stroke=PRIMARY_STROKE, label_size=9)

    # Panel 2: Token gauge
    els += rect(280, 500, 200, 180, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(290, 508, 180, 16, "Token Gauge", size=11, color=TITLE, bold=True, align="left"))
    els.append(text(290, 526, 180, 14, "94k / 128k (73%)", size=10, color=BODY, align="left"))
    # Stacked bar
    els += rect(290, 550, 30, 110, "sys", fill="#ddd6fe", stroke=AI_STROKE, label_size=9)
    els += rect(325, 580, 30, 80, "user", fill=SECONDARY_FILL, stroke=PRIMARY_STROKE, label_size=9, label_color="#ffffff")
    els += rect(360, 540, 30, 120, "assist", fill=PRIMARY_FILL, stroke=PRIMARY_STROKE, label_size=9, label_color="#ffffff")
    els += rect(395, 510, 30, 150, "tool", fill=TERTIARY_FILL, stroke=PRIMARY_STROKE, label_size=9)
    els.append(text(430, 580, 50, 14, "60%", size=10, color=ERROR_STROKE, align="left", bold=True) if False else text(430, 580, 50, 14, "60%", size=10, color=ERROR_STROKE, align="left"))

    # Panel 3: Eviction feed
    els += rect(500, 500, 220, 180, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(510, 508, 200, 16, "Eviction Feed", size=11, color=TITLE, bold=True, align="left"))
    for i, txt_ in enumerate([
        "10:22:14  freed 412 tok  LRU",
        "10:22:18  freed 1.1k tok LRU",
        "10:22:22  freed 380 tok  semantic",
        "10:22:31  freed 2.2k tok LRU",
        "10:22:40  freed 540 tok  semantic",
    ]):
        els.append(text(510, 528+i*22, 200, 16, txt_, size=9, color=INK, align="left"))

    # Panel 4: Attention heatmap
    els += rect(740, 500, 170, 180, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(750, 508, 150, 16, "Attention Heatmap", size=11, color=TITLE, bold=True, align="left"))
    # heat grid
    import random
    random.seed(7)
    colors = ["#fee2e2", "#fecaca", "#fca5a5", "#dbeafe", "#bfdbfe", "#93c5fd"]
    for i in range(8):
        for j in range(5):
            c = colors[(i*j + i + j) % len(colors)]
            els += rect(752+j*30, 528+i*18, 28, 16, "", fill=c, stroke=BODY, label_size=8)

    # Panel 5: Timeline scrubber
    els += rect(930, 500, 160, 180, "", fill="#f8fafc", stroke=PRIMARY_STROKE)
    els.append(text(940, 508, 140, 16, "Timeline Scrubber", size=11, color=TITLE, bold=True, align="left"))
    els += line(945, 580, 1080, 580, stroke=PRIMARY_STROKE, width=2)
    for i in range(8):
        els += dot(950+i*18, 580, color=PRIMARY_STROKE, r=4)
    els += dot(998, 580, color=ERROR_STROKE, r=8)
    els.append(text(940, 600, 140, 14, "scrub to T28", size=10, color=BODY, align="left"))
    els.append(text(940, 620, 140, 14, "[<<] [play] [>>]", size=10, color=INK, align="left"))

    # One-line integration footer
    els += evidence_box(60, 700, 1030, 30, [
        "client = OpenAI(api_key=..., base_url=\"http://localhost:7860/v1\")   # entire integration",
    ], line_color=EVIDENCE_GREEN)

    return els

write("livecontext", build_livecontext())

# ===== 4. agentsync =====
def build_agentsync():
    _seed[0] = 400000
    els = []
    els += title(60, 1080, "agentsync - Git-Backed Sync for AI Configs + 52-Point Audit",
                 "Seven commands -> tree-level 3-way merge -> 52-point audit across 5 categories")

    # 7-command top bar
    cmds = [
        ("init", START_FILL, START_STROKE),
        ("push", PRIMARY_FILL, PRIMARY_STROKE),
        ("pull", PRIMARY_FILL, PRIMARY_STROKE),
        ("diff", TERTIARY_FILL, PRIMARY_STROKE),
        ("audit", AI_FILL, AI_STROKE),
        ("status", END_FILL, END_STROKE),
        ("revert", WARN_FILL, WARN_STROKE),
    ]
    x = 60
    for cmd, f, st in cmds:
        els += rect(x, 100, 135, 60, cmd, fill=f, stroke=st, label_size=14)
        x += 145

    # Convergence into merge engine
    for i in range(7):
        cx = 60 + i*145 + 67
        els += arrow(cx, 160, 575, 215, stroke=BODY)

    # Merge engine
    els += rect(380, 215, 390, 100, "Three-Way Tree Merge\nparse JSON/YAML/INI -> tree diff -> reconcile at key level\n--manual for real conflicts",
                fill=AI_FILL, stroke=AI_STROKE, label_size=11)

    # Side: git transport
    els += ellipse(60, 235, 200, 70, "Remote Git Repo\norigin/main",
                   fill=START_FILL, stroke=START_STROKE, label_size=11)
    els += arrow(260, 270, 380, 265, stroke=START_STROKE, label="pull")
    els += arrow(380, 280, 260, 285, stroke=PRIMARY_STROKE, label="push")

    # Conflict resolution snippet on right
    els += evidence_box(800, 215, 290, 100, [
        "<<<<<<< OURS",
        "model: claude-opus-4.7",
        "=======",
        "model: gpt-5.5",
        ">>>>>>> THEIRS",
        "  base: claude-opus-4.6",
    ], line_color=EVIDENCE_AMBER, title="conflict (--manual)")

    # 52-point audit fan-out
    els.append(text(60, 350, 1030, 20, "52-Point Compliance Audit", size=14, color=TITLE, bold=True))

    audit_cats = [
        (60, "Security\n14 pts", "Hardcoded creds\nMissing encryption\nWildcard allowlists", WARN_FILL, WARN_STROKE),
        (270, "Compliance\n12 pts", "Audit-log toggle\nData retention\nAccess control", DECISION_FILL, DECISION_STROKE),
        (480, "Structure\n10 pts", "Key hierarchy\nDuplicate keys\nMissing version", PRIMARY_FILL, PRIMARY_STROKE),
        (690, "Performance\n8 pts", "Cache TTLs\nObject sizes\nPool config", SECONDARY_FILL, PRIMARY_STROKE),
        (900, "Documentation\n8 pts", "Comments\nExamples\nChangelog", END_FILL, END_STROKE),
    ]
    for x, head, body, f, st in audit_cats:
        label_col = "#ffffff" if f == PRIMARY_FILL else INK
        els += rect(x, 385, 175, 70, head, fill=f, stroke=st, label_size=13, label_color=label_col)
        els.append(text(x, 465, 175, 60, body, size=10, color=INK))

    # Convergence into report
    for x, *_ in audit_cats:
        cx = x + 87
        els += arrow(cx, 525, 575, 580, stroke=BODY)

    # Report
    els += evidence_box(380, 560, 390, 130, [
        "# audit-2026-05-14.md",
        "[FAIL] security/hardcoded_creds   configs/api.json:14",
        "       'api_key': 'sk-proj-...'  <-- found inline key",
        "[FAIL] compliance/audit_log       configs/audit.yaml",
        "       missing 'enabled: true'",
        "[PASS] 48 other checks",
        "",
        "Push blocked. Fix 2 failing checks before retrying.",
    ], line_color=EVIDENCE_GREEN, title="audit report (blocks push on security fail)")

    # CLI on right
    els += evidence_box(800, 560, 290, 130, [
        "$ agentsync init -r .../configs",
        "$ agentsync push -m \"tighten temp\"",
        "$ agentsync pull --manual",
        "$ agentsync diff --from HEAD~1",
        "$ agentsync audit --report",
        "$ agentsync status",
        "$ agentsync revert",
    ], line_color=EVIDENCE_AMBER, title="7 commands")

    return els

write("agentsync", build_agentsync())

# ===== 5. asr-evaluation-framework =====
def build_asr():
    _seed[0] = 500000
    els = []
    els += title(60, 1080, "ASR Evaluation Framework - Five Models, 15+ Scenarios, Three Metrics",
                 "Sequential model load -> per-scenario WER/CER/RTF -> stable JSON output for reproducible ranking")

    # Audio dataset input on left
    els += ellipse(60, 130, 180, 80, "Test Audio\n15+ scenarios",
                   fill=START_FILL, stroke=START_STROKE, label_size=12)
    # Scenarios as small dots
    scenarios = ["clean", "office noise", "street noise", "accents",
                 "fast speech", "slow speech", "whispered",
                 "technical vocab", "phone-quality", "music bg",
                 "multi-speaker", "long-form", "code-switch",
                 "numerics", "short utts"]
    els.append(text(40, 230, 220, 14, "Scenarios:", size=10, color=BODY, bold=True, align="left"))
    for i, sc in enumerate(scenarios):
        col = i % 2
        row = i // 2
        els.append(text(40+col*120, 250+row*18, 120, 14, f"- {sc}", size=9, color=INK, align="left"))

    # 5 parallel model columns
    models = [
        ("Whisper", "encoder-decoder", "1.2x", PRIMARY_FILL, PRIMARY_STROKE),
        ("Wav2Vec2", "self-supervised", "0.5x", SECONDARY_FILL, PRIMARY_STROKE),
        ("Distil-Whisper", "distilled", "0.4x", TERTIARY_FILL, PRIMARY_STROKE),
        ("NVIDIA Canary", "multi-task", "1.5x", AI_FILL, AI_STROKE),
        ("IBM Granite", "code-instruct + ASR", "2.0x", END_FILL, END_STROKE),
    ]
    x0 = 290
    col_w = 155
    for i, (name, arch, rtf, f, st) in enumerate(models):
        x = x0 + i*col_w
        col = "#ffffff" if f == PRIMARY_FILL else INK
        els += rect(x, 130, col_w - 15, 70, f"{name}\n{arch}", fill=f, stroke=st, label_size=11, label_color=col)
        els.append(text(x, 210, col_w - 15, 14, f"RTF approx {rtf}", size=10, color=BODY))

    els += arrow(240, 170, 290, 170, label="loaded\nsequentially")

    # Loader note
    els.append(text(290, 230, 760, 14,
                    "Models loaded one at a time (single-GPU friendly) -> unload between models",
                    size=10, color=BODY, align="left"))

    # Metric engine
    els += rect(290, 290, 760, 80, "Metric Engine\nWER (word error rate)   |   CER (character error rate)   |   RTF (real-time factor)",
                fill=AI_FILL, stroke=AI_STROKE, label_size=13)
    for i in range(5):
        cx = x0 + i*col_w + (col_w - 15)//2
        els += arrow(cx, 240, 670, 290, stroke=BODY)

    # Per-scenario score bars (showcase 4 models on the "office noise" scenario)
    els.append(text(60, 400, 1030, 20, "Per-Scenario Output (example: office_noise)", size=13, color=TITLE, bold=True))
    bars = [
        ("Whisper",        0.91, "WER 9.0%"),
        ("Distil-Whisper", 0.88, "WER 11.8%"),
        ("Canary",         0.93, "WER 7.1%"),
        ("Wav2Vec2",       0.72, "WER 28.0%"),
        ("Granite",        0.66, "WER 34.0%"),
    ]
    for i, (name, acc, lbl) in enumerate(bars):
        y = 432 + i*32
        els.append(text(60, y, 130, 22, name, size=11, color=INK, align="left"))
        # background bar
        els += rect(200, y, 600, 22, "", fill="#e2e8f0", stroke=BODY, label_size=8)
        # filled portion
        w = int(600 * acc)
        fill_col = END_FILL if acc >= 0.85 else (DECISION_FILL if acc >= 0.75 else WARN_FILL)
        stroke_col = END_STROKE if acc >= 0.85 else (DECISION_STROKE if acc >= 0.75 else WARN_STROKE)
        els += rect(200, y, w, 22, "", fill=fill_col, stroke=stroke_col, label_size=8)
        els.append(text(810, y, 140, 22, lbl, size=11, color=stroke_col, align="left", bold=True))

    # JSON result schema on the right (already taken by bars; put below)
    els += evidence_box(60, 610, 520, 110, [
        "{",
        "  \"model\": \"Whisper\",",
        "  \"scenario\": \"office_noise\",",
        "  \"wer\": 0.090, \"cer\": 0.041,",
        "  \"rtf\": 1.21, \"inference_s\": 12.4",
        "}",
    ], line_color=EVIDENCE_GREEN, title="results/whisper.json (stable schema)")

    # CLI
    els += evidence_box(600, 610, 490, 110, [
        "$ python run_evaluation.py --all",
        "$ python run_evaluation.py --accuracy",
        "$ python run_evaluation.py --speed",
        "$ python run_evaluation.py --all \\",
        "    --data-path ./my_data --output-path ./results",
    ], line_color=EVIDENCE_AMBER, title="CLI")

    return els

write("asr-evaluation-framework", build_asr())

print("done")
