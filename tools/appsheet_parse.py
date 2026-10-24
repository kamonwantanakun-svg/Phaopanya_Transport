# -*- coding: utf-8 -*-
"""
Deterministic parser for the AppSheet "Application Documentation" PDF export.

The PDF is a browser print of an HTML attribute dump.  Every attribute is a
(label cell, value cell) pair.  Poppler's `-bbox-layout` output exposes each table
cell as a <block>; the DOM order of those blocks is the row order of the table.

Layout facts recovered from the document (all measured, not guessed):
  * label cells start left of x=150 (observed label columns: 69.0, 72.7, 87.8,
    97.6); value cells start right of x=150 (observed value columns: 191.8,
    212.3, 216.0, 217.5, 218.0, 221.3).
  * a cell may wrap over several lines -> one block, several lines.
  * Chrome wraps a value cell either at a space (the space is consumed) or in the
    middle of a token when the token does not fit (the cell uses word-break).
    The two are told apart by the width of the fragments - see join_value.
  * poppler sometimes splits one cell into several blocks (emoji fallback fonts,
    multi-line label cells) and sometimes merges a label cell with its value
    cell.  Both are repaired below; the result is checked by a full round-trip
    against the source text (work/verify_roundtrip.py).

Input : work/words2.json  ->  [page][block][line][word] = [xMin, xMax, yMin, text]
Output: work/records.json  ->  [{kind, name, page, fields{}}]
"""
import json, re, collections, os

WORDCH = re.compile(r'[0-9A-Za-z_฀-๿]')
VALUE_X_MIN = 150.0          # >= this x  -> value column
HEAD_PATTERNS = [
    re.compile(r'^Table name\s+\S'), re.compile(r'^Schema Name\s+\S'),
    re.compile(r'^Column \d+:\s*\S'), re.compile(r'^Slice Name\s+\S'),
    re.compile(r'^View name\s+\S'), re.compile(r'^Action name\s+\S'),
    re.compile(r'^Rule name\s+\S'),
]
SECTION_TITLES = {'Data', 'Tables', 'Columns', 'Slices', 'UX', 'Views',
                   'Format Rules', 'Behavior', 'Actions', 'Behavior Summary',
                   'UX Summary', 'Data Summary'}
HEAD_KEYWORDS = {'Table name', 'Schema Name', 'Slice Name', 'View name',
                 'Action name', 'Rule name'}


def block_info(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return None
    # copy the line structure: the repairs below rewrite cells in place and the
    # caller must be able to parse the same input again (the parser runs twice)
    lines = [list(ln) for ln in lines]
    words = [w for ln in lines for w in ln]
    return {'x0': min(w[0] for w in words), 'x1': max(w[1] for w in words),
            'y0': min(w[2] for w in words), 'y1': max(w[3] for w in words),
            'words': words, 'lines': lines}


def _relines(words):
    """Rebuild line grouping for words sorted by (y, x)."""
    lines, cur, cy = [], [], None
    for w in sorted(words, key=lambda w: (round(w[2], 1), w[0])):
        if cy is None or abs(w[2] - cy) > 3.0:
            if cur:
                lines.append(cur)
            cur, cy = [w], w[2]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def join_label(lines):
    """Join the lines of a label cell (labels always break at a space)."""
    return ' '.join(' '.join(w[4] for w in ln) for ln in lines).strip()


def split_label_value(lines, vcol):
    """Split a block that poppler merged into (label cell + value cell)."""
    lab, val = [], []
    for ln in lines:
        L = [w for w in ln if w[0] < vcol]
        R = [w for w in ln if w[0] >= vcol]
        if L:
            lab.append(L)
        if R:
            val.append(R)
    return lab, val


KNOWN_COLUMNS = None      # every column name in the app
STRIPPED_COLUMNS = None   # the same names without spaces
JSON_VOCAB = None         # keys and values that really occur in the app's JSON


def _bad_refs(text):
    """Bracket references in `text` that are one space away from a real column.

    AppSheet references a column as [Column Name]; a wrapped line that lost a
    space turns [Email พนักงาน] into [Emailพนักงาน], which resolves to nothing.
    """
    if not STRIPPED_COLUMNS:
        return False
    for m in re.finditer(r'\[([^\[\]]+)\]', text):
        ref = m.group(1)
        if ref in KNOWN_COLUMNS:
            continue
        if ref.replace(' ', '') in STRIPPED_COLUMNS:
            return True
    return False


def _json_keys_ok(text):
    """True while every completed string in `text` looks right.

    AppSheet writes its configuration JSON with a deterministic shape: keys are
    identifiers and never contain a space, so a space inside a key proves that
    the line was broken inside that key - and that the break must not be
    joined with a space.  A value may contain a space, but only one that the
    app really uses - the vocabulary is learned from the JSON that parses.
    """
    in_str = False
    escaped = False
    is_value = False
    start = 0
    for i, ch in enumerate(text):
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"':
            if in_str:
                if not is_value and ' ' in text[start:i]:
                    return False
                in_str = False
            else:
                in_str = True
                j = i - 1
                while j >= 0 and text[j] == ' ':
                    j -= 1
                is_value = j >= 0 and text[j] == ':'
                start = i + 1
    return True


_JSON_CACHE = {}


def _json_assignment(texts):
    """Find the line-break separators that make the cell valid JSON.

    A space inside a JSON cell is only legitimate when it sits inside a string
    value, so the separators are searched - spaces first - and the first
    assignment that parses, and whose keys are all clean, wins.
    """
    n = len(texts) - 1
    if n <= 0 or n > 16:
        return None
    key = tuple(texts)
    hit = _JSON_CACHE.get(key)
    if hit is not None:
        return hit
    dec = json.JSONDecoder()
    best = None

    def dfs(i, cur):
        nonlocal best
        if best is not None:
            return
        if i == n:
            try:
                json.loads(cur)
            except Exception:
                return
            best = None if _bad_refs(cur) else cur
            return
        for sep in (' ', ''):
            cand = cur + sep + texts[i + 1]
            if not _json_keys_ok(cand):
                continue
            try:
                dec.raw_decode(cand)
                # the document is already complete -> nothing may follow
                if i + 1 == n and not _bad_refs(cand):
                    best = cand
                return
            except Exception:
                pass
            dfs(i + 1, cand)
            if best is not None:
                return

    dfs(0, texts[0])
    _JSON_CACHE[key] = best
    return best


def join_value(lines, cellw=None, right=None):
    """Join the lines of a value cell.

    Chrome wraps a value cell at a space (the space is consumed) or inside a
    token when the token does not fit on a line (the cell is rendered with
    word-break).  Geometry alone cannot tell the two apart, so the join is
    resolved like this:

      * a cell holding JSON is different: the document is walked character by
        character, so it is known whether a break falls inside a key (no spaces
        allowed -> the break is inside a token) or inside a value (a space may
        be part of the value).  The result is checked with json.loads.
      * every other cell is joined with spaces, unless that leaves a [Column]
        reference unresolvable, in which case the alternative join is tried.
    """
    if not lines:
        return ''
    texts = [' '.join(w[4] for w in ln) for ln in lines]
    if len(lines) == 1:
        return texts[0]

    out = ' '.join(texts)
    s = out.strip()
    if s.startswith('{') and s.endswith('}'):
        fixed = _json_assignment(texts)
        if fixed is not None:
            return fixed
        try:
            json.loads(out)
            return out
        except Exception:
            pass
        joined = ''.join(texts)
        return repair_json_text(joined, JSON_VOCAB)
    if _bad_refs(out):
        alt = ''.join(texts)
        if not _bad_refs(alt):
            return alt
    return out


TOKEN_SET = None   # words that are complete tokens somewhere in the document
USE_TOKEN_SET = True


def _build_token_set(pages):
    """Words that are complete tokens somewhere in the document.

    A cell that is rendered with word-break splits long tokens at arbitrary
    points; the fragments it produces are not real tokens and must not be used
    to decide whether a line break happened at a space.  Only cells that are
    *not* rendered that way contribute their words.
    """
    words = set()
    for blocks in pages:
        R = max((b['x1'] for b in blocks if b['x0'] >= VALUE_X_MIN), default=0.0)
        for b in blocks:
            if b['x0'] < VALUE_X_MIN:
                continue
            filled = any(max(w[1] for w in ln) >= R - 3.0 for ln in b['lines'])
            if filled:
                continue
            for ln in b['lines']:
                for w in ln:
                    words.add(w[4])
    return words


def build_events(words_pages):
    """Turn the raw block stream into a flat list of LABEL / VALUE / HEAD events."""
    global TOKEN_SET
    events = []
    all_pages = []
    for pi, pg in enumerate(words_pages):
        blocks = [b for b in (block_info(x) for x in pg) if b]
        all_pages.append(blocks)
    TOKEN_SET = _build_token_set(all_pages)

    for pi, blocks in enumerate(all_pages):
        page_no = pi + 2          # words_pages[0] is the summary card
        starts = collections.Counter(round(b['x0'], 1) for b in blocks)
        vcands = [(x, c) for x, c in starts.items() if x >= VALUE_X_MIN]
        vcol = max(vcands, key=lambda t: (t[1], -t[0]))[0] if vcands else None
        # A page can hold nested tables with different value columns (the Columns
        # section mixes a schema-level table with a column-level table).  Every
        # value column starting >=2 cells on the page is a real column, not a
        # stray fragment.
        vcols = {x for x, c in vcands if c >= 2}
        if vcol is not None:
            vcols.add(vcol)
        # right edge of the value column on this page -> cell width
        R = max((b['x1'] for b in blocks if b['x0'] >= VALUE_X_MIN), default=0.0)

        # poppler can split one cell into several blocks (emoji fallback fonts,
        # and any glyph run that uses a different font).  Such a fragment is
        # re-attached to the line whose baseline is closest, then the line is
        # rebuilt with all words sorted by x.
        frag = [i for i, b in enumerate(blocks)
                if b['x0'] >= VALUE_X_MIN and round(b['x0'], 1) not in vcols]
        for i in frag:
            bi = blocks[i]
            merged = False
            for fl in bi['lines']:
                fx0 = min(w[0] for w in fl)
                fy = min(w[2] for w in fl)
                best, bestkey = None, None
                for j, bj in enumerate(blocks):
                    if j == i or j in frag:
                        continue
                    for lj, bl in enumerate(bj['lines']):
                        lx1 = max(w[1] for w in bl)
                        ly = min(w[2] for w in bl)
                        # a fragment continues the line that ends where it starts
                        adj = 0 if fx0 >= lx1 - 6 else 1
                        key = (adj, abs(ly - fy) + abs(lx1 - fx0) * 0.3)
                        if bestkey is None or key < bestkey:
                            best, bestkey = (j, lj), key
                if best is None:
                    continue
                j, lj = best
                host = blocks[j]
                host['lines'][lj] = sorted(host['lines'][lj] + fl, key=lambda w: w[0])
                host['words'] = sorted(host['words'] + fl, key=lambda w: (w[2], w[0]))
                host['x1'] = max(host['x1'], bi['x1'])
                merged = True
            if merged:
                blocks[i] = None
        blocks = [b for b in blocks if b]

        # the label column of this page (used to tell a heading from a field)
        lcands = [(x, c) for x, c in starts.items() if 40 <= x <= 140]
        lcol = max(lcands, key=lambda t: (t[1], -t[0]))[0] if lcands else None

        # poppler sometimes splits a heading into two blocks (emoji fallback):
        # "View name" + "<name>".  Re-join them.
        merged_heads = []
        i = 0
        while i < len(blocks):
            b = blocks[i]
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            txt = join_label(b['lines'])
            if (lcol is not None and b['x0'] < lcol - 1.5 and
                    txt in HEAD_KEYWORDS and nxt is not None and
                    nxt['x0'] < VALUE_X_MIN and nxt['x0'] > b['x0']):
                nxt = dict(nxt)
                nxt['lines'] = b['lines'] + nxt['lines']
                nxt['words'] = b['words'] + nxt['words']
                nxt['x0'] = b['x0']
                nxt['y0'] = min(b['y0'], nxt['y0'])
                nxt['y1'] = max(b['y1'], nxt['y1'])
                if os.environ.get('AP_DEBUG_MERGE'):
                    print('MERGE', page_no, repr(txt), '+', repr(join_label(nxt['lines'])),
                          'x', b['x0'], nxt['x0'], 'lcol', lcol)
                merged_heads.append(nxt)
                i += 2
                continue
            merged_heads.append(b)
            i += 1
        blocks = merged_heads

        for b in blocks:
            if b['x0'] >= VALUE_X_MIN:
                cellw = R - b['x0'] if R else None
                events.append({'t': 'VALUE', 'page': page_no, 'x0': b['x0'],
                               'y0': b['y0'], 'y1': b['y1'],
                               'lines': b['lines'], 'cellw': cellw, 'right': R})
                continue
            lab, val = None, None
            whole = join_label(b['lines'])
            is_head = (whole in SECTION_TITLES or
                       any(p.match(whole) for p in HEAD_PATTERNS))
            if not is_head and vcol is not None:
                # poppler merged a label cell with its value cell: the value part
                # starts exactly at a real value column.
                hit = next((w for w in b['words']
                            if round(w[0], 1) in vcols), None)
                if hit is not None:
                    lab, val = split_label_value(b['lines'], hit[0])
            if lab is None:
                lab, val = b['lines'], None
            txt = join_label(lab)
            if not is_head:
                is_head = (txt in SECTION_TITLES or
                           any(p.match(txt) for p in HEAD_PATTERNS))
            events.append({'t': 'HEAD' if is_head else 'LABEL',
                           'page': page_no, 'text': txt, 'x0': b['x0'],
                           'y0': b['y0'], 'y1': b['y1']})
            if val:
                cellw = R - hit[0] if R else None
                events.append({'t': 'VALUE', 'page': page_no, 'x0': b['x0'],
                               'y0': b['y0'], 'y1': b['y1'],
                               'lines': val, 'cellw': cellw, 'right': R})
    return events


def merge_split_labels(events):
    """Re-join label cells that poppler split into several blocks.

    A split label shows up as two LABEL events with no VALUE in between.  The
    document itself provides the answer: if the concatenation of the two label
    texts is a label that elsewhere in the document is followed by a value,
    the two blocks are one cell.
    """
    vocab = set()
    for i, e in enumerate(events):
        if e['t'] == 'LABEL':
            j = i + 1
            if j < len(events) and events[j]['t'] == 'VALUE':
                vocab.add(e['text'])

    out = []
    i, n = 0, len(events)
    while i < n:
        e = events[i]
        if e['t'] != 'LABEL':
            out.append(e)
            i += 1
            continue
        j = i + 1
        parts = [e['text']]
        while j < n and events[j]['t'] == 'LABEL':
            cand = ' '.join(parts + [events[j]['text']])
            if cand in vocab:
                parts.append(events[j]['text'])
                j += 1
            else:
                break
        if len(parts) > 1:
            merged = {**e, 'text': ' '.join(parts)}
            merged['y1'] = events[j - 1].get('y1', merged['y1'])
            out.append(merged)
            i = j
        else:
            out.append(e)
            i += 1
    return out


def build_records(events):
    """Group the event stream into table / schema / column / slice / view /
    action / format_rule records.

    A label and its value are paired by the row they share, not by the order
    they appear in: when poppler splits a two-line label cell into two blocks
    it emits both of them before the value of the row above, which shifts the
    sequence.  Matching on the vertical position of the two cells recovers the
    right pairing in every case.

    A value cell is often split into several blocks by poppler; the pieces are
    collected per field and joined once, so that a cell holding JSON can be
    re-assembled correctly.
    """
    records = []
    cur = None
    pend = []              # labels waiting for their value
    stats = collections.Counter()
    page_open = []         # value pieces that arrived before their label

    def overlap(a, b):
        return min(a['y1'], b['y1']) - max(a['y0'], b['y0'])

    def finalize():
        """Turn the collected value pieces of every pending label into text."""
        for lb in pend:
            if cur is None:
                continue
            lines = [ln for blk in lb['prefix'] for ln in blk] + list(lb['lines'])
            if not lines:
                if lb.get('assigned'):
                    cur['fields'][lb['text']] = ''
                    stats['field_no_value'] += 1
                continue
            cur['fields'][lb['text']] = join_value(lines, lb.get('cellw'),
                                                    lb.get('right'))
            lb['done'] = True
        pend.clear()

    prev_page = None
    prev_type = None
    for e in events:
        if e['t'] == 'HEAD':
            finalize()
            if cur is not None:
                records.append(cur)
                cur = None
            page_open = []
            txt = e['text']
            kind = None
            if txt.startswith('Table name'):
                kind = 'table'
            elif txt.startswith('Schema Name'):
                kind = 'schema'
            elif re.match(r'^Column \d+:', txt):
                kind = 'column'
            elif txt.startswith('Slice Name'):
                kind = 'slice'
            elif txt.startswith('View name'):
                kind = 'view'
            elif txt.startswith('Action name'):
                kind = 'action'
            elif txt.startswith('Rule name'):
                kind = 'format_rule'
            if kind:
                cur = {'kind': kind, 'name': txt, 'page': e['page'], 'fields': {}}
                stats['record_' + kind] += 1
            else:
                stats['section_title'] += 1
            prev_page = e['page']
            prev_type = 'HEAD'
            continue

        if e['t'] == 'LABEL':
            if cur is None:
                stats['label_outside_record'] += 1
                page_open = []
                finalize()
                prev_page = e['page']
                prev_type = 'LABEL'
                continue
            finalize()
            pend.append({'text': e['text'], 'lines': [], 'prefix': page_open,
                         'assigned': False, 'cellw': None, 'right': None,
                         'y0': e.get('y0', 0.0), 'y1': e.get('y1', 0.0)})
            page_open = []
            stats['label'] += 1
            prev_page = e['page']
            prev_type = 'LABEL'
            continue

        # VALUE
        best, bestov = None, 0.0
        for lb in pend:
            ov = overlap(lb, e)
            if ov > bestov:
                best, bestov = lb, ov
        if best is None and pend and prev_type == 'LABEL':
            best = pend[0]
        if best is not None:
            best['lines'].extend(e['lines'])
            best['assigned'] = True
            best['cellw'] = e.get('cellw')
            best['right'] = e.get('right')
            stats['field'] += 1
        elif prev_type == 'VALUE' and pend:
            # poppler split this value cell into several blocks -> same field
            pend[-1]['lines'].extend(e['lines'])
            pend[-1]['assigned'] = True
            stats['value_continuation'] += 1
        else:
            page_open.append(e['lines'])
            stats['value_orphan'] += 1
        prev_type = 'VALUE'
        prev_page = e['page']

    finalize()
    if cur is not None:
        records.append(cur)
    return records, stats


def parse_app_summary(pg):
    """Page 1 is the app summary card, not a regular table: a title, a
    generation stamp, three count boxes and a 7-row metadata table."""
    blocks = [b for b in (block_info(x) for x in pg) if b]
    rec = {'kind': 'app', 'name': 'Application Summary', 'page': 1, 'fields': {}}
    labels = ('Short Name', 'Version', 'Default app folder', 'Function',
              'Runnable?', 'Deployable?', 'Personal use only?')
    used = set()
    for bi, b in enumerate(blocks):
        txt = join_label(b['lines'])
        if txt not in labels:
            continue
        best, bestov = None, 0.0
        for j, c in enumerate(blocks):
            if j == bi or j in used or c['x0'] < 100:
                continue
            ov = min(b['y1'], c['y1']) - max(b['y0'], c['y0'])
            if ov > bestov:
                best, bestov = j, ov
        if best is None:
            continue
        used.add(best)
        rec['fields'][txt] = join_value(blocks[best]['lines'])
    for b in blocks:
        txt = join_label(b['lines'])
        if 'Documentation' in txt and b['x0'] < 100:
            rec['fields']['Document header'] = txt
        elif txt.startswith('Generated at:'):
            rec['fields']['Generated at'] = txt
    for b in blocks:
        if b['x0'] < 250:
            continue
        lines = [' '.join(w[4] for w in ln) for ln in b['lines']]
        if lines and lines[0].endswith('Tables'):
            rec['fields']['Counts: Data'] = ' | '.join(lines)
        elif lines and lines[0].endswith('Views'):
            rec['fields']['Counts: UX'] = ' | '.join(lines)
        elif lines and lines[0].endswith('Actions'):
            rec['fields']['Counts: Behavior'] = ' | '.join(lines)
        elif 180 < b['y0'] < 260:
            rec['fields']['App title'] = join_value(b['lines'])
    return rec


def repair_json_text(text, vocab):
    """Repair the spaces a wrapped line swallowed inside a JSON string.

    A value string such as "Auto" that was broken as "A uto" is restored when
    the space-less form is one the app really uses.
    """
    if not vocab or ' ' not in text:
        return text
    out = []
    last = 0
    for m in re.finditer(r'"([^"\\\\]*)"', text):
        body = m.group(1)
        if ' ' not in body:
            continue
        cands = [body.replace(' ', '')]
        parts = body.split(' ')
        for k in range(1, len(parts)):
            cands.append(' '.join(parts[:k]) + parts[k].replace(' ', ''))
        fixed = None
        for c in cands:
            if c in vocab:
                fixed = c
                break
        if fixed is None:
            continue
        out.append(text[last:m.start(1)])
        out.append(fixed)
        last = m.end(1)
    out.append(text[last:])
    return ''.join(out)


def collect_json_vocab(records):
    """Keys and string values that really occur in the app's JSON documents.

    A line break inside a value string can swallow a space ("Auto" -> "A uto").
    The vocabulary of the documents that parse cleanly shows what the app
    really uses, so the broken ones can be repaired.
    """
    vocab = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                vocab.add(k)
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, str):
            vocab.add(v)

    for r in records:
        for val in r['fields'].values():
            if not isinstance(val, str) or '{' not in val:
                continue
            try:
                d = json.loads(val)
            except Exception:
                continue
            walk(d)
    return {v for v in vocab if len(v) < 80}


def parse(words_pages):
    global KNOWN_COLUMNS, STRIPPED_COLUMNS, JSON_VOCAB
    app = parse_app_summary(words_pages[0])
    ev = merge_split_labels(build_events(words_pages[1:]))
    recs, stats = build_records(ev)
    JSON_VOCAB = collect_json_vocab(recs)
    # second pass: now that the column catalogue is known, ambiguous line
    # breaks can be resolved by checking that every [Column] reference points
    # at a column that really exists.
    cols = set()
    for r in recs:
        if r['kind'] == 'column':
            n = r['fields'].get('Column name')
            if n:
                cols.add(n)
    KNOWN_COLUMNS = cols
    STRIPPED_COLUMNS = {c.replace(' ', '') for c in cols}
    ev = merge_split_labels(build_events(words_pages[1:]))
    recs, stats = build_records(ev)
    return [app] + recs, stats


if __name__ == '__main__':
    W = json.load(open('work/words3.json', encoding='utf-8'))
    recs, stats = parse(W)
    print('records:', len(recs))
    print(collections.Counter(r['kind'] for r in recs))
    print('stats:', dict(stats))
    json.dump(recs, open('work/records.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
