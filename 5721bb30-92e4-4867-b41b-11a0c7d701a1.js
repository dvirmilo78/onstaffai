// src/demo.jsx — live agent demo chat
const LiveDemo = ({ head, agents, scripts, lang, ctaLabel }) => {
  const demoable = ["reception", "finance", "marketing"];
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
    const q = input;
    setInput("");
    setTyping(true);
    setTimeout(() => {
      setTyping(false);
      const reply = lang === "he"
        ? `תודה על השאלה. כסוכן **${list.find(a=>a.k===activeK)?.name}** — זה בדיוק במסגרת המומחיות שלי. אשמח לענות בפירוט אחרי חיבור ראשוני לעסק שלך. נתחיל?`
        : `Thanks for asking. As the **${list.find(a=>a.k===activeK)?.name}** agent — that's right in my lane. Happy to dive in once I'm connected to your business. Shall we start?`;
      setMessages(prev => [...prev, { role: "bot", text: reply }]);
    }, 1500);
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
          <div className="demo-sidebar">
            <h4>{lang === "he" ? "בחר סוכן" : "Pick an agent"}</h4>
            <div className="demo-list">
              {list.map(a => (
                <button key={a.k} className={"demo-item" + (activeK === a.k ? " on" : "")} onClick={() => setActiveK(a.k)}>
                  <span className="dot" style={{ background: a.color }}/>
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
