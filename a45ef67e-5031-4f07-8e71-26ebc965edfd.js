// src/hero.jsx — hero section with looping SVG/CSS animated "video"
const HeroVideo = ({ animKind = "flow", lang = "he" }) => {
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
  const ink = "var(--ink)";
  const revenue = useCountUp(248);
  const calls = useCountUp(1247);
  const saved = useCountUp(82);
  const fmt = (n) => n.toLocaleString("en-US");
  const kpis = [
    { label: lang === "he" ? "הכנסות" : "Revenue", val: lang === "he" ? `${fmt(revenue)}K ₪` : `$${fmt(revenue<68?revenue:68)}K`, delta: "+12%", color: "var(--butter)" },
    { label: lang === "he" ? "שיחות" : "Calls", val: fmt(calls), delta: "+34%", color: "var(--mint)" },
    { label: lang === "he" ? "חיסכון" : "Saved", val: lang === "he" ? `${fmt(saved)}K ₪` : `$${fmt(saved<23?saved:23)}K`, delta: "+8%", color: "var(--sky)" },
  ];
  const bars = [38,55,72,48,86,68,100,92,118,88,140,112,96];
  const maxBar = Math.max(...bars);
  const chartW = 480, chartH = 220, chartInnerTop = 40, chartInnerBottom = 200;
  return (
    <svg viewBox="0 0 520 420" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" direction="ltr">
      <defs>
        <clipPath id="chartReveal">
          <rect x="0" y="0" width="0" height="300">
            <animate attributeName="width" from="0" to="500" dur="2.5s" begin="0.3s" fill="freeze"/>
          </rect>
        </clipPath>
      </defs>

      {/* KPI cards */}
      {kpis.map((k, i) => (
        <g key={i} transform={`translate(${14 + i * 164},16)`}>
          <rect width="156" height="86" rx="12" fill="var(--card)" stroke={ink} strokeWidth="1.5"/>
          <circle cx={lang==="he" ? 140 : 16} cy="26" r="4" fill={k.color}/>
          <text x={lang==="he" ? 132 : 26} y="30" fontSize="11" fill={ink} opacity=".65" fontFamily="'Heebo',sans-serif" fontWeight="500" textAnchor={lang==="he" ? "end" : "start"}>{k.label}</text>
          <text x="16" y="56" fontSize="24" fontWeight="800" fill={ink} fontFamily="'Space Grotesk',sans-serif" letterSpacing="-0.02em" direction="ltr">{k.val}</text>
          <g transform="translate(16 68)">
            <rect width="52" height="18" rx="9" fill="var(--accent)" opacity=".14"/>
            <text x="26" y="13" textAnchor="middle" fontSize="10" fontWeight="700" fill="var(--accent)" fontFamily="'JetBrains Mono',monospace" direction="ltr">{k.delta} ↑</text>
          </g>
        </g>
      ))}

      {/* chart card */}
      <g transform="translate(14 118)">
        <rect width="492" height="286" rx="14" fill="var(--card)" stroke={ink} strokeWidth="1.5"/>
        <text x={lang==="he" ? 472 : 20} y="34" fontSize="12" fill={ink} opacity=".7" fontFamily="'Heebo',sans-serif" fontWeight="600" textAnchor={lang==="he" ? "end" : "start"}>
          {lang === "he" ? "פעילות סוכנים" : "Agent activity · 12 hours"}
        </text>
        <g transform={lang==="he" ? "translate(74 20)" : "translate(472 20)"}>
          <rect x="-54" width="54" height="16" rx="8" fill="var(--accent)" opacity=".14"/>
          <circle cx="-44" cy="8" r="3" fill="var(--accent)" className="counter"/>
          <text x="-36" y="11" fontSize="9" fontWeight="700" fill="var(--accent)" fontFamily="'JetBrains Mono',monospace" direction="ltr">LIVE</text>
        </g>

        {/* gridlines */}
        {[0,1,2,3,4].map(i => (
          <line key={i} x1="20" x2="472" y1={chartInnerTop + i*40} y2={chartInnerTop + i*40} stroke={ink} strokeWidth="1" strokeDasharray="2 4" opacity=".1"/>
        ))}

        {/* bars */}
        <g>
          {bars.map((h, i) => {
            const barW = 24;
            const gap = (chartW - 40 - bars.length * barW) / (bars.length - 1);
            const x = 20 + i * (barW + gap);
            const scaledH = (h / maxBar) * (chartInnerBottom - chartInnerTop);
            const isPeak = h === maxBar;
            return (
              <g key={i} className="bar-grow" style={{ animationDelay: `${i*0.08}s`, transformOrigin: `${x + barW/2}px ${chartInnerBottom}px` }}>
                <rect x={x} y={chartInnerBottom - scaledH} width={barW} height={scaledH} rx="4" fill={isPeak ? "var(--accent)" : ink} opacity={isPeak ? 1 : 0.78}/>
                {isPeak && (
                  <g transform={`translate(${x + barW/2} ${chartInnerBottom - scaledH - 8})`}>
                    <rect x="-22" y="-16" width="44" height="18" rx="4" fill={ink}/>
                    <text textAnchor="middle" y="-4" fontSize="10" fontWeight="700" fill="var(--accent)" fontFamily="'JetBrains Mono',monospace" direction="ltr">PEAK</text>
                  </g>
                )}
              </g>
            );
          })}
        </g>

        {/* x-axis */}
        <g transform={`translate(0 ${chartInnerBottom + 18})`} fontFamily="'JetBrains Mono',monospace" fontSize="9" fill={ink} opacity=".4" direction="ltr">
          {["08","10","12","14","16","18","20"].map((h, i) => (
            <text key={i} x={20 + 40 + i * 70} textAnchor="middle">{h}:00</text>
          ))}
        </g>

        {/* sweeping cursor */}
        <line x1="20" x2="20" y1={chartInnerTop} y2={chartInnerBottom + 6} stroke="var(--accent)" strokeWidth="1.5" opacity="0">
          <animate attributeName="x1" values="20;500;500" keyTimes="0;0.75;1" dur="4.5s" repeatCount="indefinite"/>
          <animate attributeName="x2" values="20;500;500" keyTimes="0;0.75;1" dur="4.5s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0;0.55;0.55;0" keyTimes="0;0.05;0.7;1" dur="4.5s" repeatCount="indefinite"/>
        </line>
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
              <a className="btn btn-accent" href="#pricing">{tCta.primary} →</a>
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
