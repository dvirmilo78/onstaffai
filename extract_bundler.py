import json
import base64
import zlib
import re
import os

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    os.makedirs('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/src_bundle', exist_ok=True)
    
    for file_id, file_data in manifest.items():
        data = base64.b64decode(file_data['data'])
        if file_data.get('compressed'):
            try:
                data = zlib.decompress(data)
            except zlib.error:
                try:
                    data = zlib.decompress(data, -zlib.MAX_WBITS)
                except zlib.error:
                    data = zlib.decompress(data, zlib.MAX_WBITS|32) # gzip
        
        path = file_data.get('path', file_id)
        if path:
            # Handle absolute paths properly so they don't break os.path.join
            if path.startswith('/'):
                path = path[1:]
            full_path = os.path.join('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/src_bundle', path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as out_f:
                out_f.write(data)
            print(f"Extracted {path}")
