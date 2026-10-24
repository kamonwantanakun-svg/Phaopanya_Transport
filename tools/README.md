# tools/ — สคริปต์สกัดข้อมูล (เครื่องมือสร้างข้อมูลซ้ำได้)

โฟลเดอร์นี้คัดลอกมาจากชุดสกัดข้อมูลต้นทาง
(`/workspace/appsheet-scg-jwd-transport/tools/`) แบบ **ไม่แก้ไขไฟล์ต้นฉบับ**
ทุกสคริปต์เป็น read-only ต่อไฟล์ต้นทาง และรันซ้ำได้เสมอ (idempotent)

---

## 1. สายการทำงาน (pipeline)

```
Application Documentation.PDF
        │  pdftotext -bbox-layout
        ▼
   bbox.xhtml ──► extract_words.py ──► words3.json      (กล่องคำ + ตำแหน่ง)
                                                │
                                                ▼
                                appsheet_parse.py  (records.json)
                                                │
                        ┌───────────────────────┼────────────────────────┐
                        ▼                       ▼                        ▼
              verify_roundtrip.py        build_repo.py             build_workbook.py
              (ตรวจครบทุกตัวอักษร)      (CSV/JSON ทั้งแอป)      (xlsx 14 ชีต)
                                                │
                                                ▼
                                         build_readme.py
```

> ### ⚠️ สถานะจริง ณ วันที่ส่งมอบ — อ่านก่อนรัน
>
> **`run_pipeline.sh` ยังรันครบสายไม่ได้** เพราะตั้ง `set -euo pipefail`:
>
> | ขั้น | สถานะวันนี้ |
> |---|---|
> | 1/4 `extract_words.py` | ✅ ผ่าน |
> | 2/4 `appsheet_parse.py` | ✅ ผ่าน (ได้ `records.json` 2,834 records) |
> | 3/4 `verify_roundtrip.py` | ❌ **exit 1** — ดูคำอธิบายด้านล่าง |
> | 4/4 `build_repo.py` | ⚠️ **ไม่เคยถูกเรียก** เพราะขั้น 3 หยุดสายก่อน |
>
> **ทำไมขั้น 3/4 ถึง FAIL (ยืนยันด้วยการรันเองแล้ว — ไม่ใช่ปัญหาของข้อมูล):**
> ตัว gate เทียบ **ข้อความทั้งหมดใน PDF** กับ **ข้อความที่ประกอบจาก records** แต่ record ของ parser
> **ไม่มีหัวข้อโครงสร้าง** (`Data`, `Tables`, `Columns`, `UX`, `Behavior` …) ติดไปด้วย
> ตัวอักษรที่ "หาย" 2,213 ตัวจึงเป็น **ตัวอักษรอังกฤษของหัวข้อ** (D,a,t,T,b,l,e,s,n,m — ไม่มีอักษรไทยหายเลย)
> ส่วนตัวสคริปต์รุ่นก่อน (เทียบแบบเรียงลำดับ) รายงาน `CONTENT: MISMATCH - 19 regions`
> ซึ่งเป็น **ลำดับการอ่าน** (2 ตารางแรกสลับกัน, คำไทยถูกตัดคนละจุด) ไม่ใช่เนื้อหาหาย
>
> **สรุป: gate ยังไม่ผ่าน แต่ข้อมูลที่ได้ไม่ได้หาย** — พิสูจน์ได้ด้วยการ rebuild ขั้น 2 → 4:
> **102/105 ไฟล์ที่ `build_repo.py` สร้างตรงกับชุดที่ส่งมอบทุกไบต์**
> (ต่างกันแค่ timestamp `extracted_at`/`generated_at` ใน `MANIFEST.json`, `app/app.json`,
> `schema/app_schema.json`) → **ข้อมูลถูกต้องและสร้างซ้ำได้**
>
> **ทางออกสำหรับผู้ใช้:**
> 1. รันขั้น 1, 2, 4 เอง (ดู §2) — ได้ข้อมูลชุดเดิมแบบ byte-identical
> 2. ถ้าจะทำให้ gate ผ่าน: ให้ parser **emit หัวข้อโครงสร้างเป็น record** หรือให้ gate
>    **ตัดหัวข้อออกจากฝั่ง PDF** ก่อนเทียบ (ทั้งสองฝั่งต้องตัดหักเหมือนกัน)
>
> ข้อควรรู้: ขั้น 3/4 เป็น **ตาข่ายนิภัย** โดยเจตนา — ถ้ามีตัวอักษรหายจริงต้องหยุด
> แต่ ณ วันนี้ gate ยังเทียบผิดฝั่ง (ดูรายละเอียดข้างบน) → ให้ถือว่าเป็น **known issue**
> ดู `../docs/VERIFICATION_REPORT.md` และบันทึกของทีมใน `.mavis/memory/`

---

## 2. รันซ้ำทั้งสาย (แนะนำ)

```bash
# ต้องมี pdftotext (poppler-utils) และ python3 + lxml
./run_pipeline.sh "/path/to/Application Documentation.PDF" /path/to/out-dir
```

`run_pipeline.sh` จะทำ 4 ขั้นให้อัตโนมัติ

| ขั้น | คำสั่ง | ผลลัพธ์ |
|---|---|---|
| 1/4 | `pdftotext -bbox-layout` + `extract_words.py` | `words3.json` |
| 2/4 | `appsheet_parse.parse()` | `records.json` |
| 3/4 | `verify_roundtrip.py` | ตรวจว่าทุกตัวอักษรใน PDF ถูกอ่านครบและจับคู่กลับได้ (ตอนนี้ FAIL — ดู §1) |
| 4/4 | `build_repo.py` | `tables/`, `columns/`, `formulas/`, `views/`, `actions/`, `slices/`, `format_rules/`, `schema/`, `app/`, `MANIFEST.json` |

> ขั้น 3/4 คือ "กันพลาด" — ถ้ามีตัวอักษรหายหรือซ้ำ สคริปต์จะหยุดและไม่เขียนไฟล์ผลลัพธ์
> (ผลจริงวันนี้: หยุดที่ขั้น 3 ด้วย exit 1 → ขั้น 4 ไม่ทำงาน ดู §1)

### รันทีละส่วน (เส้นทางที่ใช้ได้จริงวันนี้)

```bash
pdftotext -bbox-layout "Application Documentation.PDF" bbox.xhtml
python3 extract_words.py bbox.xhtml words3.json
python3 -c "import json,sys,appsheet_parse; r,s=appsheet_parse.parse(json.load(open('words3.json'))); json.dump(r,open('records.json','w'),ensure_ascii=False,indent=1)"
python3 verify_roundtrip.py words3.json     # ขั้นตรวจ — ตอนนี้ exit 1 (known issue: เทียบหัวข้อโครงสร้างด้วย)
python3 build_repo.py records.json <out-dir>
python3 build_workbook.py <out-dir> appsheet-export.xlsx
python3 build_readme.py <out-dir>
```

---

## 3. แต่ละสคริปต์ทำอะไร

| ไฟล์ | หน้าที่ |
|---|---|
| `run_pipeline.sh` | ตัวรันทั้งสาย (4 ขั้น) — จุดเริ่มต้นเดียวที่ต้องใช้ |
| `extract_words.py` | อ่าน `bbox.xhtml` จาก poppler ออกมาเป็นตารางคำ + กรอบตำแหน่ง (`words3.json`) |
| `appsheet_parse.py` | แก้โครงสร้าง (label cell, value cell) ของ PDF ให้เป็น record: `table` / `schema` / `column` / `slice` / `view` / `format_rule` / `action` / `app` |
| `verify_roundtrip.py` | เทียบ token stream ของ PDF กับ record ที่ parse ได้ — ยืนยันว่าไม่มีข้อมูลหายและไม่มีการซ้ำซ้อน |
| `build_repo.py` | เขียน CSV/JSON ทั้งแอป (`tables/`, `columns/`, `formulas/`, `views/`, `actions/`, `slices/`, `format_rules/`, `schema/`, `app/`) + `MANIFEST.json` |
| `build_workbook.py` | รวม CSV/JSON เป็น workbook `xlsx` 14 ชีต (มี freeze panes + auto filter) |
| `build_readme.py` | สร้าง `README.md` ของชุดข้อมูลจากตัวเลขจริงใน `MANIFEST.json` (ตัวเลขไม่ drift) |

### ข้อกำหนดสภาพแวดล้อม

* Python 3.8+ (ใช้เฉพาะ stdlib เว้น `lxml` ที่ `extract_words.py` ใช้อ่าน xhtml)
* `poppler-utils` (`pdftotext -bbox-layout`)
* ไฟล์ PDF ต้นทางคือ “Application Documentation.PDF” (export จากแอป AppSheet)

---

## 4. ชั้นข้อมูล `data/` ของรีโพนี้

โฟลเดอร์ `data/` (ดัชนีตาราง, ไฟล์ต่อตาราง, คอลัมน์, วิว/แอคชัน, ตารางอ้างอิง)
**สร้างจากต้นไม้ข้อมูลที่ `build_repo.py` สร้าง** — ไม่ได้อ่าน PDF ซ้ำ:

```bash
python3 build_data_layer.py /workspace/appsheet-scg-jwd-transport /workspace/gh-repo
python3 verify_data_layer.py /workspace/gh-repo /workspace/appsheet-scg-jwd-transport
```

* `build_data_layer.py` — แปลงชุดข้อมูลดิบเป็นชั้นข้อมูลชื่อไฟล์อังกฤษ (`data/tables/real/*.csv`,
  `data/tables/bot/*.csv`, `data/references/*.csv`, …)
* `verify_data_layer.py` — ตรวจอัตโนมัติว่าแถวรวม = 2304, หัวตารางตรงกันทุกไฟล์,
  ชื่อในตารางอ้างอิงมีอยู่จริง, ชื่อไฟล์ถูกรูปแบบ, workbook 14 ชีต

สคริปต์สองไฟล์นี้อยู่ที่
`<outputs>/build-data-layer/` ของงาน hand-off (ดู `deliverable.md`)
— เจ้าของรีโพจะย้ายเข้า `tools/` ได้ถ้าต้องการให้รีโพ rebuild ได้เอง

---

## 5. หมายเหตุเรื่องคุณภาพข้อมูล

PDF เป็น “browser print” ของหน้า attribute dump จึงมีจุดที่ข้อความถูกตัดกลางคัน
(เช่น `ReferencedTableName` ของคอลัมน์ชนิด `Ref` หายไป) — โครงสร้างและค่าที่เหลือยังถูกต้อง
`verify_roundtrip.py` เป็นตัวกันเหนี้ว่าการอ่านไม่ได้ทำให้อักขระหายหรือซ้ำ
