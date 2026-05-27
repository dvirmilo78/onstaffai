import json
import base64
import zlib
import gzip
import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
if file_id in manifest:
    data = base64.b64decode(manifest[file_id]['data'])
    try:
        data = gzip.decompress(data)
        text = data.decode('utf-8')
        
        # Modify the success message color as requested
        text = text.replace("color: 'var(--mint)'", "color: '#10B981', fontWeight: 'bold', fontSize: '18px'")
        
        # ADD PLAN AND AGENTS FIELDS AND EMAILJS/FIREBASE LOGIC TO THE FORM
        # But for now, just test if it repacks successfully
        new_data = text.encode('utf-8')
        comp_data = gzip.compress(new_data)
        
        manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
        new_manifest_json = json.dumps(manifest)
        new_html = html.replace(manifest_json, new_manifest_json)
        
        with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI_test3.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Success! Gzip works.")
    except Exception as e:
        print(f"Failed: {e}")
