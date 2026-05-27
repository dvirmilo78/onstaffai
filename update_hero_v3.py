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
        
        # English replacements
        text = text.replace('h: ["Replace", "employees", "with agents."]', 'h: ["Your Best Employee.", "Times Ten.", "Always On."]')
        text = text.replace('h: ["A full team,", "without payroll.", ""]', 'h: ["Your Best Employee.", "Times Ten.", "Always On."]')
        text = text.replace('h: ["Your business,", "on autopilot.", ""]', 'h: ["Your Best Employee.", "Times Ten.", "Always On."]')
        
        en_sub = '"OnStaffAI places AI employees in your business — trained for your workflows, working 24/7, costing less than half a human."'
        text = re.sub(r'sub:\s*"AI agents that answer customers, close meetings, manage finances, and market your business — 24/7, for the cost of a coffee per day."', f'sub: {en_sub}', text)
        text = re.sub(r'sub:\s*"12 smart agents replace whole departments. Up and running in 10 minutes."', f'sub: {en_sub}', text)
        text = re.sub(r'sub:\s*"Automation that saves 60 hours a week. Support, marketing, finance — all in one place."', f'sub: {en_sub}', text)

        # Hebrew replacements
        text = text.replace('h: ["החלף", "עובדים", "בסוכנים."]', 'h: ["העובד המצטיין שלך.", "חזק פי עשרה.", "תמיד מחובר."]')
        text = text.replace('h: ["צוות שלם,", "בלי תלושים.", ""]', 'h: ["העובד המצטיין שלך.", "חזק פי עשרה.", "תמיד מחובר."]')
        text = text.replace('h: ["העסק שלך,", "על אוטומט.", ""]', 'h: ["העובד המצטיין שלך.", "חזק פי עשרה.", "תמיד מחובר."]')
        
        he_sub = '"OnStaffAI מטמיעה סוכני AI בעסק שלך - מאומנים לתהליכי העבודה שלך, פועלים 24/7, ועולים פחות מחצי מעובד אנושי."'
        text = re.sub(r'sub:\s*"סוכני AI שעונים ללקוחות, סוגרים פגישות, מנהלים כספים ומשווקים את העסק — 24/7, בעלות של כוס קפה ליום."', f'sub: {he_sub}', text)
        text = re.sub(r'sub:\s*"12 סוכנים חכמים מחליפים משרדים שלמים. מתחילים לעבוד תוך 10 דקות."', f'sub: {he_sub}', text)
        text = re.sub(r'sub:\s*"אוטומציה שחוסכת 60 שעות בשבוע. מענה, שיווק, פיננסים — הכל במקום אחד."', f'sub: {he_sub}', text)

        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

        new_manifest_json = json.dumps(manifest, separators=(',', ':'))
        new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
        
        with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
            out.write(new_html)
        print("Successfully updated OnStaffAI.html using literal replacement.")
    else:
        print(f"Chunk {uuid} not found in manifest")
else:
    print("Manifest not found")
