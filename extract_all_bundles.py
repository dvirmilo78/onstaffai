import json
import base64
import gzip
import re
import os

os.makedirs('bundle_dump', exist_ok=True)

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    for uuid, entry in manifest.items():
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        name = entry.get('name', 'unknown') + '_' + uuid + '.js'
        name = name.replace('/', '_')
        with open(os.path.join('bundle_dump', name), 'w', encoding='utf-8') as out:
            out.write(text)
    print(f"Dumped {len(manifest)} files to bundle_dump/")
