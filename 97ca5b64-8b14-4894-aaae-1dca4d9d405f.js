// src/data.jsx — all copy in HE + EN
const t = {
  he: {
    nav: { agents: "סוכנים", how: "איך זה עובד", roi: "חישוב חיסכון", demo: "דמו חי", pricing: "מחירון", login: "התחברות" },
    cta: { primary: "התחל חינם", secondary: "צפה בדמו", talk: "דבר עם סוכן" },
    hero: {
      eyebrow: "12 סוכנים. אפס גיוסים.",
      variants: [
        { h: ["החלף", "עובדים", "בסוכנים."], sub: "סוכני AI שעונים ללקוחות, סוגרים פגישות, מנהלים כספים ומשווקים את העסק — 24/7, בעלות של כוס קפה ליום." },
        { h: ["צוות שלם,", "בלי תלושים.", ""], sub: "12 סוכנים חכמים מחליפים משרדים שלמים. מתחילים לעבוד תוך 10 דקות." },
        { h: ["העסק שלך,", "על אוטומט.", ""], sub: "אוטומציה שחוסכת 60 שעות בשבוע. מענה, שיווק, פיננסים — הכל במקום אחד." },
      ],
      trust: "מעל 2,400 עסקים כבר חסכו",
    },
    metrics: [
      { num: "₪28,400", lbl: "חיסכון חודשי ממוצע" },
      { num: "60 שעות", lbl: "בשבוע חוזרות אליך" },
      { num: "24/7", lbl: "זמינות מלאה" },
      { num: "10 דק׳", lbl: "להתחלה מלאה" },
    ],
    agentsHead: { tag: "// הסל המלא", h: "12 סוכנים. סל אחד.", p: "כל סוכן הוא מומחה בתחומו. הם מדברים ביניהם, חולקים נתונים, ועובדים כמו צוות אמיתי." },
    howHead: { tag: "// תהליך", h: "מהרישום לסוכן עובד בפחות מרבע שעה.", p: "התהליך פשוט בכוונה. לא צריך מפתחים, לא צריך אינטגרציות מסובכות." },
    how: [
      { t: "בוחרים סוכן", d: "מתוך 12 סוכנים מוכנים לעבודה. אפשר להתחיל מאחד, להוסיף עוד בכל עת." },
      { t: "מלמדים אותו", d: "מזינים את פרטי העסק, טון הדיבור ושאלות נפוצות. לוקח 5 דקות." },
      { t: "מחברים ערוצים", d: "וואטסאפ, מייל, אתר, אינסטגרם. חיבור בלחיצת כפתור." },
      { t: "נהנים מהתוצאות", d: "הסוכן מתחיל לעבוד מיד. אתם מקבלים דוחות שבועיים." },
    ],
    roiHead: { tag: "// חישוב חיסכון", h: "כמה OnStaffAI יחסוך לך?", p: "הזיזו את הסליידרים. המספרים אמיתיים, מבוססים על נתוני לקוחות." },
    roi: {
      employees: "כמה עובדים עונים ללקוחות?",
      hours: "שעות בשבוע על משימות חוזרות",
      salary: "שכר חודשי ממוצע (₪)",
      result: "חיסכון שנתי",
      monthly: "חיסכון חודשי",
      time: "שעות שחזרו אליך",
      productivity: "עליה בפרודוקטיביות",
      note: "מבוסס על דגימה של 820 לקוחות OnStaffAI ב-12 החודשים האחרונים.",
    },
    demoHead: { tag: "// דמו חי", h: "נסה לדבר עם סוכן.", p: "בחר סוכן, שלח הודעה, קבל תשובה אמיתית תוך שניות." },
    quotesHead: { tag: "// לקוחות מספרים", h: "חסכו חודשים של עבודה. תוך שבועות.", p: "לקוחות אמיתיים, חיסכון אמיתי. סיפורי הצלחה מתעדכנים כל חודש." },
    quotes: [
      { body: "הסוכן של מענה ללקוחות ענה ל-1,400 שיחות בחודש הראשון. חסכנו את העלות של שני עובדים, ולקוחות מקבלים תשובה תוך 12 שניות.", name: "מאיה לביא", role: "מנכ״לית, Cloud9 Studios", metric: "−₪32,000/חודש", color: "var(--butter)" },
      { body: "הסוכן הפיננסי סוגר לנו את החודש עצמאית. התאמות בנק, דוחות, התראות על חריגות — דברים שלקחו 3 ימים, עכשיו זה 20 דקות.", name: "יוסי ברק", role: "בעלים, Barak Plumbing", metric: "3 ימים → 20 דק׳", color: "var(--sky)" },
      { body: "הסוכן השיווקי כותב לנו 30 פוסטים בחודש, משגר קמפיינים במייל ומנתח תוצאות. ה-ROI שלנו עלה פי 4 ברבעון הראשון.", name: "דנה כהן", role: "VP מרקטינג, Tzela Beauty", metric: "ROI x4", color: "var(--mint)" },
    ],
    pricingHead: { tag: "// מחירון", h: "תשלום לפי שימוש. בלי הפתעות.", p: "אין חוזים שנתיים, אין עמלות הקמה. משדרגים ומורידים בכל עת." },
    plans: [
      { name: "התחלה", badge: "START", price: "₪490", unit: "/חודש", feats: ["עד 2 סוכנים", "1,000 אינטראקציות בחודש", "חיבור לוואטסאפ ומייל", "תמיכה בצ'אט", "דוחות שבועיים"], cta: "התחל חינם" },
      { name: "צמיחה", badge: "POPULAR", price: "₪1,490", unit: "/חודש", feats: ["עד 6 סוכנים", "10,000 אינטראקציות", "כל הערוצים + CRM", "תמיכה בטלפון 24/6", "אוטומציות מותאמות", "ניתוח מתקדם"], cta: "בחר צמיחה", featured: true },
      { name: "ארגוני", badge: "SCALE", price: "לפי בקשה", unit: "", feats: ["כל 12 הסוכנים", "אינטראקציות ללא הגבלה", "איש קשר ייעודי", "אינטגרציות מותאמות", "SLA של 99.9%", "הדרכות צוות"], cta: "דבר איתנו" },
    ],
    faqHead: { tag: "// שאלות נפוצות", h: "יש לך שאלות. יש לנו תשובות." },
    faq: [
      { q: "כמה זמן לוקח להטמיע סוכן?", a: "רוב הלקוחות מעלים סוכן ראשון לאוויר תוך 10-15 דקות. מילוי פרטי העסק, בחירת טון, וחיבור לוואטסאפ או מייל — זה כל התהליך. סוכנים מורכבים יותר (כמו הסוכן הפיננסי) עשויים לדרוש חצי יום של לימוד על נתוני העסק." },
      { q: "הסוכנים מדברים עברית?", a: "כן. כל 12 הסוכנים מדברים עברית, אנגלית וערבית ברמת שפת-אם. הם מבינים סלנג, מונחים מקצועיים, ואפילו מבטאים שונים בשיחות טלפון." },
      { q: "מה קורה כשהסוכן לא יודע תשובה?", a: "הסוכן מודה שהוא לא יודע, מבקש פרטים, ומעביר את הפנייה לבן אדם — עם סיכום של השיחה והמלצה לתשובה. אפס ניסיונות להמציא תשובות." },
      { q: "אפשר לבטל בכל עת?", a: "כן, אין חוזים. מבטלים מהלוח בקליק אחד. כל הנתונים נשארים שלך לייצוא בפורמט JSON/CSV." },
      { q: "איך שומרים על פרטיות הלקוחות?", a: "אנחנו תואמים GDPR ומאחסנים נתונים רק בישראל/האיחוד האירופי. הצפנת AES-256, ביקורות אבטחה רבעוניות, ונתונים אף פעם לא משמשים לאימון מודלים." },
      { q: "אפשר לחבר למערכת ה-CRM הקיימת?", a: "כן. יש אינטגרציות מוכנות ל-Salesforce, HubSpot, Monday, Priority, SAP ועוד 40+ מערכות. אם המערכת שלך לא ברשימה — אנחנו בונים חיבור תוך 48 שעות." },
    ],
    ctaBanner: { h: "העסק שלך מחכה לסוכן שלו.", p: "14 ימי ניסיון חינם. בלי כרטיס אשראי. בלי מחויבות.", btn: "התחל עכשיו, חינם" },
    footer: {
      tagline: "סוכני AI לעסקים שרוצים לרוץ.",
      cols: [
        { h: "מוצר", links: ["סוכנים", "מחירון", "אינטגרציות", "דמו חי", "מה חדש"] },
        { h: "חברה", links: ["אודות", "לקוחות", "קריירה", "בלוג", "צור קשר"] },
        { h: "משאבים", links: ["מרכז עזרה", "API", "סטטוס", "אבטחה", "תנאי שימוש"] },
      ],
      copy: "© 2026 OnStaffAI. כל הזכויות שמורות. עשוי בישראל.",
    },
  },
  en: {
    nav: { agents: "Agents", how: "How it works", roi: "ROI", demo: "Live demo", pricing: "Pricing", login: "Sign in" },
    cta: { primary: "Start free", secondary: "Watch demo", talk: "Talk to an agent" },
    hero: {
      eyebrow: "12 agents. Zero hiring.",
      variants: [
        { h: ["Replace", "employees", "with agents."], sub: "AI agents that answer customers, close meetings, manage finances, and market your business — 24/7, for the cost of a coffee per day." },
        { h: ["A full team,", "without payroll.", ""], sub: "12 smart agents replace whole departments. Up and running in 10 minutes." },
        { h: ["Your business,", "on autopilot.", ""], sub: "Automation that saves 60 hours a week. Support, marketing, finance — all in one place." },
      ],
      trust: "2,400+ businesses already saving",
    },
    metrics: [
      { num: "$7,800", lbl: "Avg. monthly savings" },
      { num: "60 hrs", lbl: "Back on your calendar" },
      { num: "24/7", lbl: "Always on" },
      { num: "10 min", lbl: "To get started" },
    ],
    agentsHead: { tag: "// The full roster", h: "12 agents. One basket.", p: "Each agent is a specialist. They talk to each other, share data, and work like a real team." },
    howHead: { tag: "// Process", h: "From signup to a working agent in 15 minutes.", p: "Built to be simple. No developers, no painful integrations." },
    how: [
      { t: "Pick an agent", d: "From 12 ready-to-go agents. Start with one, add more anytime." },
      { t: "Teach it", d: "Feed your business details, tone of voice, and FAQs. Takes 5 minutes." },
      { t: "Connect channels", d: "WhatsApp, email, website, Instagram. One-click setup." },
      { t: "Reap the results", d: "Your agent starts working immediately. Weekly reports land in your inbox." },
    ],
    roiHead: { tag: "// Savings calculator", h: "How much will OnStaffAI save you?", p: "Slide the sliders. The numbers are real, based on actual customer data." },
    roi: {
      employees: "Employees handling customer messages",
      hours: "Hours/week on repetitive tasks",
      salary: "Avg. monthly salary ($)",
      result: "Annual savings",
      monthly: "Monthly savings",
      time: "Hours reclaimed",
      productivity: "Productivity lift",
      note: "Based on a sample of 820 OnStaffAI customers over the last 12 months.",
    },
    demoHead: { tag: "// Live demo", h: "Try talking to an agent.", p: "Pick an agent, send a message, get a real answer in seconds." },
    quotesHead: { tag: "// Customer stories", h: "Save months of work. In weeks.", p: "Real customers, real savings. Updated monthly." },
    quotes: [
      { body: "The support agent handled 1,400 calls in the first month. We saved two full-time hires, and customers get an answer in 12 seconds.", name: "Maya Levi", role: "CEO, Cloud9 Studios", metric: "−$8,700/mo", color: "var(--butter)" },
      { body: "The finance agent closes our books on its own. Reconciliations, reports, flagging anomalies — a 3-day job is now 20 minutes.", name: "Yossi Barak", role: "Owner, Barak Plumbing", metric: "3 days → 20 min", color: "var(--sky)" },
      { body: "The marketing agent writes 30 posts a month, runs our email campaigns, and analyzes results. ROI jumped 4× in the first quarter.", name: "Dana Cohen", role: "VP Marketing, Tzela Beauty", metric: "ROI ×4", color: "var(--mint)" },
    ],
    pricingHead: { tag: "// Pricing", h: "Pay as you use. No surprises.", p: "No annual contracts, no setup fees. Upgrade or downgrade anytime." },
    plans: [
      { name: "Start", badge: "START", price: "$139", unit: "/mo", feats: ["Up to 2 agents", "1,000 interactions/mo", "WhatsApp + email", "Chat support", "Weekly reports"], cta: "Start free" },
      { name: "Growth", badge: "POPULAR", price: "$420", unit: "/mo", feats: ["Up to 6 agents", "10,000 interactions", "All channels + CRM", "Phone support 24/6", "Custom automations", "Advanced analytics"], cta: "Choose Growth", featured: true },
      { name: "Enterprise", badge: "SCALE", price: "Custom", unit: "", feats: ["All 12 agents", "Unlimited interactions", "Dedicated CSM", "Custom integrations", "99.9% SLA", "Team training"], cta: "Talk to us" },
    ],
    faqHead: { tag: "// FAQ", h: "You have questions. We have answers." },
    faq: [
      { q: "How long does onboarding take?", a: "Most customers go live with their first agent in 10-15 minutes. Fill in business details, pick a tone, connect WhatsApp or email — that's it. More complex agents (like Finance) may need half a day to learn your data." },
      { q: "Do agents speak Hebrew?", a: "Yes. All 12 agents speak Hebrew, English, and Arabic at native level. They understand slang, professional jargon, and even different accents on phone calls." },
      { q: "What if the agent doesn't know an answer?", a: "It admits it doesn't know, asks for context, and hands off to a human — with a conversation summary and suggested reply. Zero hallucinations." },
      { q: "Can I cancel anytime?", a: "Yes, no contracts. Cancel from the dashboard with one click. All data stays yours — exportable as JSON/CSV." },
      { q: "How do you handle customer privacy?", a: "We're GDPR compliant and store data only in Israel/EU. AES-256 encryption, quarterly security audits, and your data is never used to train models." },
      { q: "Can I connect my existing CRM?", a: "Yes. Ready-made integrations with Salesforce, HubSpot, Monday, Priority, SAP and 40+ more. If yours isn't listed, we build the connector in 48 hours." },
    ],
    ctaBanner: { h: "Your business is waiting for its agent.", p: "14-day free trial. No credit card. No commitment.", btn: "Start for free" },
    footer: {
      tagline: "AI agents for businesses that want to run.",
      cols: [
        { h: "Product", links: ["Agents", "Pricing", "Integrations", "Live demo", "What's new"] },
        { h: "Company", links: ["About", "Customers", "Careers", "Blog", "Contact"] },
        { h: "Resources", links: ["Help center", "API", "Status", "Security", "Terms"] },
      ],
      copy: "© 2026 OnStaffAI. All rights reserved. Made in Israel.",
    },
  },
};

// 12 agents — colors map to palette tokens, each has a unique illustration key
const AGENTS_HE = [
  { k: "reception", name: "סוכן מענה ללקוחות", short: "SUPPORT", desc: "עונה בצ׳אט, מייל ובטלפון. מבין את המוצר שלך, פותר בעיות, מעביר לבן אדם כשצריך.", stats: [["זמן תגובה","12ש׳"],["שפות","9"]], color: "var(--butter)" },
  { k: "scheduler", name: "סוכן תיאום פגישות", short: "SCHEDULE", desc: "מתאם פגישות עם לקוחות, שולח תזכורות, מנהל ביטולים — סנכרון מלא עם Google ו-Outlook.", stats: [["מעודכן","בזמן אמת"],["שיעור הגעה","+41%"]], color: "var(--sky)" },
  { k: "marketing", name: "סוכן שיווק", short: "MARKETING", desc: "כותב פוסטים, מריץ קמפיינים, מנתח תוצאות. יודע מתי לכתוב ובאיזה טון — מתאים לקהל שלך.", stats: [["פוסטים/חודש","30"],["ROI ממוצע","x4.2"]], color: "var(--rose)" },
  { k: "finance", name: "סוכן פיננסי", short: "FINANCE", desc: "סגירת חודש, התאמות בנק, דוחות מס, זיהוי חריגות. עובד עם כל תוכנות ההנה״ח הישראליות.", stats: [["זמן סגירה","20 דק׳"],["דיוק","99.6%"]], color: "var(--mint)" },
  { k: "sales", name: "סוכן מכירות", short: "SALES", desc: "מחמם לידים, שולח הצעות מחיר, סוגר עסקאות פשוטות בעצמו. יודע מתי לערב מוכר אנושי.", stats: [["שיחות/יום","∞"],["המרה","+28%"]], color: "var(--violet)" },
  { k: "hr", name: "סוכן גיוס ו-HR", short: "HR", desc: "מסנן קורות חיים, מזמן לראיונות, עונה על שאלות עובדים. מנהל את תיקי הכ״א.", stats: [["קו״ח/שבוע","400"],["זמן גיוס","-60%"]], color: "var(--lime)" },
  { k: "data", name: "סוכן נתונים ו-BI", short: "DATA", desc: "מושך נתונים מכל המערכות, בונה דוחות, מזהה טרנדים. ״שאל אותו״ בעברית בלבד.", stats: [["מקורות","40+"],["דוחות","אוטומטי"]], color: "var(--butter)" },
  { k: "techsupport", name: "סוכן תמיכה טכנית", short: "TECH", desc: "פותר בעיות טכניות, כותב מדריכים, פותח טיקטים. יודע לזהות באג אמיתי מול בלבול משתמש.", stats: [["פתרון L1","87%"],["זמינות","24/7"]], color: "var(--sky)" },
  { k: "inventory", name: "סוכן מלאי ורכש", short: "INVENTORY", desc: "עוקב אחרי מלאי, מזמין חידוש אוטומטית, מנהל קשר עם ספקים. מתריע לפני שנגמר.", stats: [["חיסכון","-18%"],["ספקים","∞"]], color: "var(--mint)" },
  { k: "collect", name: "סוכן גבייה ותזכורות", short: "COLLECT", desc: "שולח תזכורות עדינות על חובות, מציע פריסות תשלום, מעדכן את המערכת. עם הרבה טאקט.", stats: [["גבייה","+34%"],["שיחות מביכות","0"]], color: "var(--rose)" },
  { k: "content", name: "סוכן כתיבת תוכן", short: "CONTENT", desc: "פוסטים לבלוג, תיאורי מוצר, ניוזלטרים, מיילים. תמיד בקול של המותג שלך.", stats: [["מילים/חודש","80K"],["בדיקה אנוש","0"]], color: "var(--violet)" },
  { k: "translate", name: "סוכן תרגום ולוקליזציה", short: "TRANSLATE", desc: "תרגום אתר, מוצרים ושיחות ל-47 שפות. שומר על ניואנסים תרבותיים, לא רק מילים.", stats: [["שפות","47"],["זמן","בזמן אמת"]], color: "var(--lime)" },
];

const AGENTS_EN = [
  { k: "reception", name: "Customer Support", short: "SUPPORT", desc: "Answers chat, email, and phone. Knows your product, resolves issues, hands off when needed.", stats: [["Response","12s"],["Languages","9"]], color: "var(--butter)" },
  { k: "scheduler", name: "Scheduling", short: "SCHEDULE", desc: "Books meetings, sends reminders, manages cancellations — full sync with Google and Outlook.", stats: [["Realtime","yes"],["Show rate","+41%"]], color: "var(--sky)" },
  { k: "marketing", name: "Marketing", short: "MARKETING", desc: "Writes posts, runs campaigns, analyzes results. Knows when and how to write — matched to your audience.", stats: [["Posts/mo","30"],["Avg ROI","×4.2"]], color: "var(--rose)" },
  { k: "finance", name: "Finance", short: "FINANCE", desc: "Month-end close, bank reconciliations, tax reports, anomaly detection. Works with every Israeli accounting system.", stats: [["Close","20 min"],["Accuracy","99.6%"]], color: "var(--mint)" },
  { k: "sales", name: "Sales", short: "SALES", desc: "Warms leads, sends quotes, closes simple deals on its own. Knows when to loop in a human.", stats: [["Calls/day","∞"],["Conv.","+28%"]], color: "var(--violet)" },
  { k: "hr", name: "HR & Recruiting", short: "HR", desc: "Screens résumés, schedules interviews, answers employee questions. Manages personnel files.", stats: [["CVs/wk","400"],["Time-to-hire","-60%"]], color: "var(--lime)" },
  { k: "data", name: "Data & BI", short: "DATA", desc: "Pulls data from every system, builds reports, spots trends. Ask it anything in plain language.", stats: [["Sources","40+"],["Reports","auto"]], color: "var(--butter)" },
  { k: "techsupport", name: "Tech Support", short: "TECH", desc: "Fixes technical issues, writes docs, opens tickets. Tells real bugs from user confusion.", stats: [["L1 solve","87%"],["Uptime","24/7"]], color: "var(--sky)" },
  { k: "inventory", name: "Inventory & Procurement", short: "INVENTORY", desc: "Tracks inventory, auto-reorders, manages suppliers. Alerts you before you run out.", stats: [["Savings","-18%"],["Vendors","∞"]], color: "var(--mint)" },
  { k: "collect", name: "Collections & Reminders", short: "COLLECT", desc: "Sends gentle reminders, offers payment plans, updates the books. With plenty of tact.", stats: [["Collection","+34%"],["Awkward calls","0"]], color: "var(--rose)" },
  { k: "content", name: "Content Writing", short: "CONTENT", desc: "Blog posts, product descriptions, newsletters, emails. Always in your brand voice.", stats: [["Words/mo","80K"],["Human edits","0"]], color: "var(--violet)" },
  { k: "translate", name: "Translation & Localization", short: "TRANSLATE", desc: "Translates sites, products, and conversations into 47 languages. Keeps cultural nuance, not just words.", stats: [["Languages","47"],["Speed","realtime"]], color: "var(--lime)" },
];

// demo conversation scripts, per agent key
const DEMO_SCRIPTS = {
  he: {
    reception: [
      { u: "היי, האם המשלוח שלי יוצא היום?" },
      { b: "שלום חני 👋 בדקתי — ההזמנה #4821 שלך יוצאת היום ב-14:30 עם שליח **דוד**. קישור למעקב יגיע ב-SMS בעוד כ-30 דקות. צריכה עוד משהו?" },
    ],
    finance: [
      { u: "מה מצב הסגירה של חודש מרץ?" },
      { b: "מרץ סגור ✅ הכנסות: **₪248,340** (+12% מול פברואר). הוצאות: ₪112,700. הרווח הגולמי: **₪135,640**. זיהיתי 3 חריגות בחשבון ספק שדורשות את אישורך — לשלוח לך לניקוד?" },
    ],
    marketing: [
      { u: "תכין לי 3 כיוונים לקמפיין של קיץ" },
      { b: "על הדרך:\n\n**1. ״קיץ בלי תורים״** — מבליט את החיסכון בזמן. טון חברי.\n**2. ״הכירו את הצוות הדיגיטלי״** — מספר על הסוכנים כ-״עובדים חדשים״.\n**3. ״0₪ לעבודה, 24/7 לתוצאות״** — השוואה ישירה למחיר שכר.\n\nאיזה מהם נרוץ לראשון?" },
    ],
  },
  en: {
    reception: [
      { u: "Hey, is my order shipping today?" },
      { b: "Hi Chani 👋 Checked — your order #4821 ships today at 2:30 PM with our courier **David**. Tracking link arrives by SMS in ~30 minutes. Anything else?" },
    ],
    finance: [
      { u: "What's the March close looking like?" },
      { b: "March is closed ✅ Revenue: **$68,900** (+12% vs Feb). Expenses: $31,300. Gross profit: **$37,600**. I flagged 3 anomalies on one vendor account that need your sign-off — want me to summarize them?" },
    ],
    marketing: [
      { u: "Draft me 3 directions for the summer campaign" },
      { b: "Here you go:\n\n**1. ″No queues this summer″** — highlights time savings. Friendly tone.\n**2. ″Meet the digital team″** — presents the agents as new hires.\n**3. ″$0 for the work, 24/7 for the results″** — direct comparison to payroll.\n\nWhich one runs first?" },
    ],
  },
};

Object.assign(window, { T: t, AGENTS_HE, AGENTS_EN, DEMO_SCRIPTS });
