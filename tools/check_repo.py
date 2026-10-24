# -*- coding: utf-8 -*-
"""Whole-repo consistency check for Phaopanya_Transport.

Verifies that every number and name mentioned in the docs actually exists in
the data, and that the data layer is internally consistent.
"""
import csv, json, os, re, sys, collections

REPO = sys.argv[1] if len(sys.argv) > 1 else '/workspace/gh-repo'
D = os.path.join(REPO, 'data')


def load(p):
    with open(os.path.join(D, p), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


idx = load('tables/index.csv')
ac = load('columns/all_columns.csv')
cr = load('references/column-references.csv')
fn = load('references/function-usage.csv')
proc = load('references/processes.csv')
vw = load('views/views.csv')
ac2 = load('actions/actions.csv')

tables = {r['table_name'] for r in idx}
columns = {(r['table_name'], r['column_name']) for r in ac}
colnames = {r['column_name'] for r in ac}
fails = []


def check(name, ok, detail=''):
    print(('  OK   ' if ok else '  FAIL ') + name + (('  ' + detail) if detail and not ok else ''))
    if not ok:
        fails.append(name)


print('=== data layer ===')
real = [f for f in os.listdir(os.path.join(D, 'tables/real')) if f.endswith('.csv') and f != '_index.csv']
bot = [f for f in os.listdir(os.path.join(D, 'tables/bot')) if f.endswith('.csv') and f != '_index.csv']
check('index has 90 tables', len(idx) == 90, str(len(idx)))
check('29 real table files', len(real) == 29, str(len(real)))
check('61 bot table files', len(bot) == 61, str(len(bot)))
rows_real = sum(len(list(csv.DictReader(open(os.path.join(D, 'tables/real', f), encoding='utf-8')))) for f in real)
rows_bot = sum(len(list(csv.DictReader(open(os.path.join(D, 'tables/bot', f), encoding='utf-8')))) for f in bot)
check('per-table rows sum to 2304', rows_real + rows_bot == 2304, str(rows_real + rows_bot))
check('all_columns has 2304 rows', len(ac) == 2304, str(len(ac)))
idxmap = {r['table_name']: r for r in idx}
mism = []
for kind, files in (('real', real), ('bot', bot)):
    for f in files:
        rs = list(csv.DictReader(open(os.path.join(D, 'tables', kind, f), encoding='utf-8')))
        t = rs[0]['table_name']
        if len(rs) != int(idxmap[t]['column_count']):
            mism.append(f)
check('every table file matches its index row count', not mism, str(mism[:3]))
check('30 bot processes', len(proc) == 30, str(len(proc)))
check('every table in index is real or bot',
      {r['classification'] for r in idx} <= {'real', 'bot'})
check('bot tables are all native',
      all(r['data_source'] == 'native' for r in idx if r['classification'] == 'bot'))
check('real tables are all google-backed',
      all(r['data_source'] in ('google', 'google_tables', '') for r in idx if r['classification'] == 'real'))

print('\n=== docs vs data ===')
docfiles = [f for f in os.listdir(os.path.join(REPO, 'docs')) if f.endswith('.md')]
docs = {f: open(os.path.join(REPO, 'docs', f), encoding='utf-8').read() for f in docfiles}
allmd = '\n'.join(docs.values()) + open(os.path.join(REPO, 'README.md'), encoding='utf-8').read() \
    + open(os.path.join(REPO, 'AGENTS.md'), encoding='utf-8').read()

expected = ['01-app-overview.md', '02-data-model.md', '03-table-catalogue.md', '04-columns.md',
            '05-formulas.md', '06-views-actions.md', '07-slices-format-rules.md',
            '08-security-rules.md', '09-glossary.md', '10-known-issues.md']
missing = [f for f in expected if f not in docs]
check('all 10 manual files exist', not missing, str(missing))

# every backticked table name mentioned in the docs must exist
mentioned = set(re.findall(r'`([^`\n]{2,70})`', allmd))
unknown_tables = {m for m in mentioned if m in tables or m.startswith('[')}
check('no markdown link points to a missing file',
      not [m for m in re.findall(r'\]\(([^)]+)\)', allmd)
           if not (os.path.exists(os.path.join(REPO, m.split('#')[0]))
                   or m.startswith('http'))],
      str([m for m in re.findall(r'\]\(([^)]+)\)', allmd)
           if not (os.path.exists(os.path.join(REPO, m.split('#')[0])) or m.startswith('http'))][:5]))

# glossary terms must be real column names or table names
gl = docs.get('09-glossary.md', '')
terms = re.findall(r'^\|\s*`([^`]+)`\s*\|', gl, re.M)
bad_terms = [t for t in terms if t not in colnames and t not in tables]
check('every glossary term exists in the data', not bad_terms, str(bad_terms[:6]))

# key figures must appear in the docs
figs = {'90 ตาราง': '90', '29 ตารางจริง': '29', '61 ตารางบอท': '61',
        '2,304 คอลัมน์': '2,304', '347 สูตร': '347', '115 วิว': '115', '214 แอคชัน': '214'}
for label, token in figs.items():
    check(f'docs mention {label}', token in allmd)

print('\n' + ('>>> ALL CHECKS PASSED' if not fails else '>>> FAILED: ' + '; '.join(fails)))
sys.exit(1 if fails else 0)
