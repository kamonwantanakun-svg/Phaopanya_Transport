# สูตรทั้งหมด 345 สูตร

หนึ่งแถว = หนึ่งสูตร · ระดับคอลัมน์ 316 (App formula 190 + Initial value 126) · ระดับตาราง 29 (Expression for update mode 22 + Security filter 7)

| ตาราง | คอลัมน์ | ประเภท | สูตร | ฟังก์ชันที่ใช้ | อ้างอิงคอลัมน์ | หน้า PDF |
|---|---|---|---|---|---|---|
| Acknowledge_Logs | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "ADDS_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 17 |
| Acknowledge_Logs | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 514 |
| Acknowledge_Logs | ID_ประกาศ | Initial value | =MAXROW( "Announcements", "วันที่ประกาศ", NOT(IN([ID_ประกาศ], SELECT(Acknowledge_Logs[ID_ประกาศ], [Email พนักงาน] = USEREMAIL()))) ) | MAXROW; NOT; IN; SELECT; USEREMAIL | ID_ประกาศ; Email พนักงาน | 513 |
| Acknowledge_Logs | ID_รับทราบ | Initial value | UNIQUEID() | UNIQUEID | - | 512 |
| Acknowledge_Logs | ข้อความประกาศ | App formula | =CONCATENATE( " ประกาศ/แจ้งเตือน" "เรื่อง: ", [ID_ประกาศ]. [หัวข้อประกาศ], " ---------------------- ", [ID_ประกาศ].[เนื้อหาประกาศ], " -- -------------… | CONCATENATE | ID_ประกาศ; หัวข้อประกาศ; เนื้อหาประกาศ; Note | 519 |
| Acknowledge_Logs | ชื่อ - นามสกุล | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ชื่อ - นามสกุล") | LOOKUP; USEREMAIL | - | 515 |
| Acknowledge_Logs | ทะเบียนรถ | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ทะเบียนรถ") | LOOKUP; USEREMAIL | - | 516 |
| Acknowledge_Logs | วันที่และเวลารับทราบ | Initial value | =NOW() | NOW | - | 514 |
| Announcements | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 17 |
| Announcements | ID_ประกาศ | Initial value | UNIQUEID() | UNIQUEID | - | 521 |
| Announcements | Related Acknowledge_Logs | App formula | REF_ROWS("Acknowledge_Logs", "ID_ประกาศ") | REF_ROWS | - | 524 |
| Announcements | วันที่ประกาศ | Initial value | =TODAY() | TODAY | - | 521 |
| Doc_Return | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 11 |
| Doc_Return | ID_Doc_Return | Initial value | UNIQUEID() | UNIQUEID | - | 305 |
| Doc_Return | Related Image_Doc_Returns | App formula | REF_ROWS("Image_Doc_Return", "ID_Doc_Return") | REF_ROWS | - | 308 |
| Doc_Return | Related SCGนครหลวงJWDภูมิภาคs | App formula | REF_ROWS("SCGนครหลวงJWDภูมิภาค", "ID_Doc_Return") | REF_ROWS | - | 309 |
| FILTER | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 9 |
| FILTER | ID_เบิกค่าเข้ารับสินค้าคืนคลัง | Initial value | UNIQUEID() | UNIQUEID | - | 262 |
| FILTER | ทำเบิกค่ายกขึ้นชั้น | App formula | =FILTER( รับงานคืนได้เงิน200, AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[STARTDATE], [วันที่เข้ารับ] <= [_THISROW].[ENDDATE], [ส… | FILTER; AND; ISNOTBLANK | วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 269 |
| FILTER | ราคา_ทำเบิกค่ายกขึ้นชั้น | App formula | =SUM(SELECT( รับงานคืนได้เงิน200[ราคา], AND(ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[STARTDATE], [วันที่เข้ารับ] <= [_THISROW].[END… | SUM; SELECT; AND; ISNOTBLANK | ราคา; วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 270 |
| FILTER | ราคา_ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง | App formula | =SUM(SELECT( รับงานคืนได้เงิน200[ราคา], AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW]. [STARTDATE], [วันที่เข้ารับ] <= [_THISROW].[E… | SUM; SELECT; AND; ISNOTBLANK; IN; LIST | ราคา; วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 266 |
| FILTER | ราคา_ได้เพิ่ม50%ของค่าเที่ยว | App formula | e":null,"DecimalDigits":2,"NumericDigits":null,"ShowThousandsSeparator":true,"NumberDisplayMode":"Auto","Valid_If":null,"Error_Message_If_Invalid":nul… | SUM; SELECT; AND; ISNOTBLANK | ราคา; วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 272 |
| FILTER | วันที่ออกเอกสาร | Initial value | =TODAY() | TODAY | - | 264 |
| FILTER | สรุปจำนวนจุดส่งงาน | App formula | =SELECT( ตารางงานประจำวัน[ID_งานประจำวัน], AND( [ลำดับแรก] = TRUE, ISNOTBLANK([Plan Delivery]), [Plan Delivery] >= [_THISROW].[STARTDATE], [Plan Deliv… | SELECT; AND; ISNOTBLANK | ID_งานประจำวัน; ลำดับแรก; Plan Delivery; _THISROW; STARTDATE; ENDDATE | 268 |
| FILTER | ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง | App formula | =FILTER( รับงานคืนได้เงิน200, AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[STARTDATE], [วันที่เข้ารับ] <= [_THISROW].[ENDDATE], IN… | FILTER; AND; ISNOTBLANK; IN; LIST | วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 267 |
| FILTER | ได้เพิ่ม50%ของค่าเที่ยว | App formula | =FILTER( รับงานคืนได้เงิน200, AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[STARTDATE], [วันที่เข้ารับ] <= [_THISROW].[ENDDATE], [ส… | FILTER; AND; ISNOTBLANK | วันที่เข้ารับ; _THISROW; STARTDATE; ENDDATE; สถานะการเข้ารับสินค้า | 271 |
| Image_Doc_Return | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 11 |
| Image_Doc_Return | ID_Image_Doc_Return | Initial value | =UNIQUEID() | UNIQUEID | - | 311 |
| PDFพนักงาน | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 6 |
| PDFพนักงาน | ID_XLSXพนักงาน | Initial value | UNIQUEID() | UNIQUEID | - | 198 |
| PDFพนักงาน | debugenddate | App formula | =[EndDate] | - | EndDate | 204 |
| PDFพนักงาน | debugstartdate | App formula | =[StartDate] | - | StartDate | 204 |
| PDFพนักงาน | ผลลัพท์. | App formula | {\"ReferencedTableName\":\"ข้อมูลการวาง บิล\",\"ReferencedRootTableName\":\"ข้อมูลการวาง บิล\",\"ReferencedType\":\"Text\",\"ReferencedTypeQualifier\"… | FILTER; AND | ชื่อ - นามสกุล; _THISROW; วันที่; StartDate; EndDate | 203 |
| PDFพนักงาน | ราคารวม | App formula | =SUM(SELECT(ข้อมูลการวางบิล[ราคา], AND([ชื่อ - นามสกุล]=[_THISROW].[ชื่อ - นามสกุล],[วันที่] >= [_THISROW].[Startdate], [วันที่] <= [_THISROW].[Enddat… | SUM; SELECT; AND | ราคา; ชื่อ - นามสกุล; _THISROW; วันที่; Startdate; Enddate | 200 |
| PriceOverride | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 15 |
| PriceOverride | ID_PriceOverride | Initial value | =UNIQUEID() | UNIQUEID | - | 490 |
| Price_Table | ID_Price Table | Initial value | UNIQUEID() | UNIQUEID | - | 496 |
| SCGนครหลวงJWDภูมิภาค | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 2 |
| SCGนครหลวงJWDภูมิภาค | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER","ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 2 |
| SCGนครหลวงJWDภูมิภาค | Document_Return | App formula | =[ID_Doc_Return].[ข้อความอธิบาย_Document_Return] | - | ID_Doc_Return; ข้อความอธิบาย_Document_Return | 91 |
| SCGนครหลวงJWDภูมิภาค | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 69 |
| SCGนครหลวงJWDภูมิภาค | ID_Doc_Return | Initial value | =LOOKUP( [_THISROW].[รหัสลูกค้า], "Doc_Return", "รหัสลูกค้า", "ID_Doc_Return" ) | LOOKUP | _THISROW; รหัสลูกค้า | 71 |
| SCGนครหลวงJWDภูมิภาค | ID_SCGนครหลวงJWDภูมิภาค | Initial value | =UNIQUEID() | UNIQUEID | - | 60 |
| SCGนครหลวงJWDภูมิภาค | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 79 |
| SCGนครหลวงJWDภูมิภาค | Image_Document_Return | App formula | =[ID_Doc_Return].[Related Image_Doc_Returns] | - | ID_Doc_Return; Related Image_Doc_Returns | 92 |
| SCGนครหลวงJWDภูมิภาค | LAT | Initial value | =LAT([จุดส่งสินค้าปลายทาง]) | LAT | จุดส่งสินค้าปลายทาง | 70 |
| SCGนครหลวงJWDภูมิภาค | LONG | Initial value | =LONG([จุดส่งสินค้าปลายทาง]) | LONG | จุดส่งสินค้าปลายทาง | 70 |
| SCGนครหลวงJWDภูมิภาค | Related ทำเบิกส่วนต่างScgวังน้อยs | App formula | REF_ROWS("ทำเบิกส่วนต่างScgวังน้อย", "ID_SCGนครหลวงJWDภูมิภาค") | REF_ROWS | - | 94 |
| SCGนครหลวงJWDภูมิภาค | Related สรุปเบิกส่วนต่างs | App formula | REF_ROWS("สรุปเบิกส่วนต่าง", "_ComputedKey_ID_SCGนครหลวงJWDภูมิภาค") | REF_ROWS | - | 93 |
| SCGนครหลวงJWDภูมิภาค | SM_Link_SCG | Initial value | =ANY(SELECT(ตารางงานประจำวัน[ID_งานประจำวัน], AND([Invoice No] = ANY([_THISROW].[Invoice No]), [_ROWNUMBER] = MIN(SELECT(ตารางงานประจำ วัน[_ROWNUMBER]… | ANY; SELECT; AND; MIN | ID_งานประจำวัน; Invoice No; _THISROW; _ROWNUMBER | 78 |
| SCGนครหลวงJWDภูมิภาค | คลังสินค้า เอสซีจี เจดับเบิ้ลยูดี วังน้อย | Initial value | ="14.165716365156051, 100.62529569032515" | - | - | 72 |
| SCGนครหลวงJWDภูมิภาค | ความเร็วการเคลื่อนที่_เมตร_นาที | App formula | =IF( TOTALMINUTES([ระยะเวลาใช้งาน_นาที]) > 0, [ระยะขยับจากจุดเริ่มต้น_เมตร] / TOTALMINUTES([ระยะเวลาใช้งาน_นาที]), 0 ) | IF; TOTALMINUTES | ระยะเวลาใช้งาน_นาที; ระยะขยับจากจุดเริ่มต้น_เมตร | 83 |
| SCGนครหลวงJWDภูมิภาค | จุดส่งสินค้าปลายทาง | Initial value | =HERE() | HERE | - | 62 |
| SCGนครหลวงJWDภูมิภาค | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 63 |
| SCGนครหลวงJWDภูมิภาค | ชื่อปลายทาง | Initial value | =[SM_Link_SCG].[ชื่อปลายทาง] | - | SM_Link_SCG; ชื่อปลายทาง | 68 |
| SCGนครหลวงJWDภูมิภาค | ชื่อเจ้าของสินค้า | Initial value | =[SM_Link_SCG].[ชื่อเจ้าของสินค้า] | - | SM_Link_SCG; ชื่อเจ้าของสินค้า | 67 |
| SCGนครหลวงJWDภูมิภาค | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 63 |
| SCGนครหลวงJWDภูมิภาค | ที่อยู่ปลายทาง | Initial value | =[SM_Link_SCG].[ที่อยู่ปลายทาง] | - | SM_Link_SCG; ที่อยู่ปลายทาง | 73 |
| SCGนครหลวงJWDภูมิภาค | ที่อยู่ปลายทาง_LatLong_Api | App formula | =LOOKUP([_THISROW].[ชื่อปลายทาง],"ตารางงานประจำวัน","ชื่อ ปลายทาง","ที่อยู่ปลายทาง_LatLong") | LOOKUP | _THISROW; ชื่อปลายทาง | 93 |
| SCGนครหลวงJWDภูมิภาค | ผลการตรวจสอบงานส่ง | App formula | AND([ระยะขยับจากจุดเริ่มต้น_เมตร] <= 60, TOTALMINUTES([ระยะเวลาใช้งาน_นาที]) <= 15), "WARNING", OR([ระยะขยับจากจุดเริ่มต้น_เมตร] > 100, [ความเร็วการเค… | AND; TOTALMINUTES; OR | ระยะขยับจากจุดเริ่มต้น_เมตร; ระยะเวลาใช้งาน_นาที; ความเร็วการเคลื่อนที่_เมตร_นาที | 84 |
| SCGนครหลวงJWDภูมิภาค | พิกัดตอนกดบันทึก_เปลี่ยนแล้ว | App formula | =AND( ISNOTBLANK([พิกัดตอนกดบันทึกงาน]), [พิกัดตอนกดบันทึกงาน] <> [_THISROW_BEFORE].[พิกัดตอนกดบันทึกงาน] ) | AND; ISNOTBLANK | พิกัดตอนกดบันทึกงาน; _THISROW_BEFORE | 96 |
| SCGนครหลวงJWDภูมิภาค | พิกัดตอนกดบันทึกงาน | Initial value | =HERE() | HERE | - | 80 |
| SCGนครหลวงJWDภูมิภาค | รหัสลูกค้า | Initial value | =[SM_Link_SCG].[รหัสลูกค้า] | - | SM_Link_SCG; รหัสลูกค้า | 67 |
| SCGนครหลวงJWDภูมิภาค | ระยะขยับจากจุดเริ่มต้น_เมตร | App formula | =DISTANCE( [จุดส่งสินค้าปลายทาง], [พิกัดตอนกดบันทึกงาน] ) * 1000 | DISTANCE | จุดส่งสินค้าปลายทาง; พิกัดตอนกดบันทึกงาน | 82 |
| SCGนครหลวงJWDภูมิภาค | ระยะเวลาใช้งาน_นาที | App formula | =[เวลาบันทึกงานสำเร็จ] - [เวลาที่ส่งสินค้า] | - | เวลาบันทึกงานสำเร็จ; เวลาที่ส่งสินค้า | 82 |
| SCGนครหลวงJWDภูมิภาค | วันที่ส่งสินค้า | Initial value | =TODAY() | TODAY | - | 61 |
| SCGนครหลวงJWDภูมิภาค | เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No | App formula | [ชื่อปลายทาง], " "), ""), IF(ISNOTBLANK([จุดส่งสินค้าปลายทาง]), CONCATENATE("Lat/Lng ", TEXT([จุดส่งสินค้าปลายทาง]), " "), ""), IF(ISNOTBLANK([Invoice… | IF; ISNOTBLANK; CONCATENATE; TEXT; INDEX | ชื่อปลายทาง; จุดส่งสินค้าปลายทาง; Invoice No | 90 |
| SCGนครหลวงJWDภูมิภาค | เดือน | Initial value | =IF( ISBLANK([วันที่ส่งสินค้า]), "", CONCATENATE( YEAR([วันที่ส่งสินค้า]) - IF(YEAR([วันที่ส่งสินค้า]) > 2500, 543, 0), "-", TEXT([วันที่ส่งสินค้า], "… | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่ส่งสินค้า | 76 |
| SCGนครหลวงJWDภูมิภาค | เวลาถ่ายรูปหน้าร้าน_หน้าบ้าน | Initial value | =IF( ISNOTBLANK([รูปหน้าร้าน / บ้าน]), TIMENOW(), [_THIS] ) | IF; ISNOTBLANK; TIMENOW | รูปหน้าร้าน / บ้าน; _THIS | 86 |
| SCGนครหลวงJWDภูมิภาค | เวลาที่ส่งสินค้า | Initial value | =TIMENOW() | TIMENOW | - | 61 |
| SCGนครหลวงJWDภูมิภาค | เวลาบันทึกงานสำเร็จ | Initial value | =TIMENOW() | TIMENOW | - | 81 |
| SCGนครหลวงJWDภูมิภาค | เวลาเริ่มกรอกงาน | Initial value | =TIMENOW() | TIMENOW | - | 80 |
| SCGนครหลวงJWDภูมิภาค | เหตุผิดปกติที่ตรวจพบ | App formula | =UNIQUE( LIST( IF([ระยะขยับจากจุดเริ่มต้น_เมตร] > 60, "มีการเคลื่อนที่จากจุดเริ่มต้น", ""), IF(TOTALMINUTES([ระยะเวลาใช้งาน_นาที]) > 15, "ใช้เวลานานกว… | UNIQUE; LIST; IF; TOTALMINUTES | ระยะขยับจากจุดเริ่มต้น_เมตร; ระยะเวลาใช้งาน_นาที; ความเร็วการเคลื่อนที่_เมตร_นาที | 85 |
| ScanDocs | ID_ScanDocs | Initial value | UNIQUEID() | UNIQUEID | - | 455 |
| ScanDocs | Invoice_No | App formula | =ANY( SELECT(ตารางงานประจำวัน[ID_งานประจำวัน], [Invoice No] = IF(ISNOTBLANK([Scan_Invoice]), [Scan_Invoice], [Select_Invoice]) ) ) | ANY; SELECT; IF; ISNOTBLANK | ID_งานประจำวัน; Invoice No; Scan_Invoice; Select_Invoice | 459 |
| ScanDocs | Scan_By | Initial value | =USEREMAIL() | USEREMAIL | - | 458 |
| ScanDocs | Scan_DateTime | Initial value | =NOW() | NOW | - | 457 |
| ScanDocs | Scan_Method | Initial value | =IF(ISNOTBLANK([Select_Invoice]), "Manual", "Barcode") | IF; ISNOTBLANK | Select_Invoice | 459 |
| ScanDocs | Shipment No | Initial value | =[Invoice_No].[Shipment No] | - | Invoice_No; Shipment No | 462 |
| ScanDocs | จำนวน_ทั้งหมด | App formula | =COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], [Plan Delivery] = [_THISROW].[เลือกวันที่] ) ) ) | COUNT; UNIQUE; SELECT | Invoice No; Plan Delivery; _THISROW; เลือกวันที่ | 464 |
| ScanDocs | จำนวน_รอสแกน | App formula | =[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว] | - | จำนวน_ทั้งหมด; จำนวน_สแกนแล้ว | 466 |
| ScanDocs | จำนวน_สแกนแล้ว | App formula | =COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Plan Delivery] = [_THISROW].[เลือกวันที่], [ScanStatus] = "สแกนรับแล้ว" ) ) ) ) | COUNT; UNIQUE; SELECT; AND | Invoice No; Plan Delivery; _THISROW; เลือกวันที่; ScanStatus | 465 |
| ScanDocs | ชื่อเจ้าของสินค้า | Initial value | =[Invoice_No].[ชื่อเจ้าของสินค้า] | - | Invoice_No; ชื่อเจ้าของสินค้า | 461 |
| ScanDocs | ทะเบียนรถ | Initial value | =[Invoice_No].[ทะเบียนรถ] | - | Invoice_No; ทะเบียนรถ | 461 |
| ScanDocs | วันที่ส่งสินค้า | Initial value | =[Invoice_No].[Plan Delivery] | - | Invoice_No; Plan Delivery | 463 |
| ScanDocs | เลือกวันที่ | App formula | =IF( TOTALHOURS(NOW() - TODAY()) >= 16, TODAY(), TODAY() - 1 ) | IF; TOTALHOURS; NOW; TODAY | - | 467 |
| _Per User Settings | _EMAIL | App formula | USEREMAIL() | USEREMAIL | - | 49 |
| _Per User Settings | _NAME | App formula | USERNAME() | USERNAME | - | 49 |
| _Per User Settings | _THISUSER | Initial value | onlyvalue | - | - | 58 |
| ข้อมูลการวางบิล | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 3 |
| ข้อมูลการวางบิล | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER","ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 3 |
| ข้อมูลการวางบิล | Email ผู้อนุมัติ | App formula | =IF([สถานะการอนุมัติ]="อนุมัติ", USEREMAIL(), [Email ผู้อนุมัติ]) | IF; USEREMAIL | สถานะการอนุมัติ; Email ผู้อนุมัติ | 120 |
| ข้อมูลการวางบิล | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 114 |
| ข้อมูลการวางบิล | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 108 |
| ข้อมูลการวางบิล | ID_วางบิล | Initial value | =UNIQUEID() | UNIQUEID | - | 109 |
| ข้อมูลการวางบิล | SM | App formula | :null,"ShowThousandsSeparator":false,"NumberDisplayMode":"Auto","Valid_If":null,"Error_Message_If_Invalid":null,"Show_If":null,"Required_If":null,"Edi… | LEFT; FIND | พิมอธิบายทุกอย่างที่สำคัญ | 141 |
| ข้อมูลการวางบิล | ข้อความแจ้งเตือน | App formula | =IF([ยืนยันการกรอกข้อมูล] = "ตรวจสอบข้อมูลเรียบร้อย", " ✅ ยืนยัน สำเร็จ กลับไปบันทึกข้อมูลได้", "") | IF | ยืนยันการกรอกข้อมูล | 138 |
| ข้อมูลการวางบิล | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 111 |
| ข้อมูลการวางบิล | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 111 |
| ข้อมูลการวางบิล | ยืนยันการกรอกข้อมูล | Initial value | ="ไม่ได้ตรวจสอบ" | - | - | 126 |
| ข้อมูลการวางบิล | ระยะทางที่วิ่ง (KM) | Initial value | =LOOKUP([_THISROW].[ชื่องาน], "ข้อมูลชื่องานต้นทางปลายทาง", "ชื่องาน", "ระยะทางคงที่") | LOOKUP | _THISROW; ชื่องาน | 116 |
| ข้อมูลการวางบิล | ราคา | Initial value | =IFS( ISBLANK([ชื่องาน]), 0, ISNOTBLANK(LOOKUP([_THISROW].[ชื่องาน], "ข้อมูลชื่องาน ต้นทางปลายทาง", "ชื่องาน", "ราคาคงที่")), LOOKUP([_THISROW]. [ชื่อ… | IFS; ISBLANK; ISNOTBLANK; LOOKUP | ชื่องาน; _THISROW; ราคาจุดเพิ่ม; Shipment No; ราคาตามระยะทาง; ราคาเพิ่ม | 119 |
| ข้อมูลการวางบิล | ราคาก่อนส่งสินค้า | App formula | =LOOKUP([_THISROW].[Shipment No],"ราคาในระบบก่อนส่ง สินค้า","Shipment No","ราคา") | LOOKUP | _THISROW; Shipment No | 140 |
| ข้อมูลการวางบิล | ราคาจุดเพิ่ม | App formula | =IFS( AND([ชื่องาน] = "เบทาโกร+เหมาตู้",[จำนวนจุดรับ / จุดส่ง] >=11), ([จำนวนจุดรับ / จุดส่ง] - 11) * 50, AND([ชื่องาน] = "ไอโรบอท",[จำนวนจุดรับ / จุด… | IFS; AND | ชื่องาน; จำนวนจุดรับ / จุดส่ง; จำนวนร้านที่ยกขึ้นชั้น | 134 |
| ข้อมูลการวางบิล | ราคาตามระยะทาง | App formula | =ANY( SELECT( Price_Table[Price], AND( IN( [_THISROW].[ชื่องาน], SPLIT([ชื่องาน], ",") ), [เรทน้ำมัน_Minimum] <= [_THISROW].[เรทดีเซล], [เรทน้ำมัน_Max… | ANY; SELECT; AND; IN; SPLIT | Price; _THISROW; ชื่องาน; เรทน้ำมัน_Minimum; เรทดีเซล; เรทน้ำมัน_Maximum; ระยะทาง_Minimum; ระยะทางที่วิ่ง (KM); ระยะทาง_Maximum | 135 |
| ข้อมูลการวางบิล | ราคาที่อนุมัติแล้ว | App formula | =IF( [สถานะการอนุมัติ] = "อนุมัติ", [ราคา], 0 ) | IF | สถานะการอนุมัติ; ราคา | 140 |
| ข้อมูลการวางบิล | ราคาหลังส่งสินค้า | App formula | =LOOKUP([_THISROW].[Shipment No],"ราคาในระบบก่อนส่ง สินค้า","Shipment No","ราคาหลังส่งสินค้า") | LOOKUP | _THISROW; Shipment No | 139 |
| ข้อมูลการวางบิล | ราคาหลังส่งเอเธน | App formula | =IF( [ชื่องาน] = "เอเทน", LOOKUP( [SM], "ราคาในระบบก่อนส่ง สินค้า", "Shipment No", "ราคาหลังส่งสินค้า" ), "" ) | IF; LOOKUP | ชื่องาน; SM | 142 |
| ข้อมูลการวางบิล | ราคาเพิ่ม | App formula | =IF([เลือกเพิ่มเติม] = "เพิ่มแรงงาน1คน",500, IF([เลือกเพิ่มเติม] = "จอง รถก่อน14.00+แรงงาน1คน",1200, IF([เลือกเพิ่มเติม] = "งานMeSpace+แพ็คสินค้า",240… | IF | เลือกเพิ่มเติม | 137 |
| ข้อมูลการวางบิล | วันที่ | Initial value | =TODAY() | TODAY | - | 110 |
| ข้อมูลการวางบิล | สถานที่รับงาน (ต้นทาง) | Initial value | =LOOKUP([_THISROW].[ชื่องาน],"ข้อมูลชื่องานต้นทางปลาย ทาง","ชื่องาน","สถานที่รับสินค้า (ต้นทาง)") | LOOKUP | _THISROW; ชื่องาน | 112 |
| ข้อมูลการวางบิล | สถานที่ส่งงาน (ปลายทาง) | Initial value | =LOOKUP([_THISROW].[ชื่องาน],"ข้อมูลชื่องานต้นทางปลาย ทาง","ชื่องาน","สถานที่ส่งสินค้า (ปลายทาง)") | LOOKUP | _THISROW; ชื่องาน | 113 |
| ข้อมูลการวางบิล | สถานะการอนุมัติ | Initial value | ="รอการอนุมัติ” | - | - | 120 |
| ข้อมูลการวางบิล | เดือน | Initial value | =IF( ISBLANK([วันที่]), "", (YEAR([วันที่]) - IF(YEAR([วันที่]) > 2500, 543, 0)) & "-" & TEXT([วันที่], "MM") ) | IF; ISBLANK; YEAR; TEXT | วันที่ | 127 |
| ข้อมูลการวางบิล | เรทดีเซล | App formula | PriceOverride[UsePriceDate], AND( [StartDate] <= [_THISROW]. [วันที่], [EndDate] >= [_THISROW].[วันที่], ISBLANK([JobName]) ) ) ) ), ANY( SELECT( ราคา… | AND; ISBLANK; ANY; SELECT; DATE; CONCATENATE; YEAR; EOMONTH; RIGHT; MONTH | UsePriceDate; StartDate; _THISROW; วันที่; EndDate; JobName; ราคา/หน่วย | 136 |
| ข้อมูลการเข้าบำรุงรักษา | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 3 |
| ข้อมูลการเข้าบำรุงรักษา | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER","ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 3 |
| ข้อมูลการเข้าบำรุงรักษา | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 104 |
| ข้อมูลการเข้าบำรุงรักษา | ID_การเข้าบำรุงรักษา | Initial value | UNIQUEID() | UNIQUEID | - | 97 |
| ข้อมูลการเข้าบำรุงรักษา | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 106 |
| ข้อมูลการเข้าบำรุงรักษา | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 99 |
| ข้อมูลการเข้าบำรุงรักษา | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 99 |
| ข้อมูลการเข้าบำรุงรักษา | วันที่เข้าบำรุงรักษา | Initial value | =NOW() | NOW | - | 98 |
| ข้อมูลการเข้าบำรุงรักษา | เดือน | Initial value | =IF( ISBLANK([วันที่เข้าบำรุงรักษา]), "", CONCATENATE( YEAR([วันที่เข้าบำรุงรักษา]) - IF(YEAR([วันที่เข้าบำรุงรักษา]) > 2500, 543, 0),"-", TEXT([วันที… | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่เข้าบำรุงรักษา | 105 |
| ข้อมูลงานRT | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 8 |
| ข้อมูลงานRT | ID_RT | Initial value | =UNIQUEID() | UNIQUEID | - | 253 |
| ข้อมูลงานRT | Related แจ้งปั ญหาระหว่างวันs | App formula | =REF_ROWS("แจ้งปั ญหาระหว่างวัน", "RT_Link") | REF_ROWS | - | 260 |
| ข้อมูลงานRT | เดือน | App formula | =IF( ISBLANK([วันที่เข้ารับ]), "", CONCATENATE( YEAR([วันที่เข้ารับ]) - IF(YEAR([วันที่เข้ารับ]) > 2500, 543, 0), "-", TEXT([วันที่เข้ารับ],"MM") ) ) | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่เข้ารับ | 259 |
| ข้อมูลงานRW | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 12 |
| ข้อมูลงานRW | ID_ข้อมูลงานRW | Initial value | UNIQUEID() | UNIQUEID | - | 423 |
| ข้อมูลชื่องานต้นทางปลายทาง | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 10 |
| ข้อมูลชื่องานต้นทางปลายทาง | ID_ชื่องาน | Initial value | =UNIQUEID() | UNIQUEID | - | 290 |
| ข้อมูลชื่องานต้นทางปลายทาง | Row ID | Initial value | UNIQUEID("PackedUUID") | UNIQUEID | - | 289 |
| ข้อมูลพนักงาน | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 9 |
| ข้อมูลพนักงาน | ID_พนักงาน | Initial value | =UNIQUEID() | UNIQUEID | - | 275 |
| ข้อมูลพนักงาน | Related SCGนครหลวงJWDภูมิภาคs | App formula | REF_ROWS("SCGนครหลวงJWDภูมิภาค", "ID_พนักงาน") | REF_ROWS | - | 281 |
| ข้อมูลพนักงาน | Related ข้อมูลการวางบิลs | App formula | REF_ROWS("ข้อมูลการวางบิล", "ID_พนักงาน") | REF_ROWS | - | 285 |
| ข้อมูลพนักงาน | Related ข้อมูลการเข้าบำรุงรักษาs | App formula | REF_ROWS("ข้อมูลการเข้าบำรุงรักษา", "ID_พนักงาน") | REF_ROWS | - | 284 |
| ข้อมูลพนักงาน | Related ทำเบิกส่วนต่างScgวังน้อยs | App formula | REF_ROWS("ทำเบิกส่วนต่างScgวังน้อย", "ID_พนักงาน") | REF_ROWS | - | 286 |
| ข้อมูลพนักงาน | Related รับงานคืนได้เงิน200s | App formula | REF_ROWS("รับงานคืนได้เงิน200", "ID_พนักงาน") | REF_ROWS | - | 283 |
| ข้อมูลพนักงาน | Related ส่งงานที่ยังไม่มีข้อมูลในระบบs | App formula | REF_ROWS("ส่งงานที่ยังไม่มีข้อมูลในระบบ", "ID_พนักงาน") | REF_ROWS | - | 287 |
| ข้อมูลพนักงาน | Related แจ้งปั ญหาระหว่างวันs | App formula | REF_ROWS("แจ้งปั ญหาระหว่างวัน", "ID_พนักงาน") | REF_ROWS | - | 282 |
| ข้อมูลพนักงาน | Row ID | Initial value | UNIQUEID("PackedUUID") | UNIQUEID | - | 274 |
| ตารางงานประจำวัน | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 4 |
| ตารางงานประจำวัน | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 4 |
| ตารางงานประจำวัน | ID_งานประจำวัน | Initial value | =UNIQUEID() | UNIQUEID | - | 144 |
| ตารางงานประจำวัน | Related SCGนครหลวงJWDภูมิภาคs | App formula | =REF_ROWS("SCGนครหลวงJWDภูมิภาค", "SM_Link_SCG") | REF_ROWS | - | 169 |
| ตารางงานประจำวัน | Related ScanDocs | App formula | REF_ROWS("ScanDocs", "Invoice_No") | REF_ROWS | - | 171 |
| ตารางงานประจำวัน | Related แจ้งปั ญหาระหว่างวันs | App formula | REF_ROWS("แจ้งปั ญหาระหว่างวัน", "SM_Link") | REF_ROWS | - | 170 |
| ตารางงานประจำวัน | จำนวนจุดที่ส่งจริง | App formula | =COUNT( SELECT( SCGนครหลวงJWDภูมิภาค[Shipment No], [Shipment No] = [_THISROW].[Shipment No]) ) | COUNT; SELECT | Shipment No; _THISROW | 167 |
| ตารางงานประจำวัน | จำนวนปลายทาง | App formula | =COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[ชื่อปลายทาง], [Shipment No] = [_THISROW].[Shipment No] ) ) ) | COUNT; UNIQUE; SELECT | ชื่อปลายทาง; Shipment No; _THISROW | 166 |
| ตารางงานประจำวัน | ลำดับแรก | App formula | =[_ROWNUMBER] = MIN( SELECT( ตารางงานประจำ วัน[_ROWNUMBER], [Shipment No] = [_THISROW].[Shipment No], ) ) | MIN; SELECT | _ROWNUMBER; Shipment No; _THISROW | 166 |
| ตารางงานประจำวัน | เดือน | App formula | =IF( ISBLANK([Plan Delivery]), "", CONCATENATE( YEAR([Plan Delivery]) - IF(YEAR([Plan Delivery]) > 2500, 543, 0), "-", TEXT([Plan Delivery], "MM") ) ) | IF; ISBLANK; CONCATENATE; YEAR; TEXT | Plan Delivery | 168 |
| ทำเบิกส่วนต่างScgวังน้อย | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 12 |
| ทำเบิกส่วนต่างScgวังน้อย | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "ADDS_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 12 |
| ทำเบิกส่วนต่างScgวังน้อย | 01เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_01],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_01 | 357 |
| ทำเบิกส่วนต่างScgวังน้อย | 02เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_02],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_02 | 360 |
| ทำเบิกส่วนต่างScgวังน้อย | 03เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_03],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_03 | 363 |
| ทำเบิกส่วนต่างScgวังน้อย | 04เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_04],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_04 | 366 |
| ทำเบิกส่วนต่างScgวังน้อย | 05เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_05],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_05 | 369 |
| ทำเบิกส่วนต่างScgวังน้อย | 06เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_06],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_06 | 372 |
| ทำเบิกส่วนต่างScgวังน้อย | 07เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_07],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_07 | 375 |
| ทำเบิกส่วนต่างScgวังน้อย | 08เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_08],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_08 | 378 |
| ทำเบิกส่วนต่างScgวังน้อย | 09เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_09],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_09 | 381 |
| ทำเบิกส่วนต่างScgวังน้อย | 10เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_10],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_10 | 384 |
| ทำเบิกส่วนต่างScgวังน้อย | 11เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_11],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_11 | 387 |
| ทำเบิกส่วนต่างScgวังน้อย | 12เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_12],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_12 | 390 |
| ทำเบิกส่วนต่างScgวังน้อย | 13เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_13],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_13 | 393 |
| ทำเบิกส่วนต่างScgวังน้อย | 14เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_14],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_14 | 396 |
| ทำเบิกส่วนต่างScgวังน้อย | 15เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_15],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_15 | 399 |
| ทำเบิกส่วนต่างScgวังน้อย | 16เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_16],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_16 | 402 |
| ทำเบิกส่วนต่างScgวังน้อย | 17เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_17],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_17 | 405 |
| ทำเบิกส่วนต่างScgวังน้อย | 18เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_18],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_18 | 408 |
| ทำเบิกส่วนต่างScgวังน้อย | 19เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_19],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_19 | 411 |
| ทำเบิกส่วนต่างScgวังน้อย | 20เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_20],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","เจ้าของสินค้า//ชื่อปลายทาง//Lat_Long//Inv No") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_20 | 414 |
| ทำเบิกส่วนต่างScgวังน้อย | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 321 |
| ทำเบิกส่วนต่างScgวังน้อย | ID_SCGนครหลวงJWDภูมิภาค | Initial value | "SCGนครหลวงJWDภูมิภาค", "Shipment No", "ID_SCGนครหลวงJWDภูมิภาค" ) | - | - | 315 |
| ทำเบิกส่วนต่างScgวังน้อย | ID_ทำเบิกส่วนต่างScgวังน้อย | Initial value | UNIQUEID() | UNIQUEID | - | 314 |
| ทำเบิกส่วนต่างScgวังน้อย | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 349 |
| ทำเบิกส่วนต่างScgวังน้อย | QR code เส้นทางรวม | App formula | =CONCATENATE( "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=",ENCODEURL(CONCATENATE([แสดงแผนที่_GoogleMapsRoutesAPI] ))) | CONCATENATE; ENCODEURL | แสดงแผนที่_GoogleMapsRoutesAPI | 419 |
| ทำเบิกส่วนต่างScgวังน้อย | ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม | App formula | =IF( AND( ISNOTBLANK([ราคาที่สมควรได้]), ISNOTBLANK([ราคาหลังส่งสินค้า]) ), [ราคาที่สมควรได้] - [ราคาหลังส่งสินค้า], 0 ) | IF; AND; ISNOTBLANK | ราคาที่สมควรได้; ราคาหลังส่งสินค้า | 418 |
| ทำเบิกส่วนต่างScgวังน้อย | จำนวนจุดส่งก่อนเริ่มงาน | Initial value | =COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[ชื่อปลายทาง], [Shipment No] = [_THISROW].[Shipment No] ) ) ) | COUNT; UNIQUE; SELECT | ชื่อปลายทาง; Shipment No; _THISROW | 343 |
| ทำเบิกส่วนต่างScgวังน้อย | จำนวนจุดส่งงานจริง | Initial value | =COUNT( SELECT( SCGนครหลวงJWDภูมิภาค[Shipment No], [Shipment No] = [_THISROW].[Shipment No]) ) | COUNT; SELECT | Shipment No; _THISROW | 343 |
| ทำเบิกส่วนต่างScgวังน้อย | จุดส่งงานลำดับสุดท้าย | App formula | =IF( ISNOTBLANK([20เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No]), [20เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No], IF( ISNOTBLANK([19เจ้… | IF; ISNOTBLANK | 20เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 19เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 18เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 17เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 16เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 15เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 14เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 13เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 12เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 11เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 10เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 09เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 08เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 07เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 06เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 05เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 04เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 03เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 02เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No; 01เจ้าของสินค้า // ชื่อปลายทาง // Lat_Long // Inv No | 420 |
| ทำเบิกส่วนต่างScgวังน้อย | ชื่อ - นามสกุล | Initial value | =[ID_SCGนครหลวงJWDภูมิภาค].[ชื่อ - นามสกุล] | - | ID_SCGนครหลวงJWDภูมิภาค; ชื่อ - นามสกุล | 317 |
| ทำเบิกส่วนต่างScgวังน้อย | ชื่องาน | Initial value | ส่งสินค้า", "Shipment No", "Truck Type"), {"นครหลวง", "ภูมิภาค", "04JB_นครหลวง_ภูมิภาค", "Idem_04ID","น้ำมะปี๊ด(ปั้ม บางจาก)FarmZaa"} ), LOOKUP([_THIS… | LOOKUP | _THISROW; Shipment No | 342 |
| ทำเบิกส่วนต่างScgวังน้อย | ชื่อปลายทาง_INV_จุดสุดท้าย | App formula | =CONCATENATE( ปลายทาง , MID( [จุดส่งงานลำดับสุดท้าย],FIND("ปลายทาง ", [จุดส่งงานลำดับสุดท้าย]) + LEN("ปลายทาง "),FIND("Lat/Lng", [จุดส่งงานลำดับสุดท้า… | CONCATENATE; MID; FIND; LEN; TRIM | จุดส่งงานลำดับสุดท้าย | 422 |
| ทำเบิกส่วนต่างScgวังน้อย | ตรวจสอบข้อมูล | App formula | =IF( AND( ISNOTBLANK([ชื่องาน]), COUNT( SELECT(SCGนครหลวงJWDภูมิภาค[Shipment No], [Shipment No] =[_THISROW].[Shipment No] ) ) > 0, COUNT( SELECT(SCGนค… | IF; AND; ISNOTBLANK; COUNT; SELECT | ชื่องาน; Shipment No; _THISROW; LAT; LONG; จุดส่งสินค้าปลายทาง; ระยะทางจากคลัง_Km; ผลการตรวจสอบงานส่ง | 344 |
| ทำเบิกส่วนต่างScgวังน้อย | ต้นทาง | Initial value | ="14.164671, 100.625358" | - | - | 318 |
| ทำเบิกส่วนต่างScgวังน้อย | ทะเบียนรถ | App formula | =[ID_SCGนครหลวงJWDภูมิภาค].[ทะเบียนรถ] | - | ID_SCGนครหลวงJWDภูมิภาค; ทะเบียนรถ | 356 |
| ทำเบิกส่วนต่างScgวังน้อย | ระยะทางในระบบก่อนส่งสินค้า | Initial value | =LOOKUP([_THISROW].[Shipment No],"ราคาในระบบก่อนส่ง สินค้า","Shipment No","ระยะทาง (km)") | LOOKUP | _THISROW; Shipment No | 346 |
| ทำเบิกส่วนต่างScgวังน้อย | ราคาจุดเพิ่ม | App formula | 50, IF( AND( IN( [ชื่องาน], {"นครหลวง", "ภูมิภาค", "04JB_นครหลวง_ภูมิภาค"} ), ISNOTBLANK([จำนวนจุดส่งงานจริง]), [จำนวนจุดส่งงานจริง] > 10 ), ([จำนวนจุ… | IF; AND; IN; ISNOTBLANK | ชื่องาน; จำนวนจุดส่งงานจริง | 355 |
| ทำเบิกส่วนต่างScgวังน้อย | ราคาตามระยะทาง | App formula | น้ำมัน_Minimum] <= [_THISROW].[เรท น้ำมันดีเซล], [เรท น้ำมัน_Maximum] >= [_THISROW].[เรท น้ำมันดีเซล], [ระยะ ทาง_Minimum] <= NUMBER([_THISROW].[ระยะ ท… | NUMBER; ANY; SELECT; AND; IN; SPLIT | _THISROW; เรท น้ำมันดีเซล; เรท น้ำมัน_Maximum; ระยะ ทาง_Minimum; ระยะ ทาง_GoogleMapAPI_Km; ระยะทาง_Maximum; ระยะทาง_GoogleMapAPI_Km; Price; ชื่องาน; เรทน้ำมัน_Minimum; เรทน้ำมัน_Maximum; เรท น้ำมัน ดีเซล; ระยะทาง_Minimum | 354 |
| ทำเบิกส่วนต่างScgวังน้อย | ราคาที่สมควรได้ | App formula | =[ราคาตามระยะทาง]+[ราคาจุดเพิ่ม] | - | ราคาตามระยะทาง; ราคาจุดเพิ่ม | 417 |
| ทำเบิกส่วนต่างScgวังน้อย | ราคาหลังส่งสินค้า | App formula | =IF( ISNOTBLANK( LOOKUP([_THISROW].[Shipment No], "ราคา ในระบบก่อนส่งสินค้า", "Shipment No", "ราคาหลังส่งสินค้า") ), LOOKUP([_THISROW].[Shipment No],… | IF; ISNOTBLANK; LOOKUP | _THISROW; Shipment No | 418 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_01 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_01],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_01 | 358 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_02 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_02],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_02 | 361 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_03 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_03],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_03 | 364 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_04 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_04],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_04 | 367 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_05 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_05],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_05 | 370 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_06 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_06],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_06 | 373 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_07 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_07],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_07 | 376 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_08 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_08],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_08 | 379 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_09 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_09],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_09 | 382 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_10 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_10],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_10 | 385 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_11 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_11],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_11 | 388 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_12 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_12],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_12 | 391 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_13 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_13],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_13 | 394 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_14 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_14],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_14 | 397 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_15 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_15],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_15 | 400 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_16 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_16],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_16 | 403 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_17 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_17],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_17 | 406 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_18 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_18],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_18 | 409 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_19 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_19],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_19 | 412 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปบิลส่งสินค้า_20 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_20],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปถ่ายบิลส่งสินค้า") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_20 | 415 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า01 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_01],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_01 | 359 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า02 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_02],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_02 | 362 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า03 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_03],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_03 | 365 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า04 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_04],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_04 | 368 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า05 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_05],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_05 | 371 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า06 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_06],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_06 | 374 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า07 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_07],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_07 | 377 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า08 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_08],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_08 | 380 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า09 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_09],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_09 | 383 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า10 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_10],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_10 | 386 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า11 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_11],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_11 | 389 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า12 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_12],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_12 | 392 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า13 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_13],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_13 | 395 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า14 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_14],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_14 | 398 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า15 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_15],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_15 | 401 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า16 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_16],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_16 | 404 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า17 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_17],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_17 | 407 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า18 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_18],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_18 | 410 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า19 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_19],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_19 | 413 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปส่งสินค้า20 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_20],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปสินค้าตอนส่ง") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_20 | 416 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน01 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_01],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_01 | 358 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน02 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_02],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_02 | 361 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน03 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_03],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_03 | 364 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน04 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_04],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_04 | 367 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน05 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_05],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_05 | 370 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน06 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_06],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_06 | 373 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน07 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_07],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_07 | 376 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน08 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_08],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_08 | 379 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน09 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_09],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_09 | 382 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน10 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_10],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_10 | 385 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน11 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_11],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_11 | 388 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน12 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_12],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_12 | 391 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน13 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_13],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_13 | 394 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน14 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_14],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_14 | 397 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน15 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_15],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_15 | 400 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน16 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_16],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_16 | 403 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน17 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_17],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_17 | 406 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน18 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_18],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_18 | 409 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน19 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_19],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_19 | 412 |
| ทำเบิกส่วนต่างScgวังน้อย | รูปหน้าร้าน_บ้าน20 | App formula | =LOOKUP([_THISROW].[Lat/Long_ปลายทาง_20],"SCGนครหลวงJWDภูมิภาค","จุดส่งสินค้าปลายทาง","รูปหน้าร้าน / บ้าน") | LOOKUP | _THISROW; Lat/Long_ปลายทาง_20 | 415 |
| ทำเบิกส่วนต่างScgวังน้อย | วันที่ส่งสินค้า | Initial value | =[ID_SCGนครหลวงJWDภูมิภาค].[วันที่ส่งสินค้า] | - | ID_SCGนครหลวงJWDภูมิภาค; วันที่ส่งสินค้า | 317 |
| ทำเบิกส่วนต่างScgวังน้อย | สถานะ | Initial value | ="รอตรวจสอบ" | - | - | 347 |
| ทำเบิกส่วนต่างScgวังน้อย | เดือน | Initial value | =IF( ISBLANK([วันที่ส่งสินค้า]), "", CONCATENATE( YEAR([วันที่ส่งสินค้า]) - IF(YEAR([วันที่ส่งสินค้า]) > 2500, 543, 0), "-", TEXT([วันที่ส่งสินค้า], "… | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่ส่งสินค้า | 348 |
| ทำเบิกส่วนต่างScgวังน้อย | เรท น้ำมันดีเซล | App formula | =IF( ISBLANK([_THISROW].[วันที่ส่งสินค้า]), "", IF( ISNOTBLANK(ANY( SELECT( PriceOverride[UsePriceDate], AND( [StartDate]<= [_THISROW].[วันที่ส่งสินค้… | IF; ISBLANK; ISNOTBLANK; ANY; SELECT; AND; DATE; CONCATENATE; YEAR; EOMONTH; RIGHT; MONTH | _THISROW; วันที่ส่งสินค้า; UsePriceDate; StartDate; EndDate; JobName; ชื่องาน; ราคา/หน่วย; วันที่ | 353 |
| ปริ๊นใบวางบิล | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 6 |
| ปริ๊นใบวางบิล | ID_ปริ๊นใบวางบิล | Initial value | UNIQUEID() | UNIQUEID | - | 190 |
| ปริ๊นใบวางบิล | ผลลัพท์ | App formula | =FILTER("ข้อมูลการวางบิล",(AND([ชื่องาน]=[_THISROW].[ชื่องาน], [วันที่]>=[_THISROW].[StartDate],[วันที่]<=[_THISROW]. [EndDate]))) | FILTER; AND | ชื่องาน; _THISROW; วันที่; StartDate; EndDate | 196 |
| ปริ๊นใบวางบิล | ราคารวม | App formula | =SUM(SELECT(ข้อมูลการวางบิล[ราคา], AND([ชื่องาน]= [_THISROW].[ชื่องาน],[วันที่] >= [_THISROW].[Startdate], [วันที่] <= [_THISROW].[Enddate]))) | SUM; SELECT; AND | ราคา; ชื่องาน; _THISROW; วันที่; Startdate; Enddate | 192 |
| ปริ๊นใบวางบิล | วันที่ออกเอกสาร | Initial value | =TODAY() | TODAY | - | 195 |
| รับงานคืนได้เงิน200 | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 8 |
| รับงานคืนได้เงิน200 | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 8 |
| รับงานคืนได้เงิน200 | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 245 |
| รับงานคืนได้เงิน200 | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 249 |
| รับงานคืนได้เงิน200 | ID_รับงานคืนได้เงิน200 | Initial value | =UNIQUEID() | UNIQUEID | - | 229 |
| รับงานคืนได้เงิน200 | LINK_IMAGE | App formula | =TEXT( LIST( IF(ISNOTBLANK([รูปสินค้า]), CONCATENATE( "https://www.appsheet.com/template/gettablefileurl?", "appName=", ENCODEURL("เผ่าปั ญญาทรานสปอร์… | TEXT; LIST; IF; ISNOTBLANK; CONCATENATE; ENCODEURL | รูปสินค้า; รูปบิลรับคืน; รูปจุดที่ส่งงาน | 250 |
| รับงานคืนได้เงิน200 | Lat / Long | App formula | =HERE() | HERE | - | 244 |
| รับงานคืนได้เงิน200 | Shipment (รับคืน) | App formula | =LOOKUP([_THISROW].[Shipment (หลัก)],"ข้อมูล งานRT","Shipment (หลัก)","Shipment (รับคืน)") | LOOKUP | _THISROW; Shipment (หลัก) | 234 |
| รับงานคืนได้เงิน200 | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 232 |
| รับงานคืนได้เงิน200 | ชื่อลูกค้าที่เข้ารับ | App formula | =IF( IN([สถานะการเข้ารับสินค้า],{"เบิกค่าขนส่งตามระยะทาง","ทำ เบิกค่ายกขึ้นชั้น"}), LOOKUP(ANY([_THISROW].[Invoice No]), "ตารางงานประจำวัน", "Invoice… | IF; IN; LOOKUP; ANY | สถานะการเข้ารับสินค้า; _THISROW; Invoice No; เลขที่เอกสารรับคืน | 240 |
| รับงานคืนได้เงิน200 | ชื่อเจ้าของสินค้า | App formula | =IF( IN([สถานะการเข้ารับสินค้า],{"เบิกค่าขนส่งตามระยะทาง","ทำ เบิกค่ายกขึ้นชั้น"}), LOOKUP(ANY([_THISROW].[Invoice No]), "ตารางงานประจำวัน", "Invoice… | IF; IN; LOOKUP; ANY | สถานะการเข้ารับสินค้า; _THISROW; Invoice No; รหัสลูกค้า | 238 |
| รับงานคืนได้เงิน200 | ตรวจสอบก่อนบันทึกข้อมูล | App formula | =IF( IN([สถานะการเข้ารับสินค้า],{"เบิกค่าขนส่งตามระยะทาง","ทำ เบิกค่ายกขึ้นชั้น"}), 1, IF( COUNT( SELECT( ข้อมูลงานRT[เลขที่ เอกสารรับคืน], AND( [วันท… | IF; IN; COUNT; SELECT; AND | สถานะการเข้ารับสินค้า; เลขที่ เอกสารรับคืน; วันที่เข้ารับ; _THISROW; ชื่อ - นามสกุล; Shipment (หลัก); Shipment (รับคืน); เลขที่เอกสารรับคืน | 248 |
| รับงานคืนได้เงิน200 | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 232 |
| รับงานคืนได้เงิน200 | รหัสลูกค้า | App formula | เบิกค่ายกขึ้นชั้น"}), LOOKUP(ANY([_THISROW].[Invoice No]), "ตารางงานประจำวัน", "Invoice No", "รหัสลูกค้า"), LOOKUP([_THISROW].[เลขที่เอกสารรับคืน], "ข… | LOOKUP; ANY | _THISROW; Invoice No; เลขที่เอกสารรับคืน | 239 |
| รับงานคืนได้เงิน200 | ราคา | Initial value | =IFS( OR( [สถานะการเข้ารับสินค้า] = "(ได้เพิ่ม200) ไม่มีในจุด ที่ส่ง งานวันนี้", [สถานะการเข้ารับสินค้า] = "(ได้เพิ่ม200) ไม่มีสินค้าคืน หรือ ร้านปิ ด… | IFS; OR; LOOKUP | สถานะการเข้ารับสินค้า; Shipment (หลัก) | 245 |
| รับงานคืนได้เงิน200 | รายชื่อจุดส่งในตารางงานประจำวัน | App formula | =SUBSTITUTE( ANY( SELECT( ตารางงานประจำวัน[รายชื่อปลายทาง_System], [Shipment No] = IF(ISNOTBLANK([_THISROW].[Shipment (หลัก)]), [_THISROW].[Shipment (… | SUBSTITUTE; ANY; SELECT; IF; ISNOTBLANK | รายชื่อปลายทาง_System; Shipment No; _THISROW; Shipment (หลัก) | 252 |
| รับงานคืนได้เงิน200 | วันที่เข้ารับ | Initial value | =TODAY() | TODAY | - | 231 |
| รับงานคืนได้เงิน200 | เดือน | Initial value | =IF( ISBLANK([วันที่เข้ารับ]), "", CONCATENATE( YEAR([วันที่เข้ารับ]) - IF(YEAR([วันที่เข้ารับ]) > 2500, 543, 0), "-", TEXT([วันที่เข้ารับ],"MM") ) ) | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่เข้ารับ | 249 |
| ราคาน้ำมันดีเซล | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 4 |
| ราคาน้ำมันดีเซล | ID_น้ำมันดีเซล | Initial value | UNIQUEID() | UNIQUEID | - | 173 |
| ราคาในระบบก่อนส่งสินค้า | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 5 |
| ราคาในระบบก่อนส่งสินค้า | เดือน | App formula | =IF( ISBLANK([วันที่ส่งสินค้า]), "", CONCATENATE( YEAR([วันที่ส่งสินค้า]) - IF(YEAR([วันที่ส่งสินค้า]) > 2500, 543, 0), "-", TEXT([วันที่ส่งสินค้า], "… | IF; ISBLANK; CONCATENATE; YEAR; TEXT | วันที่ส่งสินค้า | 185 |
| สรุป_Shipment | จำนวน_รอสแกน | App formula | =[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว] | - | จำนวน_ทั้งหมด; จำนวน_สแกนแล้ว | 488 |
| สรุป_Shipment | จำนวน_สแกนแล้ว | App formula | =COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStatus] = "สแกนรับแล้ว" ) ) ) ) | COUNT; UNIQUE; SELECT; AND | Invoice No; Shipment No; _THISROW; ShipmentNo; ScanStatus | 487 |
| สรุป_Shipment | รายการ_ทั้งหมด | App formula | =FILTER( "ตารางงานประจำวัน", [Shipment No] = [_THISROW]. [ShipmentNo] ) | FILTER | Shipment No; _THISROW; ShipmentNo | 484 |
| สรุป_Shipment | รายการ_รอสแกน | App formula | =FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], OR( ISBLANK([ScanStatus]), [ScanStatus] <> "สแกนรับแล้ว" ) ) ) | FILTER; AND; OR; ISBLANK | Shipment No; _THISROW; ShipmentNo; ScanStatus | 486 |
| สรุป_Shipment | รายการ_สแกนแล้ว | App formula | =FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStatus] = "สแกนรับแล้ว" ) ) | FILTER; AND | Shipment No; _THISROW; ShipmentNo; ScanStatus | 485 |
| สรุป_Shipment | สรุปยอด | App formula | =" "&[จำนวน_ทั้งหมด] &" "&[จำนวน_สแกนแล้ว] &" "&[จำนวน_รอสแกน] &IF([จำนวน_E-POD_ทั้งหมด]>0," "&[จำนวน_E-POD_ทั้งหมด],"") | IF | จำนวน_ทั้งหมด; จำนวน_สแกนแล้ว; จำนวน_รอสแกน; จำนวน_E-POD_ทั้งหมด | 489 |
| สรุป_เจ้าของสินค้า | LastUpdated | Initial value | =NOW() | NOW | - | 472 |
| สรุป_เจ้าของสินค้า | SummaryKey | Initial value | =UNIQUEID() | UNIQUEID | - | 469 |
| สรุป_เจ้าของสินค้า | จำนวน_รอสแกน | App formula | =[จำนวน_ทั้งหมด]-[จำนวน_สแกนแล้ว] | - | จำนวน_ทั้งหมด; จำนวน_สแกนแล้ว | 477 |
| สรุป_เจ้าของสินค้า | จำนวน_สแกนแล้ว | App formula | AND( [ชื่อเจ้าของสินค้า] = [_THISROW].[SoldToName], [Plan Delivery] = [_THISROW].[PlanDelivery], [ScanStatus] = "สแกนรับ แล้ว" ) ) ) ) | AND | ชื่อเจ้าของสินค้า; _THISROW; SoldToName; Plan Delivery; PlanDelivery; ScanStatus | 476 |
| สรุป_เจ้าของสินค้า | รายการ_ทั้งหมด | App formula | =FILTER( "ตารางงานประจำวัน", AND( [ชื่อเจ้าของสินค้า] = [_THISROW].[SoldToName], [Plan Delivery] = [_THISROW]. [PlanDelivery] ) ) | FILTER; AND | ชื่อเจ้าของสินค้า; _THISROW; SoldToName; Plan Delivery; PlanDelivery | 473 |
| สรุป_เจ้าของสินค้า | รายการ_รอสแกน | App formula | =FILTER( "ตารางงานประจำวัน", AND( [ชื่อเจ้าของสินค้า] = [_THISROW].[SoldToName], [Plan Delivery] = [_THISROW]. [PlanDelivery], OR( ISBLANK([ScanStatus… | FILTER; AND; OR; ISBLANK | ชื่อเจ้าของสินค้า; _THISROW; SoldToName; Plan Delivery; PlanDelivery; ScanStatus | 475 |
| สรุป_เจ้าของสินค้า | รายการ_สแกนแล้ว | App formula | =FILTER( "ตารางงานประจำวัน", AND( [ชื่อเจ้าของสินค้า] = [_THISROW].[SoldToName], [Plan Delivery] = [_THISROW]. [PlanDelivery], [ScanStatus] = "สแกนรับ… | FILTER; AND | ชื่อเจ้าของสินค้า; _THISROW; SoldToName; Plan Delivery; PlanDelivery; ScanStatus | 474 |
| สรุป_เจ้าของสินค้า | สรุปยอด | App formula | =IF( [จำนวน_E-POD_ทั้งหมด] > 0, " 𝐄 ─ ✅🟰𝐃 " & [จำนวน_E-POD_ทั้งหมด], " 📋🟰" & [จำนวน_ทั้งหมด] & "" &[จำนวน_สแกนแล้ว] & " ⏳🟰" & [จำนวน_รอสแกน] ) | IF | จำนวน_E-POD_ทั้งหมด; จำนวน_ทั้งหมด; จำนวน_สแกนแล้ว; จำนวน_รอสแกน | 478 |
| สรุปเบิกส่วนต่าง | ID_สรุปเบิกส่วนต่าง | Initial value | UNIQUEID() | UNIQUEID | - | 296 |
| สรุปเบิกส่วนต่าง | ราคารวม_ทำเบิกส่วนต่างScgวังน้อย | App formula | =SUM(SELECT( ทำเบิกส่วนต่างScgวังน้อย[ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม], AND(ISNOTBLANK([วันที่ส่งสินค้า]), [วันที่ส่งสินค้า] >=[_THISROW].[วันที่เริ่มต… | SUM; SELECT; AND; ISNOTBLANK | ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม; วันที่ส่งสินค้า; _THISROW; วันที่เริ่มต้น; วันที่สิ้นสุด; สถานะ | 303 |
| สรุปเบิกส่วนต่าง | สรุป_ทำเบิกส่วนต่างScgวังน้อย | App formula | =FILTER( ทำเบิกส่วนต่างSCGวังน้อย, AND(ISNOTBLANK([วันที่ส่งสินค้า]), [วันที่ส่งสินค้า] >= [_THISROW].[วันที่เริ่มต้น], [วันที่ส่งสินค้า]<= [_THISROW]… | FILTER; AND; ISNOTBLANK | วันที่ส่งสินค้า; _THISROW; วันที่เริ่มต้น; วันที่สิ้นสุด; สถานะ | 302 |
| สร้างเอกสาร | ID_สร้างเอกสาร | Initial value | UNIQUEID() | UNIQUEID | - | 434 |
| สร้างเอกสาร | ทำเบิกค่ายกขึ้นชั้น | App formula | [วันที่เข้ารับ] >= [_THISROW].[StartDate], [วันที่เข้ารับ] <= [_THISROW].[EndDate], [สถานะการเข้ารับสินค้า]="ทำเบิกค่ายกขึ้น ชั้น")) | - | วันที่เข้ารับ; _THISROW; StartDate; EndDate; สถานะการเข้ารับสินค้า | 449 |
| สร้างเอกสาร | ปริ๊นทำเบิกส่วนต่างScgวังน้อย | App formula | =FILTER( ทำเบิกส่วนต่างSCGวังน้อย, AND(ISNOTBLANK([วันที่ส่งสินค้า]), [วันที่ส่งสินค้า] >= [_THISROW].[StartDate], [วันที่ส่งสินค้า]<= [_THISROW].[End… | FILTER; AND; ISNOTBLANK | วันที่ส่งสินค้า; _THISROW; StartDate; EndDate; สถานะ | 445 |
| สร้างเอกสาร | ปริ๊นใบป่ ะหน้า | App formula | =FILTER("ข้อมูลการวางบิล",(AND([ชื่อ - นามสกุล]=[_THISROW].[ชื่อ - นามสกุล],[วันที่]>=[_THISROW].[StartDate],[วันที่]<=[_THISROW]. [EndDate]))) | FILTER; AND | ชื่อ - นามสกุล; _THISROW; วันที่; StartDate; EndDate | 444 |
| สร้างเอกสาร | ปริ๊นใบวางบิล | App formula | [วันที่]>=[_THISROW].[StartDate],[วันที่]<=[_THISROW]. [EndDate]))) | - | วันที่; _THISROW; StartDate; EndDate | 443 |
| สร้างเอกสาร | ราคา_ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง | App formula | [StartDate], [วันที่เข้ารับ] <= [_THISROW].[EndDate], IN( [สถานะการเข้ารับสินค้า], LIST( "(ได้เพิ่ม200) ไม่มีสินค้าคืน หรือ ร้านปิ ด", "(ได้เพิ่ม200)… | IN; LIST | StartDate; วันที่เข้ารับ; _THISROW; EndDate; สถานะการเข้ารับสินค้า | 451 |
| สร้างเอกสาร | ราคา_ได้เพิ่ม50%ของค่าเที่ยว | App formula | =SUM(SELECT( รับงานคืนได้เงิน200[ราคา], AND(ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[StartDate], [วันที่เข้ารับ] <= [_THISROW].[End… | SUM; SELECT; AND; ISNOTBLANK | ราคา; วันที่เข้ารับ; _THISROW; StartDate; EndDate; สถานะการเข้ารับสินค้า | 453 |
| สร้างเอกสาร | ราคารวม | App formula | =SUM(SELECT(ข้อมูลการวางบิล[ราคา], AND([ชื่องาน]= [_THISROW].[ชื่องาน],[วันที่] >= [_THISROW].[Startdate], [วันที่] <= [_THISROW].[Enddate]))) | SUM; SELECT; AND | ราคา; ชื่องาน; _THISROW; วันที่; Startdate; Enddate | 437 |
| สร้างเอกสาร | ราคารวม_ทำเบิกส่วนต่างScgวังน้อย | App formula | =SUM(SELECT( ทำเบิกส่วนต่างScgวังน้อย[ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม], AND(ISNOTBLANK([วันที่ส่งสินค้า]), [วันที่ส่งสินค้า] >=[_THISROW].[StartDate],… | SUM; SELECT; AND; ISNOTBLANK | ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม; วันที่ส่งสินค้า; _THISROW; StartDate; EndDate; สถานะ | 446 |
| สร้างเอกสาร | ราคารวมคนขับ | App formula | =SUM(SELECT(ข้อมูลการวางบิล[ราคา], AND([ชื่อ - นามสกุล]=[_THISROW].[ชื่อ - นามสกุล],[วันที่] >= [_THISROW].[Startdate], [วันที่] <= [_THISROW].[Enddat… | SUM; SELECT; AND | ราคา; ชื่อ - นามสกุล; _THISROW; วันที่; Startdate; Enddate | 441 |
| สร้างเอกสาร | วันที่ออกเอกสาร | Initial value | =TODAY() | TODAY | - | 440 |
| สร้างเอกสาร | สรุปจำนวนจุดส่งงาน | App formula | = TRUE, ISNOTBLANK([Plan Delivery]), [Plan Delivery] >= [_THISROW].[StartDate], [Plan Delivery] <= [_THISROW]. [EndDate] ) ) | ISNOTBLANK | Plan Delivery; _THISROW; StartDate; EndDate | 447 |
| สร้างเอกสาร | ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง | App formula | =FILTER( รับงานคืนได้เงิน200, AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[StartDate], [วันที่เข้ารับ] <= [_THISROW].[EndDate], IN… | FILTER; AND; ISNOTBLANK; IN; LIST | วันที่เข้ารับ; _THISROW; StartDate; EndDate; สถานะการเข้ารับสินค้า | 448 |
| สร้างเอกสาร | ได้เพิ่ม50%ของค่าเที่ยว | App formula | =FILTER( รับงานคืนได้เงิน200, AND( ISNOTBLANK([วันที่เข้ารับ]), [วันที่เข้ารับ] >= [_THISROW].[StartDate], [วันที่เข้ารับ] <= [_THISROW].[EndDate], [ส… | FILTER; AND; ISNOTBLANK | วันที่เข้ารับ; _THISROW; StartDate; EndDate; สถานะการเข้ารับสินค้า | 450 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 509 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 510 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | ID_ส่งงานที่ยังไม่มีข้อมูลในระบบ | Initial value | UNIQUEID() | UNIQUEID | - | 501 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | จุดส่งสินค้าปลายทาง | Initial value | =HERE() | HERE | - | 509 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 503 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 503 |
| ส่งงานที่ยังไม่มีข้อมูลในระบบ | วันที่ส่งสินค้า | Initial value | =TODAY() | TODAY | - | 502 |
| หน้าหลัก | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER", "READ_ONLY", "READ_ONLY") | SWITCH; USERROLE | - | 5 |
| แจ้งปั ญหาระหว่างวัน | (table level) | Security filter | =OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL()) | OR; USERROLE; USEREMAIL | Email พนักงาน | 7 |
| แจ้งปั ญหาระหว่างวัน | (table level) | Expression for update mode | =SWITCH(USERROLE(), "ADMIN", "ALL_CHANGES", "USER","ADDS_AND_UPDATES", "READ_ONLY") | SWITCH; USERROLE | - | 7 |
| แจ้งปั ญหาระหว่างวัน | Email พนักงาน | Initial value | =USEREMAIL() | USEREMAIL | - | 222 |
| แจ้งปั ญหาระหว่างวัน | ID_พนักงาน | Initial value | =LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ID_พนักงาน") | LOOKUP; USEREMAIL | - | 226 |
| แจ้งปั ญหาระหว่างวัน | ID_แจ้งปั ญหาระหว่างวัน | Initial value | UNIQUEID() | UNIQUEID | - | 206 |
| แจ้งปั ญหาระหว่างวัน | LINK_Image_แจ้งปั ญหา | App formula | {"MaxLength":null,"MinLength":null,"LongTextFormatting":"Plain Text","IsMulticolumnKey":false,"Valid_If":null,"Error_Message_If_I nvalid":null,"Show_I… | TEXT; LIST; IF; ISNOTBLANK; CONCATENATE; ENCODEURL | รูป1; รูป2; รูป3 | 227 |
| แจ้งปั ญหาระหว่างวัน | Lat/Long | Initial value | =HERE() | HERE | - | 221 |
| แจ้งปั ญหาระหว่างวัน | LatLong_ตรวจสอบ | Initial value | =HERE() | HERE | - | 221 |
| แจ้งปั ญหาระหว่างวัน | RT_Link | Initial value | =ANY(SELECT(ข้อมูลงานRT[ID_RT], [เลขที่เอกสารรับคืน] = ANY([_THISROW].[Invoice No]))) | ANY; SELECT | ID_RT; เลขที่เอกสารรับคืน; _THISROW; Invoice No | 224 |
| แจ้งปั ญหาระหว่างวัน | SM_Link | Initial value | =ANY(SELECT(ตารางงานประจำวัน[ID_งานประจำวัน], AND([Invoice No] = ANY([_THISROW].[Invoice No]), [_ROWNUMBER] = MIN(SELECT(ตารางงานประจำ วัน[_ROWNUMBER]… | ANY; SELECT; AND; MIN | ID_งานประจำวัน; Invoice No; _THISROW; _ROWNUMBER | 223 |
| แจ้งปั ญหาระหว่างวัน | กดปุ่ มนี้เพื่อส่งข้อมูลแจ้งปั ญหา | Initial value | =false | - | - | 207 |
| แจ้งปั ญหาระหว่างวัน | ชื่อ - นามสกุล | Initial value | =[ID_พนักงาน].[ชื่อ - นามสกุล] | - | ID_พนักงาน; ชื่อ - นามสกุล | 212 |
| แจ้งปั ญหาระหว่างวัน | ชื่อปลายทาง | Initial value | =IF(ISNOTBLANK([SM_Link]), [SM_Link].[ชื่อปลายทาง], IF(ISNOTBLANK([RT_Link]), [RT_Link].[ชื่อลูกค้าที่เข้ารับ], "ไม่พบ ข้อมูล" ) ) | IF; ISNOTBLANK | SM_Link; ชื่อปลายทาง; RT_Link; ชื่อลูกค้าที่เข้ารับ | 218 |
| แจ้งปั ญหาระหว่างวัน | ชื่อผู้รับเหมา | Initial value | =[SM_Link].[ชื่อผู้รับเหมา] | - | SM_Link; ชื่อผู้รับเหมา | 214 |
| แจ้งปั ญหาระหว่างวัน | ทะเบียนรถ | Initial value | =[ID_พนักงาน].[ทะเบียนรถ] | - | ID_พนักงาน; ทะเบียนรถ | 213 |
| แจ้งปั ญหาระหว่างวัน | รหัสผู้รับเหมา | Initial value | =[SM_Link].[รหัสผู้รับเหมา] | - | SM_Link; รหัสผู้รับเหมา | 213 |
| แจ้งปั ญหาระหว่างวัน | รหัสลูกค้า | Initial value | =IF(ISNOTBLANK([SM_Link]), [SM_Link].[รหัสลูกค้า], IF(ISNOTBLANK([RT_Link]), [RT_Link].[รหัสลูกค้า], "ไม่พบข้อมูล" ) ) | IF; ISNOTBLANK | SM_Link; รหัสลูกค้า; RT_Link | 217 |
| แจ้งปั ญหาระหว่างวัน | วันที่+เวลา | Initial value | =NOW() | NOW | - | 211 |
| แจ้งปั ญหาระหว่างวัน | อัพเดตข้อมูลการแจ้งปั ญหา ไป ตารางส่งงานSCG | Initial value | =false | - | - | 220 |
| แจ้งปั ญหาระหว่างวัน | เดือน | Initial value | =IF( ISBLANK([วันที่+เวลา]), "", (YEAR(DATE([วันที่+เวลา])) - IF(YEAR(DATE([วันที่+เวลา])) > 2500, 543, 0)) & "-" & TEXT(DATE([วันที่+เวลา]), "MM") ) | IF; ISBLANK; YEAR; DATE; TEXT | วันที่+เวลา | 223 |
