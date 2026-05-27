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
        
        old_brand = '<img src="assets/onstaff_logo.png" alt="OnStaffAI" style={{height: "90px"'
        old_brand_full = '<img src="assets/onstaff_logo.png" alt="OnStaffAI" style={{height: "90px", width: "auto", display: "block"}}/>'
        
        new_brand = '<div style={{display: "flex", alignItems: "center", gap: "10px"}}><img src="assets/onstaff_icon.png" alt="OnStaffAI Icon" style={{height: "65px", width: "auto"}}/><img src="assets/onstaff_text.png" alt="OnStaffAI Text" style={{height: "45px", width: "auto"}}/></div>'
        
        if old_brand_full in text:
            text = text.replace(old_brand_full, new_brand)
        elif old_brand in text:
            # Fallback regex if spacing differs
            text = re.sub(r'<img src="assets/onstaff_logo.png" alt="OnStaffAI" style={{.*?}}/>', new_brand, text)
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    # Also update the loading screen in OnStaffAI.html
    old_loading = '<img src="assets/onstaff_logo.png" alt="OnStaffAI Loading" style="height: 125px; margin-bottom: 20px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.1));" />'
    new_loading = '<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;"><img src="assets/onstaff_icon.png" style="height: 100px;"/><img src="assets/onstaff_text.png" style="height: 70px;"/></div>'
    if old_loading in new_html:
        new_html = new_html.replace(old_loading, new_loading)

    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)

# 2. Update index.html (Vanilla template)
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = re.sub(r'<img src="assets/onstaff_logo.png" alt="OnStaffAI Logo" style="height: \d+px; width: auto;" />', 
                  '<div style="display: flex; align-items: center; gap: 10px;"><img src="assets/onstaff_icon.png" alt="Icon" style="height: 65px;"/><img src="assets/onstaff_text.png" alt="Text" style="height: 45px;"/></div>', 
                  idx_html)

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(idx_html)

print("Successfully split logo and updated HTML.")
