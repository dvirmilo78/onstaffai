import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r') as f:
    html = f.read()

# Extract manifest
manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    for uuid, entry in manifest.items():
        if entry.get('mime') in ['text/javascript', 'application/javascript']:
            data = base64.b64decode(entry['data'])
            if entry.get('compressed'):
                data = gzip.decompress(data)
            
            with open(f'{uuid}.js', 'wb') as out:
                out.write(data)
            print(f'Extracted {uuid}.js')

# Extract template
template_match = re.search(r'<script type="__bundler/template">(.*?)</script>', html, re.DOTALL)
if template_match:
    template_json = template_match.group(1)
    with open('template.html', 'w') as out:
        out.write(json.loads(template_json))
    print('Extracted template.html')

