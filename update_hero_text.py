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
    
    # Target chunk with translations
    uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if uuid in manifest:
        entry = manifest[uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        
        text = data.decode('utf-8', errors='ignore')
        
        # Define the new content
        new_en_h = '["Your Best Employee.", "Times Ten.", "Always On."]'
        new_he_h = '["העובד המצטיין שלך.", "פי עשרה יותר.", "תמיד מחובר."]'
        
        # Replace EN variants
        # The structure is variants: [ { h: [...], sub: "..." }, ... ]
        # We replace the h arrays inside variants for both he and en
        
        # Find the HE hero section
        he_hero_match = re.search(r'he: \{.*?hero: \{.*?variants: \[(.*?)\]', text, re.DOTALL)
        if he_hero_match:
            variants_content = he_hero_match.group(1)
            # Replace all h arrays in the Hebrew variants
            new_variants_content = re.sub(r'h:\s*\[[^\]]+\]', f'h: {new_he_h}', variants_content)
            text = text.replace(variants_content, new_variants_content)
            print("Updated Hebrew variants.")

        # Find the EN hero section
        en_hero_match = re.search(r'en: \{.*?hero: \{.*?variants: \[(.*?)\]', text, re.DOTALL)
        if en_hero_match:
            variants_content = en_hero_match.group(1)
            # Replace all h arrays in the English variants
            new_variants_content = re.sub(r'h:\s*\[[^\]]+\]', f'h: {new_en_h}', variants_content)
            text = text.replace(variants_content, new_variants_content)
            print("Updated English variants.")

        # Re-compress and re-encode
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

        new_manifest_json = json.dumps(manifest, separators=(',', ':'))
        new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
        
        with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
            out.write(new_html)
        print("Successfully updated OnStaffAI.html")
    else:
        print(f"Chunk {uuid} not found in manifest")
else:
    print("Manifest not found")
