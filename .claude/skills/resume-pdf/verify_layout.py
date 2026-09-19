# -*- coding: utf-8 -*-
"""Verify the built resume PDF against the layout contract.

Usage: python verify_layout.py [path-to.pdf]
Requires PyMuPDF (`pip install pymupdf`). Exits non-zero if any check fails.
"""
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO_ROOT, "public", "AlexanderVanNessResume.pdf")

# (text prefix, expected span top in points) — fixed header anchors.
ANCHORS = [
    ("Alexander Van Ness", 42.6),
    ("PATIENT SUCCESS", 66.0),
    ("Avanness213@gmail.com", 79.0),
    ("SUMMARY", 105.8),
    ("Licensed Massage Therapist and", 123.4),
]
REQUIRED_HEADINGS = ["SUMMARY", "CORE SKILLS", "EXPERIENCE", "CREDENTIALS", "TECHNOLOGY"]
RULES = [97.5, 119.0]
BOTTOM_LIMIT = 739.2      # 792 - 52.8 bottom margin
TOLERANCE = 0.15

doc = fitz.open(PDF)
failures = []

if doc.page_count != 1:
    failures.append(f"expected 1 page, got {doc.page_count}")

page = doc[0]
if tuple(round(v, 1) for v in page.rect[2:]) != (612.0, 792.0):
    failures.append(f"expected 612x792 page, got {page.rect}")

spans = []
for block in page.get_text("dict")["blocks"]:
    for line in block.get("lines", []):
        for span in line["spans"]:
            spans.append((span["text"], span["bbox"][0], span["bbox"][1], span["font"], span["size"]))

for prefix, expected_top in ANCHORS:
    hit = next((s for s in spans if s[0].startswith(prefix)), None)
    if hit is None:
        failures.append(f"missing text: {prefix!r}")
    elif abs(hit[2] - expected_top) > TOLERANCE:
        failures.append(f"{prefix!r} at y={hit[2]:.2f}, expected {expected_top}")

for heading in REQUIRED_HEADINGS:
    if not any(s[0] == heading for s in spans):
        failures.append(f"missing section heading: {heading}")

rules = sorted(round(d["items"][0][1].y, 1) for d in page.get_drawings() if d["items"][0][0] == "l")
for expected in RULES:
    if not any(abs(expected - r) <= TOLERANCE for r in rules):
        failures.append(f"missing rule at y={expected} (found {rules})")
if len(rules) != 1 + len(REQUIRED_HEADINGS):
    failures.append(f"expected {1 + len(REQUIRED_HEADINGS)} rules, found {len(rules)}")

last = max(s[2] + s[4] for s in spans)
if last > BOTTOM_LIMIT:
    failures.append(f"content overflows bottom margin: last line at {last:.1f} > {BOTTOM_LIMIT}")

right_edge = max(s[1] for s in spans)
if right_edge > 559.2 + 1:
    failures.append(f"text starts beyond the right column edge: {right_edge:.1f}")

fonts = {s[3] for s in spans}
unexpected = {f for f in fonts if "Inter" not in f}
if unexpected:
    failures.append(f"non-Inter fonts in use: {sorted(unexpected)}")

print(f"{PDF}\n  pages={doc.page_count} spans={len(spans)} rules={rules} "
      f"last_line={last:.1f} (limit {BOTTOM_LIMIT}) fonts={sorted(fonts)}")
if failures:
    print("\nFAILED:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("\nOK — layout matches the contract.")
