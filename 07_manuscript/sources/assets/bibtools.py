"""Dedupe master.bib by citekey and emit an index (citekey, year, title, authors)."""
import re, json, sys, io

SRC = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/assets/master.bib"

def split_entries(text):
    # split on @type{ at line start
    parts = re.split(r'(?m)^(?=@\w+\s*\{)', text)
    return [p for p in parts if p.strip().startswith('@')]

def field(entry, name):
    m = re.search(r'(?im)^\s*' + name + r'\s*=\s*[{"]', entry)
    if not m:
        return None
    i = m.end() - 1
    open_ch = entry[i]
    close_ch = '}' if open_ch == '{' else '"'
    depth = 0
    out = []
    for ch in entry[i:]:
        if ch == '{':
            depth += 1
            if depth == 1 and open_ch == '{':
                continue
        elif ch == '}':
            depth -= 1
            if depth == 0 and open_ch == '{':
                break
            out.append(ch); continue
        elif ch == '"' and open_ch == '"' and depth == 0 and out:
            break
        out.append(ch)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

text = open(SRC, encoding='utf-8', errors='replace').read()
entries = split_entries(text)
seen = {}
order = []
for e in entries:
    m = re.match(r'@\w+\s*\{\s*([^,]+),', e)
    if not m:
        continue
    key = m.group(1).strip()
    if key not in seen:
        seen[key] = e.rstrip() + "\n\n"
        order.append(key)

# write deduped bib
with open(SRC, 'w', encoding='utf-8') as f:
    for k in order:
        f.write(seen[k])

# build index
idx = []
for k in order:
    e = seen[k]
    auth = field(e, 'author') or ''
    first = ''
    if auth:
        first = auth.split(' and ')[0]
        # bibtex "Surname, Given" or "Given Surname"
        first = first.split(',')[0].strip() if ',' in first else first.split()[-1]
    idx.append({
        'key': k,
        'year': field(e, 'year') or '',
        'first': first,
        'title': (field(e, 'title') or '').replace('{', '').replace('}', '')[:90],
    })

print(f"deduped entries: {len(order)}")
with io.open("G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/assets/bib_index.json", 'w', encoding='utf-8') as f:
    json.dump(idx, f, ensure_ascii=False, indent=0)
print("wrote bib_index.json")
