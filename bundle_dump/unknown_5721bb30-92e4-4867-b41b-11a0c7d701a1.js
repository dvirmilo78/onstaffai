// src/demo.jsx — live agent demo chat
const LiveDemo = ({ head, agents, scripts, lang, ctaLabel }) => {
  const demoable = ["reception", "finance", "marketing", "techsupport", "inventory"];
  const list = agents.filter(a => demoable.includes(a.k));
  const [activeK, setActiveK] = React.useState("reception");
  const [messages, setMessages] = React.useState([]);
  const [typing, setTyping] = React.useState(false);
  const [input, setInput] = React.useState("");
  const timers = React.useRef([]);

  const playScript = (k) => {
    timers.current.forEach(clearTimeout); timers.current = [];
    setMessages([]); setTyping(false);
    const script = scripts[lang][k] || scripts.he[k];
    script.forEach((m, i) => {
      const delay = 600 + i * 1400;
      if (m.b) {
        timers.current.push(setTimeout(() => setTyping(true), delay - 400));
        timers.current.push(setTimeout(() => {
          setTyping(false);
          setMessages(prev => [...prev, { role: "bot", text: m.b }]);
        }, delay));
      } else {
        timers.current.push(setTimeout(() => {
          setMessages(prev => [...prev, { role: "user", text: m.u }]);
        }, delay));
      }
    });
  };

  React.useEffect(() => { playScript(activeK); return () => timers.current.forEach(clearTimeout); }, [activeK, lang]);

  const submitUser = () => {
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
      }
      
      setMessages(prev => [...prev, { role: "bot", text: reply }]);
    }, 1200 + Math.random() * 800);
  };

  const render = (txt) => {
    const parts = txt.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((p, i) => p.startsWith("**") ? <b key={i}>{p.slice(2, -2)}</b> : <span key={i}>{p}</span>);
  };

  return (
    <section id="demo">
      <div className="wrap">
        <SectionHead {...head}/>
        <div className="demo-wrap">
          <style>{`
          .tech-pulse {
            animation: pulseTech 1.5s infinite;
          }
          @keyframes pulseTech {
            0% { box-shadow: 0 0 0 0 var(--sky); }
            70% { box-shadow: 0 0 0 8px transparent; }
            100% { box-shadow: 0 0 0 0 transparent; }
          }
        `}</style><div className="demo-sidebar">
            <h4>{lang === "he" ? "בחר סוכן" : "Pick an agent"}</h4>
            <div className="demo-list">
              {list.map(a => (
                <button key={a.k} className={"demo-item" + (activeK === a.k ? " on" : "")} onClick={() => setActiveK(a.k)}>
                  <span className={"dot" + (a.k === "techsupport" ? " tech-pulse" : "")} style={{ background: a.color }}/>
                  <span>{a.name}</span>
                </button>
              ))}
            </div>
            <div style={{ marginTop: 28, padding: 14, borderRadius: 12, background: "var(--card)", border: "1px solid var(--line)", fontSize: 12, color: "var(--mute)", lineHeight: 1.5 }}>
              {lang === "he"
                ? "זה דמו. בתצורה אמיתית הסוכן מחובר למערכות שלך, מכיר את הלקוחות ויש לו גישה לנתונים בזמן אמת."
                : "This is a demo. In production, the agent is connected to your systems, knows your customers, and has real-time data access."}
            </div>
          </div>
          <div className="demo-chat">
            {messages.map((m, i) => (
              <React.Fragment key={i}>
                <div className={"msg " + m.role}>{render(m.text).map((el, j) => <React.Fragment key={j}>{el.props.children.split ? el.props.children.split("\n").map((line, k) => <React.Fragment key={k}>{k>0 && <br/>}{line}</React.Fragment>) : el}</React.Fragment>)}</div>
                {m.role === "bot" && <div className="msg-meta">● {lang === "he" ? "סוכן" : "agent"} · {(Math.random()*0.7+0.3).toFixed(1)}s</div>}
              </React.Fragment>
            ))}
            {typing && (
              <div className="msg bot">
                <div className="typing"><span/><span/><span/></div>
              </div>
            )}
            <div className="demo-input">
              <input
                placeholder={lang === "he" ? "כתוב הודעה…" : "Type a message…"}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && submitUser()}
              />
              <button onClick={submitUser} aria-label="send">
                <svg width="16" height="16" viewBox="0 0 16 16"><path d="M2 8 L14 2 L10 14 L8 9 L2 8Z" fill="currentColor"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

Object.assign(window, { LiveDemo });
