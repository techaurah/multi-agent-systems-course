#!/usr/bin/env python3
"""Generate the course's SVG visuals.

White canvas, navy headings, cyan accents, measured numbers only.
Every figure quoted in a visual is produced by the course's own code
on the bundled fixtures (see the lesson cited in each subtitle).
Run: python3 generate_visuals.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = "#0B1F4A"
CYAN = "#0891B2"
LIGHT = "#E0F2FE"
AMBER = "#F59E0B"
GREY = "#475569"
RED = "#DC2626"
GREEN = "#059669"


def save(name, svg):
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", name)


def head(w, h, title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" fill="white"/>
<text x="48" y="64" font-family="Georgia, serif" font-size="30" fill="{NAVY}" font-weight="bold">{title}</text>
<text x="48" y="94" font-family="Georgia, serif" font-size="16" fill="{GREY}">{subtitle}</text>
'''


def foot(w, h, text):
    return f'''<text x="48" y="{h - 24}" font-family="Georgia, serif" font-size="13" fill="{GREY}">{text}</text>
</svg>'''


def box(x, y, w, h, fill, title, lines, tcolor="white", size=15):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>']
    out.append(f'<text x="{x + w/2}" y="{y + 30}" text-anchor="middle" font-family="Georgia, serif" font-size="{size}" fill="{tcolor}" font-weight="bold">{title}</text>')
    for i, line in enumerate(lines):
        out.append(f'<text x="{x + w/2}" y="{y + 54 + i*20}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{tcolor}">{line}</text>')
    return "\n".join(out)


def arrow(x1, y, x2, color=CYAN):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="3"/>'
            f'<polygon points="{x2},{y} {x2-10},{y-6} {x2-10},{y+6}" fill="{color}"/>')


# 1. Course map ------------------------------------------------------------
modules = [
    ("Module 0", "Foundations", "Lessons 00-02"),
    ("Module 1", "One agent first", "Lessons 03-05"),
    ("Module 2", "Topologies", "Lessons 06-09"),
    ("Module 3", "Communication", "Lessons 10-13"),
    ("Module 4", "State and memory", "Lessons 14-16"),
    ("Module 5", "Failure modes", "Lessons 17-20"),
    ("Module 6", "Verification and safety", "Lessons 21-23"),
    ("Module 7", "Cost and scaling", "Lessons 24-26"),
    ("Module 8", "Evaluation", "Lessons 27-28"),
    ("Module 9", "Capstone", "Lessons 29-31"),
]
svg = head(1000, 560, "Multi-Agent Systems: course map",
           "32 lessons, 10 modules, one measured capstone. Every claim runs on bundled fixtures.")
for i, (tag, name, lessons) in enumerate(modules):
    x = 48 + (i % 5) * 184
    y = 140 + (i // 5) * 170
    fill = NAVY if i in (0, 9) else CYAN
    svg += box(x, y, 168, 120, fill, tag, [name, lessons])
svg += foot(1000, 560, "Start at Lesson 00. The capstone gates are fixed in Lesson 29, before the system is built in Lesson 30.")
save("course-map.svg", svg)

# 2. Topology family ---------------------------------------------------------
svg = head(960, 520, "Five ways to arrange agents",
           "Successes on the 12-order Fernhill set, from Lessons 06 to 13.")
svg += box(48, 150, 160, 110, NAVY, "Sequential", ["pipeline", "10 of 12 with review"])
svg += box(232, 150, 160, 110, CYAN, "Parallel", ["fan-out batch", "makespan priced"])
svg += box(416, 150, 160, 110, CYAN, "Hierarchical", ["delegation tax", "7 of 12"])
svg += box(600, 150, 160, 110, CYAN, "Debate", ["two scorers + judge", "12 of 12"])
svg += box(784, 150, 128, 110, CYAN, "Blackboard", ["shared board", "10 of 12"])
svg += box(48, 310, 864, 90, LIGHT, "And the baseline they must beat",
           ["single agent: 7 of 12, 4 policy escapes, cheapest per success at 169.7 tokens"],
           tcolor=NAVY)
svg += foot(960, 520, "No topology wins everywhere: on chained orders the pipeline ties the single agent at 2.24x the tokens (Lesson 05).")
save("topology-family.svg", svg)

# 3. Coordination ledger: tokens per success --------------------------------
rows = [
    ("blackboard (pointer priced)", 86.7, AMBER),
    ("single agent", 169.7, NAVY),
    ("pipeline (plain)", 334.3, RED),
    ("orchestrated", 362.9, CYAN),
    ("debate", 389.2, CYAN),
    ("pipeline + reviewer", 432.3, CYAN),
]
svg = head(960, 520, "Cost per success, all six systems",
           "Tokens per successful order, Lesson 24. Cost per success refuses to let a system look cheap by failing cheaply.")
maxv = 432.3
for i, (label, value, color) in enumerate(rows):
    y = 150 + i * 52
    wbar = int(560 * value / maxv)
    svg += f'<text x="48" y="{y + 22}" font-family="Georgia, serif" font-size="15" fill="{NAVY}">{label}</text>'
    svg += f'<rect x="300" y="{y}" width="{wbar}" height="26" rx="5" fill="{color}"/>'
    svg += f'<text x="{312 + wbar}" y="{y + 20}" font-family="Georgia, serif" font-size="15" fill="{NAVY}" font-weight="bold">{value}</text>'
svg += foot(960, 520, "The plain pipeline is the worst row: coordination prices for the baseline's exact results. Blackboard messages price pointers, not board content.")
save("coordination-ledger.svg", svg)

# 4. Cascade -----------------------------------------------------------------
rows = [("healthy pipeline", 7, CYAN), ("one extractor fault", 0, RED),
        ("with checkpoint fix", 11, GREEN)]
svg = head(960, 520, "One small fault, system-wide silence",
           "Successes of 12 when the extractor drops the budget field, Lesson 17.")
for i, (label, value, color) in enumerate(rows):
    y = 160 + i * 80
    wbar = int(620 * value / 12)
    svg += f'<text x="48" y="{y + 26}" font-family="Georgia, serif" font-size="16" fill="{NAVY}">{label}</text>'
    svg += f'<rect x="280" y="{y}" width="{max(wbar, 4)}" height="34" rx="6" fill="{color}"/>'
    svg += f'<text x="{292 + wbar}" y="{y + 24}" font-family="Georgia, serif" font-size="16" fill="{NAVY}" font-weight="bold">{value} of 12</text>'
svg += foot(960, 520, "The fault is one line and produces no error message. The checkpoint blind spot (word-form budgets) is named in Lesson 17.")
save("cascade.svg", svg)

# 5. Scaling curve -------------------------------------------------------------
svg = head(960, 520, "Scaling the pool: where the curve bends",
           "Makespan in steps for a 6-order batch, Lesson 25. Tokens and successes are flat at every pool size.")
pts = [(1, 18), (2, 9), (3, 6), (4, 6), (6, 3), (12, 3)]
ox, oy, sx, sy = 110, 420, 62, 19
svg += f'<line x1="{ox}" y1="{oy}" x2="{ox + 760}" y2="{oy}" stroke="{GREY}" stroke-width="2"/>'
svg += f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 380}" stroke="{GREY}" stroke-width="2"/>'
coords = []
for workers, steps in pts:
    x = ox + int(workers * sx)
    y = oy - int(steps * sy)
    coords.append((x, y))
    svg += f'<circle cx="{x}" cy="{y}" r="7" fill="{CYAN}"/>'
    svg += f'<text x="{x}" y="{y - 16}" text-anchor="middle" font-family="Georgia, serif" font-size="15" fill="{NAVY}" font-weight="bold">{steps}</text>'
    svg += f'<text x="{x}" y="{oy + 26}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{GREY}">{workers}w</text>'
svg += '<polyline points="' + " ".join(f"{x},{y}" for x, y in coords) + f'" fill="none" stroke="{CYAN}" stroke-width="3"/>'
svg += f'<text x="48" y="150" font-family="Georgia, serif" font-size="14" fill="{GREY}">steps</text>'
svg += foot(960, 520, "Speedup plateaus at 3.0x from 3 to 4 workers, then 6.0x. The deal, not the roster, sets the clock.")
save("scaling-curve.svg", svg)

# 6. Failure taxonomy ----------------------------------------------------------
svg = head(960, 520, "Failure taxonomy: this course vs the field",
           "Shares of classified failures. Course: 20 instances (Lesson 28). Field: MAST, Cemri et al. 2025 (RESEARCH.md).")
cats = [("Specification and design", 30, 44), ("Inter-agent misalignment", 30, 32),
        ("Task verification", 40, 24)]
for i, (label, course, field) in enumerate(cats):
    y = 150 + i * 100
    svg += f'<text x="48" y="{y + 20}" font-family="Georgia, serif" font-size="16" fill="{NAVY}">{label}</text>'
    svg += f'<rect x="48" y="{y + 30}" width="{int(7.6 * course)}" height="22" rx="5" fill="{CYAN}"/>'
    svg += f'<text x="{60 + int(7.6 * course)}" y="{y + 47}" font-family="Georgia, serif" font-size="14" fill="{NAVY}">course {course}%</text>'
    svg += f'<rect x="48" y="{y + 58}" width="{int(7.6 * field)}" height="22" rx="5" fill="{NAVY}"/>'
    svg += f'<text x="{60 + int(7.6 * field)}" y="{y + 75}" font-family="Georgia, serif" font-size="14" fill="{NAVY}">field {field}%</text>'
svg += foot(960, 520, "The course is verification-heavy by construction: 4 of its 12 fixture orders carry a policy trap.")
save("failure-taxonomy.svg", svg)

# 7. Capstone pipeline ----------------------------------------------------------
svg = head(1000, 560, "The capstone system and its verdict",
           "Router, pipeline, reviewer, field check. Gates fixed in Lesson 29 before the build (Lesson 31).")
svg += box(48, 170, 170, 110, NAVY, "Router", ["traps to review", "clean orders pass"])
svg += arrow(218, 225, 258)
svg += box(258, 170, 190, 110, CYAN, "Pipeline", ["extract, score", "draft"])
svg += arrow(448, 225, 488)
svg += box(488, 170, 190, 110, CYAN, "Reviewer", ["verdict + one", "safe redraft"])
svg += arrow(678, 225, 718)
svg += box(718, 170, 200, 110, GREEN, "Field check", ["careful re-read", "on thin extracts"])
svg += box(48, 340, 420, 90, "#FEF3C7", "As built: 4 of 5 gates",
           ["success 0.8333 fails the 0.9 gate; the rest pass"], tcolor=NAVY)
svg += box(500, 340, 418, 90, "#D1FAE5", "Hardened: 5 of 5 gates",
           ["12 of 12 orders, 0 escapes, 349.3 tokens per success"], tcolor=NAVY)
svg += foot(1000, 560, "The hardened system still costs about 2.06x the single agent's tokens per success. That residue is printed, not hidden.")
save("capstone-pipeline.svg", svg)
