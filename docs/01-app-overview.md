# 01 — ภาพรวมแอป "เผ่าปั ญญา ทรานสปอร์ต" (SCG JWD Transport)

> เอกสารนี้เป็นไฟล์ที่ 1 จาก 10 ไฟล์ อ่านตามลำดับ
> ทุกตัวเลขมาจากไฟล์ข้อมูลดิบใน `data/` ของรีโพนี้นี้ (ไม่ใช่การคาดเดา)
> แหล่งทั้งหมดอ้างในวงเล็บ เช่น `[data/tables/index.csv]`

---

## 1. แอปนี้คืออะไร

| รายการ | ค่า | แหล่ง |
|---|---|---|
| ชื่อแอป | เผ่าปั ญญา ทรานสปอร์ต | `[data/schema/app-schema.json]` |
| โฟลเดอร์ใน AppSheet | `/appsheet/data/เผ่าปั ญญาทรานสปอร์ต-915154893` | `[data/schema/app-schema.json]` |
| เวอร์ชัน | 1.004638 | `[data/schema/app-schema.json]` |
| Function | Other | `[data/schema/app-schema.json]` |
| Runnable? | Yes | `[data/schema/app-schema.json]` |
| Deployable? | No | `[data/schema/app-schema.json]` |
| Personal use only? | No | `[data/schema/app-schema.json]` |
| เอกสารต้นฉบับถูกสร้างเมื่อ | 15/9/2569 02:56:32 (พ.ศ.) | `[data/schema/app-schema.json]` |
| ที่มาของข้อมูลทั้งหมด | ไฟล์ `Application Documentation.PDF` ที่แอปสร้างเอง — 1,946 หน้า | `[data/schema/app-schema.json]` |

**คำอธิบายในหนึ่งประโยค:** เป็นแอปจัดการงานขนส่ง/กระจายสินค้า (last-mile delivery) ของ
**SCG ในภูมิภาคนครหลวง + JWD** ตั้งแต่รับงานประจำวัน → สแกนรับเอกสาร → วางบิล/คิดค่าขนส่ง
→ อนุมัติราคา → เบิกส่วนต่าง → ออกเอกสาร/ใบป่ะหน้า → ประกาศรับทราบ

หลักฐานที่ยืนยันการอ่านนี้จากข้อมูลจริง (ไม่ใช่การคาดเดา):

| หลักฐาน | จากไฟล์ | รายละเอียด |
|---|---|---|
| ชื่อตารางหลัก | `[data/tables/index.csv]` | `ตารางงานประจำวัน`, `ข้อมูลการวางบิล`, `SCGนครหลวงJWDภูมิภาค`, `รับงานคืนได้เงิน200`, `ทำเบิกส่วนต่างScgวังน้อย`, `แจ้งปั ญหาระหว่างวัน` |
| ชื่อคอลัมน์ที่สื่อกระบวนการ | `[data/columns/all_columns.csv]` | `Plan Delivery`, `Shipment No`, `Invoice No`, `ScanStatus`, `DeliveryStatus`, `สถานะการอนุมัติ`, `ราคาตามระยะทาง`, `เรทดีเซล`, `ระยะทางที่วิ่ง (KM)`, `ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม`, `ผลการตรวจสอบงานส่ง` |
| ตารางราคา | `[data/tables/index.csv]` | `ราคาน้ำมันดีเซล`, `Price_Table`, `PriceOverride`, `ราคาในระบบก่อนส่งสินค้า`, `ข้อมูลชื่องานต้นทางปลายทาง` |
| ตารางเอกสาร | `[data/tables/index.csv]` | `ปริ๊นใบวางบิล`, `PDFพนักงาน`, `สร้างเอกสาร` — มีคอลัมน์ `Export to xlsx` / `Export to XLSX` / `EXPORT TO PDF` |
| ตารางประกาศ | `[data/tables/index.csv]` | `Announcements` + `Acknowledge_Logs` (มีคอลัมน์ `ลงชื่อพนักงาน` ชนิด Signature) |
| ระบบเดินเส้นทาง | `[data/references/processes.csv]` | process `Bot_4ตัว_จัดเรียงเส้นทาง` → `GoogleMapsRoutesAPI_Step Output` |

---

## 2. ตัวเลขสำคัญทั้งหมด

### 2.1 ตัวเลขที่แอปประกาศเอง (หน้า 1 ของ PDF)

| กลุ่ม | ที่แอปรายงาน | แหล่ง |
|---|---|---|
| Data | `90 Tables \| 2304 Columns \| 8 Slices` | `[data/schema/app-schema.json]` |
| UX | `115 Views \| 11 Format Rules` | `[data/schema/app-schema.json]` |
| Behavior | `214 Actions \| 0 Workflow Rules` | `[data/schema/app-schema.json]` |

### 2.2 ตัวเลขที่สกัดได้จริง (นับจากไฟล์)

| รายการ | จำนวน | แหล่ง |
|---|---:|---|
| ตารางทั้งหมด | **90** | `[data/tables/index.csv]` |
| ├ ตารางจริง (ผูกกับชีต) | **29** | `[data/tables/index.csv]` |
| └ ตารางบอท (`Data Source = native`) | **61** | `[data/tables/index.csv]` |
| ├─ process-state | 30 | `[data/tables/index.csv]` |
| ├─ process-output | 30 | `[data/tables/index.csv]` |
| └─ per-user-settings | 1 | `[data/tables/index.csv]` |
| process ของบอท | **30 สาย** | `[data/references/processes.csv]` |
| คอลัมน์ทั้งหมด | **2,304** | `[data/columns/all_columns.csv]` |
| ├ ในตารางจริง | 595 (คำนวณ 313) | `[data/tables/index.csv]` |
| └ ในตารางบอท | 1,709 (คำนวณ 3) | `[data/tables/index.csv]` |
| สูตร/นิพจน์ | **345** | `[data/formulas/formulas.csv]` |
| ├ ระดับคอลัมน์ | 316 (App formula 190 + Initial value 126) | `[data/formulas/formulas.csv]` |
| └ ระดับตาราง | 29 (Expression for update mode 22 + Security filter 7) | `[data/formulas/formulas.csv]` |
| วิว | **115** | `[data/views/views.csv]` |
| แอกชัน | **214** | `[data/actions/actions.csv]` |
| สไลซ์ | **8** | `[data/slices/slices.csv]` |
| ฟอร์แมตรูล | **11** | `[data/format-rules/format_rules.csv]` |
| ชนิดคอลัมน์ (ค่า `type` ที่ต่างกัน) | **113** | `[data/columns/by-type.csv]` |
| ฟังก์ชันที่ใช้ | **50 ตัว / 569 ครั้ง** | `[data/references/function-usage.csv]` |
| การอ้างอิงคอลัมน์ในสูตร | 637 (resolve ได้ 474 / ไม่ได้ 163) | `[data/references/column-references.csv]` |
| Workflow Rules | **0** | หน้า 1 ของ PDF (`[data/schema/app-schema.json]`) |

> ตัวเลขทุกตัวตรงกับที่แอปสรุปไว้เองในหน้าแรกของ PDF — ดูรายละเอียดการตรวจสอบใน `10-known-issues.md`

---

## 3. ใครใช้แอปนี้

### 3.1 สองบทบาทที่ประกาศไว้ในแอป

`ข้อมูลพนักงาน.ROLE` เป็นคอลัมน์ชนิด `Enum` ที่ PDF หน้า 280 พิมพ์ค่าไว้ว่า
`["ADMIN","USER"]` — ดูหัวข้อ “การยืนยันกลับไปที่ PDF” ใน `10-known-issues.md` วิธีอ่านค่า Enum

| บทบาท | ใคร | ทำอะไรได้ |
|---|---|---|
| `ADMIN` | ผู้ดูแลระบบ / ผู้บริหาร (ผู้อนุมัติราคา, ปิดงาน, ออกเอกสาร) | อนุมัติราคา, แก้ไขทุกตาราง, เห็นข้อมูลของทุกคน, เรียกบอทปริ๊นเอกสาร |
| `USER` | พนักงานขับรถ / ผู้รับงาน | บันทึกงานของตัวเอง, สแกนรับเอกสาร, ส่งแจ้งปัญหา, เปิดใบป่ะหน้าของตัวเอง |

หลักฐาน: `Expression for update mode` ของ 22 ตารางจริงใช้ `SWITCH(USERROLE(), …)` แบ่ง
ADMIN/USER เสมอ — `[data/formulas/formulas.csv]` (ดูรายละเอียดใน `08-security-rules.md`)

### 3.2 กลุ่มผู้ใช้ที่อนุมานจากวิวและแอกชัน

| กลุ่มผู้ใช้ | หลักฐานในข้อมูล | แหล่ง |
|---|---|---|
| พนักงานขับรถ (USER) | ตารางงานประจำวันมี `Email พนักงาน`, `ชื่อ - นามสกุล`, `ทะเบียนรถ`; มีคอลัมน์ `Related …s` ของพนักงาน 7 รายการ | `[data/columns/all_columns.csv]` |
| ผู้อนุมัติราคา (ADMIN) | แอกชัน `อนุมัติ` / `รอการอนุมัติ` มีเงื่อนไข `USERROLE() = "ADMIN"`; สไลซ์ `รอการอนุมัติ` กรอง `=USERROLE()= "ADMIN"` | `[data/actions/actions.csv]`, `[data/slices/slices.csv]` |
| ฝ่ายเอกสาร/บัญชี | ตาราง `ปริ๊นใบวางบิล`, `PDFพนักงาน`, `สร้างเอกสาร`, `FILTER` มีแอกชัน `Export to xlsx`/`EXPORT TO PDF` และสูตรรวมยอดราคา | `[data/tables/index.csv]`, `[data/actions/actions.csv]` |
| ผู้ดูแลระบบ | แอกชัน `COMPOSITE` เรียกบอท 13 สาย (`ปริ๊นวางบิลทุกงาน`) และ 19 รายบุคคล (`สร้างใบป่ ะหน้าทุกคน`) | `[data/actions/actions.csv]` |

> **ข้อมูลในเอกสารไม่ระบุ** จำนวนผู้ใช้จริง, จำนวนคนต่อบทบาท, หน่วยงานที่ใช้ และชื่อผู้ใช้ทั้งหมด
> (มีอีเมลปรากฏในเงื่อนไข `Show_If` ของ `ข้อมูลการวางบิล` เช่น `punpama1981@gmail.com`,
> `thawatchai81335@gmail.com` — `[data/columns/all_columns.csv]` — แต่ไม่ได้บอกว่าเป็นของใคร/บทบาทอะไร)

---

## 4. กระบวนการหลักตั้งแต่รับงานจนปิดงาน

ลำดับนี้อ่านจากคีย์การเชื่อมโยงของสูตรและคอลัมน์ ไม่ใช่จากความเดา
(รายละเอียดผังข้อมูลทั้งหมดอยู่ใน `02-data-model.md`)

```
① รับงานประจำวัน
   ตารางงานประจำวัน: Plan Delivery, Invoice No, Shipment No, ชื่อปลายทาง,
   ที่อยู่ปลายทาง_LatLong, จำนวนปลายทาง, ScanStatus
        │
        │  พนักงานบันทึกงานจริง → SCGนครหลวงJWDภูมิภาค (พิกัด/เวลา/ผลตรวจสอบ)
        ▼
② สแกนรับเอกสาร
   ScanDocs: Scan_Invoice, Select_Invoice, Scan_DateTime, Scan_By, Scan_Method (Barcode|Manual)
   → อัปเดต ScanStatus ของตารางงานประจำวัน (process "Update ScanStatus เมื่อสแกน Invoice - 1")
        │
        ▼
③ วางบิล / คิดค่าขนส่ง
   ข้อมูลการวางบิล: ราคา, ราคาตามระยะทาง, ราคาจุดเพิ่ม, ราคาเพิ่ม,
   สถานะการอนุมัติ, รูปถ่ายบิลงาน
   ← ราคาในระบบก่อนส่งสินค้า (ราคาจริงก่อน/หลังส่งสินค้า)
   ← Price_Table (ชื่องาน × ช่วงเรทน้ำมัน × ช่วงระยะทาง)
        │
        ▼
④ ราคา & อนุมัติ
   เรทดีเซล ← ราคาน้ำมันดีเซล (รายวัน) ← PriceOverride (ทับราคาเป็นช่วงวันที่)
   ผู้อนุมัติกดแอกชัน อนุมัติ → ราคาที่อนุมัติแล้ว = IF([สถานะการอนุมัติ]="อนุมัติ", [ราคา], 0)
        │
        ▼
⑤ เบิกส่วนต่าง
   ทำเบิกส่วนต่างScgวังน้อย: ราคาที่สมควรได้, ราคาหลังส่งสินค้า,
   ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม + รูปหลักฐาน 20 จุด (รูปบิลส่งสินค้า/หน้าร้าน/ส่งสินค้า ×20)
   → สรุปเบิกส่วนต่าง (รวมค่าขนส่งส่วนเพิ่ม) → FILTER
        │
        ▼
⑥ เอกสาร
   ปริ๊นใบวางบิล (พิมพ์รายคลัง) · PDFพนักงาน (ใบป่ะหน้ารายคนขับ)
   · สร้างเอกสาร (รวมทุกอย่างเป็นไฟล์ xlsx/PDF)
   ← บอท 30 process ทำงานแทน (ปริ๊นวางบิลทุกงาน = COMPOSITE 13 สาย)
        │
        ▼
⑦ ประกาศ / รับทราบ
   Announcements (หัวข้อประกาศ, เนื้อหาประกาศ) → Acknowledge_Logs
   (วันที่และเวลารับทราบ, ลงชื่อพนักงาน = Signature)
```

**ขั้นตอนข้างเคียงที่อยู่ในระบบด้วย:** คืนสินค้า (`รับงานคืนได้เงิน200`, `ข้อมูลงานRT`,
`Doc_Return`, `Image_Doc_Return`) และเข้าบำรุงรักษารถ (`ข้อมูลการเข้าบำรุงรักษา`)

---

## 5. โครงสร้างข้อมูลบอกอะไรบ้าง (6 ข้อสรุปที่มีหลักฐาน)

### 5.1 ตารางจริง 29 ตาราง = ข้อมูลธุรกิจที่คนกรอก · ตารางบอท 61 ตาราง = หน่วยความจำของบอท

| หลักฐาน | ตารางจริง 29 | ตารางบอท 61 |
|---|---|---|
| `Data Source` | `google` 24 + `google_tables` 1 + ว่าง 4 | `native` 61 |
| `Visible?` | `ALWAYS` 29 | `NEVER` 61 |
| `Are updates allowed?` | `ALL_CHANGES` 29 | `READ_ONLY` 60 + `UPDATES_ONLY` 1 |
| มีวิว/แอกชันผูก | 108 วิว / 214 แอกชัน | **0 รายการ** |

แหล่ง: `[data/tables/index.csv]`, `[data/views/views.csv]`, `[data/actions/actions.csv]`
→ **ผลสำหรับผู้อ่าน: ห้าม “แก้” ตารางบอท — ให้ระบบสร้างใหม่เอง**

### 5.2 แอปเป็น “เก็บหลักฐานรูป” มากกว่าแอปบัญชีทั่วไป

- `Image` 503 คอลัมน์ (22 ตาราง) — `[data/columns/by-type.csv]`
- `LongText` 177 คอลัมน์ — `[data/columns/by-type.csv]`
- ตาราง `ทำเบิกส่วนต่างScgวังน้อย` คอยเดียวมี Image 61 คอลัมน์
  (`รูปบิลส่งสินค้า_01`–`_20`, `รูปหน้าร้าน_บ้าน01`–`20`, `รูปส่งสินค้า01`–`20`) — `[data/columns/all_columns.csv]`
- มีระบบ OCR ในตัว: `OCR_เลขไมล์รถยนต์ก่อนเข้าบำรุงรักษา`, `OCR_รายการเข้าบำรุงรักษา`
  — `[data/columns/all_columns.csv]`

### 5.3 เกือบทุกสูตรอยู่ที่ตารางจริง

345 สูตร → 342 อยู่ที่ตารางจริง, 3 อยู่ที่ตารางบอท (ทั้งหมดที่ `_Per User Settings`)
— `[data/formulas/formulas.csv]`
แปลว่าตารางบอทเป็นแค่ท่อส่งข้อมูล ไม่ใช่ที่คำนวณธุรกิจ

### 5.4 ราคาในแอปคำนวณเองเกือบทั้งหมด

`ราคาตามระยะทาง`, `ราคาจุดเพิ่ม`, `ราคาเพิ่ม`, `ราคาหลังส่งสินค้า`, `ราคาที่อนุมัติแล้ว`,
`เรทดีเซล` เป็น **App formula** ทั้งหมด — `[data/formulas/formulas.csv]`
ค่าที่คนกรอกเองมีเพียง `ราคา` ซึ่งเป็น **Initial value** (แก้ได้) — ดูข้อสังเกตใน `10-known-issues.md`

### 5.5 สิทธิ์แบ่งเป็น 3 ชั้น

ชั้นตาราง (update mode + security filter) → ชั้นคอลัมน์ (Editable_If/Show_If/Valid_If 97 คอลัมน์ที่มี `USERROLE()`)
→ ชั้นวิว/แอกชัน (เงื่อนไข `USERROLE()`) — `[data/formulas/formulas.csv]`, `[data/columns/all_columns.csv]`, `[data/views/views.csv]`, `[data/actions/actions.csv]`

### 5.6 บอทเป็นสายการผลิตเอกสาร 30 สาย

ทุก process มี 1 State Table + 0–3 Step Output; มี action `COMPOSITE` ชื่อ `ปริ๊นวางบิลทุกงาน`
ที่เรียก 13 สายเรียงกัน — `[data/references/processes.csv]`, `[data/actions/actions.csv]`

---

## 6. จะตอบคำถามเรื่องแอปนี้ยังไง (ลำดับการอ่านไฟล์)

| ถาม | เปิดไฟล์ |
|---|---|
| มีตารางอะไรบ้าง | `[data/tables/index.csv]` |
| ตารางนี้มีคอลัมน์อะไร | `[data/tables/real/<slug>.csv]` หรือ `[data/columns/all_columns.csv]` |
| ราคาคำนวณจากอะไร | `[data/formulas/formulas.csv]` + `[data/references/function-usage.csv]` |
| ใครเห็นอะไร | `[data/formulas/formulas.csv]` (Security filter) + `[data/slices/slices.csv]` |
| ผู้ใช้กดอะไรได้ | `[data/actions/actions.csv]` + `[data/views/views.csv]` |
| เรท/ราคาตั้งไว้ที่ไหน | `[data/tables/real/price-table.csv]`, `price-override.csv`, `diesel-price.csv` |
| อะไรที่ “ดูเหมือนพัง” | `docs/10-known-issues.md` |

---

## 7. ต่อไปอ่านอะไรต่อ

- `02-data-model.md` — ผังการไหลของข้อมูลและตารางแกนหลัก
- `03-table-catalogue.md` — ตารางทั้ง 90 ตาราง แยกตามโดเมน
- `09-glossary.md` — ศัพท์ไทย ↔ อังกฤษ (อ่านก่อนถ้าไม่คุ้นคำในแอป)
