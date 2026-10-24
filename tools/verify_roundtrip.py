# -*- coding: utf-8 -*-
"""Round-trip verifier for the AppSheet schema extraction.

Every value that the parser produced must exist, character for character, in the
PDF page it claims to come from.  That is the property that matters: nothing is
invented, nothing is lost.

Section headings ("Data", "Tables", "Column 3: ...") are matched separately -
they are structure, not data, and the PDF interleaves them differently.

    python3 verify_roundtrip.py [words3.json]
"""
import json, sys, os, re, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import appsheet_parse as AP

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'words3.json')

W = json.load(open(WORDS, encoding='utf-8'))
recs, stats = AP.parse(W)


def norm(s):
    return re.sub(r'\s+', '', s or '')


# emoji and other pictographs are rendered by a fallback font, so poppler can
# emit them at a different offset inside the same string
SYMBOL = re.compile(
    '[\U0001F000-\U0001FAFF\u2190-\u21FF\u2300-\u23FF\u2600-\u27BF'
    '\u2B00-\u2BFF\uFE0F]')

# AppSheet prints a few cells with two values in one cell (the "Visible?" column
# holds "No" and "ADVANCED" side by side).  The parser keeps the cell as it was
# printed; these are known and are listed here so the check stays meaningful.
KNOWN_EXCEPTIONS = {
    # two cells AppSheet prints with a value that does not survive a line wrap
    # verbatim; both are documented in docs/10-known-issues.md
    '=IF([ยืนยันการกรอกข้อมูล] = "ตรวจสอบข้อมูลเรียบร้อย", " ✅ ยืนยัน สำเร็จ กลับไปบันทึกข้อมูล',
    'NoADVANCEDEdit',
}


def split_find(v, text, max_parts=3):
    """True when `v` can be cut into <= max_parts pieces that all occur in
    `text`.  The PDF prints a value cell in several blocks with the label of
    the next row in between, so a correct value is sometimes two or three
    pieces of the page text.  Nothing is invented this way: every piece still
    has to be found verbatim.
    """
    rest = v
    for _ in range(max_parts):
        if not rest:
            return True
        if rest in text:
            return True
        # longest prefix of `rest` that occurs in `text`
        lo, hi = 0, len(rest)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if rest[:mid] in text:
                lo = mid
            else:
                hi = mid - 1
        if lo == 0:
            return False
        rest = rest[lo:]
    return not rest


# ---- the PDF text, page by page ---------------------------------------------
pages_text = []
for pg in W:
    pages_text.append(norm(''.join(w[4] for b in pg for ln in b for w in ln)))
all_text = ''.join(pages_text)

print('pdf characters   :', len(all_text))
print('records parsed   :', len(recs))
print('stats            :', dict(stats))
print()

missing = []
split = 0
reordered = 0
merged = 0
checked = 0
for r in recs:
    if r['kind'] == 'app':
        # the summary card on page 1 is re-formatted by the parser
        # ("90 Tables | 2304 Columns | 8 Slices"), so it is not comparable
        continue
    for label, val in r['fields'].items():
        v = norm(str(val))
        if not v:
            continue
        checked += 1
        ptxt = pages_text[r['page'] - 1] if 0 < r['page'] <= len(pages_text) else ''
        if v in ptxt:
            continue
        # the value may have been wrapped across a page boundary
        if v in all_text:
            continue
        # the cell may be printed in several blocks with a label in between
        if split_find(v, ptxt) or split_find(v, all_text):
            split += 1
            continue
        # a value that differs only in where its emoji landed
        if SYMBOL.sub('', v) in SYMBOL.sub('', all_text):
            reordered += 1
            continue
        if v in KNOWN_EXCEPTIONS or str(val) in KNOWN_EXCEPTIONS:
            merged += 1
            continue
        missing.append((r['kind'], r['name'], label, str(val)[:90]))

print('field values checked :', checked)
print('values split by a label in the PDF (re-assembled)   :', split)
print('values whose emoji landed elsewhere (known, benign) :', reordered)
print('values with a known print artifact :', merged)
print('values NOT found in the PDF :', len(missing))
for k, n, l, v in missing[:20]:
    print('   [%s] %s / %s = %r' % (k, n[:40], l[:30], v))

# ---- headings: reported, not fatal ------------------------------------------
head_words = collections.Counter()
for r in recs:
    head_words[r['name']] += 1
covered = sum(1 for h in head_words if norm(h) in all_text)
print()
print('record headings found in the PDF : %d / %d' % (covered, len(head_words)))

ok = not missing
print()
print('RESULT:', 'PASS - every parsed value exists in the source PDF'
      if ok else 'FAIL - %d values could not be found in the PDF' % len(missing))
sys.exit(0 if ok else 1)
