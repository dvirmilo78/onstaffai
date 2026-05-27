import json
import base64
import zlib
import re
import os
import gzip

html_path = 'OnStaffAI.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if not manifest_match:
    print("Manifest not found")
    exit(1)

manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

bundle_dir = 'src_bundle'
if not os.path.exists(bundle_dir):
    print("src_bundle directory not found")
    exit(1)

for filename in os.listdir(bundle_dir):
    file_id = filename
    if file_id in manifest:
        file_path = os.path.join(bundle_dir, filename)
        with open(file_path, 'rb') as f:
            new_data = f.read()
        
        # Determine compression from the original manifest data
        if manifest[file_id].get('compressed'):
            orig_data = base64.b64decode(manifest[file_id]['data'])
            # We compress using gzip as used in update_bundle.py previously
            comp_data = gzip.compress(new_data)
            manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
        else:
            manifest[file_id]['data'] = base64.b64encode(new_data).decode('utf-8')

new_manifest_json = json.dumps(manifest, separators=(',', ':'))
new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Repacked successfully from src_bundle")
