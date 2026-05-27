import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    # 1. Update Hero component (chunk a45ef67e-5031-4f07-8e71-26ebc965edfd)
    hero_uuid = "a45ef67e-5031-4f07-8e71-26ebc965edfd"
    if hero_uuid in manifest:
        entry = manifest[hero_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Replace href="#pricing" with href="#contact" inside the hero-cta
        text = text.replace('<a className="btn btn-accent" href="#pricing">{tCta.primary}', '<a className="btn btn-accent" href="#contact">{tCta.primary}')
        
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    # 2. Update App component and ContactForm (chunk 4a6fb28c-5e65-4bc9-ba76-50164d056976)
    app_uuid = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
    if app_uuid in manifest:
        entry = manifest[app_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Replace href="#pricing" in the nav
        text = text.replace('<a href="#pricing" className="btn btn-primary"', '<a href="#contact" className="btn btn-primary"')
        
        # Replace Contact Form title
        old_title = "{isHe ? 'יצירת קשר ותחילת תהליך' : 'Contact Us & Onboarding'}"
        new_title = "{isHe ? 'מהפכת ה AI כבר כאן , עכשיו הזמן שלהם שתצטרפו אליה' : 'The AI revolution is here, time to join it'}"
        text = text.replace(old_title, new_title)
        
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated CTA links and Contact form title.")
