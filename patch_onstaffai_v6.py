import json
import base64
import gzip
import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
data = base64.b64decode(manifest[file_id]['data'])
data = gzip.decompress(data)
text = data.decode('utf-8')

# Replace the plans array — add Lite plan at the top
old_plans = """  const plans = [
    { id: 'starter', name: isHe ? 'Starter' : 'Starter', price: '₪490', agents: 3, desc: isHe ? 'לסטארטאפים ועסקים קטנים' : 'For startups and small businesses' },
    { id: 'growth', name: isHe ? 'Growth' : 'Growth', price: '₪990', agents: 6, desc: isHe ? 'לעסקים בצמיחה מהירה' : 'For fast-growing businesses' },
    { id: 'business', name: isHe ? 'Business' : 'Business', price: '₪1990', agents: 10, desc: isHe ? 'לארגונים וחברות מבוססות' : 'For established organizations' }
  ];"""

new_plans = """  const plans = [
    { id: 'lite', name: 'Lite', price: '₪190', agents: 1, desc: isHe ? 'לעסק עם סוכן אחד' : 'For businesses needing one agent' },
    { id: 'starter', name: 'Starter', price: '₪490', agents: 3, desc: isHe ? 'לסטארטאפים ועסקים קטנים' : 'For startups and small businesses' },
    { id: 'growth', name: 'Growth', price: '₪990', agents: 6, desc: isHe ? 'לעסקים בצמיחה מהירה' : 'For fast-growing businesses' },
    { id: 'business', name: 'Business', price: '₪1990', agents: 10, desc: isHe ? 'לארגונים וחברות מבוססות' : 'For established organizations' }
  ];"""

if old_plans in text:
    text = text.replace(old_plans, new_plans)
    print("✅ Plans array patched — Lite plan added.")
else:
    print("❌ Could not find plans array. Check the bundle content.")
    exit(1)

comp_data = gzip.compress(text.encode('utf-8'))
manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
new_manifest_json = json.dumps(manifest)
new_html = html.replace(manifest_json, new_manifest_json)

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✅ Patch V6 applied to OnStaffAI.html successfully!")
