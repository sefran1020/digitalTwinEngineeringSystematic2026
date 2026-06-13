#!/usr/bin/env python3
# In Markdown TABLE rows only (lines starting with '|'), strip any author text
# that precedes a [@cite] so the cell shows the bare numeric citation [x].
# Prose lines (no leading '|') are untouched, so narrative citations are safe.
import re

FILES = [
    '../sources_md/03_results.md',       # Tables 2 and 3 (Study column)
    '../sources_md/01d_related_reviews.md',  # Table 1 (Review column)
]
# "| <author text>[@key]"  ->  "| [@key]"   (text = no pipe, no '[')
pat = re.compile(r'(\|\s*)[^|\[]*?(\[@[^\]]+\])')

total = 0
for f in FILES:
    lines = open(f, encoding='utf-8').read().split('\n')
    out = []
    for ln in lines:
        if ln.lstrip().startswith('|') and '[@' in ln:
            new = pat.sub(lambda m: m.group(1) + m.group(2), ln)
            if new != ln:
                total += 1
            out.append(new)
        else:
            out.append(ln)
    open(f, 'w', encoding='utf-8').write('\n'.join(out))
print(f'rows updated: {total}')
