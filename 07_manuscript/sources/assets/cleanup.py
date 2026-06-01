# -*- coding: utf-8 -*-
"""Clean internal artifact references, remove 'Supporting material' lines, renumber figures/tables."""
import re, glob, os
B = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/build"

def renumber_figs(t):
    # protect the F1 metric ("accuracy, F1, inference latency")
    t = t.replace("accuracy, F1,", "accuracy, \x02,")
    # shift F10..F1 -> +1 (PRISMA flow takes Figure 1)
    for n in range(10, 0, -1):
        t = re.sub(r'\bF%d([ab]?)\b' % n, lambda m, n=n: '\x00%d\x00%s' % (n + 1, m.group(1)), t)
    t = re.sub(r'\x00(\d+)\x00', r'\1', t)
    t = t.replace("\x02", "F1")
    return t

def clean(t):
    # remove parenthetical groups consisting only of backtick code spans (internal files)
    t = re.sub(r'\s*\(`[^`]*`(?:[;,]\s*`[^`]*`)*\)', '', t)
    # remove "; `...`" or ", `...`" trailing internal refs
    t = re.sub(r'[;,]\s*`[^`]*`', '', t)
    # remove any remaining standalone backtick code spans
    t = re.sub(r'\s*`[^`]*`', '', t)
    # tidy ' .' and double spaces and ' ;' and orphan '()' and ' ,'
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'\s+([.;,])', r'\1', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    return t

for fp in glob.glob(B + "/0*.md"):
    t = open(fp, encoding='utf-8').read()
    # remove the "Supporting material:" italic anchor lines entirely
    t = re.sub(r'(?m)^\*Supporting material:.*\*\s*$\n?', '', t)
    # also the multi-line variant "*Supporting material: ... \n ... *"
    t = re.sub(r'\*Supporting material:.*?\*', '', t, flags=re.S)
    t = renumber_figs(t)
    t = clean(t)
    open(fp, 'w', encoding='utf-8').write(t)
    print("cleaned", os.path.basename(fp))
