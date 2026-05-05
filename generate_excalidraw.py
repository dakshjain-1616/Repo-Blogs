#!/usr/bin/env python3
"""Generate .excalidraw JSON files for the 17 new blog posts."""
import json, os

OUT = "/root/blogs/public/images/diagrams"

def rect(id, x, y, w, h, label, stroke, bg, seed):
    return {
        "type": "rectangle", "id": id,
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": seed, "version": 1, "versionNonce": seed+1,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False
    }

def txt(id, x, y, w, h, text, font_size=11, bold=False, color="#1e293b", align="center"):
    return {
        "type": "text", "id": id,
        "x": x, "y": y, "width": w, "height": h,
        "text": text, "originalText": text,
        "fontSize": font_size,
        "fontFamily": 3,
        "fontStyle": "bold" if bold else "normal",
        "textAlign": align,
        "verticalAlign": "middle",
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": id.__hash__() % 9000 + 1000 if isinstance(id, str) else id,
        "version": 1, "versionNonce": id.__hash__() % 9000 + 1001 if isinstance(id, str) else id+1,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "lineHeight": 1.25
    }

def arrow(id, x1, y1, x2, y2, seed):
    return {
        "type": "arrow", "id": id,
        "x": x1, "y": y1,
        "width": abs(x2-x1), "height": abs(y2-y1),
        "points": [[0, 0], [x2-x1, y2-y1]],
        "strokeColor": "#475569", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": seed, "version": 1, "versionNonce": seed+1,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "startArrowhead": None, "endArrowhead": "arrow"
    }

def title_el(text, subtitle, seed=100):
    return [
        txt("title", 50, 15, 800, 35, text, font_size=20, bold=True, color="#1e293b"),
        txt("subtitle", 50, 55, 800, 22, subtitle, font_size=12, color="#475569")
    ]

def save(name, elements):
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}
    }
    path = os.path.join(OUT, f"{name}.excalidraw")
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"  saved {name}.excalidraw")


# Color constants
BLUE="#1e40af"; LBLUE="#dbeafe"; SBLU="#3b82f6"
GREEN="#065f46"; LGRN="#d1fae5"
RED="#991b1b"; LRED="#fee2e2"
PURP="#6d28d9"; LPURP="#ede9fe"
AMBE="#92400e"; LAMB="#fef3c7"
GREY="#475569"; LGREY="#f1f5f9"
TEAL="#0f766e"; LTEAL="#ccfbf1"
ORG="#c2410c"; LORG="#fed7aa"


# ── 1. loop-anti-pattern-linter ──────────────────────────────────────────────
def d_loop_linter():
    els = title_el("Loop Anti-Pattern Linter", "AST-based Python loop performance analyzer — 7 pattern detectors, auto-fix suggestions")
    els = title_el("Loop Anti-Pattern Linter", "AST-based Python loop performance analyzer — 7 pattern detectors, auto-fix suggestions")
    boxes = [
        ("src",    40,  90, 140, 60, "Python\nSource File",    LRED,  RED),
        ("parse",  220, 90, 140, 60, "AST\nParser",            LBLUE, SBLU),
        ("detect", 400, 90, 160, 60, "Pattern\nDetector",      LGRN,  GREEN),
        ("report", 600, 90, 140, 60, "Report\nGenerator",      LAMB,  AMBE),
        ("fix",    600,200, 140, 60, "Auto-Fix\nSuggestions",  LPURP, PURP),
        ("p1",     40, 200, 130, 40, "quadratic_pattern",      LGREY, GREY),
        ("p2",     40, 250, 130, 40, "nested_concat",          LGREY, GREY),
        ("p3",     40, 300, 130, 40, "repeated_lookup",        LGREY, GREY),
        ("p4",     180,200, 130, 40, "list_append_loop",       LGREY, GREY),
        ("p5",     180,250, 130, 40, "range_len_pattern",      LGREY, GREY),
        ("p6",     320,200, 130, 40, "unnecessary_copy",       LGREY, GREY),
        ("p7",     320,250, 130, 40, "sort_in_loop",           LGREY, GREY),
    ]
    seed = 2000
    for b in boxes:
        bid,x,y,w,h,lbl,bg,stroke = b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+w//2-40,y+h//2-10,80,20,lbl,font_size=9,color="#1e293b"))
    arrows_data = [("a1",180,120,220,120),("a2",360,120,400,120),("a3",560,120,600,120)]
    for aid,x1,y1,x2,y2 in arrows_data:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("loop-anti-pattern-linter", els)


# ── 2. rag-retrieval-semantic-deduplication ───────────────────────────────────
def d_rag_dedup():
    els = title_el("RAG Retrieval Semantic Deduplication", "Semantic dedup for RAG pipelines — 30-50% token reduction, 5 strategies, streaming support")
    rows = [
        ("query",  40,  90, 140, 60, "User\nQuery",         LAMB,  AMBE),
        ("embed",  220, 90, 140, 60, "Embedding\nModel",    LBLUE, SBLU),
        ("ret",    400, 90, 160, 60, "Vector\nRetrieval",   LGRN,  GREEN),
        ("dedup",  600, 90, 160, 60, "Semantic\nDedup",     LPURP, PURP),
        ("rank",   800, 90, 140, 60, "Reranker",            LRED,  RED),
        ("ctx",    800,200, 140, 60, "Context\nAssembly",   LTEAL, TEAL),
        ("s1",     600,200, 140, 40, "cosine_threshold",    LGREY, GREY),
        ("s2",     600,250, 140, 40, "mmr_diversity",       LGREY, GREY),
        ("s3",     600,300, 140, 40, "cluster_dedup",       LGREY, GREY),
        ("s4",     600,350, 140, 40, "hash_exact",          LGREY, GREY),
        ("s5",     600,400, 140, 40, "sliding_window",      LGREY, GREY),
    ]
    seed = 3000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180,120,220,120),("a2",360,120,400,120),
                              ("a3",560,120,600,120),("a4",760,120,800,120),
                              ("a5",870,150,870,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("rag-retrieval-semantic-deduplication", els)


# ── 3. low-latency-model-router ───────────────────────────────────────────────
def d_model_router():
    els = title_el("Low-Latency Model Router", "Sub-0.1ms LLM selector — 4 priority modes, Redis cache, circuit breaker, failover")
    rows = [
        ("req",    40,  90, 130, 60, "Incoming\nRequest",    LAMB,  AMBE),
        ("cache",  210, 90, 130, 60, "Redis\nCache",         LBLUE, SBLU),
        ("router", 380, 90, 150, 60, "Model\nRouter",        LGRN,  GREEN),
        ("cb",     570, 90, 130, 60, "Circuit\nBreaker",     LPURP, PURP),
        ("m1",     740, 60, 120, 50, "GPT-4o",               LBLUE, SBLU),
        ("m2",     740,120, 120, 50, "Claude 3.5",           LGRN,  GREEN),
        ("m3",     740,180, 120, 50, "Ollama Local",         LAMB,  AMBE),
        ("p1",      40,200, 120, 40, "cost_priority",        LGREY, GREY),
        ("p2",      40,250, 120, 40, "latency_priority",     LGREY, GREY),
        ("p3",     170,200, 120, 40, "quality_priority",     LGREY, GREY),
        ("p4",     170,250, 120, 40, "capability_match",     LGREY, GREY),
    ]
    seed = 4000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",530,120,570,120),("a4",700,85,740,85),
                              ("a5",700,145,740,145),("a6",700,205,740,205)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("low-latency-model-router", els)


# ── 4. local-model-behavior-prober ────────────────────────────────────────────
def d_behavior_prober():
    els = title_el("Local Model Behavior Prober", "YAML probe suites for local LLM behavioral testing — Ollama, 8 probe categories, HTML reports")
    rows = [
        ("yaml",   40,  90, 130, 60, "YAML\nProbe Suite",    LAMB,  AMBE),
        ("parse",  210, 90, 130, 60, "Probe\nParser",        LBLUE, SBLU),
        ("run",    380, 90, 150, 60, "Test\nRunner",         LGRN,  GREEN),
        ("ollama", 570, 90, 130, 60, "Ollama\nBackend",      LPURP, PURP),
        ("score",  740, 90, 130, 60, "Response\nScorer",     LRED,  RED),
        ("report", 740,200, 130, 60, "HTML\nReport",         LTEAL, TEAL),
        ("c1",      40,200, 120, 40, "instruction_follow",   LGREY, GREY),
        ("c2",      40,250, 120, 40, "factual_accuracy",     LGREY, GREY),
        ("c3",     170,200, 120, 40, "refusal_behavior",     LGREY, GREY),
        ("c4",     170,250, 120, 40, "format_compliance",    LGREY, GREY),
        ("c5",     300,200, 120, 40, "consistency",          LGREY, GREY),
        ("c6",     300,250, 120, 40, "multilingual",         LGREY, GREY),
        ("c7",     430,200, 120, 40, "context_retention",    LGREY, GREY),
        ("c8",     430,250, 120, 40, "calibration",          LGREY, GREY),
    ]
    seed = 5000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",530,120,570,120),("a4",700,120,740,120),
                              ("a5",805,150,805,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("local-model-behavior-prober", els)


# ── 5. token-budget-negotiator ────────────────────────────────────────────────
def d_token_negotiator():
    els = title_el("Token Budget Negotiator", "Greedy ablation prompt compressor — CLI, library, MCP server, 40-60% reduction")
    rows = [
        ("prompt", 40,  90, 130, 60, "Input\nPrompt",        LAMB,  AMBE),
        ("parse",  210, 90, 130, 60, "Section\nParser",      LBLUE, SBLU),
        ("score",  380, 90, 150, 60, "Importance\nScorer",   LGRN,  GREEN),
        ("ablate", 570, 90, 150, 60, "Greedy\nAblation",     LPURP, PURP),
        ("verify", 750, 90, 130, 60, "Quality\nVerifier",    LRED,  RED),
        ("out",    750,200, 130, 60, "Compressed\nPrompt",   LTEAL, TEAL),
        ("iface1",  40,210, 110, 40, "CLI",                  LGREY, GREY),
        ("iface2",  40,260, 110, 40, "Python Library",       LGREY, GREY),
        ("iface3", 160,210, 110, 40, "MCP Server",           LGREY, GREY),
        ("m1",     380,210, 110, 40, "tiktoken",             LGREY, GREY),
        ("m2",     380,260, 110, 40, "semantic_sim",         LGREY, GREY),
        ("m3",     500,210, 110, 40, "section_priority",     LGREY, GREY),
    ]
    seed = 6000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",530,120,570,120),("a4",720,120,750,120),
                              ("a5",815,150,815,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("token-budget-negotiator", els)


# ── 6. llm-behavior-diff-detector ────────────────────────────────────────────
def d_behavior_diff():
    els = title_el("LLM Behavior Diff Detector", "Semantic diff across model versions — prompt suites, embedding comparison, HTML drift reports")
    rows = [
        ("suite",  40,  90, 140, 60, "Prompt\nTest Suite",   LAMB,  AMBE),
        ("ma",     220, 60, 130, 60, "Model A\n(baseline)",  LBLUE, SBLU),
        ("mb",     220,130, 130, 60, "Model B\n(new)",       LGRN,  GREEN),
        ("embed",  400, 90, 140, 60, "Embedding\nComparator",LPURP, PURP),
        ("diff",   580, 90, 150, 60, "Drift\nAnalyzer",      LRED,  RED),
        ("report", 770, 90, 130, 60, "HTML\nReport",         LTEAL, TEAL),
        ("d1",     580,200, 130, 40, "semantic_drift",       LGREY, GREY),
        ("d2",     580,250, 130, 40, "format_change",        LGREY, GREY),
        ("d3",     580,300, 130, 40, "length_delta",         LGREY, GREY),
        ("d4",     720,200, 130, 40, "regression_flag",      LGREY, GREY),
        ("d5",     720,250, 130, 40, "improvement_flag",     LGREY, GREY),
    ]
    seed = 7000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180, 90,220, 90),("a2",180,160,220,160),
                              ("a3",350, 90,400, 90),("a4",350,160,400,160),
                              ("a5",540,120,580,120),("a6",730,120,770,120)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("llm-behavior-diff-detector", els)


# ── 7. synthetic-data-flywheel ────────────────────────────────────────────────
def d_flywheel():
    els = title_el("Synthetic Data Flywheel", "8-stage self-improving data pipeline — LLM judge, diversity filter, recycling loop, A2A agent")
    rows = [
        ("seed",   40,  90, 120, 60, "Seed\nDataset",        LAMB,  AMBE),
        ("gen",    200, 90, 120, 60, "LLM\nGenerator",       LBLUE, SBLU),
        ("judge",  360, 90, 120, 60, "LLM\nJudge",           LGRN,  GREEN),
        ("div",    520, 90, 120, 60, "Diversity\nFilter",    LPURP, PURP),
        ("aug",    680, 90, 120, 60, "Data\nAugmentor",      LRED,  RED),
        ("store",  840, 90, 120, 60, "Dataset\nStore",       LTEAL, TEAL),
        ("eval",   840,200, 120, 60, "Model\nEvaluator",     LBLUE, SBLU),
        ("cycle",  680,200, 120, 60, "Recycle\nLoop",        LGRN,  GREEN),
        ("a2a",     40,220, 120, 40, "A2A Agent\nProtocol",  LPURP, PURP),
        ("s1",     200,220, 110, 35, "template_fill",        LGREY, GREY),
        ("s2",     200,265, 110, 35, "paraphrase",           LGREY, GREY),
        ("s3",     320,220, 110, 35, "quality_score",        LGREY, GREY),
        ("s4",     320,265, 110, 35, "halluc_detect",        LGREY, GREY),
    ]
    seed = 8000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",160,120,200,120),("a2",320,120,360,120),
                              ("a3",480,120,520,120),("a4",640,120,680,120),
                              ("a5",800,120,840,120),("a6",900,150,900,200),
                              ("a7",800,230,840,230),("a8",740,230,680,230)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("synthetic-data-flywheel", els)


# ── 8. llm-powered-git-bisect ─────────────────────────────────────────────────
def d_git_bisect():
    els = title_el("LLM-Powered Git Bisect", "Automated git bisect + Ollama local explanation — binary search, diff analysis, root cause")
    rows = [
        ("bug",    40,  90, 130, 60, "Bug\nReport",          LRED,  RED),
        ("hist",   210, 90, 130, 60, "Commit\nHistory",      LBLUE, SBLU),
        ("bisect", 380, 90, 140, 60, "Git Bisect\nEngine",   LGRN,  GREEN),
        ("diff",   560, 90, 130, 60, "Diff\nAnalyzer",       LPURP, PURP),
        ("ollama", 730, 90, 130, 60, "Ollama\nLocal LLM",    LAMB,  AMBE),
        ("explain",730,200, 130, 60, "Root Cause\nReport",   LTEAL, TEAL),
        ("b1",      40,210, 120, 40, "binary_search",        LGREY, GREY),
        ("b2",      40,260, 120, 40, "auto_test_run",        LGREY, GREY),
        ("b3",     170,210, 120, 40, "commit_classify",      LGREY, GREY),
        ("b4",     170,260, 120, 40, "diff_context",         LGREY, GREY),
        ("b5",     300,210, 120, 40, "natural_language",     LGREY, GREY),
        ("b6",     300,260, 120, 40, "fix_suggestion",       LGREY, GREY),
    ]
    seed = 9000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",520,120,560,120),("a4",690,120,730,120),
                              ("a5",795,150,795,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("llm-powered-git-bisect", els)


# ── 9. claude-opus-vs-gpt55-vs-deepseek-v4-benchmark ─────────────────────────
def d_three_model_bench():
    els = title_el("Claude Opus 4.7 vs GPT-5.5 vs DeepSeek V4 Benchmark", "13-task evaluation: Claude 9.23, GPT-5.5 9.15, DeepSeek 7.31 — cost/quality/speed analysis")
    rows = [
        ("tasks",  40,  90, 140, 60, "13 Eval\nTasks",       LAMB,  AMBE),
        ("claude", 230, 60, 130, 60, "Claude\nOpus 4.7",     LBLUE, SBLU),
        ("gpt",    230,130, 130, 60, "GPT-5.5",              LGRN,  GREEN),
        ("deep",   230,200, 130, 60, "DeepSeek V4",          LPURP, PURP),
        ("score",  410, 90, 140, 60, "Scoring\nEngine",      LTEAL, TEAL),
        ("analysis",590,90, 140, 60, "Analysis\n& Report",   LRED,  RED),
        ("r1",     770, 60, 130, 50, "Claude: 9.23/10",      LBLUE, SBLU),
        ("r2",     770,120, 130, 50, "GPT-5.5: 9.15/10",     LGRN,  GREEN),
        ("r3",     770,180, 130, 50, "DeepSeek: 7.31/10",    LPURP, PURP),
        ("t1",      40,220, 120, 35, "code_generation",      LGREY, GREY),
        ("t2",      40,265, 120, 35, "reasoning",            LGREY, GREY),
        ("t3",     170,220, 120, 35, "math_problems",        LGREY, GREY),
        ("t4",     170,265, 120, 35, "long_context",         LGREY, GREY),
    ]
    seed = 10000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180, 90,230, 90),("a2",180,160,230,160),
                              ("a3",180,230,230,230),("a4",360, 90,410, 90),
                              ("a5",360,160,410,160),("a6",360,230,410,230),
                              ("a7",550,120,590,120),("a8",730, 85,770, 85),
                              ("a9",730,145,770,145),("a10",730,205,770,205)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("claude-opus-vs-gpt55-vs-deepseek-v4-benchmark", els)


# ── 10. a2a-mcp-dual-protocol-reference-agent ────────────────────────────────
def d_a2a_mcp():
    els = title_el("A2A + MCP Dual-Protocol Reference Agent", "Canonical reference agent — Google A2A + Anthropic MCP, DeepSeek V4-Flash, task lifecycle")
    rows = [
        ("client", 40,  90, 130, 60, "Agent\nClient",        LAMB,  AMBE),
        ("a2a",    210, 60, 130, 60, "A2A\nProtocol",        LBLUE, SBLU),
        ("mcp",    210,130, 130, 60, "MCP\nProtocol",        LGRN,  GREEN),
        ("agent",  390, 90, 140, 60, "Reference\nAgent Core",LPURP, PURP),
        ("llm",    570, 90, 130, 60, "DeepSeek\nV4-Flash",   LRED,  RED),
        ("tools",  750, 90, 130, 60, "Tool\nRegistry",       LTEAL, TEAL),
        ("state",  570,200, 130, 60, "Task\nState Machine",  LBLUE, SBLU),
        ("s1",     750,200, 120, 35, "submitted",            LGREY, GREY),
        ("s2",     750,245, 120, 35, "working",              LGREY, GREY),
        ("s3",     750,290, 120, 35, "completed",            LGREY, GREY),
        ("s4",     880,200, 120, 35, "failed",               LGREY, GREY),
        ("s5",     880,245, 120, 35, "canceled",             LGREY, GREY),
    ]
    seed = 11000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170, 90,210, 90),("a2",170,160,210,160),
                              ("a3",340, 90,390, 90),("a4",340,160,390,160),
                              ("a5",530,120,570,120),("a6",700,120,750,120),
                              ("a7",635,150,635,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("a2a-mcp-dual-protocol-reference-agent", els)


# ── 11. long-horizon-agent-benchmark ─────────────────────────────────────────
def d_long_horizon():
    els = title_el("Long-Horizon Agent Benchmark", "50+ tool call benchmark: Opus 0.90/19 calls vs Kimi 0.90/93 calls vs DeepSeek 0.85/$0.11")
    rows = [
        ("tasks",  40,  90, 140, 60, "10 Long-Horizon\nTasks",      LAMB,  AMBE),
        ("harness",220, 90, 140, 60, "Test\nHarness",               LBLUE, SBLU),
        ("opus",   400, 60, 140, 55, "Claude Opus 4.7\n0.90 / 19c", LBLUE, SBLU),
        ("kimi",   400,125, 140, 55, "Kimi K2\n0.90 / 93 calls",    LGRN,  GREEN),
        ("dsk",    400,190, 140, 55, "DeepSeek V4\n0.85 / $0.11",   LPURP, PURP),
        ("score",  590, 90, 140, 60, "Scorer",                      LTEAL, TEAL),
        ("report", 770, 90, 130, 60, "Benchmark\nReport",           LRED,  RED),
        ("m1",      40,210, 130, 35, "tool_call_count",             LGREY, GREY),
        ("m2",      40,255, 130, 35, "success_rate",                LGREY, GREY),
        ("m3",     180,210, 130, 35, "cost_per_task",               LGREY, GREY),
        ("m4",     180,255, 130, 35, "time_to_complete",            LGREY, GREY),
    ]
    seed = 12000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180,120,220,120),("a2",360, 88,400, 88),
                              ("a3",360,152,400,152),("a4",360,217,400,217),
                              ("a5",540,120,590,120),("a6",730,120,770,120)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("long-horizon-agent-benchmark", els)


# ── 12. smolvlm2-edge-vision-agent ────────────────────────────────────────────
def d_smolvlm2():
    els = title_el("SmolVLM2 Edge Vision Agent", "Offline CPU-only vision monitoring — SmolVLM2 2.2B, motion-gating, RTSP/MJPEG streams")
    rows = [
        ("cam",    40,  90, 130, 60, "Camera\nStream",        LAMB,  AMBE),
        ("gate",   210, 90, 130, 60, "Motion\nGate",          LBLUE, SBLU),
        ("vlm",    380, 90, 150, 60, "SmolVLM2\n2.2B",        LGRN,  GREEN),
        ("parse",  570, 90, 130, 60, "Response\nParser",      LPURP, PURP),
        ("action", 740, 90, 130, 60, "Alert/Action\nRouter",  LRED,  RED),
        ("store",  740,200, 130, 60, "Local\nSQLite Store",   LTEAL, TEAL),
        ("f1",      40,210, 120, 35, "RTSP stream",           LGREY, GREY),
        ("f2",      40,255, 120, 35, "MJPEG stream",          LGREY, GREY),
        ("f3",     170,210, 120, 35, "pixel_diff",            LGREY, GREY),
        ("f4",     170,255, 120, 35, "frame_skip",            LGREY, GREY),
        ("f5",     300,210, 120, 35, "prompt_template",       LGREY, GREY),
        ("f6",     300,255, 120, 35, "cpu_only_infer",        LGREY, GREY),
    ]
    seed = 13000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",530,120,570,120),("a4",700,120,740,120),
                              ("a5",805,150,805,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("smolvlm2-edge-vision-agent", els)


# ── 13. deepseek-v4-context-benchmark ────────────────────────────────────────
def d_deepseek_ctx():
    els = title_el("DeepSeek V4 Million-Token Context Benchmark", "1M token NIAH test: Flash 100% at $0.14 vs Scout 33% — multi-doc QA, latency, cost analysis")
    rows = [
        ("corpus", 40,  90, 140, 60, "1M Token\nCorpus",      LAMB,  AMBE),
        ("niah",   220, 90, 130, 60, "NIAH\nProber",           LBLUE, SBLU),
        ("flash",  390, 60, 140, 55, "DeepSeek V4-Flash\n100% / $0.14", LGRN, GREEN),
        ("scout",  390,125, 140, 55, "DeepSeek Scout\n33% recall",      LPURP, PURP),
        ("score",  570, 90, 140, 60, "Scoring &\nAnalysis",    LTEAL, TEAL),
        ("report", 750, 90, 130, 60, "Benchmark\nReport",      LRED,  RED),
        ("t1",      40,210, 130, 35, "needle_placement",       LGREY, GREY),
        ("t2",      40,255, 130, 35, "multi_doc_qa",           LGREY, GREY),
        ("t3",     180,210, 130, 35, "latency_measure",        LGREY, GREY),
        ("t4",     180,255, 130, 35, "cost_tracking",          LGREY, GREY),
        ("t5",     320,210, 130, 35, "recall_at_depth",        LGREY, GREY),
    ]
    seed = 14000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180,120,220,120),("a2",350, 88,390, 88),
                              ("a3",350,152,390,152),("a4",530,120,570,120),
                              ("a5",710,120,750,120)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("deepseek-v4-context-benchmark", els)


# ── 14. morph-ast-refactoring ─────────────────────────────────────────────────
def d_morph():
    els = title_el("Morph: AST-Level LLM Refactoring", "LLM declares typed ops (RenameSymbol, MoveFunction) — NetworkX dep graph, tree-sitter apply")
    rows = [
        ("goal",   40,  90, 130, 60, "Refactoring\nGoal",     LAMB,  AMBE),
        ("llm",    210, 90, 130, 60, "LLM\nPlanner",          LBLUE, SBLU),
        ("ops",    380, 90, 150, 60, "Typed\nOperation Plan", LGRN,  GREEN),
        ("graph",  570, 90, 140, 60, "NetworkX\nDep Graph",   LPURP, PURP),
        ("ast",    750, 90, 130, 60, "tree-sitter\nApplier",  LRED,  RED),
        ("test",   750,200, 130, 60, "pytest\nVerification",  LTEAL, TEAL),
        ("git",    580,200, 130, 60, "git\nRollback",         LBLUE, SBLU),
        ("o1",      40,210, 130, 35, "RenameSymbol",          LGREY, GREY),
        ("o2",      40,255, 130, 35, "MoveFunction",          LGREY, GREY),
        ("o3",     180,210, 130, 35, "ExtractFunction",       LGREY, GREY),
        ("o4",     180,255, 130, 35, "ExtractModule",         LGREY, GREY),
        ("v1",     320,210, 130, 35, "import_conflict",       LGREY, GREY),
        ("v2",     320,255, 130, 35, "call_site_scan",        LGREY, GREY),
    ]
    seed = 15000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",530,120,570,120),("a4",710,120,750,120),
                              ("a5",815,150,815,200),("a6",750,230,710,230)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("morph-ast-refactoring", els)


# ── 15. invariant-property-testing-llms ──────────────────────────────────────
def d_invariant():
    els = title_el("Invariant: Property-Based Testing for LLMs", "7 invariants, 3 generators, auto binary-search shrinking, pytest integration")
    rows = [
        ("suite",  40,  90, 130, 60, "Invariant\nSuite",      LAMB,  AMBE),
        ("gen",    210, 90, 130, 60, "Input\nGenerator",      LBLUE, SBLU),
        ("llm",    380, 90, 140, 60, "LLM\nUnder Test",       LGRN,  GREEN),
        ("check",  560, 90, 130, 60, "Invariant\nChecker",    LPURP, PURP),
        ("shrink", 730, 90, 130, 60, "Auto\nShrinker",        LRED,  RED),
        ("pytest", 730,200, 130, 60, "pytest\nReport",        LTEAL, TEAL),
        ("i1",      40,210, 120, 30, "consistency",           LGREY, GREY),
        ("i2",      40,250, 120, 30, "instruction_follow",    LGREY, GREY),
        ("i3",      40,290, 120, 30, "json_output",           LGREY, GREY),
        ("i4",     170,210, 120, 30, "no_contradiction",      LGREY, GREY),
        ("i5",     170,250, 120, 30, "improves_w_context",    LGREY, GREY),
        ("i6",     170,290, 120, 30, "calibration",           LGREY, GREY),
        ("i7",     300,210, 120, 30, "language_match",        LGREY, GREY),
        ("g1",     430,210, 110, 30, "LLM paraphraser",       LGREY, GREY),
        ("g2",     430,250, 110, 30, "rule mutator",          LGREY, GREY),
        ("g3",     430,290, 110, 30, "adversarial LLM",       LGREY, GREY),
    ]
    seed = 16000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170,120,210,120),("a2",340,120,380,120),
                              ("a3",520,120,560,120),("a4",690,120,730,120),
                              ("a5",795,150,795,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("invariant-property-testing-llms", els)


# ── 16. contextcraft-prompt-workbench ────────────────────────────────────────
def d_contextcraft():
    els = title_el("ContextCraft: Visual Prompt Workbench", "Drag-and-drop canvas, tiktoken budget, semantic compression, Ollama/OpenRouter testing")
    rows = [
        ("canvas", 40,  90, 140, 60, "Drag-and-Drop\nCanvas",LAMB,  AMBE),
        ("token",  220, 90, 130, 60, "Token\nCounter",       LBLUE, SBLU),
        ("compress",380,90, 140, 60, "Semantic\nCompressor", LGRN,  GREEN),
        ("test",   560, 90, 130, 60, "LLM\nTest Runner",     LPURP, PURP),
        ("store",  730, 90, 130, 60, "SQLite\nVersion Store",LRED,  RED),
        ("export", 730,200, 130, 60, "Multi-Format\nExport", LTEAL, TEAL),
        ("b1",      40,210, 120, 35, "system blocks",        LGREY, GREY),
        ("b2",      40,255, 120, 35, "user blocks",          LGREY, GREY),
        ("b3",     170,210, 120, 35, "tiktoken GPT-4o",      LGREY, GREY),
        ("b4",     170,255, 120, 35, "Claude tokenizer",     LGREY, GREY),
        ("b5",     300,210, 120, 35, "sem similarity gate",  LGREY, GREY),
        ("e1",     730,270, 120, 30, "OpenAI format",        LGREY, GREY),
        ("e2",     730,310, 120, 30, "Anthropic format",     LGREY, GREY),
        ("e3",     730,350, 120, 30, "LangChain format",     LGREY, GREY),
    ]
    seed = 17000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",180,120,220,120),("a2",350,120,380,120),
                              ("a3",520,120,560,120),("a4",690,120,730,120),
                              ("a5",795,150,795,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("contextcraft-prompt-workbench", els)


# ── 17. pipelinescope-llm-pipeline-debugger ───────────────────────────────────
def d_pipelinescope():
    els = title_el("PipelineScope: LLM Pipeline Debugger", "Context/RAG/agent/proxy debugger — 4 layers, visual DAG, SQLite, WebSocket, no cloud required")
    rows = [
        ("proxy",  40,  90, 130, 60, "LLM Proxy\n(port 8001)", LAMB, AMBE),
        ("ctx",    210, 60, 130, 55, "Context\nExplorer",      LBLUE, SBLU),
        ("rag",    210,125, 130, 55, "RAG\nExplorer",          LGRN,  GREEN),
        ("agent",  210,190, 130, 55, "Agent\nExplorer",        LPURP, PURP),
        ("core",   390, 90, 140, 60, "Pipeline\nDebugger Core",LRED,  RED),
        ("sqlite", 570, 90, 130, 60, "SQLite\nStore",          LTEAL, TEAL),
        ("ws",     570,200, 130, 60, "WebSocket\nStreaming",    LBLUE, SBLU),
        ("ui",     750, 90, 130, 60, "React\nDashboard",       LAMB,  AMBE),
        ("f1",      40,240, 120, 30, "OpenAI calls",           LGREY, GREY),
        ("f2",      40,280, 120, 30, "Anthropic calls",        LGREY, GREY),
        ("f3",      40,320, 120, 30, "Ollama calls",           LGREY, GREY),
        ("v1",     570,280, 120, 30, "token heatmap",          LGREY, GREY),
        ("v2",     570,320, 120, 30, "DAG graph",              LGREY, GREY),
        ("v3",     570,360, 120, 30, "waterfall chart",        LGREY, GREY),
    ]
    seed = 18000
    for bid,x,y,w,h,lbl,bg,stroke in rows:
        els.append(rect(bid,x,y,w,h,lbl,stroke,bg,seed)); seed+=10
        els.append(txt(f"{bid}_t",x+5,y+h//2-8,w-10,20,lbl,font_size=9))
    for aid,x1,y1,x2,y2 in [("a1",170, 88,210, 88),("a2",170,152,210,152),
                              ("a3",170,217,210,217),("a4",340,120,390,120),
                              ("a5",340,152,390,152),("a6",340,217,390,217),
                              ("a7",530,120,570,120),("a8",700,120,750,120),
                              ("a9",635,150,635,200)]:
        els.append(arrow(aid,x1,y1,x2,y2,seed)); seed+=10
    save("pipelinescope-llm-pipeline-debugger", els)


if __name__ == "__main__":
    print("Generating .excalidraw files...")
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
    print("Done — 17 .excalidraw files written.")
