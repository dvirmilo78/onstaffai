import os
import re

bundle_dir = "src_bundle"
pattern = re.compile(r'onstaffai', re.IGNORECASE)

for root, dirs, files in os.walk(bundle_dir):
    for file in files:
        path = os.path.join(root, file)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                if pattern.search(line):
                    # Skip common lines that are just urls or emails
                    if "projects/onstaffai" in line or "@onstaffai.com" in line or "onstaffai.live" in line or "LogoMark" in line:
                        continue
                    print(f"File: {path}, Line: {idx+1}")
                    print(line.strip())
                    print("-" * 50)
