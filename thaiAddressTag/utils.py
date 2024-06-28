import re

def preprocess(text: str) -> str:
    """
    Generalized function to preprocess an input
    """
    text = text.strip()
    text = text.replace("ส่ง ", "")
    text = text.replace("จัดส่ง", "")
    text = text.replace("ชือ.", "")
    text = text.replace("ชื่อ ", "")
    text = text.replace("ผู้รับ", "")
    text = text.replace("ส่งที่ ", " ")
    text = text.replace("ที่อยู่ ", " ")
    text = text.replace("ที้อยุ่ ", " ")
    text = text.replace("ที่อยู่จ้า ", " ")
    text = text.replace("ส่งของที่ ", " ")
    text = text.replace("ส่งมาที่", " ")
    text = text.replace("โทรศัพท์", " ")
    text = text.replace("โทร.", " ")
    text = text.replace("โทร", " ")
    text = text.replace("\n-", " ")
    text = text.replace("\n", " ")
    text = text.replace(": ", " ")
    text = text.replace(":", "")
    text = text.replace("-", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace('"', "")
    # text = remove_emoji(text)
    text = " ".join([t for t in text.strip().split(" ") if t.strip() != ""])
    return text


def clean_location_text(text: str) -> str:
    """
    Clean location before using fuzzy string match
    """
    text = text.replace("หมู่บ้าน", " ")
    text = text.replace("ซอย", " ")
    text = text.replace("แขวง", " ")
    text = text.replace("เขต", " ")
    text = text.replace("อำเภอ", " ")
    text = text.replace("ตำบล", " ")
    text = text.replace("ถ.", " ")
    text = text.replace("ซ.", " ")
    text = text.replace("ตฺ", "ต.")
    text = text.replace("ต.", " ")
    text = text.replace("อ.", " ")
    text = text.replace("จ.", " ")
    text = text.replace("คอหงส์", "คอหงษ์")
    text = text.replace("กทม.", "กรุงเทพ")
    text = text.replace("กทม", "กรุงเทพ")
    text = text.replace("กรุงเทพมหานคร", "กรุงเทพ")
    text = text.replace(".", "")
    return text

def extract_name(text: str) -> str:
    """
    Extracts name from the text.
    update
     - คำว่า คุณ
     - คำนำหน้า เว้น ชื่อ
    """
    name = re.search(r'(เด็กชาย|เด็กหญิง|ด\.ช\.|ด\.ญ\.|นาย|นาง|นางสาว|น\.ส\.|ดร\.|คุณ)\s*([ก-๙]+)\s*([ก-๙]+)', text)
    if name:
        full_name = name.group(0)
        text = text.replace(full_name, " ")
        return text, full_name
    return text, ''


def extract_phone(text: str):
    """
    Extracts phone from the text.
    update
     - เบอร์ +66
     - เบอร์ 08 เว้น \dเลขเบอร์
     - เบอร์มี - .
    """
    phone_match = re.search(r'(\+66\s?|0)([2-9]\d[\s-]?\d{3}[\s-]?\d{4})', text)
    if phone_match:
        phone = phone_match.group(0)
        # Standardize phone number
        phone_standardized = phone.replace(' ', '').replace('-', '').replace('.', '')
        if phone_standardized.startswith('+66'):
            phone_standardized = '0' + phone_standardized[3:]
        text = text.replace(phone_match.group(0), " ")
        return text.strip(), phone_standardized
    return text.strip(), ''