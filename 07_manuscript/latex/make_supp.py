#!/usr/bin/env python3
# Build supp_body.tex from pandoc output of the appendix (65 included studies).
import re
s = open('supp_body_raw.tex', encoding='utf-8').read()
# drop pandoc's own section header (we provide our own in the wrapper)
s = re.sub(r'\A\\section\{Appendix A[^\n]*\n', '', s, count=1)
s = s.replace('η²', '\\ensuremath{\\eta^{2}}')
s = s.replace('χ²', '\\ensuremath{\\chi^{2}}')
uni = {
    'κ': '\\ensuremath{\\kappa}', 'φ': '\\ensuremath{\\phi}',
    '×': '\\ensuremath{\\times}', '≥': '\\ensuremath{\\geq}',
    '≤': '\\ensuremath{\\leq}', '→': '\\ensuremath{\\rightarrow}',
    '−': '\\ensuremath{-}', '€': '\\texteuro{}',
    '…': '\\ldots{}', 'А': 'A', 'м': 'm', 'ș': 'ş',
    '�': 'ä',
}
for k, v in uni.items():
    s = s.replace(k, v)
open('supp_body.tex', 'w', encoding='utf-8').write(s)
leftover = sorted({hex(ord(c)) for c in s if ord(c) > 127 and not (0xA0 <= ord(c) <= 0x17F)
                   and c not in '‘’“”–—'})
print('supp_body.tex OK | leftover:', leftover)
