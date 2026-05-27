import json
import base64
import zlib
import re
import os

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

# Modify a file
file_id = "97ca5b64-8b14-4894-aaae-1dca4d9d405f" # src/data.jsx
if file_id in manifest:
    data = base64.b64decode(manifest[file_id]['data'])
    # Try different decompression
    try:
        data = zlib.decompress(data)
        mode = 'zlib'
    except:
        try:
            data = zlib.decompress(data, -zlib.MAX_WBITS)
            mode = 'raw'
        except:
            data = zlib.decompress(data, zlib.MAX_WBITS|32)
            mode = 'gzip'
            
    text = data.decode('utf-8')
    # Make a tiny modification to test
    text = text.replace('סוכני AI לעסקים', 'סוכני AI מטורפים לעסקים')
    
    new_data = text.encode('utf-8')
    if mode == 'zlib':
        comp_data = zlib.compress(new_data)
    elif mode == 'raw':
        co = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        comp_data = co.compress(new_data) + co.flush()
    else:
        co = zlib.compressobj(wbits=zlib.MAX_WBITS|32)
        comp_data = co.compress(new_data) + co.flush()
        
    manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
    
    new_manifest_json = json.dumps(manifest)
    new_html = html.replace(manifest_json, new_manifest_json)
    
    with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI_test.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Repacked successfully")
