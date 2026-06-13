#!/usr/bin/env python3
# Post-process pandoc LaTeX (body_raw.tex) -> IEEEtran-ready body.tex.
# citations -> \cite ; standalone images -> figure* ; longtable -> table* ;
# scientific Unicode -> LaTeX (pdflatex-safe). Reproducible: re-run as needed.
import re

src = open('body_raw.tex', encoding='utf-8').read()

# ---- citations: \citep/\citet[pre][post]{keys} -> [pre] \cite{keys}[, post] ----
def fix_cite(m):
    b1, b2, keys = m.group(1), m.group(2), m.group(3)
    keys = ','.join(k.strip() for k in keys.split(','))
    cite = '\\cite{' + keys + '}'
    pre, post = '', ''
    if b1 is not None and b2 is not None:   # natbib [pre][post]
        pre, post = b1.strip(), b2.strip()
    elif b1 is not None:                    # single opt arg = [post]
        post = b1.strip()
    return (pre + ' ' if pre else '') + cite + (', ' + post if post else '')
src = re.sub(
    r'\\(?:citep|citet)\s*(?:\[([^\]]*)\])?\s*(?:\[([^\]]*)\])?\{([^}]*)\}',
    fix_cite, src)

# ---- figures: \includegraphics + "Figure N." caption -> figure* float ----
fig_re = re.compile(
    r'\\includegraphics\[[^\]]*\]\{(figs/[^}]+)\}\s*\n\s*\n'
    r'\\textbf\{Figure\s+(\d+)\.\}\s*(.*?)(?=\n\s*\n)', re.S)
def fig_repl(m):
    # single-column figure (does NOT span both columns); width = column width
    path, num, cap = m.group(1), m.group(2), re.sub(r'\s+', ' ', m.group(3).strip())
    return ('\\begin{figure}[!t]\n\\centering\n'
            '\\includegraphics[width=\\columnwidth,keepaspectratio]{' + path + '}\n'
            '\\caption{' + cap + '}\n\\label{fig:F' + num + '}\n\\end{figure}')
src = fig_re.sub(fig_repl, src)

# ---- tables: "Table N." caption + longtable -> single-column page-breaking
#      longtable with per-table tuned column widths (pandoc makes all columns
#      equal at 0.125, so narrow cols like N/ES/Design waste width). Fractions
#      sum to 1.0; the (\linewidth - 14\tabcolsep) factor already removes padding.
COLFRAC = {
    # Table 1 (Related reviews): Review Type Focus Appraises Gap
    '1': [0.17, 0.12, 0.33, 0.13, 0.25],
    # Table 2 (Empirical studies): Study Domain Design N Comparator ES KeyResult Band
    '2': [0.11, 0.10, 0.085, 0.04, 0.115, 0.04, 0.42, 0.09],
    # Table 3 (Architectures): Study Config Environ DTtype AI Pedagogy SysModelled Band
    '3': [0.12, 0.15, 0.10, 0.075, 0.165, 0.09, 0.20, 0.10],
}
def make_colspec(num):
    fr = COLFRAC.get(num)
    if not fr:
        return None
    pad = 2 * (len(fr) - 1)  # pandoc-style: (\linewidth - 2(ncol-1)\tabcolsep)
    cols = ['>{\\raggedright\\arraybackslash}p{(\\linewidth - %d\\tabcolsep) * \\real{%.4f}}' % (pad, f)
            for f in fr]
    return '@{}' + '\n  '.join([''] + cols) + '@{}'

tbl_re = re.compile(
    r'\\textbf\{Table\s+(\d+)\.\}\s*(.*?)\n\s*\n'
    r'\{\\def\\LTcaptype\{none\}[^\n]*\n'
    r'\\begin\{longtable\}\[\]\{(.*?)\}\s*\n'   # colspec ends at the } right before \toprule
    r'(\\toprule.*?\\end\{longtable\})\n\}', re.S)
def tbl_repl(m):
    # Keep pandoc's page-breaking longtable (it handles \endhead/\endlastfoot),
    # but give it a real \caption and render it in a single-column block so it
    # may break across pages (a full-width table* float cannot, and a 15-row
    # table is taller than one page -> "Float too large", silently dropped).
    num = m.group(1)
    cap = re.sub(r'\s+', ' ', m.group(2).strip())
    colspec = make_colspec(num) or m.group(3).strip()
    inner = m.group(4)  # already includes \toprule ... \end{longtable}
    return ('\\clearpage\n\\onecolumn\n\\footnotesize\n\\setlength{\\tabcolsep}{4pt}\n'
            '\\begin{longtable}{' + colspec + '}\n'
            '\\caption{' + cap + '}\\label{tab:T' + num + '}\\\\\n'
            + inner +
            '\n\\normalsize\n\\twocolumn\n')
src = tbl_re.sub(tbl_repl, src)

# ---- Unicode -> LaTeX (keys as codepoints to avoid source-encoding issues) ----
src = src.replace('η²', '\\ensuremath{\\eta^{2}}')   # eta-squared
src = src.replace('χ²', '\\ensuremath{\\chi^{2}}')   # chi-squared
uni = {
    'κ': '\\ensuremath{\\kappa}', 'φ': '\\ensuremath{\\phi}',
    'ϕ': '\\ensuremath{\\phi}',   'η': '\\ensuremath{\\eta}',
    'χ': '\\ensuremath{\\chi}',   'Δ': '\\ensuremath{\\Delta}',
    'σ': '\\ensuremath{\\sigma}', 'μ': '\\ensuremath{\\mu}',
    'µ': '\\ensuremath{\\mu}',    'β': '\\ensuremath{\\beta}',
    'α': '\\ensuremath{\\alpha}',
    '±': '\\ensuremath{\\pm}',    '≥': '\\ensuremath{\\geq}',
    '≤': '\\ensuremath{\\leq}',   '→': '\\ensuremath{\\rightarrow}',
    '×': '\\ensuremath{\\times}', '≈': '\\ensuremath{\\approx}',
    '≠': '\\ensuremath{\\neq}',   '−': '\\ensuremath{-}',
    '²': '\\textsuperscript{2}',  '³': '\\textsuperscript{3}',
    '₀': '\\textsubscript{0}',    '₁': '\\textsubscript{1}',
    '₂': '\\textsubscript{2}',    '₃': '\\textsubscript{3}',
    '°': '\\textdegree{}',        '√': '\\ensuremath{\\surd}',
    '∞': '\\ensuremath{\\infty}', '…': '\\ldots{}',
}
for k, v in uni.items():
    src = src.replace(k, v)

open('body.tex', 'w', encoding='utf-8').write(src)
keep = set('áéíóúñüÁÉÍÓÚÑÜ'
           'àèìòùçãõâêô'
           '‘’“”—– ')
leftover = sorted({hex(ord(c)) for c in src if ord(c) > 127 and c not in keep})
print('body.tex OK | leftover non-ASCII:', leftover)
print('figure* =', src.count('\\begin{figure*}'),
      '| table* =', src.count('\\begin{table*}'),
      '| cite =', src.count('\\cite{'))
