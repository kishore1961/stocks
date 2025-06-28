# import pdfplumber
# import json

# pdf_path = "gensol-291.pdf"

# output = []

# with pdfplumber.open(pdf_path) as pdf:
#     for page_number, page in enumerate(pdf.pages, start=1):
#         text = page.extract_text()
#         tables = page.extract_tables()

#         page_data = {
#             "page_number": page_number,
#             "text": text.strip() if text else "",
#             "tables": []
#         }

#         for table in tables:
#             page_data["tables"].append(table)

#         output.append(page_data)

# # Save as JSON
# with open("extracted_pdf_data.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, indent=2, ensure_ascii=False)

# # Optional: Print page-wise summary
# for page in output:
#     print(f"\n--- Page {page['page_number']} ---")
#     print("Text:")
#     print("Tables:")
#     for t in page['tables']:
#         for row in t:
#             print(row)


import pdfplumber
import json
import re

pdf_path = "gensol-291.pdf"

def extract_key_value_pairs_from_text(text):
    data = {}
    lines = text.split('\n')
    last_key = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try to extract using pattern: Key : Value OR Key   Value
        match = re.match(r"([A-Za-z\s\(\)/\-.]+?)[:\s]{1,3}(.+)", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            data[key] = value
            last_key = key
        elif last_key:
            # Likely a continuation of the previous value
            data[last_key] += ' ' + line.strip()

    return data

def extract_key_value_pairs_from_tables(tables):
    extracted = []
    for table in tables:
        record = {}
        for row in table:
            if len(row) == 2:
                key, value = row
                if key and value:
                    record[key.strip()] = value.strip()
        if record:
            extracted.append(record)
    return extracted

final_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        page_text = page.extract_text() or ""
        page_tables = page.extract_tables()

        text_kv = extract_key_value_pairs_from_text(page_text)
        table_kv_list = extract_key_value_pairs_from_tables(page_tables)

        page_output = {
            "page_number": page_number,
            "text_key_values": text_kv,
            "table_key_values": table_kv_list
        }

        final_data.append(page_output)

# Save to structured JSON
with open("structured_output.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

# Optional: Pretty print
for page in final_data:
    print(f"\n--- Page {page['page_number']} ---")
    print("From Text:")
    for k, v in page["text_key_values"].items():
        print(f"  {k}: {v}")
    print("From Tables:")
    for t in page["table_key_values"]:
        for k, v in t.items():
            print(f"  {k}: {v}")
