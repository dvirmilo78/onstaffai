import json
import base64
import gzip
import re

replacements = {
    '"סוכן מענה ללקוחות"': '"מאיה - סוכנת מענה ללקוחות"',
    '"סוכן תיאום פגישות"': '"רוני - מתאמת פגישות"',
    '"סוכן שיווק"': '"דנה - סוכנת שיווק"',
    '"סוכן פיננסי"': '"איתן - סוכן פיננסי"',
    '"סוכן מכירות"': '"טל - סוכן מכירות"',
    '"סוכן גיוס ו-HR"': '"מיכל - סוכנת גיוס"',
    '"סוכן נתונים ו-BI"': '"גיא - מנתח נתונים"',
    '"סוכן תמיכה טכנית"': '"יובל - תמיכה טכנית"',
    '"סוכן מלאי ורכש"': '"עומר - מלאי ורכש"',
    '"סוכן גבייה ותזכורות"': '"אבי - סוכן גבייה"',
    '"סוכן כתיבת תוכן"': '"שיר - כותבת תוכן"',
    '"סוכן תרגום ולוקליזציה"': '"ליהי - מתרגמת"'
}

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    for uuid, entry in manifest.items():
        if entry.get('mime') in ['text/javascript', 'application/javascript']:
            data = base64.b64decode(entry['data'])
            if entry.get('compressed'):
                data = gzip.decompress(data)
            
            text = data.decode('utf-8', errors='ignore')
            
            changed = False
            for k, v in replacements.items():
                if k in text:
                    text = text.replace(k, v)
                    changed = True
            
            if changed:
                print(f"Applying changes to {uuid}")
                new_data = text.encode('utf-8')
                if entry.get('compressed'):
                    new_data = gzip.compress(new_data)
                entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    # Ensure no backslash escaping of forward slashes to keep the same format if possible
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated OnStaffAI.html")
else:
    print("Manifest not found")

