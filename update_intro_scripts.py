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
    
    data_uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if data_uuid in manifest:
        entry = manifest[data_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We need to completely replace the DEMO_SCRIPTS object
        # Find the start and end of DEMO_SCRIPTS
        start_idx = text.find("const DEMO_SCRIPTS = {")
        if start_idx != -1:
            # Simple heuristic: find the next 'export ' or the end of the file, or count braces.
            # We know what follows DEMO_SCRIPTS? It's just before 'export { L, t_he, t_en ...' if it's the end.
            # Let's write a brace counter to find the end of DEMO_SCRIPTS object.
            brace_count = 0
            end_idx = -1
            in_string = False
            escape = False
            for i in range(start_idx + 21, len(text)):
                c = text[i]
                if escape:
                    escape = False
                    continue
                if c == '\\':
                    escape = True
                    continue
                if c == '"' or c == "'":
                    if in_string == c:
                        in_string = False
                    elif not in_string:
                        in_string = c
                    continue
                
                if not in_string:
                    if c == '{':
                        brace_count += 1
                    elif c == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                            
            if end_idx != -1:
                new_scripts = """const DEMO_SCRIPTS = {
  he: {
    reception: [
      { b: "היי! אני מאיה, נציגת שירות הלקוחות שלך 👋. אני יכולה לענות על שאלות נפוצות, לסנן פניות, לקבוע פגישות ביומן שלך ולטפל בלקוחות 24/7. על מה תרצה לשמוע פירוט?" },
    ],
    finance: [
      { b: "שלום! אני איתן, איש הכספים שלך 💼. אני מוודא שכל החשבוניות מופקות ומשולמות בזמן, שולח תזכורות גבייה חכמות ללקוחות, ודואג שהעסק תמיד ברווחיות. מה מעניין אותך לדעת?" },
    ],
    marketing: [
      { b: "היי, אני דנה, מנהלת השיווק שלך 🚀. אני בונה קמפיינים, שולחת ניוזלטרים חכמים ללקוחות עבר, ומחממת לידים קרים דרך הווטסאפ עד שהם מוכנים לרכישה. במה תרצה שאתמקד?" },
    ],
    techsupport: [
      { b: "אהלן, אני יובל מהתמיכה הטכנית 🛠️. אני פותר בעיות ללקוחות בזמן אמת, מזהה טעויות משתמש ושולח להם מדריכים, ופותח קריאות מסודרות למפתחים אם יש באג. שאל אותי כל דבר!" },
    ],
    inventory: [
      { b: "שלום! אני עומר, אחראי מלאי ורכש 📦. אני מחובר למערכת 24/7, עוקב אחרי כמויות ומוציא הזמנות אוטומטיות לספקים רגע לפני שמוצר אוזל. איך תרצה שאעזור לעסק שלך?" },
    ],
  },
  en: {
    reception: [
      { b: "Hi! I'm Maya, your customer service rep 👋. I can answer FAQs, filter inquiries, book meetings in your calendar, and handle customers 24/7. What would you like me to detail?" },
    ],
    finance: [
      { b: "Hello! I'm Eitan, your finance agent 💼. I ensure all invoices are issued and paid on time, send smart collection reminders, and keep the business profitable. What interests you?" },
    ],
    marketing: [
      { b: "Hey, I'm Dana, your marketing manager 🚀. I build campaigns, send smart newsletters to past clients, and warm up cold leads via WhatsApp. What should we focus on?" },
    ],
    techsupport: [
      { b: "Hey, I'm Yuval from tech support 🛠️. I solve customer issues in real-time, identify user errors, and open structured tickets for developers if there's a real bug. Ask me anything!" },
    ],
    inventory: [
      { b: "Hello! I'm Omer, your inventory manager 📦. I monitor stock 24/7 and automatically issue POs to suppliers right before a product runs out. How can I help your business?" },
    ],
  }
};"""
                text = text[:start_idx] + new_scripts + text[end_idx:]
                
                new_data = text.encode('utf-8')
                if entry.get('compressed'):
                    new_data = gzip.compress(new_data)
                entry['data'] = base64.b64encode(new_data).decode('utf-8')

                new_manifest_json = json.dumps(manifest, separators=(',', ':'))
                new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
                
                with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
                    out.write(new_html)
                print("Successfully updated intro scripts.")
            else:
                print("Could not find end of DEMO_SCRIPTS.")
        else:
            print("Could not find start of DEMO_SCRIPTS.")
