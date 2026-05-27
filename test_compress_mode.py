import json
import base64
import zlib
import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
if file_id in manifest:
    data = base64.b64decode(manifest[file_id]['data'])
    mode = "none"
    try:
        zlib.decompress(data)
        mode = "zlib"
    except:
        try:
            zlib.decompress(data, -zlib.MAX_WBITS)
            mode = "raw"
        except:
            try:
                zlib.decompress(data, zlib.MAX_WBITS|32)
                mode = "gzip"
            except:
                pass
    print(f"Compression mode is: {mode}")
