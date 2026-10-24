# -*- coding: utf-8 -*-
"""Generate README.md from the extracted data so the numbers can never drift."""
import csv, json, os, sys, collections

REPO = sys.argv[1] if len(sys.argv) > 1 else '.'


def read(name):
    with open(os.path.join(REPO, name), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


m = json.load(open(os.path.join(REPO, 'MANIFEST.json'), encoding='utf-8'))
app = m['app']
c = m['counts']
tidx = read('tables/INDEX.csv')
real = [r for r in tidx if r['classification'] == 'real']
bot = [r for r in tidx if r['classification'] == 'bot']
botk = collections.Counter(r['bot_table_kind'] for r in bot)

real_rows = []
for r in sorted(real, key=lambda x: -int(x['column_count'])):
    real_rows.append(
        f"| `{r['table_name']}` | {r['worksheet_qualifier'] or '—'} | "
        f"{r['column_count']} | {r['formula_column_count']} | {r['data_source']} | "
        f"{r['security_filter'][:44] or '—'} |")

bot_rows = []
for r in sorted(bot, key=lambda x: x['table_name']):
    kind = {'process-state': 'bot process state',
            'process-output': 'bot step output',
            'per-user-settings': 'per-user settings'}.get(r['bot_table_kind'], r['bot_table_kind'])
    bot_rows.append(f"| `{r['table_name']}` | {kind} | {r['column_count']} | `{r['source_path'][:52]}` |")

fn = read('formulas/functions.csv')
fn_rows = [f"| `{r['function']}` | {r['occurrences']} |" for r in fn[:14]]

refrows = read('formulas/column_references.csv')
bad = [r for r in refrows if r['resolves_to_known_column'] == 'no']
badcols = collections.Counter(r['reference'] for r in bad)

readme = f"""# เผ่าปัญญาทรานสปอร์ต — AppSheet schema (SCG JWD / นครหลวง)

ข้อมูลโครงสร้างทั้งหมดของแอป AppSheet **เผ่าปัญญาทรานสปอร์ต** ที่สกัดออกมาจากไฟล์
`Application Documentation.PDF` (เอกสาร 1,946 หน้า) เรียบร้อยแล้ว — พร้อมนำขึ้น GitHub
เพื่อ review, diff และเก็บเวอร์ชัน

> แอป: `{app['app_name']}` · เวอร์ชัน `{app['version']}` · โฟลเดอร์ `{app['app_folder']}`
> เอกสารถูกสร้างเมื่อ **{app['document_generated_at'].replace('Generated at: ', '')}**

---

## สรุปสั้น ๆ

| หัวข้อ | จำนวน |
|---|---|
| ตารางทั้งหมด | **{c['tables_total']}** |
| ├─ **ตารางจริง** (ผูกกับ Google Sheet — ต้องดูแล) | **{c['tables_real']}** |
| └─ **ตารางบอท** (AppSheet สร้างเอง — อย่าแก้) | **{c['tables_bot']}** |
| คอลัมน์ทั้งหมด | **{c['columns']}** |
| สูตร / นิพจน์ | **{c['formulas']}** |
| Views | **{c['views']}** |
| Actions | **{c['actions']}** |
| Slices | **{c['slices']}** |
| Format Rules | **{c['format_rules']}** |

ตัวเลขชุดนี้ตรงกับที่แอปสรุปไว้เองในหน้าแรกของเอกสาร
(`{app['counts_reported_by_app']['tables']}` / `{app['counts_reported_by_app']['ux']}` /
`{app['counts_reported_by_app']['behavior']}`) — ดู `docs/VERIFICATION_REPORT.md` สำหรับผลสุ่มตรวจ

---

## ตารางจริง กับ ตารางบอท — ต่างกันยังไง

นี่คือจุดสำคัญที่สุดของการแยกข้อมูล ตารางทั้ง {c['tables_total']} ในแอปนี้แบ่งเป็น 2 กลุ่ม

### ตารางจริง ({c['tables_real']} ตาราง) — ข้อมูลธุรกิจที่ต้องบริหาร

ผูกกับ worksheet ของ Google Sheet (`Data Source` = `google` / `google_tables`)
มีชื่อ worksheet ระบุชัด และมี security filter ปิดการแก้ไขสำหรับผู้ใช้ทั่วไป

| ตาราง | Worksheet | คอลัมน์ | คำนวณ | แหล่งข้อมูล | Security filter |
|---|---|---|---|---|---|
{chr(10).join(real_rows)}

### ตารางบอท ({c['tables_bot']} ตาราง) — ของภายในระบบ อย่าแก้เอง

`Data Source` = `native` หรือ `Source Path` ขึ้นต้นด้วย `/ProcessStateTables/`
หรือมี `/StepOutput_` — ทั้งหมด `Visible? = NEVER` คือ AppSheet สร้างขึ้นเองเพื่อเก็บ
state ของ bot process และผลลัพธ์ของแต่ละ step ไม่ใช่ข้อมูลที่มีคนกรอก

| ตาราง | ชนิด | คอลัมน์ | Source Path |
|---|---|---|---|
{chr(10).join(bot_rows)}

**แยกด้วยเกณฑ์นี้ได้เลย** (สคริปต์ `tools/build_repo.py` ใช้เกณฑ์เดียวกัน):

| เงื่อนไข | ผลลัพธ์ |
|---|---|
| `Data Source` เป็น `google` หรือ `google_tables` | ตารางจริง |
| `Data Source` เป็น `native` | ตารางบอท |
| `Source Path` ขึ้นต้นด้วย `/ProcessStateTables/` | ตารางบอท (process state) |
| `Source Path` มี `/StepOutput_` | ตารางบอท (step output) |
| ชื่อตารางคือ `_Per User Settings` | ตารางบอท (ตั้งค่ารายผู้ใช้) |

จำนวนตารางบอทแยกตามชนิด: process-state {botk.get('process-state', 0)} ·
process-output {botk.get('process-output', 0)} ·
per-user-settings {botk.get('per-user-settings', 0)}

---

## โครงสร้างโฟลเดอร์

```
.
├── README.md                    ← ไฟล์นี้
├── MANIFEST.json                ← ดัชนีของทุกอย่างในรีโป (นับ/เวลา/ที่มา)
├── appsheet-export.xlsx         ← workbook รวมทุกชีต (เปิดดูง่าย)
├── app/app.json                 ← ข้อมูลระดับแอป (ชื่อ เวอร์ชัน โฟลเดอร์ ฯลฯ)
├── tables/
│   ├── INDEX.csv                ← ตารางทั้งหมด + คอลัมน์ classification
│   ├── real/                    ← {c['tables_real']} ไฟล์ (หนึ่งไฟล์ต่อหนึ่งตารางจริง) + _index.csv
│   └── bot/                     ← {c['tables_bot']} ไฟล์ (หนึ่งไฟล์ต่อหนึ่งตารางบอท) + _index.csv
├── columns/
│   ├── all_columns.csv          ← คอลัมน์ทั้งหมด {c['columns']} คอลัมน์ (flatten Type Qualifier แล้ว)
│   └── by_type.csv              ← สรุปจำนวนคอลัมน์แยกตามชนิด
├── formulas/
│   ├── formulas.csv             ← สูตรทั้งหมด {c['formulas']} สูตร (คอลัมน์ + ระดับตาราง)
│   ├── functions.csv            ← ฟังก์ชันที่ใช้บ่อย เรียงตามจำนวนครั้ง
│   └── column_references.csv    ← ทุกการอ้างอิง [คอลัมน์] + ตรวจว่ามีคอลัมน์นั้นจริงไหม
├── views/views.csv              ← หน้าจอทั้งหมด {c['views']} หน้าจอ
├── actions/actions.csv          ← action ทั้งหมด {c['actions']} รายการ
├── slices/slices.csv            ← slice {c['slices']} รายการ
├── format_rules/format_rules.csv← format rule {c['format_rules']} รายการ
├── schema/app_schema.json       ← โครงสร้างเต็มทั้งแอป (JSON)
├── docs/
│   ├── ARCHITECTURE.md          ← ภาพรวมแอป: ตาราง คอลัมน์ วิว แอคชัน สลัก ฟอร์แมตรูล
│   ├── REAL_VS_BOT.md           ← เกณฑ์แยกตารางจริง/ตารางบอท + รายละเอียดทุกตาราง
│   ├── FORMULA_CATALOG.md       ← แคตตาล็อกสูตร 345 สูตร ฟังก์ชัน รูปแบบที่พบบ่อย
│   └── VERIFICATION_REPORT.md   ← ผลสุ่มตรวจข้อมูลเทียบกับ PDF ต้นฉบับ
└── tools/                       ← สคริปต์ที่ใช้สกัดข้อมูล (รันซ้ำได้จาก PDF เดิม)
```

ไฟล์ CSV หนึ่งไฟล์ต่อหนึ่งตาราง: **หนึ่งแถว = หนึ่งคอลัมน์** พร้อมคอลัมน์ `type`,
`app_formula`, `initial_value`, `valid_if`, `required_if`, `editable_if`, `show_if`,
`reset_if` และ `doc_page` (เลขหน้าใน PDF ต้นฉบับ เพื่อให้กรองกลับไปดูของจริงได้)

---

## สูตรที่ใช้บ่อย

| ฟังก์ชัน | จำนวนครั้งที่ใช้ |
|---|---|
{chr(10).join(fn_rows)}

การอ้างอิงคอลัมน์ที่ **หาไม่เจอ** ในระบบ: {len(bad)} รายการ
(ดูรายละเอียดใน `docs/FORMULA_CATALOG.md`)

---

## สร้างข้อมูลชุดนี้ขึ้นใหม่ได้อย่างไร

```bash
cd tools
./run_pipeline.sh "/path/to/Application Documentation.PDF" ..
```

ไปล์ขั้นตอน: PDF → กล่องคำพิกัด (poppler `-bbox-layout`) → โครงสร้างระเบียน
(ตาราง/คอลัมน์/วิว/แอคชัน) → ตรวจ round-trip → สร้าง CSV/JSON/โฟลเดอร์

ตัวตรวจจะยืนยันว่า **ตัวอักษรทุกตัวใน PDF ถูกย้ายไปอยู่ในฟิลด์ที่ถูกต้อง**
(เทียบอักขระแบบไม่สนใจช่องว่าง) ก่อนเขียนไฟล์ออกมา

---

## ข้อจำกัดที่ควรรู้

- เอกสารต้นฉบับเป็นเอกสาร **โครงสร้าง** ไม่ใช่ข้อมูลแถว — ที่นี่มีความหมายของตาราง/คอลัมน์/สูตร/วิว/แอคชัน
  แต่ไม่มีข้อมูลลูกค้าในแซต
- ค่าที่ขึ้นบรรทัดใน PDF (ค่าที่ยาวเกินความกว้างช่อง) อาจมีช่องว่างหายไปหนึ่งตัวในจุดที่ตัดบรรทัด
  เฉพาะจุดที่เป็น JSON ถูกยืนยันด้วย `json.loads` ว่าถูกต้อง ส่วนสูตรที่ไม่ใช่ JSON
  อาจมีความคลาดเคลื่อนของช่องว่างได้ 1 จุด — ตรวจสอบจาก `doc_page` ได้
- อีโมจิในสูตรบางสูตรอยู่คนละตำแหน่งกับข้อความใน PDF (fallback font) จึงอาจสลับตำแหน่ง
  ภายในสูตร — ไม่กระทบเนื้อหา แต่ให้ตรวจจากภาพหน้าจอ

## สิ่งที่ควรทำต่อ

1. อัปโหลดขึ้น GitHub แล้วเปิด PR ครั้งแรกเอาไฟล์ `tables/` + `columns/` + `schema/`
2. ต่อ `docs/` เข้ากับ wiki ของทีม
3. ถ้าจะเอาไปทำเป็นแอปต้นแบบใหม่: ดู `docs/ARCHITECTURE.md` ก่อน แล้วเริ่มจากตารางจริง 29 ตารางเท่านั้น
   ตารางบอท 61 ตารางปล่อยให้ AppSheet สร้างใหม่ได้
"""

with open(os.path.join(REPO, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('README.md written,', len(readme), 'chars')
