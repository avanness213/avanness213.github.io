# -*- coding: utf-8 -*-
"""Build public/AlexanderVanNessResume.pdf from resume_content.py.

Layout (top-left origin, points, US Letter 612x792):
  text column 52.8 -> 559.2, bottom limit 739.2
  name Inter-Bold 20 #111111 centered @ 42.6
  target line Inter-SemiBold 8 #23787A centered @ 66.0
  contact Inter-Regular 8.5 #888888 centered @ 79.0
  rules 0.5pt #DDDDDD                             section heads Inter-SemiBold 8 #444444
  company Inter-SemiBold 10 #111111               meta Inter-Italic 8.5 #888888
  body Inter-Regular 8.8 #1F1F1F, leading 13 (13.5 in summary), 3pt between paragraphs
  bullets: en dash + space at 52.8, wrapped lines hang to 66.8

Sections flow top to bottom; the build prints the last baseline and remaining slack and
warns on OVERFLOW. The resume must stay one page — tighten wording, never the type.
"""
import os
import sys

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from resume_content import (  # noqa: E402
    NAME, CONTACT, TARGET, SUMMARY, CORE_SKILLS, JOBS, CREDENTIALS, TECHNOLOGY, BULLET,
)

REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DEFAULT_OUT = os.path.join(REPO_ROOT, "public", "AlexanderVanNessResume.pdf")
OUT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT

PAGE_W, PAGE_H = 612.0, 792.0
LEFT, RIGHT = 52.8, 559.2
CENTER = PAGE_W / 2
BOTTOM_LIMIT = PAGE_H - 52.8

REG, ITAL, SEMI, BOLD = "Inter-Regular", "Inter-Italic", "Inter-SemiBold", "Inter-Bold"
for name in (REG, ITAL, SEMI, BOLD):
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, "fonts", name + ".ttf")))

INK = HexColor("#111111")
BODY = HexColor("#1F1F1F")
HEAD = HexColor("#444444")
MUTED = HexColor("#888888")
ACCENT = HexColor("#23787A")
RULE = HexColor("#DDDDDD")

BODY_SIZE, BODY_LEAD = 8.8, 13.0
SUMMARY_LEAD = 13.5
PARA_GAP = 3.0            # extra space between paragraphs / bullets
HANG = 14.0               # wrapped-line indent for bullets
SECTION_GAP = 20.0        # space before a section heading
HEAD_TO_BODY = 17.6       # heading top -> first body line top
ASCENT = 0.9688           # Inter hhea ascent, used to map span-top -> baseline

c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))
c.setTitle(f"{NAME} — Resume")
c.setAuthor(NAME)
c.setSubject("Resume")


def baseline(y_top, size):
    return PAGE_H - (y_top + ASCENT * size)


def text(s, y_top, x=LEFT, font=REG, size=BODY_SIZE, color=BODY, centered=False):
    c.setFont(font, size)
    c.setFillColor(color)
    if centered:
        c.drawCentredString(CENTER, baseline(y_top, size), s)
    else:
        c.drawString(x, baseline(y_top, size), s)


def rule(y_top):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(LEFT, PAGE_H - y_top, RIGHT, PAGE_H - y_top)


def wrap(words, width, font=REG, size=BODY_SIZE):
    """Greedy wrap; returns (line, remaining_words)."""
    line = ""
    while words:
        trial = (line + " " + words[0]).strip()
        if pdfmetrics.stringWidth(trial, font, size) > width and line:
            break
        line = trial
        words = words[1:]
    return line, words


def paragraph(body, y_top, x=LEFT, width=None, lead=BODY_LEAD, font=REG, size=BODY_SIZE, color=BODY):
    width = width if width is not None else RIGHT - x
    words = body.split()
    y = y_top
    while words:
        line, words = wrap(words, width, font, size)
        text(line, y, x=x, font=font, size=size, color=color)
        if words:
            y += lead
    return y


def bullet(body, y_top):
    """En-dash bullet at LEFT; first line shares that line, wraps hang to LEFT+HANG."""
    prefix = BULLET + " "
    first_x = LEFT + pdfmetrics.stringWidth(prefix, REG, BODY_SIZE)
    text(prefix, y_top)
    words = body.split()
    line, words = wrap(words, RIGHT - first_x)
    text(line, y_top, x=first_x)
    y = y_top
    if words:
        y = paragraph(" ".join(words), y_top + BODY_LEAD, x=LEFT + HANG, width=RIGHT - (LEFT + HANG))
    return y


def section(title, y):
    """Draw a section heading at y (top); return the top of the first body line."""
    text(title, y, font=SEMI, size=8, color=HEAD)
    rule(y + 13.2)
    return y + HEAD_TO_BODY


def lines(items, y):
    for i, line in enumerate(items):
        if i:
            y += BODY_LEAD + PARA_GAP
        y = paragraph(line, y)
    return y


# ── Header ──
text(NAME, 42.6, font=BOLD, size=20, color=INK, centered=True)
text(TARGET, 66.0, font=SEMI, size=8, color=ACCENT, centered=True)
text(CONTACT, 79.0, font=REG, size=8.5, color=MUTED, centered=True)
rule(97.5)

# ── Summary ──
y = section("SUMMARY", 105.8)
y = paragraph(SUMMARY, y, lead=SUMMARY_LEAD)

# ── Core skills ──
y = section("CORE SKILLS", y + SECTION_GAP)
y = lines(CORE_SKILLS, y)

# ── Experience ──
y = section("EXPERIENCE", y + SECTION_GAP)
y += 2.0
for i, (company, meta, bullets) in enumerate(JOBS):
    if i:
        y += 17.0
    text(company, y, font=SEMI, size=10, color=INK)
    text(meta, y + 14.0, font=ITAL, size=8.5, color=MUTED)
    y += 14.0 + 16.0
    for j, b in enumerate(bullets):
        if j:
            y += BODY_LEAD + PARA_GAP
        y = bullet(b, y)

# ── Credentials ──
y = section("CREDENTIALS", y + SECTION_GAP)
y = lines(CREDENTIALS, y)

# ── Technology ──
y = section("TECHNOLOGY", y + SECTION_GAP)
y = lines(TECHNOLOGY, y)

overflow = (y + ASCENT * BODY_SIZE) - BOTTOM_LIMIT
print(f"last baseline top: {y:.1f}   bottom limit: {BOTTOM_LIMIT:.1f}   "
      f"{'OVERFLOW ' + format(overflow, '.1f') if overflow > 0 else 'fits (' + format(-overflow, '.1f') + 'pt slack)'}")

c.showPage()
c.save()
print("wrote", OUT, os.path.getsize(OUT), "bytes")
if overflow > 0:
    sys.exit(1)
