import json
import base64
import gzip
import re

# 1. Update OnStaffAI.html (React bundle)
with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    app_uuid = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
    if app_uuid in manifest:
        entry = manifest[app_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We only want to shrink the logo in the nav bar, not necessarily the loading screen 
        # (although the loading screen might also be fine with 106px or left at 125px. The loading screen doesn't have a "header line").
        # The loading screen is directly in the html, not in the react bundle.
        # So we just replace 125px with 106px in the react bundle.
        
        text = text.replace('height: "125px"', 'height: "106px"')
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)

# 2. Update index.html (Vanilla template)
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = idx_html.replace('height: 125px;', 'height: 106px;')

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(idx_html)

print("Successfully shrunk logo by 15% (106px).")
