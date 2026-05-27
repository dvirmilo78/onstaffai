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
    
    # 1. Update Contact Form Button CSS (Chunk 4a6fb28c-5e65-4bc9-ba76-50164d056976)
    app_uuid = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
    if app_uuid in manifest:
        entry = manifest[app_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We need to replace the old pulse CSS with the new sheen CSS
        old_pulse_css = """<style>{`
          .contact-btn-highlight {
            animation: pulse-orange 2s infinite;
            transition: all 0.3s ease;
          }
          .contact-btn-highlight:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.6);
          }
          @keyframes pulse-orange {
            0% { box-shadow: 0 0 0 0 rgba(234, 88, 12, 0.7); }
            70% { box-shadow: 0 0 0 12px rgba(234, 88, 12, 0); }
            100% { box-shadow: 0 0 0 0 rgba(234, 88, 12, 0); }
          }
        `}</style>"""
        
        new_sheen_css = """<style>{`
          .contact-btn-highlight {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(234, 88, 12, 0.3);
          }
          .contact-btn-highlight::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%);
            transform: skewX(-25deg);
            transition: all 0.7s ease;
          }
          .contact-btn-highlight:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.6);
          }
          .contact-btn-highlight:hover::after {
            left: 150%;
            transition: left 0.7s ease-in-out;
          }
        `}</style>"""
        
        if old_pulse_css in text:
            text = text.replace(old_pulse_css, new_sheen_css)
        else:
            print("Warning: Could not find old pulse css to replace")
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    # 2. Update LiveDemo Fallbacks (Chunk 5721bb30-92e4-4867-b41b-11a0c7d701a1)
    demo_uuid = "5721bb30-92e4-4867-b41b-11a0c7d701a1"
    if demo_uuid in manifest:
        entry = manifest[demo_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # We need to replace the fallback block
        old_fallback_start = "if (!reply) {"
        old_fallback_block = """      if (!reply) {
         reply = isHe
          ? `שאלה מצוינת. כסוכן **${list.find(a=>a.k===activeK)?.name}** המומחיות שלי כוללת גם את זה. במערכת האמיתית אוכל להדגים פתרונות ממוקדים לעסק שלך ברגע שאתחבר.`
          : `Great question. As the **${list.find(a=>a.k===activeK)?.name}** agent, my expertise covers exactly that. In the real system, I can demonstrate tailored solutions once connected.`;
      }"""

        new_fallback_block = """      if (!reply) {
          if (activeK === "reception") {
              reply = isHe 
                ? "מצוין ששאלת. כנציגת שירות, אני מטפלת בדיוק בזה. ביומיום אני עונה לשאלות חוזרות בווטסאפ ובאתר, מתאמת פגישות ישירות ליומן שלך בזמנים פנויים, ומסננת שיחות ספאם - כך שרק לקוחות חמים מגיעים אליך. זה חוסך בממוצע עשרות שעות בחודש."
                : "Great question! As a reception agent, I handle this daily. I answer FAQs on WhatsApp, book meetings directly into your calendar, and filter out spam so only qualified leads reach you.";
          } else if (activeK === "finance") {
              reply = isHe
                ? "שאלה טובה. בעולמות הכספים, הגישה שלי היא לא להשאיר קצוות פתוחים. אני מבצע התאמות בנקאיות, עוקב אחרי מי לא שילם ושולח תזכורות אוטומטיות עם קישורי תשלום, ומכין את כל הנתונים לרואה החשבון בסוף חודש באופן מדויק."
                : "Good question. In finance, my goal is to leave no loose ends. I perform bank reconciliations, track unpaid invoices, send smart payment reminders with links, and prepare everything for your CPA accurately.";
          } else if (activeK === "marketing") {
              reply = isHe
                ? "מעולה. בתור מנהלת השיווק שלך, העבודה שלי היא להביא לקוחות. אני מנתחת את הקהל שלך, כותבת ניוזלטרים מותאמים אישית, ובונה אוטומציות בוואטסאפ ללקוחות שנטשו עגלה או שלא קנו הרבה זמן, הכל כדי להגדיל המרות."
                : "Excellent. As your marketing manager, my job is to drive sales. I analyze your audience, write personalized newsletters, and build WhatsApp automations for abandoned carts to boost your conversions.";
          } else if (activeK === "techsupport") {
              reply = isHe
                ? "בדיוק בשביל זה אני כאן. כשללקוח יש בעיה, אני מנתח את השגיאה, מספק לו פתרון או מדריך מיידי אם זו טעות משתמש, ופותח קריאת שירות (Ticket) מלאה למפתחים רק כשמדובר בבאג אמיתי."
                : "That's exactly why I'm here. When a user has an issue, I analyze the error, provide instant solutions for user mistakes, and open comprehensive tickets for the dev team only when it's a real bug.";
          } else if (activeK === "inventory") {
              reply = isHe
                ? "שאלה במקום. בכל הקשור למלאי ורכש, אני לא מחכה שדברים יגמרו. אני מזהה מגמות מכירה, מתריע על מוצרים שעומדים לאזול, ואף שולח בקשות רכש אוטומטיות לספקים כדי שתמיד תהיה ערוך."
                : "Spot on. For inventory, I don't wait for things to run out. I spot sales trends, alert on low stock, and send automated POs to your suppliers so you're always prepared.";
          }
      }"""
        
        if old_fallback_block in text:
            text = text.replace(old_fallback_block, new_fallback_block)
        else:
            print("Warning: Could not find old fallback block. Trying regex or manual replace.")
            # Let's try to just find "if (!reply) {" and the end of the block
            idx = text.find("if (!reply) {")
            end_idx = text.find("setMessages(prev", idx)
            if idx != -1 and end_idx != -1:
                text = text[:idx] + new_fallback_block + "\n      " + text[end_idx:]
            
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated fallbacks and button css.")
