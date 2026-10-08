---
title: Book Startup Program Data — Product Card
doc_id: CARD-book-startup-program-data
doc_type: product-card
verdict: showcase
version: 0.1
date: 2026-10-08
status: ร่างเพื่อพิจารณา
owner: Product owner (Book Dev)
---

# Book Startup Program Data — Product Card

## 1. สรุปคุณค่าในหนึ่งประโยค

ช่วยผู้ก่อตั้งเปรียบเทียบโปรแกรมสตาร์ทอัพ (accelerator, incubator, venture builder, perks) ด้วยฟิลด์ที่สำคัญจริง เช่นระยะของบริษัท การขอหุ้น และวันเริ่ม cohort

## 2. ปัญหาและผู้ใช้เป้าหมาย

- ผู้ก่อตั้งต้องเปิดหลายเว็บเพื่อเทียบเงื่อนไขและมักไม่เห็นว่าโปรแกรมไหนขอ equity
- ผู้ใช้เป้าหมาย: ผู้ก่อตั้งและทีมเล็ก **[สมมติฐาน]** ไม่มีหลักฐานผู้ใช้จริง

## 3. สิ่งที่ทำได้จริงตอนนี้

- CLI `contract`, `demo --open-only/--query`, `validate` บน contract `startup_program.v1`
- source policy ทางการ 5 แหล่ง (Google for Startups Accelerator, Google Startup School, AWS Activate, Antler, Entrepreneurs First) capture แบบสั่งด้วยมือผ่าน shared lake runtime
- แยกชนิดมูลค่า (cash/credit/in-kind/access) และห้ามรวมเป็นรายได้เงินสด
- test 4 ไฟล์ offline

## 4. หลักฐานสถานะ

- Stack: Python
- Commits: 11 (แรก 2026-09-09 → ล่าสุด 2026-10-01), branch `main`; working tree สะอาด
- Source: 8 ไฟล์ / 769 บรรทัด; test 4 ไฟล์
- CI: 1 workflow
- Deploy config: ไม่มี
- Live URL: ไม่พบใน repo
- โครงสร้างไฟล์เหมือนกับ repo อื่นอีก 12 ตัวในตระกูลเดียวกัน (structure signature เดียวกัน)

## 5. คุณค่าและจุดต่าง

- ฟิลด์ `equity_required` และ `startup_stage` เป็นจุดเทียบที่มีประโยชน์จริง
- คู่แข่งคือรายการ accelerator ที่มีอยู่มากและฟรี; 5 แหล่งยังน้อยเกินกว่าจะเป็นจุดต่าง
- มุมรายได้: แทบไม่มี เว้นแต่เป็นเนื้อหาประกอบชุมชน founder **[สมมติฐาน]**

## 6. ช่องว่างสำคัญ

- ครอบคลุม 5 โปรแกรมระดับโลก ไม่มีโปรแกรมไทย/อาเซียน
- ยังไม่มีผู้ใช้ปลายทาง: README ระบุว่าไม่มี scheduler, hosted API หรือ consumer integration (`Consumers: integration planned`)
- โครงซ้ำกับอีก 12 repo ในตระกูล

## 7. คำตัดสิน

**showcase** — โค้ดและ contract ทำงานจริง เหมาะเป็นหลักฐาน data product แต่ข้อมูลน้อยและไม่มีผู้ใช้ จึงไม่ใช่ธุรกิจ

จะเปลี่ยนเป็น `invest` เมื่อมีโปรแกรมในภูมิภาคและมีผู้ใช้กลุ่ม founder ที่ยืนยันว่าใช้งาน; ถ้ารวมตระกูลให้เปลี่ยนเป็น `merge`

## 8. ขั้นต่อไป

1. เพิ่มโปรแกรมไทย/อาเซียนที่มีหน้าเงื่อนไขสาธารณะ
2. ตัดสินใจรวมตระกูล intake 13 repo
3. ทำ README ให้บอกจำนวนแหล่งและข้อจำกัดชัดเจน (ทำแล้วบางส่วน)

## การอนุมัติ

| บทบาท | สถานะ | วันที่ | ลงนาม |
|---|---|---|---|
| Product owner (Book Dev) | รอพิจารณา | — | ________ |

## แหล่งข้อมูล

- `README.md`
- `PRODUCT.md`
- `src/book_startup_program_data/`
- `tests/`
