#!/usr/bin/env python3
"""
Render the manuscript to a preprint-style PDF (reportlab).

Layout follows arXiv/SSRN single-column preprint convention: Times text, a
vertical identifier stamp down the left edge of page 1, DOI block, abstract
panel, numbered sections, floated figures with captions, booktabs-style rules.
"""
import os, re, sys, importlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, KeepTogether,
                                HRFlowable)

LANG = os.environ.get("PAPER_LANG", "en").lower()
C = importlib.import_module("paper_content" if LANG == "en"
                            else f"paper_content_{LANG}")

# per-language furniture, with English defaults
L_ABS = C.META.get("abstract_head", "ABSTRACT")
L_KW = C.META.get("kw_label", "Keywords")
L_FIG = C.META.get("fig_label", "Figure")
L_TAB = C.META.get("tab_label", "Table")
L_RUN = C.META.get("running", "Escoda · The Half-Life of Compute")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "06-SUBMISSION"))
EQD = os.path.join(HERE, "_eq", LANG)
os.makedirs(OUT, exist_ok=True); os.makedirs(EQD, exist_ok=True)

# ── fonts ────────────────────────────────────────────────────────────────────
SUP = "/System/Library/Fonts/Supplemental"
try:
    pdfmetrics.registerFont(TTFont("TNR", f"{SUP}/Times New Roman.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-B", f"{SUP}/Times New Roman Bold.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-I", f"{SUP}/Times New Roman Italic.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-BI", f"{SUP}/Times New Roman Bold Italic.ttf"))
    pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-B",
                                  italic="TNR-I", boldItalic="TNR-BI")
    BASE, BOLD, ITAL = "TNR", "TNR-B", "TNR-I"
except Exception:
    BASE, BOLD, ITAL = "Times-Roman", "Times-Bold", "Times-Italic"

INK = colors.HexColor("#111111")
GREY = colors.HexColor("#6b6b6b")
LGREY = colors.HexColor("#9a9a9a")
RULE = colors.HexColor("#333333")
ACCENT = colors.HexColor("#8c2d04")

PW, PH = A4
LM = RM = 27 * mm
TM, BM = 22 * mm, 20 * mm
CW = PW - LM - RM

# ── inline markup → reportlab rich text ──────────────────────────────────────
GREEK = {r"\lambda": "λ", r"\kappa": "κ", r"\delta": "δ",
         r"\sigma": "σ", r"\rho": "ρ", r"\alpha": "α",
         r"\beta": "β", r"\mu": "μ", r"\theta": "θ", r"\infty": "∞",
         r"\approx": "≈", r"\simeq": "≈", r"\geq": "≥", r"\leq": "≤",
         r"\times": "×", r"\cdot": "·", r"\in": "∈", r"\Delta": "Δ",
         r"\log": " log", r"\ln": " ln", r"\min": "min",
         r"\bigl": "", r"\bigr": "",
         r"\,": " ", r"\;": " ", r"\!": "", r"\mathrm": "", r"\left": "",
         r"\right": ""}


_TAGS = re.compile(r"</?(?:super|sub)>")


def _script(tag, body):
    """reportlab cannot nest <super>/<sub>; flatten any inner scripts."""
    return f"<{tag}>{_TAGS.sub('', body)}</{tag}>"


def _inline_math(m):
    s = m.group(1)
    for k, v in GREEK.items():
        s = s.replace(k, v)
    # resolve innermost braces first so nesting never produces crossed tags
    for _ in range(6):
        new = re.sub(r"\^\{([^{}]*)\}", lambda x: _script("super", x.group(1)), s)
        new = re.sub(r"_\{([^{}]*)\}", lambda x: _script("sub", x.group(1)), new)
        if new == s:
            break
        s = new
    # single-character scripts; \w misses symbols such as ∞, so allow any
    # non-space, non-brace character
    s = re.sub(r"\^([^\s{}^_])", lambda x: _script("super", x.group(1)), s)
    s = re.sub(r"_([^\s{}^_])", lambda x: _script("sub", x.group(1)), s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return f'<font face="{ITAL}">{s}</font>'


def rt(t):
    """Markdown-ish + inline LaTeX → reportlab markup.

    Math is extracted to placeholders BEFORE markdown runs, otherwise a `*` in
    an exponent (e.g. $\\kappa^{*}$) is mis-read as an italic delimiter.
    """
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    stash = []

    def _hold(m):
        stash.append(_inline_math(m))
        return f"\x00{len(stash)-1}\x00"

    t = re.sub(r"\$([^$]+)\$", _hold, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], t)


# ── display equations rendered via matplotlib mathtext ───────────────────────
def eq_lines(tex):
    """mathtext has no `aligned` environment, split into standalone lines."""
    t = tex.replace(r"\begin{aligned}", "").replace(r"\end{aligned}", "")
    t = t.replace(r"\qquad", r"\ \ \ \ ").replace(r"\quad", r"\ \ ")
    parts = [p.strip() for p in t.split(r"\\") if p.strip()]
    return [p.replace("&", "") for p in parts]


def eq_png(tex, key):
    p = os.path.join(EQD, f"eq_{key}.png")
    if os.path.exists(p):
        return p
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${tex}$", fontsize=15, math_fontfamily="stix")
    fig.savefig(p, dpi=420, bbox_inches="tight", pad_inches=0.06,
                transparent=True)
    plt.close(fig)
    return p


# ── styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(name=name, fontName=BASE, fontSize=10, leading=13.6,
                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(**base)


st_title = S("t", fontName=BOLD, fontSize=17, leading=21, alignment=TA_CENTER, spaceAfter=9)
st_auth = S("a", fontSize=11.5, leading=14, alignment=TA_CENTER, spaceAfter=2)
st_aff = S("af", fontName=ITAL, fontSize=9.2, leading=11.6, alignment=TA_CENTER,
           textColor=GREY, spaceAfter=1)
st_date = S("dt", fontSize=8.8, leading=11, alignment=TA_CENTER, textColor=GREY, spaceAfter=10)
st_abshd = S("ah", fontName=BOLD, fontSize=9.4, leading=12, alignment=TA_CENTER, spaceAfter=4)
st_abs = S("ab", fontSize=9.2, leading=12.4)
st_meta = S("mt", fontSize=8.6, leading=11.4, textColor=GREY)
st_h1 = S("h1", fontName=BOLD, fontSize=11.8, leading=14.5, spaceAfter=4, alignment=TA_LEFT)
st_h2 = S("h2", fontName="TNR-BI" if BASE == "TNR" else "Times-BoldItalic",
          fontSize=10.4, leading=13, spaceAfter=3, alignment=TA_LEFT)
st_p = S("p", firstLineIndent=0, spaceAfter=6)
st_bul = S("b", leftIndent=11, bulletIndent=2, spaceAfter=3.4)
st_quote = S("q", fontName=ITAL, fontSize=10, leading=13.6, leftIndent=14,
             rightIndent=14, textColor=RULE, spaceAfter=6)
st_cap = S("c", fontSize=8.5, leading=11, alignment=TA_LEFT, textColor=INK, spaceAfter=2)
st_note = S("n", fontSize=7.9, leading=10.2, textColor=GREY, spaceAfter=2)
st_cell = S("tc", fontSize=8.2, leading=10.4, alignment=TA_LEFT, spaceAfter=0)
st_cellh = S("tch", fontName=BOLD, fontSize=8.2, leading=10.4, alignment=TA_LEFT)
st_ref = S("r", fontSize=8.7, leading=11.2, leftIndent=11, firstLineIndent=-11,
           spaceAfter=3.6)


# ── page furniture ───────────────────────────────────────────────────────────
def stamp_first(canvas, doc):
    """Vertical preprint identifier down the left edge, arXiv convention.

    Drawn on page 1 only; the template does not auto-switch, so gate on the
    page number rather than relying on a NextPageTemplate flowable.
    """
    _footer(canvas, doc)


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(BASE, 8.2); canvas.setFillColor(GREY)
    canvas.drawCentredString(PW / 2, BM - 9 * mm, str(canvas.getPageNumber()))
    if canvas.getPageNumber() > 1:
        canvas.setFont(BASE, 7.6); canvas.setFillColor(LGREY)
        canvas.drawString(LM, PH - TM + 5 * mm, L_RUN)
        canvas.drawRightString(PW - RM, PH - TM + 5 * mm, C.META["date"])
    canvas.restoreState()


def later(canvas, doc):
    _footer(canvas, doc)


# ── flowable builders ────────────────────────────────────────────────────────
def fig_flow(path, caption, label):
    if not os.path.exists(path):
        return [Paragraph(rt(f"*[missing figure: {os.path.basename(path)}]*"), st_note)]
    from PIL import Image as PILImage
    try:
        w, h = PILImage.open(path).size
    except Exception:
        w, h = 1100, 620
    tw = CW * 0.86
    img = Image(path, width=tw, height=tw * h / w)
    cap = Paragraph(f'<font face="{BOLD}">{L_FIG} {label}.</font> {rt(caption)}', st_cap)
    return [Spacer(1, 5), KeepTogether([img, Spacer(1, 3.5), cap]), Spacer(1, 8)]


def table_flow(caption, label, headers, rows, note):
    head = Paragraph(f'<font face="{BOLD}">{L_TAB} {label}.</font> {rt(caption)}', st_cap)
    data = [[Paragraph(rt(h), st_cellh) for h in headers]]
    for r in rows:
        data.append([Paragraph(rt(str(c)), st_cell) for c in r])
    ncol = len(headers)
    if ncol == 5 and label == "3":
        # partial-severance table: long regime names in column 0
        widths = [CW * x for x in (.26, .17, .19, .14, .24)]
    elif ncol == 5:
        widths = [CW * x for x in (.11, .245, .12, .155, .37)]
    elif ncol == 6:
        widths = [CW * x for x in (.155, .125, .195, .18, .215, .13)]
    else:
        widths = [CW / ncol] * ncol
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#fafafa")]),
    ]))
    out = [Spacer(1, 5), head, Spacer(1, 3), t]
    if note:
        out += [Spacer(1, 2.5), Paragraph(rt(note), st_note)]
    return [KeepTogether(out), Spacer(1, 8)]


def eq_flow(tex, label):
    from PIL import Image as PILImage
    lines = eq_lines(tex)
    rows = []
    for i, ln in enumerate(lines):
        p = eq_png(ln, f"{label.replace('.', '_')}_{i}")
        w, h = PILImage.open(p).size
        scale = 0.30
        if w * scale > CW * 0.78:
            scale = CW * 0.78 / w
        img = Image(p, width=w * scale, height=h * scale)
        tag = Paragraph(f"({label})", st_cell) if i == len(lines) - 1 else Paragraph("", st_cell)
        rows.append([img, tag])
    t = Table(rows, colWidths=[CW * 0.86, CW * 0.14], hAlign="CENTER")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ALIGN", (0, 0), (0, -1), "CENTER"),
                           ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    return [Spacer(1, 4), KeepTogether(t), Spacer(1, 7)]


# ── document ─────────────────────────────────────────────────────────────────
def build(path):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title=C.META["title"], author=C.META["authors"],
                          subject="Compute governance; export controls",
                          keywords=C.META["keywords"])
    frame = Frame(LM, BM, CW, PH - TM - BM, id="f", leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[frame], onPage=stamp_first),
        PageTemplate(id="rest", frames=[frame], onPage=later)])

    F = []
    M = C.META
    F += [Paragraph(rt(M["title"]), st_title),
          Paragraph(f'{M["authors"]}<super>1</super>', st_auth),
          Paragraph(f'<super>1</super> {M["affiliation"]} · {M["email"]}', st_aff),
          Paragraph(f'ORCID {M["orcid"]}', st_aff),
          Paragraph(M["date"], st_date)]

    # DOI / identifier block
    doi = Table([[Paragraph(
        f'<font face="{BOLD}">DOI</font>&nbsp;&nbsp;{M["doi"]}', st_meta)]],
        colWidths=[CW], hAlign="CENTER")
    doi.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.HexColor("#cccccc")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    F += [doi, Spacer(1, 11)]

    # abstract panel
    ab = Table([[Paragraph(L_ABS, st_abshd)],
                [Paragraph(rt(C.ABSTRACT), st_abs)]],
               colWidths=[CW * 0.92], hAlign="CENTER")
    ab.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 7), ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f7f5")),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE)]))
    F += [ab, Spacer(1, 7)]
    F += [Paragraph(f'<font face="{BOLD}">{L_KW}</font> &nbsp;{rt(M["keywords"])}', st_meta),
          Spacer(1, 2),
          Paragraph(f'<font face="{BOLD}">JEL</font> &nbsp;{M["jel"]}'
                    f'&nbsp;&nbsp;·&nbsp;&nbsp;<font face="{BOLD}">ACM CCS</font> '
                    f'&nbsp;{M["acm"]}', st_meta),
          Spacer(1, 12)]

    for blk in C.ALL:
        kind = blk[0]
        if kind == "h1":
            F += [Spacer(1, 8), Paragraph(rt(blk[1]), st_h1),
                  HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"),
                             spaceBefore=1, spaceAfter=5)]
        elif kind == "h2":
            F += [Spacer(1, 4), Paragraph(rt(blk[1]), st_h2)]
        elif kind == "p":
            F += [Paragraph(rt(blk[1]), st_p)]
        elif kind == "quote":
            F += [Spacer(1, 2),
                  Table([[Paragraph(rt(blk[1]), st_quote)]], colWidths=[CW],
                        style=TableStyle([
                            ("LINEBEFORE", (0, 0), (0, 0), 2, ACCENT),
                            ("LEFTPADDING", (0, 0), (-1, -1), 10),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)])),
                  Spacer(1, 7)]
        elif kind == "bullets":
            for it in blk[1]:
                F += [Paragraph(rt(it), st_bul, bulletText="•")]
            F += [Spacer(1, 4)]
        elif kind == "numbers":
            for i, it in enumerate(blk[1], 1):
                F += [Paragraph(rt(it), st_bul, bulletText=f"{i}.")]
            F += [Spacer(1, 4)]
        elif kind == "eq":
            F += eq_flow(blk[1], blk[2])
        elif kind == "fig":
            F += fig_flow(blk[1], blk[2], blk[3])
        elif kind == "table":
            F += table_flow(blk[1], blk[2], blk[3], blk[4], blk[5])
        elif kind == "refs":
            for r in blk[1]:
                F += [Paragraph(rt(r), st_ref)]

    doc.build(F)
    return path


STEM = {"en": "Escoda-2026-Half-Life-of-Compute-preprint",
        "it": "Escoda-2026-Emivita-del-Calcolo-preprint-IT",
        "fr": "Escoda-2026-Demi-Vie-du-Calcul-preprint-FR"}

if __name__ == "__main__":
    p = build(os.path.join(OUT, f"{STEM.get(LANG, 'paper-' + LANG)}.pdf"))
    print(f"PDF [{LANG}] →", p, f"({os.path.getsize(p)/1024:.0f} KB)")
