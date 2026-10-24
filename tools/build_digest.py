# -*- coding: utf-8 -*-
"""Build the digest/ files: compact, answer-ready reference tables for AI."""
import csv, json, os, re, collections, sys

SRC = '/workspace/appsheet-scg-jwd-transport'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/workspace/gh-repo/digest'
os.makedirs(OUT, exist_ok=True)


def load(p):
    with open(os.path.join(SRC, p), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


idx = load('tables/INDEX.csv')
ac = load('columns/all_columns.csv')
fr = load('formulas/formulas.csv')
fn = load('formulas/functions.csv')
cr = load('formulas/column_references.csv')
vw = load('views/views.csv')
ac2 = load('actions/actions.csv')
sl = load('slices/slices.csv')
frl = load('format_rules/format_rules.csv')
bt = load('columns/by_type.csv')

per_table = collections.Counter(r['table_name'] for r in ac)
appf = collections.Counter(r['table_name'] for r in fr if r['field'] == 'App formula')
init = collections.Counter(r['table_name'] for r in fr if r['field'] == 'Initial value')
tblf = collections.Counter(r['table_name'] for r in fr if r['field'] in
                            ('Security filter', 'Expression for update mode'))
views_of = collections.defaultdict(list)
for r in vw:
    views_of[r['name']].append(r)
actions_of = collections.defaultdict(list)
for r in ac2:
    actions_of[r.get('For a record of this table', '')].append(r)
refs_of = collections.defaultdict(list)
for r in cr:
    refs_of[r['table_name']].append(r)


def esc(s):
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()


def w(name, title, intro, header, rows, note=''):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n{intro}\n\n')
        if note:
            f.write(note + '\n\n')
        f.write('| ' + ' | '.join(header) + ' |\n')
        f.write('|' + '---|' * len(header) + '\n')
        for r in rows:
            f.write('| ' + ' | '.join(str(x) for x in r) + ' |\n')
    print('wrote', name, len(rows), 'rows')


# ---------------------------------------------------------------- tables ---
rows = []
for t in sorted(idx, key=lambda r: (r['classification'] != 'real', -int(r['column_count']))):
    n = t['table_name']
    rows.append([esc(n), 'จริง' if t['classification'] == 'real' else 'บอท',
                 t['bot_table_kind'] or '-', t['column_count'],
                 appf.get(n, 0), init.get(n, 0), tblf.get(n, 0),
                 len(views_of.get('', [])), len(actions_of.get(n, [])),
                 t['data_source'] or '-', t['doc_page']])
w('tables.md', 'สรุปตารางทั้ง 90 ตาราง',
  'หนึ่งแถว = หนึ่งตาราง · คอลัมน์ "คำนวณ" = จำนวนคอลัมน์ที่มี App formula (คำนวญซ้ำอัตโนมัติ) '
  '"ค่าเริ่มต้น" = จำนวนคอลัมน์ที่มี Initial value (ค่าเริ่มต้นตอนสร้างแถว) '
  '· "สูตรระดับตาราง" = Security filter + Expression for update mode '
  '· ดูรายละเอียดรายตารางที่ `docs/03-table-catalogue.md`',
  ['ตาราง', 'ชนิด', 'ชนิดบอท', 'คอลัมน์', 'คำนวณ', 'ค่าเริ่มต้น', 'สูตรระดับตาราง',
   'วิว', 'แอคชัน', 'Data Source', 'หน้า PDF'], rows,
  '> ตารางบอท 61 ตารางสร้างโดย AppSheet เอง (state ของ bot process) — ห้ามแก้ ให้ระบบสร้างใหม่แทน')

# --------------------------------------------------------------- columns ---
rows = []
for t in sorted(idx, key=lambda r: (r['classification'] != 'real', -int(r['column_count']))):
    n = t['table_name']
    if t['classification'] != 'real':
        continue
    cols = [c for c in ac if c['table_name'] == n]
    key = [c['column_name'] for c in cols if c['key'] == 'Yes']
    calc = [c['column_name'] for c in cols if c['app_formula']]
    init_ = [c['column_name'] for c in cols if c['initial_value']]
    rows.append([esc(n), t['column_count'], esc(', '.join(key) or '-'),
                 esc(', '.join(init_) or '-'),
                 esc(', '.join(calc[:4]) + (' …' if len(calc) > 4 else '') if calc else '-'),
                 esc(', '.join(sorted({c['type'] for c in cols})[:8]))])
w('columns.md', 'สรุปคอลัมน์ของตารางจริง 29 ตาราง',
  'หนึ่งแถว = หนึ่งตาราง · คอลัมน์ทั้งหมด 2,304 คอลัมน์อยู่ที่ `data/columns/all_columns.csv` '
  '· คอลัมน์ต่อตารางอยู่ที่ `data/tables/real/<slug>.csv`',
  ['ตาราง', 'คอลัมน์', 'คีย์', 'ค่าเริ่มต้น (Initial value)', 'คำนวณ (App formula)', 'ชนิดข้อมูล'], rows)

# --------------------------------------------------------------- formulas ---
rows = []
for r in sorted(fr, key=lambda x: (x['table_name'], x['column_name'])):
    f = r['formula']
    rows.append([esc(r['table_name']), esc(r['column_name']), esc(r['field']),
                 esc(f[:150]) + ('…' if len(f) > 150 else ''),
                 esc(r['functions_used']) or '-',
                 esc(r['column_references']) or '-', r['doc_page']])
w('formulas.md', 'สูตรทั้งหมด %d สูตร' % len(fr),
  'หนึ่งแถว = หนึ่งสูตร · ระดับคอลัมน์ 318 (App formula 191 + Initial value 127) '
  '· ระดับตาราง 29 (Expression for update mode 22 + Security filter 7)',
  ['ตาราง', 'คอลัมน์', 'ประเภท', 'สูตร', 'ฟังก์ชันที่ใช้', 'อ้างอิงคอลัมน์', 'หน้า PDF'], rows)

# ---------------------------------------------------------- views/actions ---
rows = []
for r in vw:
    rows.append(['วิว', esc(r['name']), esc(r.get('View type', '')),
                 esc(r.get('Visible?', '')), esc(r.get('Menu order', '')), r['doc_page']])
for r in ac2:
    rows.append(['แอคชัน', esc(r['name']), esc(r.get('Do this', '')[:40]),
                 esc(r.get('Prominence', '')),
                 esc(r.get('For a record of this table', '')),
                 esc(r.get('Attach to column', '')) or '-', r['doc_page']])
w('views-actions.md', 'วิว 115 ตัว + แอคชัน 214 ตัว',
  'หนึ่งแถว = หนึ่งวิวหรือหนึ่งแอคชัน · ไฟล์เต็ม: `data/views/views.csv`, `data/actions/actions.csv`',
  ['ชนิด', 'ชื่อ', 'View type / Do this', 'การมองเห็น / Prominence',
   'ตาราง', 'คอลัมน์', 'หน้า PDF'], rows)

# --------------------------------------------------------------- functions ---
rows = [[esc(r['function']), r['occurrences']] for r in fn]
w('functions.md', 'ฟังก์ชัน AppSheet ที่ใช้ในแอปนี้',
  f'ใช้ฟังก์ชัน {len(fn)} ตัว รวม {sum(int(r["occurrences"]) for r in fn)} ครั้งใน {len(fr)} สูตร · '
  'คำอธิบายความหมายในบริบทแอปอยู่ที่ `docs/05-formulas.md`',
  ['ฟังก์ชัน', 'จำนวนครั้ง'], rows)
print('digest done')
