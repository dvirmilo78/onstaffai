import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Smooth Scrolling
# Ensure the very first <style> tag in the head contains the scroll-behavior
if "scroll-behavior: smooth;" not in html:
    html = html.replace("<style>", "<style>\nhtml { scroll-behavior: smooth !important; }\n", 1)

# Now, we need to modify the bundled React chunks for the arrow.
manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    # 2. Fix the Arrow in the Hero component
    hero_uuid = "a45ef67e-5031-4f07-8e71-26ebc965edfd"
    if hero_uuid in manifest:
        entry = manifest[hero_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We need to find the arrow and replace it.
        # Original: <a className="btn btn-accent" href="#contact">{tCta.primary} →</a>
        # New: <a className="btn btn-accent" href="#contact" style={{display:'flex',gap:'8px',alignItems:'center'}}>{lang === 'he' ? '←' : ''} {tCta.primary} {lang !== 'he' ? '→' : ''}</a>
        
        old_btn_str = '<a className="btn btn-accent" href="#contact">{tCta.primary} →</a>'
        new_btn_str = '<a className="btn btn-accent" href="#contact" style={{display:"flex",gap:"8px",alignItems:"center"}}>{lang === "he" ? "←" : ""} {tCta.primary} {lang !== "he" ? "→" : ""}</a>'
        
        if old_btn_str in text:
            text = text.replace(old_btn_str, new_btn_str)
        else:
            print("Warning: Could not find the old button string in the Hero chunk.")
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    # Also, we should check App component for smooth scrolling override.
    # In chunk 4a6fb28c-5e65-4bc9-ba76-50164d056976, check if there's any preventDefault on nav links
    app_uuid = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
    if app_uuid in manifest:
        entry = manifest[app_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Sometimes <a href="#id"> doesn't smooth scroll in React due to hash routing or lack of html { scroll-behavior: smooth }
        # Adding it to the <head> usually works. Let's make sure we also add a script to intercept link clicks just in case.
        # Actually, standard anchor links work fine with CSS scroll-behavior unless intercepted.
        
        # Let's also check if there is an explicit arrow in the App chunk
        
    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated arrow and scrolling.")
