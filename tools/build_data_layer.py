# -*- coding: utf-8 -*-
"""Build the AI-friendly data layer of the Phaopanya_Transport GitHub repo.

Source (read-only) : /workspace/appsheet-scg-jwd-transport
Target (written)   : /workspace/gh-repo

Everything in the target is a copy or a lossless transformation of the source;
the source tree is never modified.

Usage:  python3 build_data_layer.py [source_dir] [target_repo]
"""
import csv, json, os, re, shutil, sys, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else '/workspace/appsheet-scg-jwd-transport'
REPO = sys.argv[2] if len(sys.argv) > 2 else '/workspace/gh-repo'

# --------------------------------------------------------------------------
# English slugs.  Key = original table name (as shown in the app), value =
# meaningful english kebab-case slug.  Names that are already latin are
# translated to lower kebab-case; thai names are translated by hand so the
# slug keeps the meaning of the original table.
# --------------------------------------------------------------------------
REAL_SLUGS = {
    'SCGนครหลวงJWDภูมิภาค': 'scg-nakhonluang-jwd-region',
    'ข้อมูลการเข้าบำรุงรักษา': 'maintenance-arrival-data',
    'ข้อมูลการวางบิล': 'billing-data',
    'ตารางงานประจำวัน': 'daily-job-schedule',
    'ราคาน้ำมันดีเซล': 'diesel-price',
    'ราคาในระบบก่อนส่งสินค้า': 'system-price-before-delivery',
    'หน้าหลัก': 'home',
    'ปริ๊นใบวางบิล': 'print-invoice',
    'PDFพนักงาน': 'employee-pdf',
    'แจ้งปั ญหาระหว่างวัน': 'daily-issue-report',
    'รับงานคืนได้เงิน200': 'delivery-200-baht',
    'ข้อมูลงานRT': 'rt-job-data',
    'FILTER': 'filter',
    'ข้อมูลพนักงาน': 'employee-data',
    'ข้อมูลชื่องานต้นทางปลายทาง': 'job-name-data',
    'สรุปเบิกส่วนต่าง': 'expense-summary',
    'Doc_Return': 'doc-return',
    'Image_Doc_Return': 'image-doc-return',
    'ทำเบิกส่วนต่างScgวังน้อย': 'scg-wan-noy-expense',
    'ข้อมูลงานRW': 'rw-job-data',
    'สร้างเอกสาร': 'create-document',
    'ScanDocs': 'scan-docs',
    'สรุป_เจ้าของสินค้า': 'cargo-owner-summary',
    'สรุป_Shipment': 'shipment-summary',
    'PriceOverride': 'price-override',
    'Price_Table': 'price-table',
    'ส่งงานที่ยังไม่มีข้อมูลในระบบ': 'delivery-without-system-data',
    'Acknowledge_Logs': 'acknowledge-logs',
    'Announcements': 'announcements',
}

# bot tables: state tables and their step-output tables.
BOT_STATE_SLUGS = {
    'ปริ๊นใบวางบิล': 'print-invoice',
    'Telegram_แจ้งปั ญหา - 1': 'telegram-daily-issue-report',
    'Bot_รับสินค้าคืน - 1': 'bot-product-return',
    'เพิ่มรูปรับคืน - 1': 'add-return-photo',
    'ใบป่ ะหน้า - 1': 'delivery-note',
    'ปริ๊นใบวางบิลเอเทน - 1': 'print-invoice-atten',
    'สรุปส่วนต่าง - 1': 'expense-summary',
    'สรุปจำนวนจุดที่ส่งงานSCGวังน้อย': 'scg-wan-noy-delivery-points-summary',
    'ปริ๊นใบวางบิลโอนคลัง มโนยนต์ (นวนคร)': 'print-invoice-warehouse-transfer-motor-naw-nakhon',
    'ปริ๊นใบวางบิล_โอนคลัง กระสอบ2(บางบัวทอง)': 'print-invoice-warehouse-transfer-krachob2-bang-buathong',
    'ปริ๊นใบวางบิล_ไอโรบอท': 'print-invoice-ai-bot',
    'ปริ๊นใบวางบิล_โอนคลัง เอเธน': 'print-invoice-warehouse-transfer-atten',
    'ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) สตีเบล': 'print-invoice-receive-document-stibel',
    'ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง)': 'print-invoice-receive-document',
    '\u0e3a Bot_4ตัว_จัดเรียงเส้นทาง': 'bot-4-trucks-route-arrangement',
    'โอนคลัง (GQ) จีคิว': 'warehouse-transfer-gq-gqueue',
    'MeSpace': 'me-space',
    'ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย': 'print-invoice-warehouse-scg-jwd-wan-noy',
    'ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง': 'extra-200-no-return-store-not-in-delivery-point',
    'ทำเบิกค่ายกขึ้นชั้น': 'tier-fee-expense',
    'ได้เพิ่ม25%ของค่าเที่ยว': 'extra-25-percent-trip-fare',
    'ทำเบิกส่วนต่างScgวังน้อย - 1': 'scg-wan-noy-expense',
    'AppSheet_KM - 1': 'appsheet-km',
    'New bot - 1': 'new-bot',
    'Update ScanStatus เมื่อสแกน Invoice - 1': 'update-scan-status-on-invoice-scan',
    'ปริ๊นใบวางบิล_เบทาโกร+เหมาตู้': 'print-invoice-beta-plus-container-truck',
    'ปริ๊นใบวางบิล_LINEMAN (6W) (SCG Express)': 'print-invoice-lineman-6w-scg-express',
    'ปริ๊นใบวางบิล_Thai paper (SCG Express) - 1': 'print-invoice-thai-paper-scg-express',
    'ปริ๊นใบวางบิล_โอนคลัง บุญถาวร เกษตร_นวมินทร์ - 1': 'print-invoice-warehouse-transfer-buntawarn-kaset-nawamin',
    'Bot_เบิกค่าขนส่งตามระยะทาง - 1': 'bot-transport-cost-by-distance',
}

BOT_OUTPUT_SLUGS = {
    'ปริ๊นใบวางบิล_step Output': 'print-invoice-step-output',
    'Telegram_แจ้งปั ญหา2 Output': 'telegram-daily-issue-report2-output',
    'เข้ารับสินค้าคืน Output': 'product-return-intake-output',
    'New step Output': 'new-step-output',
    'Clear Output': 'clear-output',
    'เคลียสรุปจุดส่ง Output': 'clear-delivery-points-summary-output',
    'Clear Output 2': 'clear-output-2',
    'Clear Output 3': 'clear-output-3',
    'Clear Output 4': 'clear-output-4',
    'Clear Output 5': 'clear-output-5',
    'Clear Output 6': 'clear-output-6',
    'Clear Output 7': 'clear-output-7',
    'GoogleMapsRoutesAPI_Step Output': 'google-maps-routes-api-step-output',
    'Clear Output 8': 'clear-output-8',
    'Clear Output 9': 'clear-output-9',
    'Clear Output 10': 'clear-output-10',
    'ทำเบิกส่วนต่างScgวังน้อยstep Output': 'scg-wan-noy-expense-step-output',
    'New step2 Output': 'new-step2-output',
    'ไม่ผ่านNew step Output': 'not-passed-new-step-output',
    'AppSheet___KM Output': 'appsheet-km-output',
    'New step Output 2': 'new-step-output-2',
    'New step Output 3': 'new-step-output-3',
    'Update Output': 'update-output',
    'Clear Output 11': 'clear-output-11',
    'Clear Output 12': 'clear-output-12',
    'Clear Output 13': 'clear-output-13',
    'Clear Output 14': 'clear-output-14',
    'เบิกตามระยะทาง Output': 'transport-cost-by-distance-output',
    'New step4 Output': 'new-step4-output',
    'New step3 Output': 'new-step3-output',
}

STATE_PREFIX = 'Process for '
STATE_SUFFIX = ' Process Table'
UUID_RE = re.compile(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})')
HELPERS = {'_THISROW', '_ROWNUMBER', '_THIS', '_THISROW_BEFORE'}
FUNCS = re.compile(r'\b([A-Z][A-Z0-9_]{1,24})\s*\(')
REFS = re.compile(r'\[([^\[\]]+)\]')


# --------------------------------------------------------------- utilities ---
def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def norm(s):
    """Whitespace-insensitive key used to compare names mangled by the PDF."""
    return re.sub(r'\s+', '', s or '')


def uuids_of(source_path):
    return UUID_RE.findall(re.sub(r'\s+', '', source_path or ''))


def slug_of(table_name, kind):
    if kind == 'real':
        return REAL_SLUGS[table_name]
    if kind == 'process-state':
        proc = table_name[len(STATE_PREFIX):-len(STATE_SUFFIX)]
        return 'process-' + BOT_STATE_SLUGS[proc] + '-state'
    if kind == 'process-output':
        return BOT_OUTPUT_SLUGS[table_name]
    if kind == 'per-user-settings':
        return 'per-user-settings'
    raise KeyError(table_name)


# ------------------------------------------------------------------- load ---
index_rows = read_csv(os.path.join(SRC, 'tables/INDEX.csv'))
all_columns = read_csv(os.path.join(SRC, 'columns/all_columns.csv'))
by_type_rows = read_csv(os.path.join(SRC, 'columns/by_type.csv'))
formulas = read_csv(os.path.join(SRC, 'formulas/formulas.csv'))
functions_rows = read_csv(os.path.join(SRC, 'formulas/functions.csv'))
col_refs = read_csv(os.path.join(SRC, 'formulas/column_references.csv'))
views_rows = read_csv(os.path.join(SRC, 'views/views.csv'))
actions_rows = read_csv(os.path.join(SRC, 'actions/actions.csv'))
slices_rows = read_csv(os.path.join(SRC, 'slices/slices.csv'))
rules_rows = read_csv(os.path.join(SRC, 'format_rules/format_rules.csv'))

table_meta = {}
for r in index_rows:
    kind = r['classification']
    btk = r['bot_table_kind']
    slug = slug_of(r['table_name'], kind if kind == 'real' else btk)
    assert slug == slug.lower(), slug
    assert ' ' not in slug, slug
    table_meta[r['table_name']] = {
        'name': r['table_name'],
        'classification': kind,
        'bot_table_kind': btk,
        'slug': slug,
        'file_name': slug + '.csv',
        'file_path': 'data/tables/%s/%s.csv' % (kind, slug),
        'column_count': int(r['column_count']),
        'formula_column_count': int(r['formula_column_count']),
        'doc_page': int(r['doc_page']),
        'visible': r['visible'],
        'shared': r['shared'],
        'data_source': r['data_source'],
        'data_locale': r['data_locale'],
        'schema': r['schema'],
        'worksheet_qualifier': r['worksheet_qualifier'],
        'source_path': r['source_path'],
        'updates_allowed': r['updates_allowed'],
        'expression_for_update_mode': r['expression_for_update_mode'],
        'security_filter': r['security_filter'],
    }

# every slug must be unique
slugs = [m['slug'] for m in table_meta.values()]
assert len(set(slugs)) == len(slugs), 'slug collision'

# columns of each table
cols_of_table = collections.defaultdict(list)
for r in all_columns:
    cols_of_table[r['table_name']].append(r)

real_names = [m['name'] for m in table_meta.values() if m['classification'] == 'real']
bot_names = [m['name'] for m in table_meta.values() if m['classification'] == 'bot']


# ------------------------------------------------------------ 1. index.csv ---
INDEX_FIELDS = [
    'table_name', 'table_slug', 'classification', 'bot_table_kind',
    'column_count', 'formula_column_count', 'file_name', 'file_path',
    'doc_page', 'visible', 'shared', 'data_source', 'data_locale', 'schema',
    'worksheet_qualifier', 'source_path', 'updates_allowed',
    'expression_for_update_mode', 'security_filter',
]
index_out = []
for r in index_rows:
    m = table_meta[r['table_name']]
    row = dict(m)
    row['table_name'] = m['name']
    row['table_slug'] = m['slug']
    row['classification'] = m['classification']
    index_out.append(row)
write_csv(os.path.join(REPO, 'data/tables/index.csv'), INDEX_FIELDS, index_out)


# ------------------------------------- 2./3. one csv per table (real + bot) ---
COLUMN_FIELDS = list(all_columns[0].keys())      # identical header everywhere
assert 'table_name' in COLUMN_FIELDS and 'doc_page' in COLUMN_FIELDS

for kind, names in (('real', real_names), ('bot', bot_names)):
    for name in names:
        m = table_meta[name]
        rows = cols_of_table[name]
        assert len(rows) == m['column_count'], (name, len(rows), m['column_count'])
        write_csv(os.path.join(REPO, m['file_path']), COLUMN_FIELDS, rows)


# ------------------------------------------------------ 4. columns/by-type ---
type_info = collections.defaultdict(lambda: {'count': 0, 'tables': set(), 'page': None})
for r in all_columns:
    t = r['type']
    info = type_info[t]
    info['count'] += 1
    info['tables'].add(r['table_name'])
    p = int(r['doc_page'])
    info['page'] = p if info['page'] is None else min(info['page'], p)
by_type_out = [
    {'type': t, 'column_count': i['count'], 'table_count': len(i['tables']),
     'doc_page': i['page']}
    for t, i in sorted(type_info.items(), key=lambda kv: (-kv[1]['count'], kv[0]))
]
write_csv(os.path.join(REPO, 'data/columns/by-type.csv'),
          ['type', 'column_count', 'table_count', 'doc_page'], by_type_out)

# all_columns.csv - verbatim copy (header identical to the per-table files)
write_csv(os.path.join(REPO, 'data/columns/all_columns.csv'), COLUMN_FIELDS, all_columns)


# ------------------------------------- 5. views / actions / slices / rules ---
def strip_name_col(rows, key, label):
    """The source 'name' column is a parse artefact ("name <x>"); replace it
    with the real label field of the record."""
    out = []
    for r in rows:
        d = {k: v for k, v in r.items() if k != 'name'}
        value = r.get(label) or (r.get('name') or '')
        value = value.replace('name ', '', 1).replace('Name ', '', 1).strip()
        d[key] = value
        out.append(d)
    return out


def order_fields(primary, rows, drop=()):
    seen = [primary] + sorted({k for r in rows for k in r if k not in (primary,) + drop})
    return seen


# The source files use the AppSheet UI labels as csv headers ("Bulk action?").
# They are English but not machine friendly, so they are converted to
# snake_case; the values are untouched.
HEADER_ALIASES = {
    'ActionType': 'action_type',
}


def snake(name):
    if name in HEADER_ALIASES:
        return HEADER_ALIASES[name]
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


def snake_headers(rows):
    out = []
    for r in rows:
        out.append({snake(k): v for k, v in r.items()})
    return out


def strip_name_col(rows, key, label):
    """Kept for reference: the source 'name' column is a parse artefact."""
    out = []
    for r in rows:
        d = {k: v for k, v in r.items() if k != 'name'}
        value = r.get(label) or (r.get('name') or '')
        value = value.replace('name ', '', 1).replace('Name ', '', 1).strip()
        d[key] = value
        out.append(d)
    return out


def build_ux_rows(rows, primary, label, rename=None):
    """The source files carry a parse artefact column ("name <x>") and use the
    AppSheet UI labels as csv headers.  The artefact is dropped, the record
    name becomes the primary column, optional labels are renamed and the
    remaining headers are converted to snake_case (values are untouched)."""
    rename = rename or {}
    out = []
    for r in rows:
        d = {k: v for k, v in r.items() if k not in ('name', label)}
        d[primary] = (r.get(label) or (r.get('name') or '')).replace('name ', '', 1) \
            .replace('Name ', '', 1).strip()
        for old, new in rename.items():
            if old in d:
                d[new] = d.pop(old)
        out.append({snake(k): v for k, v in d.items()})
    return out


view_rows = build_ux_rows(views_rows, 'view_name', 'View name')
write_csv(os.path.join(REPO, 'data/views/views.csv'),
          order_fields('view_name', view_rows), view_rows)

action_rows = build_ux_rows(actions_rows, 'action_name', 'Action name')
write_csv(os.path.join(REPO, 'data/actions/actions.csv'),
          order_fields('action_name', action_rows), action_rows)

slice_rows = build_ux_rows(slices_rows, 'slice_name', 'Slice Name')
write_csv(os.path.join(REPO, 'data/slices/slices.csv'),
          order_fields('slice_name', slice_rows), slice_rows)

rule_rows = build_ux_rows(rules_rows, 'rule_name', 'Rule name',
                           rename={'For this data': 'source_table'})
write_csv(os.path.join(REPO, 'data/format-rules/format_rules.csv'),
          order_fields('rule_name', rule_rows), rule_rows)


# ------------------------------------------------------------ 6. schema json ---
with open(os.path.join(SRC, 'schema/app_schema.json'), encoding='utf-8') as f:
    schema = json.load(f)
for t in schema.get('tables', []):
    m = table_meta.get(t['name'])
    if m:
        t['table_slug'] = m['slug']
        t['file_path'] = m['file_path']
        t['column_count'] = m['column_count']
        t['formula_column_count'] = m['formula_column_count']
schema['data_layer'] = {
    'tables_index': 'data/tables/index.csv',
    'table_name_map': 'data/references/table-name-map.csv',
    'processes': 'data/references/processes.csv',
    'column_references': 'data/references/column-references.csv',
    'view_to_table': 'data/references/view-to-table.csv',
    'action_to_table': 'data/references/action-to-table.csv',
    'function_usage': 'data/references/function-usage.csv',
    'all_columns': 'data/columns/all_columns.csv',
    'columns_by_type': 'data/columns/by-type.csv',
    'workbook': 'xlsx/appsheet-export.xlsx',
    'note': 'Every table_name in this schema maps to exactly one csv file; '
            'the mapping is listed in tables_index and table_name_map.',
}
os.makedirs(os.path.join(REPO, 'data/schema'), exist_ok=True)
with open(os.path.join(REPO, 'data/schema/app-schema.json'), 'w', encoding='utf-8') as f:
    json.dump(schema, f, ensure_ascii=False, indent=2)


# =========================== 7. references ==================================
REF = os.path.join(REPO, 'data/references')

# --- 7.1 table-name-map -----------------------------------------------------
tmap = []
for r in index_rows:
    m = table_meta[r['table_name']]
    tmap.append({
        'table_name': m['name'],
        'table_slug': m['slug'],
        'file_name': m['file_name'],
        'file_path': m['file_path'],
        'classification': m['classification'],
        'bot_table_kind': m['bot_table_kind'],
        'column_count': m['column_count'],
        'formula_column_count': m['formula_column_count'],
        'doc_page': m['doc_page'],
    })
write_csv(os.path.join(REF, 'table-name-map.csv'), list(tmap[0].keys()), tmap)

# --- 7.2 processes ----------------------------------------------------------
state_meta = {n: m for n, m in table_meta.items() if m['bot_table_kind'] == 'process-state'}
out_meta = {n: m for n, m in table_meta.items() if m['bot_table_kind'] == 'process-output'}
# bind state table -> step output table through the uuid in Source Path
for n, m in out_meta.items():
    su = uuids_of(m['source_path'])
    m['_state_uuid'] = su[1] if len(su) > 1 else (su[0] if su else '')

proc_rows = []
for name, m in state_meta.items():
    proc = name[len(STATE_PREFIX):-len(STATE_SUFFIX)]
    su = uuids_of(m['source_path'])
    state_uuid = su[1] if len(su) > 1 else (su[0] if su else '')
    bound = [o for o, om in out_meta.items() if om['_state_uuid'] == state_uuid]
    # the ref column inside the state table that points at the step output
    binding = []
    state_columns = {norm(c['column_name']): c['column_name']
                     for c in cols_of_table.get(name, [])}
    for o in bound:
        # the step name is the tail of the source path
        # /ProcessStateTables/<app>/<state-uuid>/StepOutput_<step>
        sp = re.sub(r'\s+', '', out_meta[o]['source_path'])
        step = sp.split('StepOutput_')[-1] if 'StepOutput_' in sp else ''
        if step and norm(step) in state_columns:
            binding.append(state_columns[norm(step)])
    proc_rows.append({
        'process_name': proc,
        'state_table_name': name,
        'state_table_slug': m['slug'],
        'state_table_uuid': state_uuid,
        'state_table_file': m['file_path'],
        'step_output_name': '; '.join(bound),
        'step_output_slug': '; '.join(table_meta[o]['slug'] for o in bound),
        'step_output_file': '; '.join(table_meta[o]['file_path'] for o in bound),
        'binding_column': '; '.join(binding),
        'column_count': m['column_count'],
        'formula_column_count': m['formula_column_count'],
        'doc_page': m['doc_page'],
    })
proc_rows.sort(key=lambda r: r['doc_page'])
write_csv(os.path.join(REF, 'processes.csv'), list(proc_rows[0].keys()), proc_rows)

# --- 7.3 column-references --------------------------------------------------
formula_by_key = {}
for f in formulas:
    formula_by_key.setdefault((f['table_name'], f['column_name'], f['field']), f)

col2tables = collections.defaultdict(set)
for r in all_columns:
    col2tables[r['column_name']].add(r['table_name'])

ref_rows = []
for r in col_refs:
    ref = r['reference']
    is_helper = ref in HELPERS
    candidates = sorted(col2tables.get(ref, []))
    f = formula_by_key.get((r['table_name'], r['column_name'], r['field']))
    if is_helper:
        kind, resolves = 'helper', 'no'
    elif candidates:
        kind, resolves = 'column', 'yes'
    else:
        kind, resolves = 'unknown', 'no'
    ref_rows.append({
        'table_name': r['table_name'],
        'column_name': r['column_name'],
        'field': r['field'],
        'formula': (f or {}).get('formula', ''),
        'reference': ref,
        'reference_kind': kind,
        'resolves': resolves,
        'is_helper': 'yes' if is_helper else 'no',
        'resolved_tables': '; '.join(candidates),
        'resolved_table_count': len(candidates),
        'doc_page': (f or {}).get('doc_page', ''),
    })
write_csv(os.path.join(REF, 'column-references.csv'), list(ref_rows[0].keys()), ref_rows)

# --- 7.4 view-to-table ------------------------------------------------------
JSON_KEYS = {
    'ColumnOrder', 'GroupBy', 'GroupAggregate', 'SortBy', 'PrimarySortColumn',
    'PrimarySortDescending', 'Events', 'EventType', 'EventAction', 'Icon',
    'IconRunnerUps', 'MenuOrder', 'ColumnWidth', 'EnableQuickEdit', 'RowKey',
    'FormStyle', 'PageStyle', 'FormFooterStyle', 'MaxNestedRows', 'AudioInput',
    'FinishView', 'AutoSave', 'AutoReopen', 'MainSlideshowImageColumn',
    'DetailContentColumn', 'HeaderColumns', 'QuickEditColumns', 'ImageStyle',
    'Layout', 'UseCardLayout', 'DisplayMode', 'SlideshowMode',
    'DesktopSplitMode', 'UseDesktopMultiColumn', 'ShowInNavigation',
    'ShowInActionBar', 'ShowInDetailView', 'ShowInEditView', 'ShowInDeck',
    'ShowInGallery', 'EditMode', 'MainDeckImageColumn', 'ImageShape',
    'PrimaryDeckHeaderColumn', 'SecondaryDeckHeaderColumn', 'DeckSummaryColumn',
    'DeckNestedTableColumn',
    'ShowActionBar', 'TemplateFillColumns', 'TemplateFillComplete',
    'TemplateFillExistingRecords', 'TemplateFillSettings', 'AutoEnable',
    'RequireApproval', 'ApprovalEmailMessage', 'ApprovalEmailMessageFrom',
    'ApprovalEmailMessageSubject', 'ApprovalEmailMessageBody',
    'ApprovalPushNotification', 'ApprovalPushNotificationTitle',
    'ApprovalPushNotificationBody', 'ApprovalPushNotificationSound',
    'ApprovalPushNotificationIcon', 'ApprovalPushNotificationImage',
    'ApprovalNotificationsEnabled', 'WorkflowEmailMessage', 'EmailMessage',
    'EmailMessageFrom', 'EmailMessageSubject', 'EmailMessageBody',
    'EmailMessageContent', 'EmailMessageContentType', 'ContentType',
    'AttachTo', 'Attachment', 'Description', 'Subject', 'Recipient', 'Body',
    'AttachToColumn', 'To', 'CC', 'BCC', 'Type', 'URL', 'OpenURL',
    'CloseDialog', 'SetValue', 'Value', 'Column', 'Order', 'Data', 'Show',
    'Hide', 'Save', 'Delete', 'Cancel', 'Sheet', 'Group', 'Filter', 'Search',
    'Sort', 'Menu', 'Text', 'Number', 'Decimal', 'Price', 'Date', 'DateTime',
    'Time', 'Duration', 'Percent', 'PercentDone', 'Rating', 'Scale', 'Checkbox',
    'Switch', 'Button', 'Image', 'Signature', 'Drawing', 'Barcode', 'QRCode',
    'Location', 'YesNo', 'Normal', 'Call', 'SMS', 'Email', 'PDF', 'Default',
    'MenuItem', 'Chat', 'Mention', 'Fit', 'IsPrimarySortDescending',
}
JSON_VALUES = {
    '**auto**', '** none**', '**Automatic**', 'fa-list- ul', 'fa-list-ul',
    'fa- edit', 'fa-indent', 'Ascending', 'Descending', 'NONE', 'SUM', 'menu',
    'left', 'right most', 'Default', 'Form Saved', 'Row Selected', 'Split view',
    'Fill', 'Automatic', 'Plain Text', 'Square Image', '**auto**',
}
VIEW_SUFFIXES = ('Detail', 'Form', 'Inline', 'Table', 'Gallery', 'Deck')
slice_source = {r['slice_name']: r.get('source_table', '')
                for r in slice_rows if r['slice_name'] and r.get('source_table', '')}

# column name -> tables (normalised), used to score a view configuration
norm2real = collections.defaultdict(set)
norm2all = collections.defaultdict(set)
for r in all_columns:
    norm2all[norm(r['column_name'])].add(r['table_name'])
    if r['table_name'] in real_names:
        norm2real[norm(r['column_name'])].add(r['table_name'])


def view_config_tokens(v):
    raw = (v.get('position', '') or '') + ' ' + (v.get('view_configuration', '') or '')
    out = []
    for m in re.finditer(r'"([^"]{1,120})"', raw):
        t = m.group(1).strip()
        if not t or t in JSON_KEYS or t in JSON_VALUES:
            continue
        if t.startswith(':') or t in (',', ':', '::'):
            continue
        out.append(t)
    return out


view_map_rows = []
for v in view_rows:
    name = v['view_name']
    vtype = v.get('view_type', '')
    table, method, confidence, evidence = '', '', 'none', ''
    # 1) <table>_<Detail|Form|Inline|Table|Gallery|Deck>
    for t in real_names:
        for s in VIEW_SUFFIXES:
            if name == '%s_%s' % (t, s):
                table, method, confidence, evidence = t, 'name_pattern', 'high', name
                break
        if table:
            break
    # 2) view name == table name
    if not table and name in real_names:
        table, method, confidence, evidence = name, 'exact_name', 'high', name
    # 3) view name == slice name
    if not table and name in slice_source:
        table, method, confidence, evidence = slice_source[name], 'slice_name', 'high', name
    # 4) view name without _Detail/_Form == slice name
    if not table:
        base = re.sub(r'_(Detail|Form)$', '', name)
        if base != name and base in slice_source:
            table, method, confidence, evidence = (slice_source[base],
                                                   'slice_name_stripped', 'medium', base)
    # 5) view name starts / ends with a slice name
    if not table:
        for sn, st in slice_source.items():
            if name.startswith(sn) or name.endswith(sn):
                table, method, confidence, evidence = st, 'slice_name_affix', 'medium', sn
                break
    # 6) view name contains exactly one real table name
    if not table:
        hits = [t for t in real_names if t in name and t != name]
        if len(hits) == 1:
            table, method, confidence, evidence = hits[0], 'name_contains_table', 'medium', hits[0]
    # 7) columns used by the view configuration
    if not table:
        tokens = view_config_tokens(v)
        score = collections.Counter()
        hits = collections.defaultdict(list)
        for t in tokens:
            for tb in norm2real.get(norm(t), ()):  # real tables only
                score[tb] += 1
                hits[tb].append(t)
        if score:
            ranked = score.most_common()
            best, best_score = ranked[0]
            second = ranked[1][1] if len(ranked) > 1 else 0
            if best_score >= 2 and best_score > second:
                table = best
                method = 'view_config_columns'
                confidence = 'medium' if best_score >= 3 else 'low'
                evidence = '; '.join(list(dict.fromkeys(hits[best]))[:6])
    m = table_meta.get(table)
    view_map_rows.append({
        'view_name': name,
        'view_type': vtype,
        'table_name': table,
        'table_slug': m['slug'] if m else '',
        'table_file': m['file_path'] if m else '',
        'match_method': method or 'unmatched',
        'confidence': confidence,
        'match_evidence': evidence,
        'doc_page': v.get('doc_page', ''),
    })
write_csv(os.path.join(REF, 'view-to-table.csv'), list(view_map_rows[0].keys()), view_map_rows)

# --- 7.5 action-to-table ----------------------------------------------------
DO_THIS_FIX = {
    '': 'UNKNOWN',
    '{"Prominence":"Display_Overlay","NeedsConfirmation":false,"Con firmationMessage":"","ModifiesData":true,"BulkApplicable":true} ADD_RECORD': 'ADD_RECORD',
}
action_map_rows = []
for a in action_rows:
    table = (a.get('for_a_record_of_this_table', '') or '').strip()
    m = table_meta.get(table)
    raw_do = a.get('do_this', '') or ''
    do_this = DO_THIS_FIX.get(raw_do, raw_do)
    attach = (a.get('attach_to_column', '') or '').strip()
    setc = (a.get('set_this_column', '') or '').strip()
    in_table = ''
    if attach:
        cols = {norm(c['column_name']) for c in cols_of_table.get(table, [])}
        in_table = 'yes' if norm(attach) in cols else 'no'
    action_map_rows.append({
        'action_name': a['action_name'],
        'do_this': do_this,
        'do_this_raw': raw_do,
        'table_name': table,
        'table_slug': m['slug'] if m else '',
        'table_file': m['file_path'] if m else '',
        'attach_to_column': attach,
        'attach_column_in_table': in_table,
        'set_this_column': setc,
        'action_scope': (a.get('does_this_action_apply_to_the_whole_table', '') or '').strip(),
        'modifies_data': (a.get('modifies_data', '') or '').strip(),
        'prominence': (a.get('prominence', '') or '').strip(),
        'visible': (a.get('visible', '') or '').strip(),
        'doc_page': a.get('doc_page', ''),
    })
write_csv(os.path.join(REF, 'action-to-table.csv'), list(action_map_rows[0].keys()), action_map_rows)

# --- 7.6 function-usage -----------------------------------------------------
fn_tables = collections.defaultdict(set)
fn_cols = collections.defaultdict(set)
fn_count = collections.Counter()
fn_page = {}
for f in formulas:
    for fn in FUNCS.findall(f['formula'] or ''):
        fn_count[fn] += 1
        fn_tables[fn].add(f['table_name'])
        fn_cols[fn].add('%s.%s' % (f['table_name'], f['column_name']))
        p = int(f['doc_page'])
        fn_page[fn] = p if fn not in fn_page else min(fn_page[fn], p)
# keep the same order/counts as the source functions.csv
src_counts = {r['function']: int(r['occurrences']) for r in functions_rows}
fn_rows = []
for fn, cnt in sorted(src_counts.items(), key=lambda kv: (-kv[1], kv[0])):
    fn_rows.append({
        'function': fn,
        'occurrences': cnt,
        'table_count': len(fn_tables.get(fn, ())),
        'tables': '; '.join(sorted(fn_tables.get(fn, ()))),
        'column_count': len(fn_cols.get(fn, ())),
        'columns': '; '.join(sorted(fn_cols.get(fn, ()))),
        'doc_page': fn_page.get(fn, ''),
    })
write_csv(os.path.join(REF, 'function-usage.csv'), list(fn_rows[0].keys()), fn_rows)


# --- formulas (every formula of the app, with its owner and page) ----------
formula_out = []
for f in formulas:
    formula_out.append({
        'table_name': f['table_name'],
        'column_name': f['column_name'],
        'field': f['field'],
        'formula': f['formula'],
        'functions_used': f.get('functions_used', ''),
        'column_references': f.get('column_references', ''),
        'doc_page': f['doc_page'],
    })
write_csv(os.path.join(REPO, 'data/formulas/formulas.csv'),
          list(formula_out[0].keys()), formula_out)


# ------------------------------------------------ 8. workbook + 9. tools ---
os.makedirs(os.path.join(REPO, 'xlsx'), exist_ok=True)
shutil.copy2(os.path.join(SRC, 'appsheet-export.xlsx'),
             os.path.join(REPO, 'xlsx/appsheet-export.xlsx'))

TOOL_FILES = ['appsheet_parse.py', 'extract_words.py', 'verify_roundtrip.py',
              'build_repo.py', 'build_readme.py', 'build_workbook.py',
              'run_pipeline.sh']
os.makedirs(os.path.join(REPO, 'tools'), exist_ok=True)
for fn in TOOL_FILES:
    shutil.copy2(os.path.join(SRC, 'tools', fn), os.path.join(REPO, 'tools', fn))
os.chmod(os.path.join(REPO, 'tools/run_pipeline.sh'), 0o755)


# ------------------------------------------------------------- self check ---
def count_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return sum(1 for _ in csv.DictReader(f))


real_files = sorted(os.listdir(os.path.join(REPO, 'data/tables/real')))
bot_files = sorted(os.listdir(os.path.join(REPO, 'data/tables/bot')))
rows_total = 0
for fn in real_files + bot_files:
    d = 'real' if fn in real_files else 'bot'
    rows_total += count_rows(os.path.join(REPO, 'data/tables', d, fn))
print('real files      :', len(real_files))
print('bot files       :', len(bot_files))
print('rows in tables  :', rows_total)
print('all_columns rows:', count_rows(os.path.join(REPO, 'data/columns/all_columns.csv')))
print('index rows      :', count_rows(os.path.join(REPO, 'data/tables/index.csv')))
print('views mapped    :', sum(1 for r in view_map_rows if r['table_name']),
      '/', len(view_map_rows))
print('processes       :', len(proc_rows))
print('column refs     :', len(ref_rows))
print('actions         :', len(action_map_rows))
print('functions       :', len(fn_rows))
