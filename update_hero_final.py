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
    
    uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if uuid in manifest:
        entry = manifest[uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        
        text = data.decode('utf-8', errors='ignore')
        
        # New Content
        en_title = '["Your Best Employee.", "Times Ten.", "Always On."]'
        en_sub = '"OnStaffAI places AI employees in your business — trained for your workflows, working 24/7, costing less than half a human."'
        
        he_title = '["העובד המצטיין שלך.", "חזק פי עשרה.", "תמיד מחובר."]'
        he_sub = '"OnStaffAI מטמיעה סוכני AI בעסק שלך - מאומנים לתהליכי העבודה שלך, פועלים 24/7, ועולים פחות מחצי מעובד אנושי."'
        
        # Update Hebrew variants
        he_hero_match = re.search(r'he: \{.*?hero: \{.*?variants: \[(.*?)\]', text, re.DOTALL)
        if he_hero_match:
            variants_content = he_hero_match.group(1)
            # Replace h arrays
            variants_content = re.sub(r'h:\s*\[[^\]]+\]', f'h: {he_title}', variants_content)
            # Replace sub strings
            variants_content = re.sub(r'sub:\s*"[^"]+"', f'sub: {he_sub}', variants_content)
            text = text.replace(he_hero_match.group(1), variants_content)

        # Update English variants
        en_hero_match = re.search(r'en: \{.*?hero: \{.*?variants: \[(.*?)\]', text, re.DOTALL)
        if en_hero_match:
            variants_content = en_hero_match.group(1)
            # Replace h arrays
            variants_content = re.sub(r'h:\s*\[[^\]]+\]', f'h: {en_title}', variants_content)
            # Replace sub strings
            variants_content = re.sub(r'sub:\s*"[^"]+"', f'sub: {en_sub}', variants_content)
            text = text.replace(en_hero_match.group(1), variants_content)

        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

        new_manifest_json = json.dumps(manifest, separators=(',', ':'))
        new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
        
        with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
            out.write(new_html)
        print("Successfully updated OnStaffAI.html with final titles and subheaders.")
