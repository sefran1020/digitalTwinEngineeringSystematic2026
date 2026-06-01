# -*- coding: utf-8 -*-
"""PRISMA 2020 flow diagram for the DT-in-engineering-education review."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/build/figs"
os.makedirs(OUT, exist_ok=True)

fig, ax = plt.subplots(figsize=(9.2, 11))
ax.set_xlim(0, 10); ax.set_ylim(0, 14); ax.axis("off")

BLUE = "#d9e6f2"; GREY = "#f0f0f0"; EDGE = "#33475b"
def box(x, y, w, h, text, fc=BLUE):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                       fc=fc, ec=EDGE, lw=1.2)
    ax.add_patch(p)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8.6, wrap=True)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=14, lw=1.2, color=EDGE))

# phase labels (rotated, left margin)
for yy, lab in [(12.6, "Identification"), (8.2, "Screening"), (1.5, "Included")]:
    ax.text(-0.15, yy, lab, rotation=90, ha="center", va="center",
            fontsize=11, fontweight="bold", color=EDGE)

LX, LW = 0.7, 5.6      # left (flow) column
RX, RW = 6.9, 3.0      # right (exclusions) column

# Identification
box(LX, 12.2, LW, 1.4,
    "Records identified from databases (n = 1,504)\nScopus 772 · Dimensions 409 · IEEE Xplore 181\nEBSCO 81 · Web of Science 61")
box(RX, 12.2, RW, 1.4,
    "Records removed before screening:\nmissing title/authors (n = 38)\nduplicates (n = 279)\nno abstract (n = 9)", fc=GREY)
arrow(LX+LW, 12.9, RX, 12.9)

# Screening - records screened
box(LX, 10.4, LW, 1.0, "Records screened\n(n = 1,178)")
arrow(LX+LW/2, 12.2, LX+LW/2, 11.4)
box(RX, 10.4, RW, 1.0, "Excluded — automated\nterminological screen (n = 379)", fc=GREY)
arrow(LX+LW, 10.9, RX, 10.9)

# semantic screening
box(LX, 8.4, LW, 1.2,
    "Records assessed by semantic screening\n(3 independent LLM agents + 1 moderator agent)\n(n = 799)")
arrow(LX+LW/2, 10.4, LX+LW/2, 9.6)
box(RX, 8.4, RW, 1.2,
    "Excluded — semantic\nscreening / consensus\n(n = 552)", fc=GREY)
arrow(LX+LW, 9.0, RX, 9.0)

# human eligibility review
box(LX, 6.4, LW, 1.2,
    "Records advanced to human\neligibility review (n = 247)\n(236 uncertain + 11 agent-included)")
arrow(LX+LW/2, 8.4, LX+LW/2, 7.6)
box(RX, 6.4, RW, 1.2, "Excluded — human\nreview (n = 121)", fc=GREY)
arrow(LX+LW, 7.0, RX, 7.0)

# eligible / full text
box(LX, 4.5, LW, 1.1, "Records judged eligible\n(full texts sought) (n = 126)")
arrow(LX+LW/2, 6.4, LX+LW/2, 5.6)
box(RX, 4.5, RW, 1.1, "Reports not retrieved\n(n = 61)", fc=GREY)
arrow(LX+LW, 5.05, RX, 5.05)

# included
box(LX, 2.7, LW, 1.0, "Studies included in the review\n(n = 65)", fc="#cfe6cf")
arrow(LX+LW/2, 4.5, LX+LW/2, 3.7)

ax.text(LX, 1.7, "Inter-agent reliability (3 primary agents, n = 799): Fleiss' κ = 0.60;\n"
        "pairwise Cohen's κ = 0.56–0.63; 58% unanimous. Construct-severity\n"
        "rule applied; uncertain cases never excluded on absence of evidence.",
        ha="left", va="top", fontsize=7.3, style="italic", color="#444")

plt.tight_layout()
fig.savefig(OUT + "/F1_prisma.png", dpi=200, bbox_inches="tight")
print("wrote", OUT + "/F1_prisma.png")
