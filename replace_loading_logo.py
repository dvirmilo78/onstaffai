import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the __bundler_thumbnail SVG
old_thumbnail_regex = re.compile(r'<div id="__bundler_thumbnail">.*?</div>', re.DOTALL)
new_thumbnail = '''<div id="__bundler_thumbnail" style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
  <img src="assets/onstaff_logo.png" alt="OnStaffAI Loading" style="height: 125px; margin-bottom: 20px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.1));" />
</div>'''

if '<div id="__bundler_thumbnail">' in html:
    html = old_thumbnail_regex.sub(new_thumbnail, html)
else:
    print("Warning: Could not find __bundler_thumbnail in OnStaffAI.html")

# The React app already references assets/onstaff_logo.png (I updated it previously).
# But since I overwrote assets/onstaff_logo.png with the new image, the React app will automatically use the new image.
# I just need to save the HTML.
with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
    out.write(html)
    
print("Successfully updated loading screen logo.")
