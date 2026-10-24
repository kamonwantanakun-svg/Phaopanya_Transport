# -*- coding: utf-8 -*-
"""Generate MANIFEST.json for the Phaopanya_Transport repo from what is on disk."""
import csv, json, os, collections, datetime, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else '/workspace/gh-repo'


def load(p):
    with open(os.path.join(REPO, p), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


idx = load('data/tables/index.csv')
ac = load('data/columns/all_columns.csv')
fr = load('data/formulas/formulas.csv')
fn = load('data/references/function-usage.csv')
cr = load('data/references/column-references.csv')
vw = load('data/views/views.csv')
ac2 = load('data/actions/actions.csv')
sl = load('data/slices/slices.csv')
frl = load('data/format-rules/format_rules.csv')
bt = load('data/columns/by-type.csv')
proc = load('data/references/processes.csv')

tree = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn_ in sorted(files):
        p = os.path.relpath(os.path.join(root, fn_), REPO)
        tree.append(p.replace(os.sep, '/'))

manifest = {
    'repo': 'Phaopanya_Transport',
    'app': {
        'name': 'เผ่าปั ญญาทรานสปอร์ต',
        'name_en': 'SCG JWD Transport',
        'version': '1.004638',
        'platform': 'AppSheet',
        'domain': 'ระบบจัดการงานขนส่งและกระจายสินค้า (last-mile delivery) ภูมิภาคนครหลวง + JWD',
    },
    'source': {
        'document': 'Application Documentation.PDF',
        'pages': 1946,
        'generated_at': '15/9/2569 02:56:32',
        'extracted_by': 'tools/appsheet_parse.py (see tools/README.md)',
        'verification': 'docs/VERIFICATION_REPORT.md',
    },
    'counts': {
        'tables_total': len(idx),
        'tables_real': sum(1 for r in idx if r.get('classification') == 'real'),
        'tables_bot': sum(1 for r in idx if r.get('classification') == 'bot'),
        'bot_processes': len(proc),
        'columns': len(ac),
        'column_types': len(bt),
        'formulas': len(fr),
        'functions': len(fn),
        'function_calls': sum(int(r['occurrences']) for r in fn),
        'views': len(vw),
        'actions': len(ac2),
        'slices': len(sl),
        'format_rules': len(frl),
        'column_references': len(cr),
    },
    'layout': {
        'README.md': 'entry point - overview, file map, question router',
        'AGENTS.md': 'operating manual for AI agents - rules, conventions, pitfalls',
        'MANIFEST.json': 'this file - machine readable index',
        'docs/': 'Thai manual (10 topics) + verification report',
        'digest/': 'compact reference tables for fast AI reading',
        'data/': 'raw extracted data (CSV + JSON) - source of truth',
        'data/references/': 'join tables (processes, column references, view/action mapping)',
        'xlsx/': 'multi-sheet workbook for humans',
        'tools/': 'scripts to re-extract everything from the source PDF',
    },
    'conventions': {
        'one_row_per': 'column (per-table files) / record (global files)',
        'table_name_column': 'always keeps the original Thai table name',
        'doc_page': 'page number in the source PDF (1-based)',
        'file_names': 'english, lowercase, dash-separated',
        'encoding': 'utf-8',
    },
    'files': sorted(tree),
    'manifest_generated_at': datetime.datetime.now().isoformat(timespec='seconds'),
}

with open(os.path.join(REPO, 'MANIFEST.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(json.dumps(manifest['counts'], ensure_ascii=False, indent=2))
print('files listed:', len(tree))
