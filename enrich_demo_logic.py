import json
import base64
import gzip
import re

with open('onstaffai.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
if manifest_match:
    manifest_json = manifest_match.group(1)
    manifest = json.loads(manifest_json)
    
    uuid = "5721bb30-92e4-4867-b41b-11a0c7d701a1"
    if uuid in manifest:
        entry = manifest[uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        new_submit_user = """const submitUser = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: "user", text: input }]);
    const q = input.toLowerCase();
    setInput("");
    setTyping(true);
    
    setTimeout(() => {
      setTyping(false);
      let reply = "";
      const isHe = lang === "he";
      
      // AI Logic Simulation
      if (q.includes("שלום") || q.includes("היי") || q.includes("אהלן") || q.includes("hi") || q.includes("hello")) {
          reply = isHe ? "שלום! איך אפשר לעזור לך היום? 😊" : "Hello! How can I help you today? 😊";
      } else if (q.includes("מה קורה") || q.includes("מה נשמע") || q.includes("מה המצב") || q.includes("how are you")) {
          reply = isHe ? "הכל מצוין, תודה! אני כאן לעזור. במה אוכל לסייע?" : "Everything is great, thanks! How can I assist you?";
      } else if (q.includes("מחיר") || q.includes("עולה") || q.includes("כסף") || q.includes("תמחור") || q.includes("price") || q.includes("cost")) {
        reply = isHe ? "העלות שלי היא שבריר מעלות של עובד אנושי ממוצע, וההחזר על ההשקעה (ROI) בדרך כלל מכסה את עצמו כבר בחודש הראשון! אפשר לראות פירוט בעמוד המחירון שלנו. 💸" : "I cost a fraction of a human employee, and the ROI usually covers the cost in the first month. Check our pricing section. 💸";
      } else if (q.includes("אינטגרציה") || q.includes("מערכות") || q.includes("חיבור") || q.includes("להתחבר") || q.includes("integrate") || q.includes("system")) {
        reply = isHe ? "אני מתחבר בקלות לכל המערכות שאתה כבר עובד איתן - WhatsApp, יומן גוגל, CRM (כמו Salesforce, HubSpot), מערכות סליקה, ועוד הרבה. ההטמעה לוקחת דקות בודדות! 🔌" : "I integrate seamlessly with your existing tools - WhatsApp, Google Calendar, CRM, billing, and more. Setup takes minutes. 🔌";
      } else if (q.includes("שעות") || q.includes("זמינות") || q.includes("מתי") || q.includes("hours") || q.includes("available")) {
        reply = isHe ? "אני עובד 24/7, בלי הפסקות צהריים, בלי ימי מחלה או חופשות. תמיד זמין לענות בשניות כשהלקוחות שלך צריכים אותי! ⏰" : "I work 24/7, with no lunch breaks, sick days, or vacations. Always here when your customers need me! ⏰";
      } else if (q.includes("מי אתה") || q.includes("מה אתה") || q.includes("רובוט") || q.includes("בוט") || q.includes("bot") || q.includes("who are you")) {
          reply = isHe ? "אני סוכן AI חכם שנבנה על הפלטפורמה של OnStaff AI. אני לומד את העסק שלך ויודע לבצע משימות מורכבות בצורה אוטומטית לחלוטין 🤖" : "I'm a smart AI agent built on OnStaff AI. I learn your business and automate complex tasks seamlessly 🤖";
      } else if (q.includes("איך זה עובד") || q.includes("איך המערכת") || q.includes("ללמוד") || q.includes("how it works")) {
          reply = isHe ? "זה פשוט מאוד: מעלים מסמכים או קישור לאתר שלך - ואני קורא ומבין הכל בתוך דקות. מאותו רגע אני יכול לענות לכל שאלה בצורה מדויקת על סמך הידע הזה! 🧠" : "It's simple: just upload documents or a website link, and I learn everything in minutes. I can then answer accurately based on that knowledge! 🧠";
      } else if (q.includes("אנושי") || q.includes("בן אדם") || q.includes("נציג") || q.includes("human")) {
          reply = isHe ? "למרות שאני בינה מלאכותית, אני יודע לזהות מתי צריך נציג אנושי, ובמידת הצורך אעביר את השיחה בצורה חלקה לצוות האנושי שלכם." : "While I am an AI, I know when human intervention is needed and can seamlessly route the chat to your human team.";
      } else {
        // Agent specific fallback logic
        if (activeK === "reception") {
            if (q.includes("לקוחות") || q.includes("פגישות") || q.includes("לקבוע") || q.includes("יומן") || q.includes("פגישה")) {
                reply = isHe ? "כמנהלת משרד אני מסננת לקוחות לא רלוונטיים, עונה לשאלות, וקובעת פגישות חכמות ישירות ביומן Google/Outlook של הצוות בלי שתצטרכו להתערב. 📅" : "As a receptionist, I filter irrelevant leads, answer questions, and book smart meetings directly into your Google/Outlook calendar. 📅";
            } else if (q.includes("טלפון") || q.includes("שיחות") || q.includes("מענה")) {
                reply = isHe ? "אני זמינה בוואטסאפ ובאתר כדי להבטיח שאף ליד או פנייה לא יתפספסו כשהקו עמוס או מחוץ לשעות הפעילות." : "I am available on WhatsApp and web to ensure no lead is missed when lines are busy or out of hours.";
            }
        } else if (activeK === "finance") {
            if (q.includes("חשבון") || q.includes("גבייה") || q.includes("לשלם") || q.includes("חשבונית") || q.includes("קבלות")) {
                reply = isHe ? "אני עוקב אחרי כל התשלומים, שולח תזכורות חכמות ועדינות על חובות פתוחים בוואטסאפ, ומפיק חשבוניות/קבלות אוטומטית. 💳" : "I track all payments, send smart and polite reminders for open debts on WhatsApp, and generate invoices automatically. 💳";
            } else if (q.includes("רווח") || q.includes("הוצאות") || q.includes("כסף")) {
                reply = isHe ? "אני יודע לנתח את ההוצאות וההכנסות, ולשלוח לכם דוחות פשוטים שיעזרו לכם לשמור על העסק רווחי." : "I can analyze expenses and revenues, sending you simple reports to help keep the business profitable.";
            }
        } else if (activeK === "marketing") {
            if (q.includes("לידים") || q.includes("לקוחות") || q.includes("יחס המרה") || q.includes("מכירות")) {
                reply = isHe ? "אני לוקחת גולשים מזדמנים והופכת אותם ללקוחות משלמים. אני שואלת שאלות מכוונות, שומרת את הפרטים ב-CRM ומגדילה דרמטית את יחס ההמרה! 📈" : "I turn casual visitors into paying customers. I ask qualifying questions, save details to CRM, and dramatically increase conversion rates! 📈";
            } else if (q.includes("קמפיין") || q.includes("אימייל") || q.includes("ניוזלטר") || q.includes("sms")) {
                reply = isHe ? "אני יכולה להריץ סדרות חימום באימייל או בוואטסאפ, להציע מוצרים משלימים (Upsell), ולטפל בעגלות נטושות בצורה אוטומטית." : "I can run warmup sequences via email or WhatsApp, offer upsells, and recover abandoned carts automatically.";
            }
        } else if (activeK === "techsupport") {
            if (q.includes("תקלה") || q.includes("באג") || q.includes("בעיה") || q.includes("לא עובד") || q.includes("תיקון")) {
                reply = isHe ? "אני ניזון ממאגר התמיכה (Knowledge Base). ברגע שלקוח מדווח על תקלה, אני מדריך אותו צעד אחר צעד לפתרון, או פותח טיקט ב-Jira/Zendesk במקרה של בעיית קוד מורכבת. 🛠️" : "I feed off your Knowledge Base. When a client reports an issue, I guide them step-by-step or open a Jira/Zendesk ticket for complex bugs. 🛠️";
            } else if (q.includes("סיסמא") || q.includes("איפוס") || q.includes("הגדרות")) {
                reply = isHe ? "אין בעיה! במערכת האמיתית אני מחובר ל-API ויכול לשלוח לינקים לאיפוס סיסמא וניהול משתמשים בצורה מאובטחת." : "No problem! In the real system, I am connected to the API and can send password reset links and manage users securely.";
            }
        } else if (activeK === "inventory") {
            if (q.includes("מלאי") || q.includes("מוצר") || q.includes("חסר") || q.includes("הזמנה")) {
                reply = isHe ? "אני סורק את מערכת ניהול המלאי (ERP) בכל רגע. אם מוצר עומד לאזול, אני אוטומטית מכין הצעת הזמנה לספק ומתריע למנהלים. 📦" : "I scan the ERP inventory constantly. If an item is running low, I automatically draft a PO for the supplier and alert managers. 📦";
            } else if (q.includes("ספקים") || q.includes("משלוח") || q.includes("מעקב")) {
                reply = isHe ? "אני יכול לעקוב אחרי משלוחים פתוחים, לשלוח מיילים לספקים במידה ויש עיכוב, ולעדכן את הלקוחות בסטטוס ההזמנה שלהם." : "I can track open shipments, email suppliers about delays, and update customers on their order status.";
            }
        }
      }
      
      // Default fallback
      if (!reply) {
         reply = isHe
          ? `שאלה מעולה! כסוכן ה**${list.find(a=>a.k===activeK)?.name}** (דמו) אני מדגים רק חלק מהיכולות שלי. במערכת האמיתית, עם חיבור למאגר הידע שלכם ולמערכות ה-API, אוכל לתת מענה עשיר ומדויק יותר לשאלה הזאת. ✨`
          : `Great question! As the **${list.find(a=>a.k===activeK)?.name}** (demo) agent, I'm showcasing a subset of my skills. In the real system, connected to your knowledge base and APIs, I can provide a much richer response to this. ✨`;
      }
      
      setMessages(prev => [...prev, { role: "bot", text: reply }]);
    }, 1000 + Math.random() * 800); // realistic typing delay
  };"""

        start_idx = text.find("const submitUser = () => {")
        end_idx = text.find("const render = (txt)", start_idx)
        
        if start_idx != -1 and end_idx != -1:
            text = text[:start_idx] + new_submit_user + "\n\n  " + text[end_idx:]
            
            new_data = text.encode('utf-8')
            if entry.get('compressed'):
                new_data = gzip.compress(new_data)
            entry['data'] = base64.b64encode(new_data).decode('utf-8')

            new_manifest_json = json.dumps(manifest, separators=(',', ':'))
            new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
            
            with open('onstaffai.html', 'w', encoding='utf-8') as out:
                out.write(new_html)
            print("Successfully updated demo logic.")
        else:
            print("Could not find submitUser function bounds.")
else:
    print("Manifest not found")
