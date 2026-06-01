import re

with open("OnStaffAI.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all script tags that are not the manifest or template
script_tags = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(script_tags)} script tags.")

for idx, script in enumerate(script_tags):
    if "type=\"__bundler/manifest\"" in content or "type=\"__bundler/template\"" in content:
        # Check if the script itself contains manifest/template keywords to skip
        if "__bundler" in script:
            continue
    if "submit" in script or "form" in script or "company" in script:
        print(f"--- Script {idx+1} matches submit/form/company ---")
        print(script.strip()[:500])
        print("...\n")
