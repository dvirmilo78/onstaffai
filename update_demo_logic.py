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
    
    uuid = "5721bb30-92e4-4867-b41b-11a0c7d701a1"
    if uuid in manifest:
        entry = manifest[uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # New submitUser implementation
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
      
      // Basic keyword matching
      if (q.includes("מחיר") || q.includes("עולה") || q.includes("כסף") || q.includes("price") || q.includes("cost")) {
        reply = isHe ? "העלות שלי היא שבריר מעלות של עובד אנושי ממוצע, וההחזר על ההשקעה (ROI) בדרך כלל מכסה את עצמו כבר בחודש הראשון. אפשר לראות פירוט במחירון שלנו." : "I cost a fraction of a human employee, and the ROI usually covers the cost in the first month. Check our pricing section.";
      } else if (q.includes("אינטגרציה") || q.includes("מערכות") || q.includes("חיבור") || q.includes("integrate") || q.includes("system")) {
        reply = isHe ? "אני מתחבר בקלות לכל המערכות שאתה כבר עובד איתן - WhatsApp, יומן גוגל, CRM, מערכות סליקה ועוד. ההטמעה לוקחת דקות." : "I integrate seamlessly with your existing tools - WhatsApp, Google Calendar, CRM, billing, and more. Setup takes minutes.";
      } else if (q.includes("שעות") || q.includes("זמינות") || q.includes("hours") || q.includes("available")) {
        reply = isHe ? "אני עובד 24/7, בלי הפסקות צהריים, בלי ימי מחלה או חופשות. תמיד כאן כשהלקוחות שלך צריכים אותי." : "I work 24/7, with no lunch breaks, sick days, or vacations. Always here when your customers need me.";
      } else {
        // Agent specific fallback logic
        if (activeK === "reception") {
            if (q.includes("לקוחות") || q.includes("פגישות") || q.includes("לקבוע")) {
                reply = isHe ? "אני מנהלת את כל הפניות הראשוניות, מסננת לקוחות לא רלוונטיים, וקובעת פגישות ישירות ביומן שלך בלי שתצטרך להתערב." : "I handle all initial inquiries, filter out irrelevant leads, and book meetings directly into your calendar.";
            }
        } else if (activeK === "finance") {
            if (q.includes("חשבון") || q.includes("גבייה") || q.includes("לשלם")) {
                reply = isHe ? "אני עוקב אחרי כל התשלומים, שולח תזכורות חכמות על חובות פתוחים ואוסף את הכספים בצורה אוטומטית ומנומסת." : "I track all payments, send smart reminders for open debts, and collect funds automatically and politely.";
            }
        } else if (activeK === "marketing") {
            if (q.includes("לידים") || q.includes("מיילים") || q.includes("קמפיין")) {
                reply = isHe ? "אני לוקחת לידים קרים ומחממת אותם דרך שיחות ווטסאפ וסדרות אימיילים מותאמות אישית עד שהם מוכנים לסגירה." : "I take cold leads and warm them up via WhatsApp and personalized email sequences until they are ready to close.";
            }
        }
      }
      
      // Default fallback
      if (!reply) {
         reply = isHe
          ? `שאלה מצוינת. כסוכן **${list.find(a=>a.k===activeK)?.name}** המומחיות שלי כוללת גם את זה. במערכת האמיתית אוכל לבצע פעולות מורכבות יותר ברגע שאתחבר לעסק שלך.`
          : `Great question. As the **${list.find(a=>a.k===activeK)?.name}** agent, my expertise covers exactly that. In the real system, I can perform complex actions once connected.`;
      }
      
      setMessages(prev => [...prev, { role: "bot", text: reply }]);
    }, 1200 + Math.random() * 800); // realistic typing delay
  };"""

        # Replace the old submitUser function
        # The old function starts with "const submitUser = () => {" and ends at the next "const render"
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
            
            with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
                out.write(new_html)
            print("Successfully updated demo logic.")
        else:
            print("Could not find submitUser function bounds.")
else:
    print("Manifest not found")
