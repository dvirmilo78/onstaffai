// src/hero.jsx — hero section with looping SVG/CSS animated "video"
const HeroVideo = ({ animKind = "charts", lang = "he" }) => {
  // three animation flavors: flow (network), charts (dashboard), orbit (agents around user)
  return (
    <div className="hero-video" aria-label="agents working animation">
      <div className="video-chrome">
        <span className="video-dot" style={{ background: "#ff5f57" }}/>
        <span className="video-dot" style={{ background: "#febc2e" }}/>
        <span className="video-dot" style={{ background: "#28c840" }}/>
        <span className="video-label">onstaffai.live · real-time</span>
        <span className="video-live">{lang === "he" ? "LIVE" : "LIVE"}</span>
      </div>
      <div className="video-stage">
        {animKind === "flow" && <FlowAnim lang={lang}/>}
        {animKind === "charts" && <ChartsAnim lang={lang}/>}
        {animKind === "orbit" && <OrbitAnim lang={lang}/>}
      </div>
    </div>
  );
};

const FlowAnim = ({ lang }) => {
  // central hub with incoming channels + outgoing actions
  const ink = "var(--ink)";
  const labels = lang === "he"
    ? { wa: "וואטסאפ", mail: "מייל", ig: "אינסטגרם", phone: "טלפון", crm: "CRM", cal: "יומן", pay: "תשלום", hub: "OnStaffAI" }
    : { wa: "WhatsApp", mail: "Email", ig: "Instagram", phone: "Phone", crm: "CRM", cal: "Calendar", pay: "Billing", hub: "OnStaffAI" };
  return (
    <svg viewBox="0 0 500 400" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
      {/* dotted paths */}
      <g fill="none" stroke="var(--accent)" strokeWidth="2" className="anim-flow-path" opacity=".8">
        <path d="M80 80 Q170 120 240 190"/>
        <path d="M80 320 Q170 280 240 210"/>
        <path d="M420 80 Q330 120 260 190"/>
        <path d="M420 320 Q330 280 260 210"/>
      </g>
      {/* channel chips */}
      {[
        { x: 40, y: 60, emoji: "💬", label: labels.wa, color: "var(--mint)" },
        { x: 40, y: 300, emoji: "✉", label: labels.mail, color: "var(--sky)" },
        { x: 380, y: 60, emoji: "📞", label: labels.phone, color: "var(--butter)" },
        { x: 380, y: 300, emoji: "🧾", label: labels.pay, color: "var(--rose)" },
      ].map((c, i) => (
        <g key={i} transform={`translate(${c.x},${c.y})`} className="wiggle" style={{ animationDelay: `${i*0.4}s` }}>
          <rect width="86" height="36" rx="10" fill={c.color} stroke={ink} strokeWidth="2"/>
          <text x="14" y="24" fontSize="16">{c.emoji}</text>
          <text x="36" y="24" fontSize="13" fontWeight="600" fill={ink} fontFamily="Heebo">{c.label}</text>
        </g>
      ))}
      {/* central hub */}
      <g transform="translate(250 200)">
        <circle r="76" fill="none" stroke={ink} strokeWidth="1.5" strokeDasharray="3 5" className="orbit" style={{transformOrigin:'center'}}/>
        <circle r="56" fill={ink}/>
        <circle r="48" fill="var(--accent)"/>
        <text y="-2" textAnchor="middle" fontSize="13" fontWeight="700" fill="var(--ink)" fontFamily="Space Grotesk">AGENT</text>
        <text y="14" textAnchor="middle" fontSize="10" fill="var(--ink)" fontFamily="JetBrains Mono">● thinking</text>
      </g>
      {/* moving dots on paths */}
      {[
        { cx: 80, cy: 80, dx: 240, dy: 200, d: "0s" },
        { cx: 420, cy: 80, dx: 260, dy: 200, d: "0.8s" },
        { cx: 80, cy: 320, dx: 240, dy: 210, d: "1.4s" },
        { cx: 420, cy: 320, dx: 260, dy: 210, d: "2.1s" },
      ].map((p, i) => (
        <circle key={i} r="5" fill="var(--accent)">
          <animate attributeName="cx" values={`${p.cx};${p.dx}`} dur="3s" begin={p.d} repeatCount="indefinite"/>
          <animate attributeName="cy" values={`${p.cy};${p.dy}`} dur="3s" begin={p.d} repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0;1;1;0" dur="3s" begin={p.d} repeatCount="indefinite"/>
        </circle>
      ))}
      {/* ticker */}
      <g transform="translate(250 350)">
        <rect x="-90" y="-14" width="180" height="28" rx="14" fill="var(--bg)" stroke={ink} strokeWidth="1.5"/>
        <circle cx="-76" r="4" fill="var(--accent)" className="counter"/>
        <text x="-66" y="4" fontSize="11" fontWeight="600" fill={ink} fontFamily="JetBrains Mono">
          <tspan>1,247 tasks handled today</tspan>
        </text>
      </g>
    </svg>
  );
};

const useCountUp = (target, duration = 2800, start = true) => {
  const [val, setVal] = React.useState(0);
  React.useEffect(() => {
    if (!start) return;
    const steps = 60;
    let i = 0;
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    const id = setInterval(() => {
      i++;
      const p = Math.min(1, i / steps);
      setVal(Math.round(ease(p) * target));
      if (p >= 1) clearInterval(id);
    }, duration / steps);
    return () => clearInterval(id);
  }, [target, duration, start]);
  return val;
};

const ChartsAnim = ({ lang }) => {
  const isHe = lang === "he";

  const [interactions, setInteractions] = React.useState(4821);
  const [resolved,     setResolved]     = React.useState(3904);
  const [avgResp,      setAvgResp]      = React.useState(1.4);
  const [revenue,      setRevenue]      = React.useState(182350);

  const agentNames = ["מאיה","רוני","דנה","איתן","עומר","טל","מיכל"];
  const [agentTasks, setAgentTasks] = React.useState([210,185,240,198,220,175,260]);

  const allActions = [
    { agent:"מאיה", action:"פתרה פנייה #5002",     color:"#22d3a0", bg:"#052e1e" },
    { agent:"איתן", action:"גבה ₪8,750",           color:"#f97316", bg:"#3b1600" },
    { agent:"עומר", action:"עדכן מלאי 200 יח'",    color:"#38bdf8", bg:"#0c2233" },
    { agent:"טל",   action:"סגר עסקה ₪12,000",    color:"#f97316", bg:"#3b1600" },
    { agent:"מיכל", action:'סיננה 14 קו"ח',           color:"#818cf8", bg:"#1e1b3a" },
    { agent:"דנה",  action:"שלחה 500 מיילים",         color:"#818cf8", bg:"#1e1b3a" },
    { agent:"רוני", action:"תיאם 8 פגישות",          color:"#38bdf8", bg:"#0c2233" },
    { agent:"מאיה", action:"ענתה ל-32 שיחות",        color:"#22d3a0", bg:"#052e1e" },
    { agent:"טל",   action:"הגדיל המרה ב-18%",       color:"#f97316", bg:"#3b1600" },
  ];
  const [feed, setFeed] = React.useState(allActions.slice(0,4));

  React.useEffect(() => {
    const id = setInterval(() => {
      setInteractions(v => v + Math.floor(Math.random() * 6) + 2);
      setResolved(    v => v + Math.floor(Math.random() * 5) + 1);
      setAvgResp(     v => Math.max(0.8, +(v - 0.01 + (Math.random()*0.04-0.02)).toFixed(2)));
      setRevenue(     v => v + Math.floor(Math.random() * 800) + 200);
      setAgentTasks(  arr => arr.map(t => t + Math.floor(Math.random() * 10) + 3));
      setFeed(f => {
        const next = allActions[Math.floor(Math.random() * allActions.length)];
        return [next, ...f.slice(0,3)];
      });
    }, 1800);
    return () => clearInterval(id);
  }, []);

  const fmt  = n => n.toLocaleString("en-US");
  const fmtR = n => `₪${fmt(n)}`;
  const maxTask = Math.max(...agentTasks);

  const W = 800, H = 500;
  const orange = "#f97316";
  const green  = "#22d3a0";
  const blue   = "#38bdf8";
  const yellow = "#fbbf24";
  const ink    = "var(--ink)";
  const card   = "var(--card)";

  const kpiW = 186, kpiH = 90;
  const kpiItems = [
    { label: isHe ? "אינטראקציות" : "Interactions", val: fmt(interactions), color: green,  x: 16  },
    { label: isHe ? "נפתרו"       : "Resolved",     val: fmt(resolved),     color: orange, x: 210 },
    { label: isHe ? "זמן תגובה"   : "Avg Response", val: `${avgResp}s`,    color: blue,   x: 404 },
    { label: isHe ? "הכנסות היום" : "Revenue Today",val: fmtR(revenue),    color: orange, x: 598 },
  ];

  const barAreaX = 16, barAreaY = 210, barAreaW = 490, barAreaH = 220;
  const barCount = agentTasks.length;
  const slotW  = Math.floor((barAreaW - 20) / barCount);
  const barW   = Math.floor(slotW * 0.56);
  const yBase  = barAreaH - 30;
  const maxBarH= yBase - 50;

  const feedX = 522, feedY = 198, feedW = 266, feedH = 238;
  const rowH = 52, feedTopPad = 30; // Reduced pad because title is moved out

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%"
         preserveAspectRatio="xMidYMid meet" direction="ltr"
         style={{ display:"block" }}>

      {/* KPI cards */}
      {kpiItems.map((k, i) => (
        <g key={i} transform={`translate(${k.x}, 8)`}>
          <rect width={kpiW} height={kpiH} rx="12"
                fill={card} stroke={k.color} strokeWidth="1.5" strokeOpacity="0.5"/>
          <circle cx={kpiW/2 + 50} cy="20" r="6" fill={k.color}>
            <animate attributeName="r" values="6;8;6" dur="1.8s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="1;0.5;1" dur="1.8s" repeatCount="indefinite"/>
          </circle>
          <text x={kpiW/2} y="34" textAnchor="middle" fontSize="14" fill={ink} opacity=".65"
                fontFamily="'Heebo',sans-serif" fontWeight="700">{k.label}</text>
          <text x={kpiW/2} y="64" textAnchor="middle" fontSize="26" fontWeight="900" fill={k.color}
                fontFamily="'Space Grotesk',sans-serif" letterSpacing="-0.02em"
                direction="ltr">{k.val}</text>
          <rect x={kpiW/2 - 30} y="70" width="60" height="16" rx="8" fill={k.color} opacity="0.15"/>
          <text x={kpiW/2} y="81" textAnchor="middle" fontSize="10" fontWeight="800"
                fill={k.color} fontFamily="'JetBrains Mono',monospace">↑ LIVE</text>
        </g>
      ))}

      {/* Bar chart - Left Side */}
      <g transform={`translate(${barAreaX}, ${barAreaY})`}>
        {/* Title above frame */}
        <text x={(barAreaW+4)/2 - 10} y="-15" textAnchor="middle" fontSize="14" fontWeight="800" fill={ink}
              fontFamily="'Heebo',sans-serif">
          {isHe ? "משימות שהושלמו לפי סוכן" : "Tasks completed by agent"}
        </text>
        {/* Indicator to the right of title */}
        <circle cx={(barAreaW+4)/2 + 90} cy="-20" r="5" fill={green}>
          <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
        </circle>

        {/* Frame */}
        <rect width={barAreaW + 4} height={barAreaH + 20} rx="14"
              fill={card} stroke={orange} strokeWidth="1.5" strokeOpacity="0.5"/>

        {/* LIVE badge inside frame at corner */}
        <rect x={barAreaW - 46} y="9" width="52" height="20" rx="10" fill={orange} opacity="0.15"/>
        <text x={barAreaW - 20} y="23" textAnchor="middle" fontSize="10" fontWeight="800"
              fill={orange} fontFamily="'JetBrains Mono',monospace">LIVE ↑</text>

        {/* Gridlines */}
        {[0,1,2,3].map(i => (
          <line key={i} x1="10" x2={barAreaW - 6}
                y1={40 + i * (maxBarH/4)} y2={40 + i * (maxBarH/4)}
                stroke={ink} strokeWidth="0.5" strokeDasharray="3 6" opacity=".1"/>
        ))}

        {/* Bars */}
        {agentTasks.map((h, i) => {
          const x = 10 + i * slotW + (slotW - barW) / 2;
          const scaledH = Math.max(6, Math.min(maxBarH, (h / (maxTask * 1.05)) * maxBarH));
          const isPeak = h === maxTask;
          const barColor = isPeak ? orange : (i % 2 === 0 ? blue : "#6b7280");
          const barTop = 40 + maxBarH - scaledH;

          return (
            <g key={i}>
              <rect x={x} y={barTop} width={barW} height={scaledH} rx="4"
                    fill={barColor} opacity={isPeak ? 1 : 0.65}
                    style={{ transition: "all 0.7s cubic-bezier(0.4,0,0.2,1)" }}/>
              <rect x={x + barW/2 - 22} y={barTop - 24} width="44" height="20" rx="10"
                    fill={isPeak ? orange : card} fillOpacity={isPeak ? 0.2 : 0.75}/>
              <text x={x + barW/2} y={barTop - 10}
                    textAnchor="middle" fontSize="12" fontWeight="800"
                    fill={isPeak ? orange : ink} opacity={isPeak ? 1 : 0.85}
                    fontFamily="'Space Grotesk',sans-serif" direction="ltr">{h}</text>
              <text x={x + barW/2} y={40 + maxBarH + 22} textAnchor="middle"
                    fontSize="12" fill={isPeak ? orange : ink} opacity={isPeak ? 1 : 0.6}
                    fontWeight={isPeak ? "700" : "500"}
                    fontFamily="'Heebo',sans-serif">{agentNames[i]}</text>
            </g>
          );
        })}
      </g>

      {/* Live Feed - Right Side */}
      <g transform={`translate(${feedX}, ${feedY})`}>
        {/* Title above frame */}
        <text x={feedW/2 - 10} y="-15" textAnchor="middle" fontSize="15" fontWeight="800" fill={ink}
              fontFamily="'Heebo',sans-serif">
          {isHe ? "פעילות בזמן אמת" : "Real-time feed"}
        </text>
        {/* Indicator to the right of title */}
        <circle cx={feedW/2 + 65} cy="-20" r="6" fill={yellow}>
          <animate attributeName="opacity" values="1;0.3;1" dur="1.2s" repeatCount="indefinite"/>
        </circle>

        {/* Frame */}
        <rect width={feedW} height={feedH + 10} rx="14"
              fill={card} stroke={orange} strokeWidth="1.5" strokeOpacity="0.5"/>

        {/* Content inside frame - clipped/contained */}
        <g transform="translate(0, 15)">
          {feed.map((f, i) => {
            const rowY = i * rowH;
            const rowMidY = rowY + rowH/2 - 2;
            const avatarCX = feedW - 28;
            const textCX = (feedW - 56) / 2 + 10;
            return (
              <g key={i} opacity={1 - i * 0.15}>
                <rect x="8" y={rowY} width={feedW - 16} height={rowH - 4} rx="10" fill={f.bg}/>
                <rect x={feedW - 13} y={rowY} width="5" height={rowH - 4} rx="2" fill={f.color}/>
                <circle cx={avatarCX} cy={rowMidY} r="16" fill={f.color}/>
                <text x={avatarCX} y={rowMidY + 5} textAnchor="middle"
                      fontSize="15" fill="#fff" fontFamily="'Heebo',sans-serif" fontWeight="800">
                  {f.agent.charAt(0)}
                </text>
                <text x={textCX} y={rowMidY - 8} textAnchor="middle"
                      fontSize="15" fontWeight="800" fill={f.color}
                      fontFamily="'Heebo',sans-serif">{f.agent}</text>
                <text x={textCX} y={rowMidY + 10} textAnchor="middle"
                      fontSize="13" fill="#e2e8f0"
                      fontFamily="'Heebo',sans-serif">{f.action}</text>
              </g>
            );
          })}
        </g>
      </g>

      {/* Revenue ticker */}
      <g transform="translate(16, 455)">
        <rect width="768" height="44" rx="12"
              fill={card} stroke={orange} strokeWidth="1.5" strokeOpacity="0.4"/>
        <text x="384" y="18" textAnchor="middle" fontSize="13" fontWeight="600" fill={ink} opacity=".6"
              fontFamily="'Heebo',sans-serif">
          {isHe ? "💰 הכנסות מצטברות — היום" : "💰 Revenue generated today"}
        </text>
        <text x="384" y="38" textAnchor="middle" fontSize="22" fontWeight="900"
              fill={orange} fontFamily="'Space Grotesk',sans-serif" direction="ltr">
          {fmtR(revenue)}
        </text>
      </g>
    </svg>
  );
};


const OrbitAnim = ({ lang }) => {
  const ink = "var(--ink)";
  const agents = [
    { a: 0, color: "var(--butter)", l: "💬" },
    { a: 45, color: "var(--sky)", l: "📅" },
    { a: 90, color: "var(--rose)", l: "📢" },
    { a: 135, color: "var(--mint)", l: "💰" },
    { a: 180, color: "var(--violet)", l: "🎯" },
    { a: 225, color: "var(--lime)", l: "👥" },
    { a: 270, color: "var(--butter)", l: "📊" },
    { a: 315, color: "var(--sky)", l: "🛠" },
  ];
  const R = 130;
  return (
    <svg viewBox="0 0 500 400" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
      <g transform="translate(250 200)">
        <circle r={R} fill="none" stroke={ink} strokeWidth="1" strokeDasharray="2 6" opacity=".4"/>
        <g className="orbit" style={{ transformOrigin: 'center' }}>
          {agents.map((a, i) => {
            const x = Math.cos((a.a * Math.PI) / 180) * R;
            const y = Math.sin((a.a * Math.PI) / 180) * R;
            return (
              <g key={i} transform={`translate(${x},${y})`}>
                <circle r="24" fill={a.color} stroke={ink} strokeWidth="2"/>
                <text textAnchor="middle" y="6" fontSize="18">{a.l}</text>
              </g>
            );
          })}
        </g>
        {/* center business */}
        <rect x="-60" y="-36" width="120" height="72" rx="12" fill={ink}/>
        <text textAnchor="middle" y="-6" fontSize="11" fill="var(--accent)" fontFamily="JetBrains Mono" fontWeight="600">YOUR BUSINESS</text>
        <text textAnchor="middle" y="14" fontSize="16" fontWeight="700" fill="var(--bg)" fontFamily="Space Grotesk">{lang === "he" ? "העסק שלך" : "RUNNING"}</text>
        <text textAnchor="middle" y="28" fontSize="10" fill="var(--bg)" opacity=".7" fontFamily="JetBrains Mono" className="counter">● 24/7</text>
      </g>
    </svg>
  );
};

const Hero = ({ lang, tHero, tCta, variant, animKind }) => {
  const v = tHero.variants[variant % tHero.variants.length];
  return (
    <section className="hero">
      <div className="wrap">
        <div className="hero-grid">
          <div>
            <span className="eyebrow"><span className="eyebrow-dot"/>{tHero.eyebrow}</span>
            <h1>
              {v.h[0] && <>{v.h[0]}<br/></>}
              {v.h[1] && <><span className="stroke">{v.h[1]}</span>{v.h[2] ? "" : v.h[2] === "" ? "" : " "}<br/></>}
              {v.h[2] && <span className="accent">{v.h[2]}</span>}
            </h1>
            <p className="hero-sub">{v.sub}</p>
            <div className="hero-cta">
              <a className="btn btn-accent" href="#contact" style={{display:"flex",gap:"8px",alignItems:"center"}}>{lang === "he" ? "←" : ""} {tCta.primary} {lang !== "he" ? "→" : ""}</a>
              <a className="btn btn-ghost" href="#demo">{tCta.secondary}</a>
            </div>
            <div className="hero-trust">
              <div className="avatar-row">
                <div style={{ background: "var(--butter)" }}/>
                <div style={{ background: "var(--sky)" }}/>
                <div style={{ background: "var(--mint)" }}/>
                <div style={{ background: "var(--rose)" }}/>
                <div style={{ background: "var(--violet)" }}/>
              </div>
              <span>{tHero.trust}</span>
            </div>
          </div>
          <div style={{ position: "relative" }}>
            <HeroVideo animKind={animKind} lang={lang}/>
          </div>
        </div>
      </div>
    </section>
  );
};

Object.assign(window, { Hero, HeroVideo, FlowAnim, ChartsAnim, OrbitAnim });
