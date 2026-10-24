# -*- coding: utf-8 -*-
"""Round-trip verifier.

Every glyph in the PDF must land in exactly one parsed field.  The token stream
read straight out of the PDF is compared with the token stream rebuilt from the
parsed records.  Whitespace is compared separately, because a line break in the
PDF can hide whether the source had a space there.

Page 1 is the app summary card and is parsed by a dedicated routine, so the
comparison starts at page 2.

    python3 verify_roundtrip.py [words3.json]
"""
import json, sys, os, collections, re, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import appsheet_parse as AP

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'words3.json')

W = json.load(open(WORDS, encoding='utf-8'))
recs, stats = AP.parse(W)

pdf_tokens = [w[4] for pg in W[1:] for b in pg for ln in b for w in ln]

# rebuild the token stream from the parsed records
par = []
for r in recs:
    if r['page'] == 1:
        continue
    for label, val in r['fields'].items():
        par.extend(label.split())
        par.extend(str(val).split())
    par.extend(r['name'].split())

print('pdf tokens (p2+):', len(pdf_tokens))
print('parsed           :', len(par))
print('records          :', len(recs), dict(stats))

norm = lambda ts: re.sub(r'\s+', '', ''.join(ts))
a, b = norm(pdf_tokens), norm(par)
print('normalised chars :', len(a), len(b))


def window_diff(a, b, win=600, limit=15):
    """Locate the differing regions of two strings without an O(n^2) diff."""
    regions = []
    i = j = 0
    while i < len(a) and j < len(b) and len(regions) < limit:
        if a[i] == b[j]:
            i += 1
            j += 1
            continue
        aw, bw = a[i:i + win], b[j:j + win]
        sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
        ops = sm.get_opcodes()
        if ops and ops[0][0] == 'equal':
            k = ops[0][3]
            i += k
            j += k
            continue
        last = None
        for tag, i1, i2, j1, j2 in ops:
            if tag != 'equal':
                regions.append((tag, a[i + i1:i + i2], b[j + j1:j + j2]))
            last = (i + i2, j + j2)
        if last is None:
            break
        i, j = last
        if i >= len(a) or j >= len(b):
            break
    if i < len(a) or j < len(b):
        regions.append(('tail', a[i:i + 120], b[j:j + 120]))
    return regions


if a == b:
    print('CONTENT: EXACT MATCH (whitespace-insensitive)')
else:
    regions = window_diff(a, b)
    print('CONTENT: MISMATCH - %d regions' % len(regions))
    for tag, x, y in regions[:25]:
        print('  %-8s pdf=%r parsed=%r' % (tag, x[:70], y[:70]))
    sys.exit(1)

if pdf_tokens == par:
    print('TOKENS  : EXACT MATCH')
else:
    regions = window_diff(' '.join(pdf_tokens), ' '.join(par))
    print('TOKENS  : %d differing regions (content identical)' % len(regions))
    seen = collections.Counter()
    for tag, x, y in regions:
        seen[(tag, x[:44], y[:44])] += 1
    for (tag, x, y), cnt in seen.most_common(12):
        print('   [%4d] %-8s pdf=%r parsed=%r' % (cnt, tag, x, y))
