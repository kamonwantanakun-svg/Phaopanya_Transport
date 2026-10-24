# -*- coding: utf-8 -*-
"""Build the GitHub-ready repository from the parsed AppSheet documentation.

Usage:  python3 tools/build_repo.py work/records.json <repo-dir>
"""
import csv, json, os, re, sys, collections, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- helpers ---
def slug(name, used):
    s = re.sub(r'[^\w\-]+', '-', name, flags=re.UNICODE).strip('-') or 'table'
    s = s[:70]
    base, i = s, 2
    while s.lower() in used:
        s = f'{base}-{i}'
        i += 1
    used.add(s.lower())
    return s


def read_csv_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


FUNCS = re.compile(r'\b([A-Z][A-Z0-9_]{1,24})\s*\(')
REFS = re.compile(r'\[([^\[\]]+)\]')


def functions_of(text):
    out = []
    for m in FUNCS.finditer(text or ''):
        f = m.group(1)
        if f not in out:
            out.append(f)
    return out


def refs_of(text):
    out = []
    for m in REFS.finditer(text or ''):
        r = m.group(1)
        if r not in out:
            out.append(r)
    return out


def qualifier_fields(raw):
    """Flatten the JSON type qualifier into readable columns."""
    out = {}
    if not raw:
        return out
    try:
        d = json.loads(raw)
    except Exception:
        return out
    if not isinstance(d, dict):
        return out
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False)
        out[k] = str(v)
    return out


# --------------------------------------------------------------- the build ---
def build(records_path, repo):
    recs = json.load(open(records_path, encoding='utf-8'))

    app = next(r for r in recs if r['kind'] == 'app')
    tables = [r for r in recs if r['kind'] == 'table']
    schemas = [r for r in recs if r['kind'] == 'schema']
    columns = [r for r in recs if r['kind'] == 'column']
    slices = [r for r in recs if r['kind'] == 'slice']
    views = [r for r in recs if r['kind'] == 'view']
    rules = [r for r in recs if r['kind'] == 'format_rule']
    actions = [r for r in recs if r['kind'] == 'action']

    # ---- classify tables -------------------------------------------------
    def classify(f):
        ds = (f.get('Data Source') or '').strip()
        sp = re.sub(r'\s+', '', f.get('Source Path') or '')
        if ds.startswith('native') or sp.startswith('/ProcessStateTables/') \
                or sp == '_Per User Settings' or '/StepOutput_' in sp:
            return 'bot'
        return 'real'

    def bot_kind(f):
        sp = re.sub(r'\s+', '', f.get('Source Path') or '')
        nm = re.sub(r'\s+', '', f.get('Table name') or '')
        if sp == '_PerUserSettings':
            return 'per-user-settings'
        # a step output points at the artefact of one bot step; its path still
        # lives under /ProcessStateTables/, so it has to be tested first
        if 'StepOutput_' in sp:
            return 'process-output'
        if sp.startswith('/ProcessStateTables/'):
            return 'process-state'
        if nm.endswith('Output') or 'Output' in nm:
            return 'process-output'
        return 'other'

    # ---- map schema -> table, and column -> table ------------------------
    schema_to_table = {}
    for s in schemas:
        # the schema name is also in the heading, which is always present
        sname = (s['fields'].get('Schema Name', '').strip()
                 or s['name'].replace('Schema Name ', '', 1).strip())
        for t in tables:
            tname = t['fields'].get('Table name', '').strip()
            if sname == f'{tname}_Schema' or sname == tname:
                schema_to_table[s['name']] = tname
                break
        else:
            schema_to_table[s['name']] = ''

    # Walk the records in order: a column belongs to the schema that precedes
    # it.  (Column record names such as "Column 1: _RowNumber" repeat in every
    # table, so they cannot be used as a key.)
    own = collections.defaultdict(list)
    cur_schema = None
    for r in recs:
        if r['kind'] == 'schema':
            cur_schema = r['name']
        elif r['kind'] == 'column':
            own[schema_to_table.get(cur_schema or '', '')].append(r)

    # The document prints one schema twice, so its columns appear twice.  Keep
    # the first copy of every (column name, type) pair of that schema.
    for tbl in list(own):
        seen = set()
        keep = []
        for c in own[tbl]:
            key = (c['fields'].get('Column name', ''), c['fields'].get('Type', ''),
                   c['fields'].get('App formula', ''), c['fields'].get('Initial value', ''))
            if key in seen:
                continue
            seen.add(key)
            keep.append(c)
        own[tbl] = keep
    col_table = {}
    for tbl, cl in own.items():
        seen = set()
        for c in cl:
            key = (c['fields'].get('Column name', ''), c['page'])
            col_table[id(c)] = tbl

    # ---- app metadata ----------------------------------------------------
    def appfield(k):
        return app['fields'].get(k, '')

    app_meta = {
        'app_name': appfield('App title') or 'เผ่าปั ญญา ทรานสปอร์ต',
        'app_folder': appfield('Default app folder'),
        'version': appfield('Version'),
        'function': appfield('Function'),
        'runnable': appfield('Runnable?'),
        'deployable': appfield('Deployable?'),
        'personal_use_only': appfield('Personal use only?'),
        'document_generated_at': appfield('Generated at'),
        'document_header': appfield('Document header'),
        'counts_reported_by_app': {
            'tables': appfield('Counts: Data'),
            'ux': appfield('Counts: UX'),
            'behavior': appfield('Counts: Behavior'),
        },
        'source_document': 'Application Documentation.PDF',
        'extracted_at': datetime.datetime.now().isoformat(timespec='seconds'),
    }

    # ---- tables index ----------------------------------------------------
    used_slugs = set()
    table_rows = []
    for t in tables:
        f = t['fields']
        name = f.get('Table name', '').strip()
        kind = classify(f)
        sl = slug(name, used_slugs)
        cols = own.get(name, [])
        table_rows.append({
            'table_name': name,
            'classification': kind,
            'bot_table_kind': bot_kind(f) if kind == 'bot' else '',
            'file': f'tables/{kind}/{sl}.csv',
            'slug': sl,
            'visible': f.get('Visible?', ''),
            'shared': f.get('Shared?', ''),
            'data_source': f.get('Data Source', ''),
            'data_locale': f.get('Data locale', ''),
            'schema': f.get('Schema', ''),
            'worksheet_qualifier': f.get('Worksheet Name/Qualifier', ''),
            'source_path': re.sub(r'\s+', ' ', f.get('Source Path', '')).strip(),
            'updates_allowed': f.get('Are updates allowed?', ''),
            'expression_for_update_mode': f.get('Expression for update mode', ''),
            'security_filter': f.get('Security filter', ''),
            'column_count': len(cols),
            'formula_column_count': sum(
                1 for c in cols
                if c['fields'].get('App formula') or c['fields'].get('Initial value')),
            'doc_page': t['page'],
        })

    write_csv(os.path.join(repo, 'tables', 'INDEX.csv'),
              list(table_rows[0].keys()), table_rows)
    write_csv(os.path.join(repo, 'tables', 'real', '_index.csv'),
              list(table_rows[0].keys()),
              [r for r in table_rows if r['classification'] == 'real'])
    write_csv(os.path.join(repo, 'tables', 'bot', '_index.csv'),
              list(table_rows[0].keys()),
              [r for r in table_rows if r['classification'] == 'bot'])

    # ---- one CSV per table ----------------------------------------------
    col_fields = ['table_name', 'classification', 'column_name', 'type', 'visible',
                  'read_only', 'hidden', 'label', 'key', 'part_of_key',
                  'system_defined', 'virtual', 'editable_initial_value',
                  'reset_on_edit', 'formula_version', 'locale_name', 'searchable',
                  'scannable', 'sensitive_data', 'app_formula', 'initial_value',
                  'description', 'type_qualifier', 'doc_page']
    for row in table_rows:
        t = next(x for x in tables if x['fields'].get('Table name', '').strip() == row['table_name'])
        rows = []
        for c in own.get(row['table_name'], []):
            f = c['fields']
            rows.append({
                'table_name': row['table_name'],
                'classification': row['classification'],
                'column_name': f.get('Column name', ''),
                'type': f.get('Type', ''),
                'visible': f.get('Visible?', ''),
                'read_only': f.get('Read-Only', ''),
                'hidden': f.get('Hidden', ''),
                'label': f.get('Label', ''),
                'key': f.get('Key', ''),
                'part_of_key': f.get('Part of Key?', ''),
                'system_defined': f.get('System Defined?', ''),
                'virtual': f.get('Virtual?', ''),
                'editable_initial_value': f.get('Editable Initial Value?', ''),
                'reset_on_edit': f.get('Reset on edit?', ''),
                'formula_version': f.get('Formula version', ''),
                'locale_name': f.get('LocaleName', ''),
                'searchable': f.get('Searchable', ''),
                'scannable': f.get('Scannable', ''),
                'sensitive_data': f.get('Sensitive data', ''),
                'app_formula': f.get('App formula', ''),
                'initial_value': f.get('Initial value', ''),
                'description': f.get('Description', ''),
                'type_qualifier': f.get('Type Qualifier', ''),
                'doc_page': c['page'],
            })
        write_csv(os.path.join(repo, row['file']), col_fields, rows)

    # ---- all columns -----------------------------------------------------
    all_cols = []
    for c in columns:
        f = c['fields']
        q = qualifier_fields(f.get('Type Qualifier', ''))
        all_cols.append({
            'table_name': col_table.get(id(c), ''),
            'column_name': f.get('Column name', ''),
            'type': f.get('Type', ''),
            'visible': f.get('Visible?', ''),
            'read_only': f.get('Read-Only', ''),
            'hidden': f.get('Hidden', ''),
            'key': f.get('Key', ''),
            'part_of_key': f.get('Part of Key?', ''),
            'system_defined': f.get('System Defined?', ''),
            'virtual': f.get('Virtual?', ''),
            'editable_initial_value': f.get('Editable Initial Value?', ''),
            'app_formula': f.get('App formula', ''),
            'initial_value': f.get('Initial value', ''),
            'description': f.get('Description', ''),
            'valid_if': q.get('Valid_If', ''),
            'required_if': q.get('Required_If', ''),
            'editable_if': q.get('Editable_If', ''),
            'show_if': q.get('Show_If', ''),
            'reset_if': q.get('Reset_If', ''),
            'error_message_if_invalid': q.get('Error_Message_If_Invalid', ''),
            'suggested_values': q.get('Suggested_Values', ''),
            'doc_page': c['page'],
        })
    write_csv(os.path.join(repo, 'columns', 'all_columns.csv'),
              list(all_cols[0].keys()), all_cols)

    type_count = collections.Counter(r['type'] for r in all_cols)
    write_csv(os.path.join(repo, 'columns', 'by_type.csv'),
              ['type', 'column_count'],
              [{'type': t, 'column_count': n} for t, n in
               sorted(type_count.items(), key=lambda kv: -kv[1])])

    # ---- formulas --------------------------------------------------------
    fname = {}
    for t in tables:
        fname[t['fields'].get('Table name', '').strip()] = t

    formulas = []
    for c in columns:
        f = c['fields']
        tbl = col_table.get(id(c), '')
        for field in ('App formula', 'Initial value'):
            val = f.get(field, '')
            if not val:
                continue
            formulas.append({
                'table_name': tbl,
                'column_name': f.get('Column name', ''),
                'field': field,
                'formula': val,
                'functions_used': '; '.join(functions_of(val)),
                'column_references': '; '.join(refs_of(val)),
                'doc_page': c['page'],
            })
    # table level expressions
    for t in tables:
        f = t['fields']
        tbl = f.get('Table name', '').strip()
        for field in ('Security filter', 'Expression for update mode'):
            val = f.get(field, '')
            if not val:
                continue
            formulas.append({
                'table_name': tbl,
                'column_name': '(table level)',
                'field': field,
                'formula': val,
                'functions_used': '; '.join(functions_of(val)),
                'column_references': '; '.join(refs_of(val)),
                'doc_page': t['page'],
            })
    write_csv(os.path.join(repo, 'formulas', 'formulas.csv'),
              list(formulas[0].keys()), formulas)

    fcount = collections.Counter()
    for r in formulas:
        for fn in functions_of(r['formula']):
            fcount[fn] += 1
    write_csv(os.path.join(repo, 'formulas', 'functions.csv'),
              ['function', 'occurrences'],
              [{'function': k, 'occurrences': v} for k, v in
               sorted(fcount.items(), key=lambda kv: (-kv[1], kv[0]))])

    colnames = {c['fields'].get('Column name', '') for c in columns}
    ref_rows = []
    for r in formulas:
        for ref in refs_of(r['formula']):
            ref_rows.append({
                'table_name': r['table_name'],
                'column_name': r['column_name'],
                'field': r['field'],
                'reference': ref,
                'resolves_to_known_column': 'yes' if ref in colnames else 'no',
            })
    write_csv(os.path.join(repo, 'formulas', 'column_references.csv'),
              list(ref_rows[0].keys()) if ref_rows else
              ['table_name', 'column_name', 'field', 'reference',
               'resolves_to_known_column'],
              ref_rows)

    # ---- views / actions / slices / format rules -------------------------
    def flat(kind, extra=None):
        rows = []
        for r in recs:
            if r['kind'] != kind:
                continue
            row = {'name': r['fields'].get(r['name'].split()[0], '') or
                   r['name'].split(' ', 1)[-1]}
            for k, v in r['fields'].items():
                row[k] = v
            row['doc_page'] = r['page']
            if extra:
                row.update(extra(r))
            rows.append(row)
        return rows

    view_rows = flat('view')
    write_csv(os.path.join(repo, 'views', 'views.csv'),
              sorted({k for r in view_rows for k in r}), view_rows)

    action_rows = flat('action')
    write_csv(os.path.join(repo, 'actions', 'actions.csv'),
              sorted({k for r in action_rows for k in r}), action_rows)

    slice_rows = flat('slice')
    write_csv(os.path.join(repo, 'slices', 'slices.csv'),
              sorted({k for r in slice_rows for k in r}), slice_rows)

    rule_rows = flat('format_rule')
    write_csv(os.path.join(repo, 'format_rules', 'format_rules.csv'),
              sorted({k for r in rule_rows for k in r}), rule_rows)

    # ---- schema json -----------------------------------------------------
    schema = {
        'app': app_meta,
        'tables': [],
    }
    for row in table_rows:
        t = next(x for x in tables
                 if x['fields'].get('Table name', '').strip() == row['table_name'])
        schema['tables'].append({
            'name': row['table_name'],
            'classification': row['classification'],
            'bot_table_kind': row['bot_table_kind'],
            'properties': {k: v for k, v in t['fields'].items()},
            'columns': [{
                'name': c['fields'].get('Column name', ''),
                'type': c['fields'].get('Type', ''),
                'properties': {k: v for k, v in c['fields'].items()
                               if k != 'Type Qualifier'},
                'type_qualifier': qualifier_fields(c['fields'].get('Type Qualifier', '')),
            } for c in own.get(row['table_name'], [])],
        })
    schema['slices'] = [{'name': s['fields'].get('Slice Name', ''),
                         'properties': s['fields']} for s in slices]
    schema['views'] = [{'name': v['fields'].get('View name', ''),
                        'properties': v['fields']} for v in views]
    schema['format_rules'] = [{'name': r['fields'].get('Rule name', ''),
                               'properties': r['fields']} for r in rules]
    schema['actions'] = [{'name': a['fields'].get('Action name', ''),
                          'properties': a['fields']} for a in actions]

    os.makedirs(os.path.join(repo, 'schema'), exist_ok=True)
    with open(os.path.join(repo, 'schema', 'app_schema.json'), 'w',
              encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    os.makedirs(os.path.join(repo, 'app'), exist_ok=True)
    with open(os.path.join(repo, 'app', 'app.json'), 'w', encoding='utf-8') as f:
        json.dump(app_meta, f, ensure_ascii=False, indent=2)

    # ---- manifest --------------------------------------------------------
    manifest = {
        'generated_at': app_meta['extracted_at'],
        'source': 'Application Documentation.PDF',
        'app': app_meta,
        'counts': {
            'tables_total': len(tables),
            'tables_real': sum(1 for r in table_rows if r['classification'] == 'real'),
            'tables_bot': sum(1 for r in table_rows if r['classification'] == 'bot'),
            'columns': sum(len(v) for v in own.values()),
            'column_records_in_document': len(columns),
            'slices': len(slices),
            'views': len(views),
            'format_rules': len(rules),
            'actions': len(actions),
            'formulas': len(formulas),
        },
        'layout': [
            'README.md', 'MANIFEST.json',
            'app/app.json',
            'tables/INDEX.csv', 'tables/real/', 'tables/bot/',
            'columns/all_columns.csv', 'columns/by_type.csv',
            'formulas/formulas.csv', 'formulas/functions.csv',
            'formulas/column_references.csv',
            'views/views.csv', 'actions/actions.csv', 'slices/slices.csv',
            'format_rules/format_rules.csv',
            'schema/app_schema.json',
            'docs/', 'tools/',
        ],
    }
    with open(os.path.join(repo, 'MANIFEST.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest, table_rows, all_cols, formulas


if __name__ == '__main__':
    recs_path = sys.argv[1]
    repo = sys.argv[2]
    m, table_rows, all_cols, formulas = build(recs_path, repo)
    print(json.dumps(m['counts'], indent=2))
    print('repo:', repo)
