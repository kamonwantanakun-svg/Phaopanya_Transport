# -*- coding: utf-8 -*-
"""Build the multi-sheet Excel summary workbook from the parsed AppSheet export.

Reads the CSV/JSON artefacts produced by ``build_repo.py`` and writes a single
``.xlsx`` workbook that a human can open, read and filter.

Usage:  python3 tools/build_workbook.py [repo-dir] [out-xlsx]

The script is idempotent: every run overwrites the output workbook from
scratch, so it can be re-run whenever the source export changes.

Design rules
------------
* No source file is modified.  Everything is read-only here.
* No data is truncated.  Long formula / JSON payloads are kept verbatim in
  their own column; only ``\\n`` inside a cell is turned into a visible
  marker so that a row stays a single readable line in Excel.
* Every sheet that holds a table gets: a styled header row, frozen panes,
  an auto-filter and column widths sized to the content.
* Columns are never named ``Column1`` / ``Field3`` ... - headers are real,
  human readable Thai/English labels.
"""
import csv, os, re, sys, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    sys.exit("openpyxl is required:  pip install openpyxl")


# --------------------------------------------------------------- constants ---
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=16, color="1F3864")
SECTION_FONT = Font(bold=True, size=12, color="1F3864")
LABEL_FONT = Font(bold=True, size=10)
BODY_FONT = Font(size=10)
THIN = Side(style="thin", color="D0D7E5")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

TAB_REAL = "2E7D32"     # green  - real tables
TAB_BOT = "E65100"      # orange - bot tables
TAB_DATA = "1565C0"     # blue   - column / formula data
TAB_UX = "6A1B9A"       # purple - views / actions / slices / rules
TAB_INFO = "37474F"     # grey   - index / readme

CLASS_LABEL = {
    "real": "ตารางจริง (ผูกกับ Google Sheet)",
    "bot": "ตารางบอท (AppSheet สร้างเอง)",
    "": "ไม่ระบุ",
}

BOT_KIND_LABEL = {
    "process-state": "สถานะกระบวนการบอท (Bot process state)",
    "process-output": "ผลลัพธ์ขั้นตอน (Bot step output)",
    "per-user-settings": "ตั้งค่าเฉพาะผู้ใช้ (Per-user settings)",
    "": "",
}

BOT_KIND_NOTE = {
    "process-state": "ตารางสถานะภายในของบอท AppSheet - เก็บ state ของแต่ละ process ไม่ได้ผูกกับชีตของผู้ใช้",
    "process-output": "ตารางผลลัพธ์ที่แต่ละ step ของบอทเขียนกลับมา (step output) - สร้างและลบโดย AppSheet เอง",
    "per-user-settings": "ตารางตั้งค่าส่วนตัวของผู้ใช้แต่ละคน - สร้างและจัดการโดย AppSheet เอง",
}

CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
MAX_CELL = 32767


# ----------------------------------------------------------------- helpers ---
def read_csv_rows(path):
    """Read a CSV into a list of dicts (utf-8-sig tolerant)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def clean_text(value, max_len=MAX_CELL):
    """Normalise a cell value for display without losing information."""
    if value is None:
        return ""
    s = str(value)
    s = CTRL_RE.sub("", s)
    if "\n" in s or "\r" in s:
        s = s.replace("\r\n", "\n").replace("\r", "\n")
        # keep the payload but let the cell stay on one readable line
        s = s.replace("\n", " ⏎ ")
    if len(s) > max_len:
        s = s[:max_len - 20] + " ...(ตัดที่ 32767 อักขระ)"
    return s


def raw(value):
    """Return a source value verbatim - an empty source stays an empty cell."""
    return "" if value is None else str(value)


def to_int(value, default=None):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def disp_len(s):
    """Approximate Excel column width (Thai glyphs are counted double)."""
    n = 0
    for ch in s:
        n += 2 if 0x0E00 <= ord(ch) <= 0x0E7F else 1
    return n


def set_cell(ws, row, col, value, font=None, number_format=None):
    """Write a value and force it to be stored as text (never a live formula)."""
    c = ws.cell(row=row, column=col)
    if isinstance(value, bool):
        c.value = value
    elif isinstance(value, int):
        c.value = value
    elif isinstance(value, float):
        c.value = value
    else:
        c.value = clean_text(value)
        c.data_type = "s"
    if font is not None:
        c.font = font
    if number_format:
        c.number_format = number_format
    return c


def write_table_sheet(wb, title, headers, rows, widths=None, freeze="A2",
                      tab_color=TAB_DATA):
    """Create a styled, filterable sheet from a list of row-lists.

    ``headers``  list of (key, label) or plain label strings
    ``rows``     list of row-lists (already in display order)
    ``widths``   optional {header_index: max_width} cap overrides
    """
    ws = wb.create_sheet(title=title)
    ws.sheet_properties.tabColor = tab_color

    labels = [h[1] if isinstance(h, (tuple, list)) else h for h in headers]
    keys = [h[0] if isinstance(h, (tuple, list)) else h for h in headers]

    for i, label in enumerate(labels, start=1):
        c = set_cell(ws, 1, i, label, font=HEADER_FONT)
        c.fill = HEADER_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
    ws.row_dimensions[1].height = 30

    for r, row in enumerate(rows, start=2):
        for i, value in enumerate(row, start=1):
            c = set_cell(ws, r, i, value, font=BODY_FONT)
            c.alignment = Alignment(vertical="top", horizontal="left")

    last_col = len(labels)
    last_row = max(1, len(rows) + 1)
    ws.auto_filter.ref = f"A1:{get_column_letter(last_col)}{last_row}"
    ws.freeze_panes = freeze

    # ---- column widths, sized from the data
    # p90 drives the normal width; a rare-but-long value still gets a column
    # wide enough to read (up to the per-column cap).  Nothing is truncated.
    caps = widths or {}
    for i in range(1, last_col + 1):
        lengths = [disp_len(labels[i - 1])]
        for row in rows:
            v = row[i - 1] if i - 1 < len(row) else ""
            lengths.append(disp_len(str(v)))
        longest = max(lengths)
        lengths.sort()
        p90 = lengths[int(len(lengths) * 0.9)] if lengths else 10
        cap = caps.get(i - 1, 46)
        target = max(p90, min(longest, cap))
        width = min(max(target + 2, 10), cap)
        ws.column_dimensions[get_column_letter(i)].width = width

    return ws


def list_cell(items, with_type=False, limit=None):
    """Render a list of names (optionally with types) into one cell."""
    if not items:
        return "(ไม่มี)"
    parts = []
    for i, it in enumerate(items, start=1):
        if with_type and isinstance(it, (tuple, list)):
            parts.append(f"{i}. {it[0]} ({it[1]})")
        else:
            parts.append(f"{i}. {it}")
    return " | ".join(parts)


# -------------------------------------------------------------- data access ---
def load_source(repo):
    src = {
        "tables": read_csv_rows(os.path.join(repo, "tables", "INDEX.csv")),
        "real": read_csv_rows(os.path.join(repo, "tables", "real", "_index.csv")),
        "bot": read_csv_rows(os.path.join(repo, "tables", "bot", "_index.csv")),
        "all_columns": read_csv_rows(os.path.join(repo, "columns", "all_columns.csv")),
        "by_type": read_csv_rows(os.path.join(repo, "columns", "by_type.csv")),
        "formulas": read_csv_rows(os.path.join(repo, "formulas", "formulas.csv")),
        "functions": read_csv_rows(os.path.join(repo, "formulas", "functions.csv")),
        "column_references": read_csv_rows(os.path.join(repo, "formulas", "column_references.csv")),
        "views": read_csv_rows(os.path.join(repo, "views", "views.csv")),
        "actions": read_csv_rows(os.path.join(repo, "actions", "actions.csv")),
        "slices": read_csv_rows(os.path.join(repo, "slices", "slices.csv")),
        "format_rules": read_csv_rows(os.path.join(repo, "format_rules", "format_rules.csv")),
    }
    with open(os.path.join(repo, "schema", "app_schema.json"), encoding="utf-8") as f:
        src["schema"] = json.load(f)
    with open(os.path.join(repo, "MANIFEST.json"), encoding="utf-8") as f:
        src["manifest"] = json.load(f)

    # per-table column files (richer than all_columns.csv: label/searchable/...)
    col_rows = {}
    for t in src["tables"]:
        path = os.path.join(repo, t["file"])
        if os.path.exists(path):
            col_rows[t["table_name"]] = read_csv_rows(path)
    src["table_columns"] = col_rows
    return src


def split_type(raw):
    """Split a raw type cell into (type name, remaining qualifier).

    The PDF glues the type qualifier JSON onto the type, sometimes on the same
    line (``Text {"MaxLength":...}``) and sometimes on the next one
    (``Text\\n{"MaxLength":...}``).  Type names never contain a space, so the
    last whitespace token before the JSON is the type; anything left over is
    kept in front of the qualifier so that no text is lost.
    """
    raw = raw or ""
    cut = len(raw)
    for ch in ("{", "\n"):
        i = raw.find(ch)
        if i >= 0:
            cut = min(cut, i)
    head = raw[:cut].strip()
    tail = raw[cut:].strip()
    tokens = head.split()
    type_name = tokens[-1] if tokens else ""
    extra = " ".join(tokens[:-1])
    qualifier = (f"{extra} {tail}").strip() if extra else tail
    return type_name, qualifier


def split_type_with_qualifier(raw_type, raw_qualifier):
    """Same as :func:`split_type` but re-joins a qualifier that the PDF cut in
    half across two source columns (``type`` + ``type_qualifier``)."""
    type_name, qualifier = split_type(raw_type)
    return type_name, (qualifier + (raw_qualifier or "")).strip()


def formula_columns_of(col_rows):
    """Names of columns that carry an app formula."""
    return [c["column_name"] for c in col_rows if (c.get("app_formula") or "").strip()]


# --------------------------------------------------------------- sheet: readme ---
def build_readme(wb, src, sheet_rows):
    ws = wb.create_sheet(title="README")
    ws.sheet_properties.tabColor = "0D47A1"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 86
    ws.column_dimensions["C"].width = 46

    app = src["schema"]["app"]
    counts = src["manifest"]["counts"]
    kind_count = collections.Counter(t["bot_table_kind"] for t in src["tables"]
                                     if t["classification"] == "bot")
    field_count = collections.Counter(f["field"] for f in src["formulas"])

    r = 1
    set_cell(ws, r, 1, "สรุปโครงสร้างแอป AppSheet", font=TITLE_FONT)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    r += 1
    set_cell(ws, r, 1, f"{app['app_name']}  •  เวอร์ชัน {app['version']}  •  "
                        f"แหล่งข้อมูล: {src['manifest']['app']['source_document']}  •  "
                        f"สกัดเมื่อ {app['extracted_at']}", font=LABEL_FONT)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    r += 2

    def section(title):
        nonlocal r
        set_cell(ws, r, 1, title, font=SECTION_FONT)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        for col in range(1, 4):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="E8EEF7")
        r += 1

    def kv(label, value):
        nonlocal r
        set_cell(ws, r, 1, label, font=LABEL_FONT)
        c = set_cell(ws, r, 2, value, font=BODY_FONT)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        r += 1

    section("1) ภาพรวมตัวเลขทั้งหมด")
    kv("ตารางทั้งหมด", f"{counts['tables_total']} ตาราง "
                        f"(ตารางจริง {counts['tables_real']} + ตารางบอท {counts['tables_bot']})")
    kv("คอลัมน์ทั้งหมด", f"{counts['columns']} คอลัมน์ (แมปกับตารางได้ครบ 1:1 ไม่มีคอลัมน์หลุดหรือซ้ำ)")
    kv("สูตร / นิพจน์", f"{counts['formulas']} รายการ = "
                        f"App formula {field_count.get('App formula', 0)} + "
                        f"Initial value {field_count.get('Initial value', 0)} + "
                        f"Expression for update mode {field_count.get('Expression for update mode', 0)} + "
                        f"Security filter {field_count.get('Security filter', 0)}")
    kv("ฟังก์ชันที่ถูกเรียกใช้", f"{len(src['functions'])} ฟังก์ชัน (นับจากไฟล์ formulas/functions.csv)")
    kv("วิว (View)", f"{counts['views']} วิว")
    kv("แอกชัน (Action)", f"{counts['actions']} แอกชัน")
    kv("สไลซ์ (Slice)", f"{counts['slices']} สไลซ์")
    kv("กฎการจัดรูปแบบ (Format rule)", f"{counts['format_rules']} กฎ")
    kv("ชนิดตารางบอท", f"process-state {kind_count.get('process-state', 0)} • "
                       f"process-output {kind_count.get('process-output', 0)} • "
                       f"per-user-settings {kind_count.get('per-user-settings', 0)}")
    r += 1

    section("2) ตารางจริง (29) vs ตารางบอท (61) — อ่านข้อนี้ก่อนใช้งาน")
    hdr = ["หัวข้อ", "ตารางจริง (29 ตาราง, ผูกกับ Google Sheet)",
           "ตารางบอท (61 ตาราง, สร้างโดย AppSheet เอง — bot process state / step output)"]
    for i, h in enumerate(hdr, start=1):
        c = set_cell(ws, r, i, h, font=HEADER_FONT)
        c.fill = Pattern_FILL = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
    ws.row_dimensions[r].height = 32
    r += 1
    diff_rows = [
        ("ที่มา",
         "ผูกกับชีตจริงใน Google Sheets / Drive ขององค์กร (data source = google) — ข้อมูลถูกอ่าน-เขียนจริง",
         "ไม่มีชีตจริง (data source = native) — เป็นตารางภายในระบบของ AppSheet"),
        ("ใครสร้าง",
         "ทีมงานสร้างตารางและคอลัมน์เอง เพื่อเก็บข้อมูลธุรกิจ",
         "AppSheet สร้างเองอัตโนมัติเมื่อมีการตั้งค่า bot / workflow"),
        ("ชนิดตารางบอท",
         "ไม่มี",
         f"process-state {kind_count.get('process-state', 0)} ตาราง (สถานะกระบวนการ) • "
         f"process-output {kind_count.get('process-output', 0)} ตาราง (ผลลัพธ์ step) • "
         f"per-user-settings {kind_count.get('per-user-settings', 0)} ตาราง (ตั้งค่าเฉพาะผู้ใช้)"),
        ("ข้อมูลในนั้น",
         "ข้อมูลงานจริง: วางบิล, ราคา, พนักงาน, งานประจำวัน ฯลฯ "
         f"({sum(len(src['table_columns'].get(t['table_name'], [])) for t in src['real'])} คอลัมน์)",
         "สถานะและผลลัพธ์ของบอท: เช่น ปริ๊นใบวางบิล, สรุปยอดส่งของ, แจ้งปัญหาผ่าน Telegram "
         f"({sum(len(src['table_columns'].get(t['table_name'], [])) for t in src['bot'])} คอลัมน์)"),
        ("ใครเห็นได้",
         "Visible? = ALWAYS และ Shared? = Yes (ผู้ใช้ทุกคนเห็นได้)",
         "Visible? = NEVER, Shared? = Yes (ซ่อนจากเมนู แต่ process ภายในยังเรียกใช้ได้)"),
        ("ชีตในไฟล์นี้",
         f"Real_Tables ({len(src['real'])} แถว) และ Real_Table_Columns "
         f"({sum(len(src['table_columns'].get(t['table_name'], [])) for t in src['real'])} แถว)",
         f"Bot_Tables ({len(src['bot'])} แถว) และ Bot_Table_Columns "
         f"({sum(len(src['table_columns'].get(t['table_name'], [])) for t in src['bot'])} แถว)"),
    ]
    for label, real_txt, bot_txt in diff_rows:
        set_cell(ws, r, 1, label, font=LABEL_FONT)
        for i, txt in ((2, real_txt), (3, bot_txt)):
            c = set_cell(ws, r, i, txt, font=BODY_FONT)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = BOX
        ws.cell(row=r, column=1).border = BOX
        ws.row_dimensions[r].height = 44
        r += 1
    r += 1

    section("3) ผังชีตทั้งหมดในไฟล์นี้")
    guide_head = ["ชีต", "จำนวนแถวข้อมูล", "อธิบายว่าเก็บอะไร"]
    for i, h in enumerate(guide_head, start=1):
        c = set_cell(ws, r, i, h, font=HEADER_FONT)
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
    r += 1
    for name, n, desc in sheet_rows:
        set_cell(ws, r, 1, name, font=LABEL_FONT)
        c = set_cell(ws, r, 2, n, font=BODY_FONT)
        c.alignment = Alignment(horizontal="center")
        c = set_cell(ws, r, 3, desc, font=BODY_FONT)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        for col in range(1, 4):
            ws.cell(row=r, column=col).border = BOX
        r += 1
    r += 1

    section("4) วิธีใช้งาน / อ่านยังไง")
    for txt in [
        "• ทุกชีตที่เป็นตารางมีหัวตารางบรรทัดแรก (freeze pane ไว้) + แถบ AutoFilter — "
        "คลิกลูกศร ∇ ที่หัวคอลัมน์เพื่อกรอง/ค้นหาได้ทันที",
        "• คอลัมน์ที่เนื้อหายาว (สูตร, JSON) ถูกแยกไว้ในคอลัมน์ของตัวเอง ความกว้างถูกจำกัดไว้เพื่อให้อ่านสบาย — "
        "ข้อมูลไม่ถูกตัดออก ให้คลิกที่เซลล์แล้วดูในแถบสูตร หรือขยายคอลัมน์เอง",
        "• บรรทัดใหม่ (\"⏎\") ที่โผล่ในเนื้อหาคือจุดที่เอกสาร PDF ต้นทางมีการตัดบรรทัด — แทนที่ด้วยสัญลักษณ์ ⏎ "
        "เพื่อให้แต่ละแถวอ่านได้ในบรรทัดเดียว (เนื้อหาไม่หาย)",
        "• คอลัมน์ “หน้าเอกสาร” คือเลขหน้าใน “Application Documentation.PDF” ต้นทาง "
        "— ใช้เปิดกลับไปดูรายละเอียดเชิงต้นฉบับ",
        "• คอลัมน์ “การจำแนก” ใช้คัดกรองตารางจริง (real) กับตารางบอท (bot) ได้ทุกชีต",
    ]:
        c = set_cell(ws, r, 1, txt, font=BODY_FONT)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1

    section("5) หมายเหตุ / ข้อจำกัดของข้อมูล")
    for txt in [
        "• all_columns.csv มี 2,304 แถว ครบ 90 ตาราง และแมปกับไฟล์คอลัมน์รายตารางได้ 1:1 พอดี "
        "(ชื่อตาราง+ชื่อคอลัมน์ไม่ซ้ำ ไม่หลุด ไม่มีแถวไร้ชื่อตาราง)",
        "• คอลัมน์ “ประเภท” ใน all_columns.csv ถูก PDF ตัดรวม JSON คุณสมบัติไว้ในช่องเดียว "
        "— แยกเป็น “ประเภท” (Text/Image/Ref/…) และ “รายละเอียดประเภท (JSON)” แล้ว ข้อมูลไม่หาย "
        "(ชีต Real_Table_Columns / Bot_Table_Columns ตัด JSON ข้าม 2 ฟิลด์ให้รวมกลับครบชิ้นด้วย)",
        f"• จำนวนสูตร {counts['formulas']} รายการ ตรงกันทั้ง 3 ทาง: formulas.csv, ไฟล์คอลัมน์รายตาราง "
        "และ schema/app_schema.json (App formula 190 • Initial value 126 • "
        "Expression for update mode 22 • Security filter 7)",
        "• ชนิดตารางบอทจัดจากโครงสร้างจริง: ชื่อลงท้าย “Process Table” = process-state, "
        "ชื่อลงท้าย “Output” = process-output, “_Per User Settings” = per-user-settings",
        "• วิวใน views.csv ไม่มีคอลัมน์ชื่อตารางเจ้าของ (เอกสาร PDF ไม่ได้พิมพ์มา) — จึงไม่ได้เดาชื่อตารางใส่ให้ "
        "(ซึ่งอาจทำให้เข้าใจผิดว่าวิวนี้มีที่มา) แต่คงข้อมูลวิวตามต้นฉบับครบทุกช่อง",
        "• ตารางบอทมีจำนวนคอลัมน์จริงแล้ว (เช่น Process for ปริ๊นใบวางบิล 12 คอลัมน์) "
        "เพราะข้อมูลถูกแมปกลับเข้ากับตารางที่ถูกต้องแล้ว",
    ]:
        c = set_cell(ws, r, 1, txt, font=BODY_FONT)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws.row_dimensions[r].height = 30
        r += 1

    ws.freeze_panes = "A4"
    return ws


# ------------------------------------------------------------------ main ---
def main(argv):
    repo = argv[1] if len(argv) > 1 else REPO
    out = argv[2] if len(argv) > 2 else os.path.join(repo, "appsheet-export.xlsx")

    src = load_source(repo)
    tables = src["tables"]
    table_cols = src["table_columns"]
    tbl_by_name = {t["table_name"]: t for t in tables}

    wb = Workbook()
    wb.remove(wb.active)

    # ---------------------------------------------------------------- index
    index_rows = []
    for i, t in enumerate(tables, start=1):
        cols = table_cols.get(t["table_name"], [])
        n_app = sum(1 for c in cols if (c.get("app_formula") or "").strip())
        n_init = sum(1 for c in cols if (c.get("initial_value") or "").strip())
        index_rows.append([
            i,
            t["table_name"],
            raw(t["classification"]),
            CLASS_LABEL.get(t["classification"], t["classification"]),
            raw(t["bot_table_kind"]),
            BOT_KIND_LABEL.get(t["bot_table_kind"], ""),
            to_int(t["column_count"], 0),
            len(cols),
            to_int(t["formula_column_count"], 0),
            n_app,
            n_init,
            1 if (t["expression_for_update_mode"] or "").strip() else 0,
            1 if (t["security_filter"] or "").strip() else 0,
            t["data_source"],
            raw(t["source_path"]),
            raw(t["worksheet_qualifier"]),
            raw(t["data_locale"]),
            raw(t["schema"]),
            raw(t["visible"]),
            raw(t["shared"]),
            raw(t["updates_allowed"]),
            raw(t["expression_for_update_mode"]),
            raw(t["security_filter"]),
            t["file"],
            t["slug"],
            to_int(t["doc_page"], ""),
        ])
    index_headers = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก",
        "ประเภทตารางบอท (bot_table_kind)", "คำอธิบายประเภทตารางบอท",
        "จำนวนคอลัมน์ (ตามเอกสาร)", "จำนวนคอลัมน์ (นับจริง)",
        "จำนวนคอลัมน์ที่มีสูตร/ค่าเริ่มต้น",
        "จำนวน App formula", "จำนวน Initial value",
        "มีนิพจน์โหมดอัปเดต", "มีฟิลเตอร์ความปลอดภัย",
        "แหล่งข้อมูล", "โฟลเดอร์/พาธของข้อมูล", "ชื่อชีต (Worksheet)",
        "ภาษาข้อมูล", "สคีมา", "การแสดงผล", "แชร์ร่วม", "โหมดอัปเดต",
        "นิพจน์โหมดอัปเดต", "ฟิลเตอร์ความปลอดภัย", "ไฟล์ต้นทาง", "slug", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Tables_Index", index_headers, index_rows,
        widths={1: 46, 2: 32, 3: 34, 5: 34, 6: 46, 9: 46, 13: 60, 22: 40, 23: 52, 24: 46, 25: 46},
        freeze="C2", tab_color=TAB_INFO,
    )

    # ------------------------------------------------- real / bot table list
    def table_detail_rows(subset, is_bot):
        rows = []
        for i, t in enumerate(subset, start=1):
            cols = table_cols.get(t["table_name"], [])
            names = [(c["column_name"], split_type_with_qualifier(c.get("type"), "")[0]) for c in cols]
            fcols = formula_columns_of(cols)
            icols = [c["column_name"] for c in cols if (c.get("initial_value") or "").strip()]
            head = [
                i,
                t["table_name"],
                raw(t["classification"]),
                CLASS_LABEL.get(t["classification"], t["classification"]),
            ]
            if is_bot:
                head += [
                    raw(t["bot_table_kind"]),
                    BOT_KIND_LABEL.get(t["bot_table_kind"], ""),
                    raw(BOT_KIND_NOTE.get(t["bot_table_kind"], "")),
                ]
            row = head + [
                t["data_source"],
                to_int(t["column_count"], 0),
                len(cols),
                len(fcols),
                len(icols),
                list_cell(names, with_type=True),
                list_cell(fcols),
                list_cell(icols),
                raw(t["source_path"]),
                raw(t["worksheet_qualifier"]),
                raw(t["data_locale"]),
                raw(t["visible"]),
                raw(t["shared"]),
                raw(t["updates_allowed"]),
                raw(t["security_filter"]),
                t["file"],
                to_int(t["doc_page"], ""),
            ]
            rows.append(row)
        return rows

    real_head = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก", "แหล่งข้อมูล",
        "จำนวนคอลัมน์ (ตามเอกสาร)", "จำนวนคอลัมน์ (นับจริง)",
        "จำนวน App formula", "จำนวน Initial value",
        "รายการคอลัมน์ทั้งหมด (ชื่อ + ประเภท)", "คอลัมน์ที่มีสูตร (App formula)",
        "คอลัมน์ที่มีค่าเริ่มต้น (Initial value)",
        "โฟลเดอร์/พาธของข้อมูล", "ชื่อชีต (Worksheet)", "ภาษาข้อมูล",
        "การแสดงผล", "แชร์ร่วม", "โหมดอัปเดต", "ฟิลเตอร์ความปลอดภัย",
        "ไฟล์ต้นทาง", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Real_Tables", real_head, table_detail_rows(src["real"], False),
        widths={1: 46, 3: 34, 9: 60, 10: 50, 11: 50, 12: 52, 18: 52, 19: 48},
        freeze="C2", tab_color=TAB_REAL,
    )
    bot_head = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก",
        "ประเภทตารางบอท (bot_table_kind)", "คำอธิบายประเภทตารางบอท",
        "หมายเหตุชนิดตารางบอท", "แหล่งข้อมูล",
        "จำนวนคอลัมน์ (ตามเอกสาร)", "จำนวนคอลัมน์ (นับจริง)",
        "จำนวน App formula", "จำนวน Initial value",
        "รายการคอลัมน์ทั้งหมด (ชื่อ + ประเภท)", "คอลัมน์ที่มีสูตร (App formula)",
        "คอลัมน์ที่มีค่าเริ่มต้น (Initial value)",
        "โฟลเดอร์/พาธของข้อมูล", "ชื่อชีต (Worksheet)", "ภาษาข้อมูล",
        "การแสดงผล", "แชร์ร่วม", "โหมดอัปเดต", "ฟิลเตอร์ความปลอดภัย",
        "ไฟล์ต้นทาง", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Bot_Tables", bot_head, table_detail_rows(src["bot"], True),
        widths={1: 46, 3: 34, 5: 34, 6: 60, 12: 60, 13: 50, 14: 50, 15: 52, 21: 52, 22: 48},
        freeze="C2", tab_color=TAB_BOT,
    )

    # -------------------------------------------------- per-table column list
    col_headers = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก",
        "ชื่อคอลัมน์", "ประเภท",
        "มีป้ายกำกับเฉพาะ (Label)", "คีย์", "ส่วนหนึ่งของคีย์", "กำหนดโดยระบบ",
        "เสมือน (Virtual)", "การแสดงผล", "อ่านอย่างเดียว", "ซ่อน", "ค้นหาได้",
        "สแกนได้", "ข้อมูลอ่อนไหว", "ภาษา", "สูตร (App formula)",
        "ค่าเริ่มต้น (Initial value)", "คำอธิบาย", "ตั้งค่าค่าเริ่มต้นได้",
        "รายละเอียดประเภท (JSON)", "หน้าเอกสาร",
    ]

    def column_rows(table_list):
        rows = []
        n = 0
        for t in table_list:
            for c in table_cols.get(t["table_name"], []):
                n += 1
                ctype, cqual = split_type_with_qualifier(c.get("type"), c.get("type_qualifier"))
                rows.append([
                    n,
                    t["table_name"],
                    raw(t["classification"]),
                    CLASS_LABEL.get(t["classification"], t["classification"]),
                    c["column_name"],
                    ctype,
                    c.get("label", ""),
                    c.get("key", ""),
                    c.get("part_of_key", ""),
                    c.get("system_defined", ""),
                    c.get("virtual", ""),
                    c.get("visible", ""),
                    c.get("read_only", ""),
                    c.get("hidden", ""),
                    c.get("searchable", ""),
                    c.get("scannable", ""),
                    c.get("sensitive_data", ""),
                    c.get("locale_name", ""),
                    c.get("app_formula", ""),
                    c.get("initial_value", ""),
                    c.get("description", ""),
                    c.get("editable_initial_value", ""),
                    cqual,
                    to_int(c.get("doc_page"), ""),
                ])
        return rows

    write_table_sheet(
        wb, "Real_Table_Columns", col_headers, column_rows(src["real"]),
        widths={1: 46, 3: 34, 4: 32, 18: 50, 19: 40, 20: 60, 22: 58},
        freeze="D2", tab_color=TAB_REAL,
    )
    write_table_sheet(
        wb, "Bot_Table_Columns", col_headers, column_rows(src["bot"]),
        widths={1: 46, 3: 34, 4: 32, 18: 50, 19: 40, 20: 60, 22: 58},
        freeze="D2", tab_color=TAB_BOT,
    )

    # ------------------------------------------------------------ all columns
    all_rows = []
    for i, c in enumerate(src["all_columns"], start=1):
        tname = c["table_name"]
        t = tbl_by_name.get(tname)
        clean_type, qualifier = split_type(c["type"])
        if t is not None:
            klass = CLASS_LABEL.get(t["classification"], t["classification"])
            klass_raw = raw(t["classification"])
        else:
            klass = CLASS_LABEL[""]
            klass_raw = ""
        # every row now carries a table name; keep the guard so a future
        # extraction gap is explicit instead of an invisible empty cell
        tname_out = tname if tname.strip() else "(ไม่ระบุชื่อตาราง)"
        all_rows.append([
            i,
            tname_out,
            klass_raw,
            klass,
            c["column_name"],
            clean_type,
            qualifier,
            c["visible"], c["read_only"], c["hidden"], c["key"],
            c["part_of_key"], c["system_defined"], c["virtual"],
            c["editable_initial_value"], c["app_formula"], c["initial_value"],
            c["description"], c["valid_if"], c["required_if"], c["editable_if"],
            c["show_if"], c["reset_if"], c["error_message_if_invalid"],
            c["suggested_values"], to_int(c["doc_page"], ""),
        ])
    all_headers = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก",
        "ชื่อคอลัมน์", "ประเภท",
        "รายละเอียดประเภท (JSON)", "การแสดงผล", "อ่านอย่างเดียว", "ซ่อน",
        "คีย์", "ส่วนหนึ่งของคีย์", "กำหนดโดยระบบ", "เสมือน (Virtual)",
        "ตั้งค่าค่าเริ่มต้นได้", "สูตร (App formula)", "ค่าเริ่มต้น (Initial value)",
        "คำอธิบาย", "เงื่อนไข Valid if", "เงื่อนไข Required if",
        "เงื่อนไข Editable if", "เงื่อนไข Show if", "เงื่อนไข Reset if",
        "ข้อความแจ้งข้อผิดพลาด", "ค่าที่แนะนำ", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "All_Columns", all_headers, all_rows,
        widths={1: 46, 3: 32, 4: 34, 6: 58, 15: 52, 16: 42, 17: 60,
                18: 40, 19: 44, 20: 44, 21: 44, 22: 44, 23: 44, 24: 40},
        freeze="E2", tab_color=TAB_DATA,
    )

    # ---------------------------------------------------------------- formulas
    f_rows = []
    for i, f in enumerate(src["formulas"], start=1):
        t = tbl_by_name.get(f["table_name"])
        klass = CLASS_LABEL.get(t["classification"], "") if t else CLASS_LABEL[""]
        klass_raw = raw(t["classification"]) if t else ""
        f_rows.append([
            i,
            f["table_name"],
            klass_raw,
            klass,
            f["column_name"],
            f["field"],
            f["formula"],
            f["functions_used"],
            f["column_references"],
            to_int(f["doc_page"], ""),
        ])
    f_headers = [
        "#", "ชื่อตาราง", "การจำแนก (classification)", "คำอธิบายการจำแนก",
        "ชื่อคอลัมน์", "ชนิดของสูตร",
        "สูตร / นิพจน์", "ฟังก์ชันที่ใช้", "คอลัมน์ที่อ้างถึง", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Formulas", f_headers, f_rows,
        widths={1: 46, 3: 32, 4: 30, 6: 62, 7: 46, 8: 52},
        freeze="D2", tab_color=TAB_DATA,
    )

    fn_rows = []
    for i, f in enumerate(src["functions"], start=1):
        fn_rows.append([i, f["function"], to_int(f["occurrences"], 0)])
    write_table_sheet(
        wb, "Functions", ["#", "ฟังก์ชัน", "จำนวนครั้งที่ถูกเรียกใช้"], fn_rows,
        widths={1: 26}, freeze="A2", tab_color=TAB_DATA,
    )

    # ------------------------------------------------------------ column types
    type_counter = collections.Counter()
    for c in src["all_columns"]:
        type_counter[split_type(c["type"])[0]] += 1
    raw_counter = collections.Counter()
    for r in src["by_type"]:
        raw_counter[split_type(r["type"])[0]] += to_int(r["column_count"], 0)
    t_rows = []
    for i, (tname, n) in enumerate(type_counter.most_common(), start=1):
        t_rows.append([i, tname, n, raw_counter.get(tname, 0)])
    write_table_sheet(
        wb, "Column_Types",
        ["#", "ประเภทคอลัมน์", "จำนวนคอลัมน์ (นับจาก all_columns)",
         "จำนวนคอลัมน์ (ตาม by_type.csv)"],
        t_rows, widths={1: 26}, freeze="A2", tab_color=TAB_DATA,
    )

    # ------------------------------------------------------------------ views
    v_rows = []
    for i, v in enumerate(src["views"], start=1):
        raw_pos = v.get("Position") or ""
        position = raw_pos.split("\n", 1)[0].strip()
        # the PDF sometimes breaks the view-config JSON across two fields:
        # whatever follows the position word belongs to the configuration.
        config_parts = []
        if "\n" in raw_pos:
            config_parts.append(raw_pos.split("\n", 1)[1])
        if (v.get("View configuration") or "").strip():
            config_parts.append(v.get("View configuration"))
        config = "\n".join(config_parts)
        v_rows.append([
            i,
            v.get("View name") or "(ไม่ระบุชื่อ)",
            raw(v.get("View type")),
            raw(v.get("Created by")),
            raw(position),
            to_int(v.get("Menu order"), ""),
            raw(v.get("Icon")),
            raw(v.get("Visible?")),
            raw(v.get("Show if")),
            raw(v.get("ActionType")),
            config,
            to_int(v.get("doc_page"), ""),
        ])
    v_headers = [
        "#", "ชื่อวิว", "ประเภทวิว", "ผู้สร้าง", "ตำแหน่ง", "ลำดับเมนู", "ไอคอน",
        "การแสดงผล", "แสดงเมื่อ", "ประเภทแอกชัน", "ค่าคอนฟิกวิว (JSON)", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Views", v_headers, v_rows,
        widths={1: 40, 2: 22, 4: 20, 8: 34, 9: 60, 10: 58},
        freeze="C2", tab_color=TAB_UX,
    )

    # ---------------------------------------------------------------- actions
    a_rows = []
    for i, a in enumerate(src["actions"], start=1):
        a_rows.append([
            i,
            raw(a.get("Action name")),
            raw(a.get("Do this")),
            raw(a.get("For a record of this table")),
            a.get("Action order"),
            raw(a.get("Action icon")),
            raw(a.get("Attach to column")),
            raw(a.get("Set this column")),
            raw(a.get("To this value")),
            raw(a.get("Display name")),
            raw(a.get("Prominence")),
            raw(a.get("Visible?")),
            raw(a.get("Does this action apply to the whole table?")),
            raw(a.get("Modifies data?")),
            raw(a.get("Bulk action?")),
            raw(a.get("Needs confirmation?")),
            raw(a.get("Confirmation Message")),
            raw(a.get("Only if this condition is true")),
            raw(a.get("Disable automatic updates?")),
            raw(a.get("With these properties")),
            to_int(a.get("doc_page"), ""),
        ])
    a_headers = [
        "#", "ชื่อแอกชัน", "ทำอะไร (Do this)", "ตารางที่ผูก", "ลำดับแอกชัน",
        "ไอคอน", "คอลัมน์ที่ผูก", "ตั้งค่าคอลัมน์", "ค่าที่ตั้ง", "ชื่อที่แสดง",
        "ระดับการแสดงผล (Prominence)", "การแสดงผล", "ใช้กับทั้งตาราง?",
        "แก้ไขข้อมูล?", "เป็นแอกชันกลุ่ม?", "ต้องยืนยัน?", "ข้อความยืนยัน",
        "เงื่อนไข (Only if)", "ปิดการอัปเดตอัตโนมัติ?", "ค่าคอนฟิก (JSON)", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Actions", a_headers, a_rows,
        widths={1: 40, 2: 24, 3: 44, 6: 30, 9: 30, 10: 28, 11: 26, 16: 34,
                17: 44, 19: 58},
        freeze="C2", tab_color=TAB_UX,
    )

    # ----------------------------------------------------------------- slices
    s_rows = []
    for i, s in enumerate(src["slices"], start=1):
        s_rows.append([
            i,
            raw(s.get("Slice Name")),
            raw(s.get("Source Table")),
            raw(s.get("Update mode")),
            raw(s.get("Visible?")),
            raw(s.get("Row filter condition")),
            raw(s.get("Slice Columns")),
            raw(s.get("Slice Actions")),
            to_int(s.get("doc_page"), ""),
        ])
    s_headers = [
        "#", "ชื่อสไลซ์", "ตารางต้นทาง", "โหมดอัปเดต", "การแสดงผล",
        "เงื่อนไขกรองแถว", "คอลัมน์ในสไลซ์", "สไลซ์แอกชัน", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Slices", s_headers, s_rows,
        widths={1: 26, 2: 40, 5: 44, 6: 58, 7: 44},
        freeze="C2", tab_color=TAB_UX,
    )

    # ---------------------------------------------------------- format rules
    fr_rows = []
    for i, fr in enumerate(src["format_rules"], start=1):
        fr_rows.append([
            i,
            raw(fr.get("Rule name")),
            raw(fr.get("For this data")),
            raw(fr.get("Format these columns and actions")),
            raw(fr.get("If this condition is true")),
            raw(fr.get("Like this")),
            raw(fr.get("Is this format rule disabled?")),
            fr.get("Rule order"),
            raw(fr.get("Visible?")),
            to_int(fr.get("doc_page"), ""),
        ])
    fr_headers = [
        "#", "ชื่ากฎ", "ตารางข้อมูล", "คอลัมน์ที่จัดรูปแบบ", "เงื่อนไข",
        "รูปแบบ (JSON)", "ปิดใช้งานกฎ?", "ลำดับกฎ", "การแสดงผล", "หน้าเอกสาร",
    ]
    write_table_sheet(
        wb, "Format_Rules", fr_headers, fr_rows,
        widths={1: 26, 2: 40, 3: 40, 4: 44, 5: 58},
        freeze="C2", tab_color=TAB_UX,
    )

    # ------------------------------------------------------------------ readme
    sheet_rows = [
        ("README", "-", "หน้านี้ — สรุปตัวเลขทั้งหมด, อธิบายความต่างระหว่างตารางจริง/ตารางบอท และวิธีอ่านไฟล์"),
        ("Tables_Index", f"{len(index_rows)}", "ตารางทั้งหมด 90 ตาราง + คุณสมบัติ (แหล่งข้อมูล, สิทธิ์, ฟิลเตอร์, จำนวนคอลัมน์)"),
        ("Real_Tables", f"{len(src['real'])}", "ตารางจริง 29 ตาราง (ผูกกับ Google Sheet) พร้อมรายการคอลัมน์และคอลัมน์ที่มีสูตร"),
        ("Bot_Tables", f"{len(src['bot'])}", "ตารางบอท 61 ตาราง (AppSheet สร้างเอง) พร้อมชนิดของตารางบอทและรายการคอลัมน์"),
        ("Real_Table_Columns", f"{sum(len(table_cols.get(t['table_name'], [])) for t in src['real'])}",
         "คอลัมน์ของตารางจริงทุกคอลัมน์ (1 แถว = 1 คอลัมน์) ใช้ค้นหา/กรองรายคอลัมน์"),
        ("Bot_Table_Columns", f"{sum(len(table_cols.get(t['table_name'], [])) for t in src['bot'])}",
         "คอลัมน์ของตารางบอททุกคอลัมน์ (1 แถว = 1 คอลัมน์)"),
        ("All_Columns", f"{len(all_rows)}", "คอลัมน์ทั้งหมด 2,304 คอลัมน์ รวมทุกตาราง พร้อมชนิด/สูตร/เงื่อนไขทั้งหมด"),
        ("Formulas", f"{len(f_rows)}",
         f"สูตร/นิพจน์ทั้งหมด {len(f_rows)} รายการ "
         "(App formula, Initial value, Expression for update mode, Security filter)"),
        ("Functions", f"{len(fn_rows)}", "ฟังก์ชันที่ถูกเรียกใช้ พร้อมจำนวนครั้ง"),
        ("Column_Types", f"{len(t_rows)}", "สรุปจำนวนคอลัมน์แยกตามประเภท (Text/Image/Ref/...)"),
        ("Views", f"{len(v_rows)}", "วิวทั้งหมด 115 วิว พร้อมชนิดวิวและค่าคอนฟิก"),
        ("Actions", f"{len(a_rows)}", "แอกชันทั้งหมด 214 รายการ พร้อมตาราง/คอลัมน์ที่ผูกและเงื่อนไข"),
        ("Slices", f"{len(s_rows)}", "สไลซ์ทั้งหมด 8 รายการ (ตารางต้นทาง + เงื่อนไขกรองแถว)"),
        ("Format_Rules", f"{len(fr_rows)}", "กฎการจัดรูปแบบทั้งหมด 11 กฎ (เงื่อนไข + รูปแบบที่ใช้)"),
    ]
    build_readme(wb, src, sheet_rows)

    # README ต้องมาก่อนสุด
    wb.move_sheet("README", offset=-(len(wb.sheetnames) - 1))
    wb.active = 0

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    wb.save(out)

    print(f"wrote {out}")
    print("sheets:", ", ".join(wb.sheetnames))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
