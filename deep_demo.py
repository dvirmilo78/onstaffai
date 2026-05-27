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
    
    # 1. Rename Eitan in Data Chunk
    data_uuid = "97ca5b64-8b14-4894-aaae-1dca4d9d405f"
    if data_uuid in manifest:
        entry = manifest[data_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        text = text.replace("איתן - סוכן פיננסי", "איתן - איש הכספים")
        
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    # 2. Update LiveDemo Component logic
    demo_uuid = "5721bb30-92e4-4867-b41b-11a0c7d701a1"
    if demo_uuid in manifest:
        entry = manifest[demo_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Add techsupport and inventory to demoable
        text = text.replace('const demoable = ["reception", "finance", "marketing"];', 'const demoable = ["reception", "finance", "marketing", "techsupport", "inventory"];')

        # Replace submitUser with the expanded version
        expanded_submit_user = """const submitUser = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: "user", text: input }]);
    const q = input.toLowerCase();
    setInput("");
    setTyping(true);
    
    setTimeout(() => {
      setTyping(false);
      let reply = "";
      const isHe = lang === "he";
      
      if (q.includes("מחיר") || q.includes("עולה") || q.includes("כסף") || q.includes("price") || q.includes("cost")) {
        reply = isHe ? "העלות שלי היא שבריר מעלות של עובד אנושי ממוצע, וההחזר על ההשקעה (ROI) בדרך כלל מכסה את עצמו כבר בחודש הראשון. אפשר לראות פירוט במחירון שלנו." : "I cost a fraction of a human employee, and the ROI usually covers the cost in the first month. Check our pricing section.";
      } else if (q.includes("אינטגרציה") || q.includes("מערכות") || q.includes("חיבור") || q.includes("integrate") || q.includes("system")) {
        reply = isHe ? "אני מתחבר בקלות לכל המערכות שאתה כבר עובד איתן - WhatsApp, יומן גוגל, CRM, מערכות סליקה ועוד. ההטמעה לוקחת דקות." : "I integrate seamlessly with your existing tools - WhatsApp, Google Calendar, CRM, billing, and more. Setup takes minutes.";
      } else if (q.includes("שעות") || q.includes("זמינות") || q.includes("hours") || q.includes("available")) {
        reply = isHe ? "אני עובד 24/7, בלי הפסקות צהריים, בלי ימי מחלה או חופשות. תמיד כאן כשהלקוחות שלך צריכים אותי." : "I work 24/7, with no lunch breaks, sick days, or vacations. Always here when your customers need me.";
      } else {
        if (activeK === "reception") {
            if (q.includes("לקוחות") || q.includes("פגישות") || q.includes("לקבוע")) {
                reply = isHe ? "אני מנהלת את כל הפניות הראשוניות בווטסאפ או באתר, מסננת שאלות נפוצות (כמו שעות פתיחה או מחירים), וקובעת פגישות ללקוחות רציניים ישירות ביומן שלך בלי שתצטרך להתערב." : "I handle initial inquiries on WhatsApp or website, answer FAQs, and book meetings directly into your calendar for qualified leads.";
            } else if (q.includes("לעזור") || q.includes("תמיכה") || q.includes("שירות")) {
                reply = isHe ? "אני מחליפה את מענה הווטסאפ/טלפון השוטף שלך: עונה לשאלות מלאי, משנה מועדי פגישות, מטפלת בתלונות בסיסיות, ורק כשזה מצריך התערבות אנושית אני מעבירה את השיחה אליך עם סיכום הבעיה." : "I replace your basic customer service line. I answer stock questions, reschedule meetings, handle basic complaints, and only escalate to a human when strictly necessary.";
            }
        } else if (activeK === "finance") {
            if (q.includes("חשבון") || q.includes("גבייה") || q.includes("לשלם") || q.includes("כסף")) {
                reply = isHe ? "אני עוקב אחרי כל התשלומים במערכת, מפיק חשבוניות אוטומטית כשהכסף נכנס, שולח תזכורות מנומסות וחכמות על חובות פתוחים ואוסף את הכספים דרך קישורי תשלום." : "I track all payments, issue invoices automatically upon receipt, send smart polite reminders for open debts, and collect funds via payment links.";
            } else {
                reply = isHe ? "אני איש הכספים שלך - מוודא שהעסק שלך תמיד נשאר רווחי ושכספים לא הולכים לאיבוד בין הלקוחות והספקים." : "I am your finance agent - ensuring your business stays profitable and money never falls through the cracks.";
            }
        } else if (activeK === "marketing") {
            if (q.includes("רעיונות") || q.includes("קמפיין") || q.includes("שיווק")) {
                reply = isHe ? "קח כמה רעיונות: 1. סדרת מיילים טיפים ללקוחות עבר כדי להחזיר אותם (אני אכתוב ואשלח). 2. בוט בווטסאפ שמציע שובר הנחה תמורת הפניית חבר. 3. קמפיין מבוסס התנהגות (מי שנטש עגלה יקבל ממני הודעה אישית)." : "Here are some ideas: 1. An automated email tip series for past clients. 2. A WhatsApp bot offering a referral discount. 3. Behavioral campaigns (abandoned cart personalized messages). I can execute all of these.";
            } else if (q.includes("לידים") || q.includes("מיילים")) {
                reply = isHe ? "אני לוקחת לידים קרים שמגיעים מהפייסבוק/אינסטגרם ומחממת אותם דרך שיחות ווטסאפ וסדרות אימיילים מותאמות אישית עד שהם מוכנים לסגירה." : "I take cold leads from social media and warm them up via WhatsApp and personalized email sequences until they are ready to close.";
            }
        } else if (activeK === "techsupport") {
            if (q.includes("בעיה") || q.includes("תקלה") || q.includes("באג")) {
                reply = isHe ? "אני הראשון לפגוש תקלות. אני יודע לזהות אם זו טעות משתמש ולהדריך אותו עם סרטונים ומדריכים, ואם זה באג אמיתי - אני פותח טיקט מסודר עם כל הלוגים לצוות הפיתוח." : "I'm the first line of defense. I identify user errors and provide tutorials, and if it's a real bug, I open a detailed ticket with logs for the dev team.";
            }
        } else if (activeK === "inventory") {
            if (q.includes("מלאי") || q.includes("חסר") || q.includes("ספק")) {
                reply = isHe ? "אני מחובר למערכת המלאי שלך 24/7. כשאני מזהה שמוצר עומד להיגמר, אני מוציא הזמנת רכש אוטומטית לספק ומתריע לך במייל." : "I monitor your inventory 24/7. When stock runs low, I automatically issue a purchase order to your supplier and alert you.";
            }
        }
      }
      
      if (!reply) {
         reply = isHe
          ? `שאלה מצוינת. כסוכן **${list.find(a=>a.k===activeK)?.name}** המומחיות שלי כוללת גם את זה. במערכת האמיתית אוכל להדגים פתרונות ממוקדים לעסק שלך ברגע שאתחבר.`
          : `Great question. As the **${list.find(a=>a.k===activeK)?.name}** agent, my expertise covers exactly that. In the real system, I can demonstrate tailored solutions once connected.`;
      }
      
      setMessages(prev => [...prev, { role: "bot", text: reply }]);
    }, 1200 + Math.random() * 800);
  };"""

        start_idx = text.find("const submitUser = () => {")
        end_idx = text.find("const render = (txt)", start_idx)
        
        if start_idx != -1 and end_idx != -1:
            text = text[:start_idx] + expanded_submit_user + "\n\n  " + text[end_idx:]
            
            new_data = text.encode('utf-8')
            if entry.get('compressed'):
                new_data = gzip.compress(new_data)
            entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated demo logic and Eitan's name.")
