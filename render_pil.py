#!/usr/bin/env python3
"""Pure-Python Excalidraw -> PNG renderer using Pillow.
Handles the subset of element types we use: rectangle, ellipse, diamond, line, arrow, text.
Not feature-complete with Excalidraw, but covers our diagrams cleanly."""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

PAD = 30
SCALE = 2  # 2x supersample for crisp output

_font_cache = {}
def get_font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _font_cache:
        path = (FONT_MONO_BOLD if bold else FONT_MONO) if mono else (FONT_BOLD if bold else FONT_REG)
        _font_cache[key] = ImageFont.truetype(path, int(size*SCALE))
    return _font_cache[key]

def hex_to_rgba(h, alpha=255):
    if not h or h == "transparent": return (0,0,0,0)
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c+c for c in h)
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return (r,g,b,alpha)

def bbox(elements):
    minx, miny, maxx, maxy = 1e9, 1e9, -1e9, -1e9
    for el in elements:
        if el.get("isDeleted"): continue
        x = el.get("x", 0); y = el.get("y", 0)
        w = el.get("width", 0); h = el.get("height", 0)
        if el.get("type") in ("arrow","line") and "points" in el:
            for px,py in el["points"]:
                minx = min(minx, x+px); miny = min(miny, y+py)
                maxx = max(maxx, x+px); maxy = max(maxy, y+py)
        else:
            minx = min(minx, x); miny = min(miny, y)
            maxx = max(maxx, x+w); maxy = max(maxy, y+h)
    return minx, miny, maxx, maxy

def wrap_text(draw, text, font, max_width):
    """Wrap text into lines that fit within max_width."""
    paragraphs = text.split("\n")
    lines = []
    for para in paragraphs:
        if not para:
            lines.append("")
            continue
        words = para.split(" ")
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=font) <= max_width:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    return lines

def render(infile, outfile=None):
    with open(infile) as f:
        doc = json.load(f)
    elements = [e for e in doc["elements"] if not e.get("isDeleted")]
    minx, miny, maxx, maxy = bbox(elements)
    W = int((maxx - minx + 2*PAD) * SCALE)
    H = int((maxy - miny + 2*PAD) * SCALE)
    ox, oy = -minx + PAD, -miny + PAD
    bg = hex_to_rgba(doc.get("appState",{}).get("viewBackgroundColor", "#ffffff"))
    img = Image.new("RGBA", (W,H), bg)
    draw = ImageDraw.Draw(img)

    def sx(v): return int((v + ox) * SCALE)
    def sy(v): return int((v + oy) * SCALE)
    def sw(v): return max(1, int(v * SCALE))

    # Build container id -> child text mapping
    text_by_container = {}
    for el in elements:
        if el.get("type") == "text" and el.get("containerId"):
            text_by_container[el["containerId"]] = el

    # Z-order: rectangles/ellipses/diamonds first, then lines/arrows, then text
    shape_types = {"rectangle","ellipse","diamond"}
    shapes = [e for e in elements if e.get("type") in shape_types]
    lines = [e for e in elements if e.get("type") in ("line","arrow")]
    texts = [e for e in elements if e.get("type") == "text"]

    for el in shapes:
        x, y = el["x"], el["y"]; w, h = el["width"], el["height"]
        fill = hex_to_rgba(el.get("backgroundColor","transparent"))
        stroke = hex_to_rgba(el.get("strokeColor","#000000"))
        sw_ = sw(el.get("strokeWidth", 2))
        dashed = el.get("strokeStyle") == "dashed"
        x0, y0, x1, y1 = sx(x), sy(y), sx(x+w), sy(y+h)
        if el["type"] == "rectangle":
            r = 12*SCALE if el.get("roundness") else 0
            try:
                draw.rounded_rectangle([x0,y0,x1,y1], radius=r, fill=fill, outline=stroke, width=sw_)
            except Exception:
                draw.rectangle([x0,y0,x1,y1], fill=fill, outline=stroke, width=sw_)
        elif el["type"] == "ellipse":
            draw.ellipse([x0,y0,x1,y1], fill=fill, outline=stroke, width=sw_)
        elif el["type"] == "diamond":
            cx, cy = (x0+x1)/2, (y0+y1)/2
            pts = [(cx, y0), (x1, cy), (cx, y1), (x0, cy)]
            draw.polygon(pts, fill=fill, outline=stroke)
            # widen outline
            for i in range(len(pts)):
                a = pts[i]; b = pts[(i+1)%len(pts)]
                draw.line([a,b], fill=stroke, width=sw_)
        if dashed:
            # overlay a dashed outline (best-effort)
            pass

    def draw_dashed_line(p1, p2, color, width, dash=8, gap=6):
        x1,y1=p1; x2,y2=p2
        import math
        dx, dy = x2-x1, y2-y1
        L = math.hypot(dx,dy)
        if L==0: return
        ux, uy = dx/L, dy/L
        d=0
        while d < L:
            a = (x1 + ux*d, y1 + uy*d)
            b_d = min(d+dash, L)
            b = (x1 + ux*b_d, y1 + uy*b_d)
            draw.line([a,b], fill=color, width=width)
            d += dash + gap

    for el in lines:
        pts = el.get("points", [[0,0],[el["width"], el["height"]]])
        absp = [(sx(el["x"]+px), sy(el["y"]+py)) for px,py in pts]
        stroke = hex_to_rgba(el.get("strokeColor","#000000"))
        w_ = sw(el.get("strokeWidth", 1.5))
        dashed = el.get("strokeStyle") == "dashed"
        for i in range(len(absp)-1):
            if dashed:
                draw_dashed_line(absp[i], absp[i+1], stroke, w_)
            else:
                draw.line([absp[i], absp[i+1]], fill=stroke, width=w_)
        # arrowhead
        if el.get("type") == "arrow" and len(absp) >= 2:
            import math
            x1,y1 = absp[-2]; x2,y2 = absp[-1]
            ang = math.atan2(y2-y1, x2-x1)
            ah = 10*SCALE
            spread = 0.5
            p1 = (x2 - ah*math.cos(ang-spread), y2 - ah*math.sin(ang-spread))
            p2 = (x2 - ah*math.cos(ang+spread), y2 - ah*math.sin(ang+spread))
            draw.polygon([(x2,y2), p1, p2], fill=stroke)

    for el in texts:
        x, y = el["x"], el["y"]; w, h = el["width"], el["height"]
        size = el.get("fontSize", 12)
        bold = el.get("fontStyle") == "bold"
        color = hex_to_rgba(el.get("strokeColor","#000000"))
        text = el.get("text","")
        align = el.get("textAlign","left")
        valign = el.get("verticalAlign","top")
        # use mono font for evidence (dark bg) and code-looking text
        bg_attr = el.get("backgroundColor","transparent")
        mono = False  # default proportional
        # Detect evidence panels by checking if container has dark bg
        container_id = el.get("containerId")
        font = get_font(size, bold=bold, mono=mono)
        # Wrapping
        wrap_w = (w if w > 10 else 9999) * SCALE - 8
        lines_ = wrap_text(draw, text, font, wrap_w)
        line_h = size * SCALE * 1.25
        total_h = line_h * len(lines_)
        if valign == "middle":
            cy = sy(y) + (h*SCALE - total_h)/2
        elif valign == "bottom":
            cy = sy(y+h) - total_h
        else:
            cy = sy(y) + 4
        for line in lines_:
            tw = draw.textlength(line, font=font)
            if align == "center":
                tx = sx(x) + (w*SCALE - tw)/2
            elif align == "right":
                tx = sx(x+w) - tw - 4
            else:
                tx = sx(x) + 4
            draw.text((tx, cy), line, fill=color, font=font)
            cy += line_h

    # Downsample for crispness
    final_w, final_h = W//SCALE, H//SCALE
    final = img.resize((final_w, final_h), Image.LANCZOS)
    if outfile is None:
        outfile = os.path.splitext(infile)[0] + ".png"
    final.save(outfile, "PNG")
    print(f"wrote {outfile}  ({final_w}x{final_h})")

if __name__ == "__main__":
    for path in sys.argv[1:]:
        render(path)
