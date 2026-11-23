# Thai Address Detection API

[English](README.md) | ภาษาไทย

แปลงข้อความที่อยู่ภาษาไทยแบบไม่เป็นโครงสร้างให้เป็นฟิลด์ด้วย FastAPI เวอร์ชันนี้ใช้กฎ พจนานุกรมจาก PyThaiNLP และข้อมูลที่อยู่อ้างอิง ไม่ใช้โมเดล Transformer

## เริ่มต้นใช้งาน

รันจากไดเรกทอรีหลักของ repo:

```bash
docker compose up --build
```

เปิด [Swagger UI](http://localhost:8000/docs) แล้วลอง `POST /address-check` ด้วยข้อความตัวอย่างที่สร้างขึ้น:

```json
{"text":"ต.สุเทพ อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50200"}
```

ผลลัพธ์จะอยู่ใน `address` ซึ่งมีฟิลด์ `province` (จังหวัด), `amphoe` (อำเภอ), `district` (ตำบล), `zipcode` (รหัสไปรษณีย์), `name` (ชื่อ) และ `phone` (เบอร์โทรศัพท์) ผลขึ้นกับข้อความและข้อมูลอ้างอิง ไม่ได้ยืนยันว่าสามารถจัดส่งได้

## หลักการทำงาน

[ขั้นตอนการสกัดข้อมูล](thaiAddressTag/tag.py) ตัดคำภาษาไทย ตรวจการสะกดด้วยพจนานุกรมที่กำหนดเอง แล้วจับคู่สถานที่กับ [รายการอ้างอิง](thaiAddressTag/addresses.py) หากต้องการรัน [API](main.py) โดยไม่ใช้ Docker ให้ใช้ Python 3.11 ติดตั้ง [`requirements.txt`](requirements.txt) แล้วสั่ง `python main.py`

อ่าน [โน้ตบุ๊กประกอบ](https://github.com/ffe111/thaiAddressTag) เพื่อดูแนวคิดเบื้องหลัง หรือดู [API รุ่น Transformer](https://github.com/ffe111/thai_addr_dt) เพื่อเปรียบเทียบอีกแนวทาง เมื่อแจ้งปัญหาการสกัดข้อมูล ให้ใช้ตัวอย่างสมมติแทนชื่อ เบอร์โทรศัพท์ หรือที่อยู่จริง
