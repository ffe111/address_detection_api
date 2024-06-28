from pythainlp.tag import NER

ner = NER("thainer")
tagging = ner.tag(
    "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปนาการ\n10270\nโทร.0956029655")


entities = []
other_info = []
current_entity = None
current_label = None

for word, label in tagging:
    if label == 'O':
        other_info.append(word)
        continue
    if label.startswith('B-'):
        if current_entity:
            entities.append((current_label, current_entity))
        current_entity = word
        current_label = label[2:]
    elif label.startswith('I-') and current_entity:
        current_entity += word

if current_entity:
    entities.append((current_label, current_entity))

print(entities)
print(other_info)
