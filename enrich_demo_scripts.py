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
    
    # 1. Update the initial scripts to be bulleted lists
    data_uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if data_uuid in manifest:
        entry = manifest[data_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        start_idx = text.find("const DEMO_SCRIPTS = {")
        brace_count = 0
        end_idx = -1
        in_string = False
        escape = False
        if start_idx != -1:
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
      { b: "היי! אני מאיה, נציגת שירות הלקוחות שלך 👋.\\nאני יכולה לבצע עבורך:\\n• **לענות על שאלות נפוצות** באופן מיידי (שעות, מחירים, מיקומים)\\n• **לסנן פניות** ולהעביר אליך רק לידים בשלים\\n• **לקבוע פגישות** חכמות ישירות ביומן שלך\\n• **לטפל בלקוחות 24/7** ללא זמני המתנה\\n\\nעל מה מתוך הרשימה תרצה לשמוע פירוט?" },
    ],
    finance: [
      { b: "שלום! אני איתן, איש הכספים שלך 💼.\\nאני אדאג ש:\\n• **כל חשבונית תופק ותשולם** בזמן וללא טעויות\\n• **תזכורות גבייה עדינות** יישלחו ללקוחות עם חובות\\n• **קבלות יישלחו** אוטומטית ברגע שהכסף יתקבל\\n• **העסק יישאר רווחי** על ידי מעקב אחרי הוצאות חריגות\\n\\nאיזה נושא פיננסי מעניין אותך לדעת?" },
    ],
    marketing: [
      { b: "היי, אני דנה, מנהלת השיווק שלך 🚀.\\nהמשימות המרכזיות שלי הן:\\n• **בניית קמפיינים חכמים** (נטישת עגלה, ימי הולדת)\\n• **שליחת ניוזלטרים** מותאמים אישית ללקוחות עבר\\n• **חימום לידים קרים** דרך הווטסאפ עד לרכישה\\n• **העלאת פוסטים** ומעורבות ברשתות החברתיות\\n\\nבמה תרצה שאתמקד קודם?" },
    ],
    techsupport: [
      { b: "אהלן, אני יובל מהתמיכה הטכנית 🛠️.\\nאיך אני יכול לעזור?\\n• **פתרון בעיות בזמן אמת** ללקוחות שנתקעו\\n• **זיהוי טעויות משתמש** ושליחת מדריכים מדויקים\\n• **פתיחת קריאות שירות מסודרות** למפתחים (עם הלוגים המלאים) כשיש באג אמיתי\\n• **איפוס סיסמאות** והגדרות חשבון\\n\\nשאל אותי כל דבר טכני!" },
    ],
    inventory: [
      { b: "שלום! אני עומר, אחראי מלאי ורכש 📦.\\nהפעולות השוטפות שלי כוללות:\\n• **מעקב אחרי כמויות 24/7** מול מערכת ניהול המלאי\\n• **הוצאת הזמנות אוטומטיות לספקים** רגע לפני שמוצר אוזל\\n• **התראות על מוצרים נתקעים** שיושבים במחסן יותר מדי זמן\\n• **תקשורת מהירה מול ספקים**\\n\\nאיך תרצה שאעזור למחסן שלך?" },
    ],
  },
  en: {
    reception: [
      { b: "Hi! I'm Maya, your customer service rep 👋.\\nI can perform the following:\\n• **Answer FAQs** instantly (hours, pricing, locations)\\n• **Filter inquiries** and escalate only qualified leads\\n• **Book meetings** directly into your calendar\\n• **Handle customers 24/7** with zero wait time\\n\\nWhat would you like me to detail?" },
    ],
    finance: [
      { b: "Hello! I'm Eitan, your finance agent 💼.\\nI will ensure:\\n• **All invoices are issued and paid** on time\\n• **Smart collection reminders** are sent for open debts\\n• **Receipts are generated** automatically upon payment\\n• **The business stays profitable** by tracking expenses\\n\\nWhat financial topic interests you?" },
    ],
    marketing: [
      { b: "Hey, I'm Dana, your marketing manager 🚀.\\nMy main tasks include:\\n• **Building smart campaigns** (abandoned cart, birthdays)\\n• **Sending personalized newsletters** to past clients\\n• **Warming up cold leads** via WhatsApp until they buy\\n• **Social media engagement** and posting\\n\\nWhat should we focus on first?" },
    ],
    techsupport: [
      { b: "Hey, I'm Yuval from tech support 🛠️.\\nHow can I help?\\n• **Resolve issues in real-time** for stuck users\\n• **Identify user errors** and send precise tutorials\\n• **Open structured tickets** for devs (with full logs) on real bugs\\n• **Reset passwords** and handle account settings\\n\\nAsk me anything technical!" },
    ],
    inventory: [
      { b: "Hello! I'm Omer, your inventory manager 📦.\\nMy routines include:\\n• **Tracking stock 24/7** against your inventory system\\n• **Issuing automated POs** to suppliers before we run out\\n• **Alerting on dead stock** sitting too long in the warehouse\\n• **Rapid supplier communication**\\n\\nHow can I help your warehouse?" },
    ],
  }
};"""
                text = text[:start_idx] + new_scripts + text[end_idx:]
                
                new_data = text.encode('utf-8')
                if entry.get('compressed'):
                    new_data = gzip.compress(new_data)
                entry['data'] = base64.b64encode(new_data).decode('utf-8')

    # 2. Update LiveDemo Component to add animation to tech support dot
    demo_uuid = "5721bb30-92e4-4867-b41b-11a0c7d701a1"
    if demo_uuid in manifest:
        entry = manifest[demo_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Add CSS for the pulse animation if not exists
        pulse_css = """<style>{`
          .tech-pulse {
            animation: pulseTech 1.5s infinite;
          }
          @keyframes pulseTech {
            0% { box-shadow: 0 0 0 0 var(--sky); }
            70% { box-shadow: 0 0 0 8px transparent; }
            100% { box-shadow: 0 0 0 0 transparent; }
          }
        `}</style>"""
        
        # Insert CSS at the top of LiveDemo render
        render_idx = text.rfind('<div className="demo-sidebar">')
        if render_idx != -1:
            text = text[:render_idx] + pulse_css + text[render_idx:]
        
        # Modify the span className for the dot
        old_span = '<span className="dot" style={{ background: a.color }}/>'
        new_span = '<span className={"dot" + (a.k === "techsupport" ? " tech-pulse" : "")} style={{ background: a.color }}/>'
        
        if old_span in text:
            text = text.replace(old_span, new_span)
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated demo scripts and added animation.")
