"""Extract distinct in-text citations and propose citekey matches."""
import re, json, csv, unicodedata, glob, os

BASE = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis"
JEE = BASE + "/JEE-WILEY"
ASSETS = BASE + "/entrega/assets"

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower().strip()

# --- load corpus map (label -> key, first_surname, year) ---
corpus = []  # (surname_norm, year, key, suffix)
with open(BASE + "/analisis/salidas/tablas/citas_map.csv", encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        label = row['label']
        m = re.search(r'(\d{4})([ab]?)\s*$', label)
        suffix = m.group(2) if m else ''
        corpus.append((norm(row['first_surname']).split()[0] if row['first_surname'] else '',
                       row['year'], row['citekey_bib'], suffix, label))

# --- load full bib index ---
idx = json.load(open(ASSETS + "/bib_index.json", encoding='utf-8'))
for it in idx:
    it['nfirst'] = norm(it['first']).split()[-1] if it['first'] else ''

# --- extract distinct in-text tokens ---
# match: Name [et al.| and Name] , YEAR[a/b]   (inside or outside parens)
pat = re.compile(r'([A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+(?:\s+(?:and|&)\s+[A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+|\s+et al\.)?)\s*,?\s*\((?:\d{4})|'
                 r'([A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+(?:\s+(?:and|&)\s+[A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+|\s+et al\.)?)\s*,\s*(\d{4})([ab]?)')

tokens = {}
for fp in sorted(glob.glob(JEE + "/0*.md")):
    txt = open(fp, encoding='utf-8').read()
    fn = os.path.basename(fp)
    # narrative form: Name (YEAR)
    for m in re.finditer(r'([A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'­-]+(?:\s+(?:and|&)\s+[A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+|\s+et al\.)?)\s*\((\d{4})([ab]?)\)', txt):
        name, yr, suf = m.group(1), m.group(2), m.group(3)
        key = (norm(name.split()[0]), yr, suf)
        tokens.setdefault(key, {'raw': name.strip()+f" ({yr}{suf})", 'files': set(), 'forms': set()})
        tokens[key]['files'].add(fn); tokens[key]['forms'].add('narr')
    # parenthetical form: Name, YEAR  (anywhere)
    for m in re.finditer(r'([A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'­-]+(?:\s+(?:and|&)\s+[A-ZÁÉÍÓÚÑ][\wÀ-ÿ.’\'-]+|\s+et al\.)?)\s*,\s*(\d{4})([ab]?)', txt):
        name, yr, suf = m.group(1), m.group(2), m.group(3)
        if name.lower() in ('prisma','iec','iso','abet','isa','rami'): continue
        key = (norm(name.split()[0]), yr, suf)
        tokens.setdefault(key, {'raw': name.strip()+f", {yr}{suf}", 'files': set(), 'forms': set()})
        tokens[key]['files'].add(fn); tokens[key]['forms'].add('paren')

# --- match each token ---
def candidates(surname, year):
    out = []
    for it in idx:
        if it['year'] == year and (it['nfirst'] == surname or surname in it['nfirst'] or it['nfirst'] in surname and len(surname)>3):
            out.append(it['key'])
    return sorted(set(out))

rows = []
for (sn, yr, suf), info in sorted(tokens.items()):
    # corpus match first (respect suffix)
    cmatch = [c for c in corpus if c[1]==yr and (c[0]==sn or sn in c[0] or (c[0] and c[0] in sn)) and (c[3]==suf or suf=='')]
    if suf:
        cmatch = [c for c in corpus if c[1]==yr and (c[0]==sn or sn in c[0]) and c[3]==suf]
    cand_corpus = sorted(set(c[2] for c in cmatch))
    cand_bib = candidates(sn, yr)
    rows.append({
        'token': info['raw'], 'surname': sn, 'year': yr, 'suffix': suf,
        'forms': sorted(info['forms']), 'files': sorted(info['files']),
        'corpus': cand_corpus, 'bib': cand_bib,
    })

json.dump(rows, open(ASSETS + "/match_report.json",'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"distinct tokens: {len(rows)}\n")
for r in rows:
    status = 'OK-corpus' if len(r['corpus'])==1 else ('AMBIG' if (len(r['corpus'])>1 or len(r['bib'])>1) else ('OK-bib' if len(r['bib'])==1 else 'MISSING'))
    chosen = r['corpus'][0] if len(r['corpus'])==1 else (r['bib'][0] if (not r['corpus'] and len(r['bib'])==1) else '??')
    print(f"[{status:9}] {r['token']:34} -> {chosen:38} corpus={r['corpus']} bib={r['bib']}")
