import re

def parse_receipt_data(text_data):
    receipt_info = {
        "Vendor Name": "N/A",
        "Date": "N/A",
        "Total Amount": "N/A",
        "Tax": "N/A"
    }

    # --- Extract Vendor Name ---
    lines = [line.strip() for line in text_data.split('
') if line.strip()]

    if lines:
        for line in lines:
            if len(line) < 4 or re.search(r'\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}', line) or re.fullmatch(r'[\d\s.,$€£]+', line):
                continue
            if re.search(r'\b(?:total|subtotal|tax|amount|due|invoice|order|receipt|bill|date|time)\b', line, re.IGNORECASE):
                continue
            receipt_info["Vendor Name"] = line
            break


    # --- Extract Date ---
    date_patterns = [
        r'\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}(?:\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)?\b',
        r'\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)?\b',
        r'\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2}(?:\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)?\b'
    ]

    for pattern in date_patterns:
        dates_found = re.findall(pattern, text_data)
        if dates_found:
            receipt_info["Date"] = dates_found[0].strip()
            break

    # --- Extract Total Amount ---
    total_pattern = r'(?:GRAND\s*TOTAL|TOTAL\s*(?:AMOUNT|DUE)?|AMOUNT\s*DUE|BALANCE\s*DUE|NET\s*PAYABLE|PAYABLE)\s*[:]?[\s$€£]*([\d,]+\.\d{2})'
    totals_matches = re.findall(total_pattern, text_data, re.IGNORECASE)

    if totals_matches:
        receipt_info["Total Amount"] = float(totals_matches[-1].replace(',', ''))

    # --- Extract Tax Amount ---
    tax_pattern = r'(?:TAX|VAT|GST|SERVICE\s*TAX)\s*(?:[^\d$]*?\s)?[\s$€£]*([\d,]+\.\d{2})'
    taxes_matches = re.findall(tax_pattern, text_data, re.IGNORECASE)

    if taxes_matches:
        total_tax = sum([float(t.replace(',', '')) for t in taxes_matches])
        receipt_info["Tax"] = total_tax

    return receipt_info