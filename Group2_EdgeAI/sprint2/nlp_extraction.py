import re

def extract_receipt_data(raw_text):
    extracted_data = {"merchantName": "Not Found", "date": "Not Found", "totalAmount": 0.0}

    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    if lines:
        extracted_data["merchantName"] = lines[0]

    date_match = re.search(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', raw_text)
    if date_match:
        extracted_data["date"] = date_match.group(1)

    total_match = re.search(r'(?i)total[\s:=]*\$?\s*(\d+\.\d{2})', raw_text)
    if total_match:
        extracted_data["totalAmount"] = float(total_match.group(1))

    return extracted_data

sample_text = "MAPUA STORE\n10/11/2026\nPen $1.20\nTOTAL: 5.70\n"
print("Testing Regex Extraction:")
print(extract_receipt_data(sample_text))

