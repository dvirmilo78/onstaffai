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
    
    # 1. Update DEMO_SCRIPTS in data chunk
    data_uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if data_uuid in manifest:
        entry = manifest[data_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We need to add techsupport and inventory to he and en in DEMO_SCRIPTS.
        # Find where "marketing:" is defined in he:
        he_marketing = """marketing: [
      { u: "תכין לי 3 כיוונים לקמפיין של קיץ" },
      { b: "על הדרך:\\n\\n**1. ״קיץ בלי תורים״** — מבליט את החיסכון בזמן. טון חברי.\\n**2. ״הכירו את הצוות הדיגיטלי״** — מספר על הסוכנים כ-״עובדים חדשים״.\\n**3. ״0₪ לעבודה, 24/7 לתוצאות״** — השוואה ישירה למחיר שכר.\\n\\nאיזה מהם נרוץ לראשון?" },
    ],"""
        
        he_addons = """
    techsupport: [
      { u: "לקוח מתלונן שהוא לא מצליח להתחבר למערכת" },
      { b: "טיפלתי בזה 🛠️ זיהיתי שהוא מנסה להתחבר עם אימייל לא נכון. שלחתי לו קישור לאיפוס סיסמה עם וידאו הדרכה של 20 שניות. הכל תקין עכשיו." },
    ],
    inventory: [
      { u: "מה מצב המלאי של המוצר המוביל שלנו?" },
      { b: "המלאי הנוכחי עומד על 42 יחידות 📦 בקצב המכירות הנוכחי זה יספיק ל-8 ימים. כבר הוצאתי הזמנת רכש אוטומטית לספק ל-200 יחידות נוספות (תאריך אספקה: עוד 5 ימים)." },
    ],
"""
        
        if he_marketing in text:
            text = text.replace(he_marketing, he_marketing + he_addons)

        en_marketing = """marketing: [
      { u: "Draft me 3 directions for the summer campaign" },
      { b: "Here you go:\\n\\n**1. ″No queues this summer″** — highlights time saving. Friendly tone.\\n**2. ″Meet the digital team″** — frames agents as new hires.\\n**3. ″$0 for work, 24/7 for results″** — direct cost comparison.\\n\\nWhich one should we run first?" },
    ],"""

        en_addons = """
    techsupport: [
      { u: "A customer is complaining they can't log in" },
      { b: "Handled it 🛠️ I noticed they were using the wrong email. Sent them a password reset link with a 20-second tutorial video. They are back in." },
    ],
    inventory: [
      { u: "What's the stock status for our best seller?" },
      { b: "Current stock is 42 units 📦 At the current sales rate, this will last 8 days. I've already issued an automated PO to the supplier for 200 more units (ETA: 5 days)." },
    ],
"""

        if en_marketing in text:
            text = text.replace(en_marketing, en_marketing + en_addons)

        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully added demo scripts.")
