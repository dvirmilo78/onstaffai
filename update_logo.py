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
        
        # Replace the SVG brand with the image
        old_brand = '<div className="brand"><LogoMark/> OnStaffAI</div>'
        # The user uploaded an image that contains BOTH the icon and the text "OnStaffAI"
        new_brand = '<div className="brand"><img src="assets/onstaff_logo.png" alt="OnStaffAI" style={{height: "50px", width: "auto", display: "block"}}/></div>'
        
        if old_brand in text:
            text = text.replace(old_brand, new_brand)
            
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

# Replace the logo block
# <a href="#" class="logo">
#    <div class="logo-icon">...</div>
#    OnStaffAI
# </a>
idx_logo_regex = re.compile(r'<a href="#" class="logo">\s*<div class="logo-icon">.*?</div>\s*OnStaffAI\s*</a>', re.DOTALL)
new_idx_logo = '<a href="#" class="logo" style="display: flex; align-items: center;"><img src="assets/onstaff_logo.png" alt="OnStaffAI Logo" style="height: 50px; width: auto;" /></a>'

new_idx_html = idx_logo_regex.sub(new_idx_logo, idx_html)
with open('index.html', 'w', encoding='utf-8') as out:
    out.write(new_idx_html)

print("Successfully updated logo in both HTML files.")
