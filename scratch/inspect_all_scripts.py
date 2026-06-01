import re

with open("OnStaffAI.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all script tags
matches = list(re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL))
print(f"Found {len(matches)} script tags:")

for idx, m in enumerate(matches):
    attrs = m.group(1).strip()
    body = m.group(2).strip()
    print(f"\n[{idx+1}] Attributes: {attrs}")
    print(f"    Body snippet: {body[:150]}...")
