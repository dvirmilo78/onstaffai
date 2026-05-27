// src/illustrations.jsx — SVG illustrations per agent + logo mark
const LogoMark = ({ size = 30 }) => (
  <svg width={size} height={size} viewBox="0 0 40 40" fill="none">
    <defs>
      <linearGradient id="lg1" x1="0" y1="0" x2="40" y2="40">
        <stop offset="0" stopColor="var(--ink)"/>
        <stop offset="1" stopColor="var(--accent)"/>
      </linearGradient>
    </defs>
    <rect x="2" y="2" width="36" height="36" rx="10" fill="url(#lg1)"/>
    <text x="20" y="27" textAnchor="middle" fontSize="18" fontWeight="800" fill="var(--bg)" fontFamily="Space Grotesk, sans-serif" letterSpacing="-0.04em">OS</text>
    <circle cx="33" cy="8" r="3.5" fill="var(--accent)" stroke="var(--bg)" strokeWidth="1.5"/>
  </svg>
);

// per-agent illustration — geometric, colorful, on a tinted card
const AgentIllu = ({ k, color }) => {
  const common = { width: "100%", height: "100%", viewBox: "0 0 200 160", preserveAspectRatio: "xMidYMid slice" };
  const bg = color || "var(--butter)";
  const ink = "var(--ink)";
  return (
    <div className="agent-illu" style={{ background: bg }}>
      <svg {...common}>
        {k === "reception" && (<g>
          <rect x="26" y="40" width="100" height="60" rx="10" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <circle cx="44" cy="58" r="4" fill={ink} className="pulse-dot"/>
          <rect x="56" y="56" width="50" height="4" rx="2" fill={ink} opacity=".3"/>
          <rect x="56" y="66" width="34" height="4" rx="2" fill={ink} opacity=".2"/>
          <g className="wiggle">
            <rect x="60" y="88" width="60" height="22" rx="10" fill={ink}/>
            <rect x="68" y="96" width="44" height="4" rx="2" fill="var(--bg)"/>
            <path d="M70 110 L66 116 L76 112 Z" fill={ink}/>
          </g>
          <circle cx="150" cy="46" r="18" fill={ink}/>
          <path d="M142 46l6 6 10-12" stroke={bg} strokeWidth="2.5" fill="none" strokeLinecap="round"/>
        </g>)}
        {k === "scheduler" && (<g>
          <rect x="40" y="30" width="120" height="100" rx="10" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="40" y="30" width="120" height="22" rx="10" fill={ink}/>
          {[0,1,2,3,4].map(c => [0,1,2].map(r => (
            <rect key={c+'-'+r} x={48+c*22} y={62+r*22} width="16" height="16" rx="3" fill={ink} opacity={(c===2&&r===1)?1:.1} className={(c===2&&r===1)?"pulse-dot":""}/>
          )))}
          <g className="clock-rotate" style={{transformOrigin:'140px 78px'}}>
            <circle cx="140" cy="78" r="14" fill={bg} stroke={ink} strokeWidth="2"/>
            <path d="M140 70v9l5 3" stroke={ink} strokeWidth="2" strokeLinecap="round" fill="none"/>
          </g>
        </g>)}
        {k === "marketing" && (<g>
          <rect x="30" y="90" width="20" height="40" fill={ink} className="anim-chart-bar"/>
          <rect x="58" y="60" width="20" height="70" fill={ink} opacity=".7" className="anim-chart-bar" style={{animationDelay:'.3s'}}/>
          <rect x="86" y="40" width="20" height="90" fill={ink} className="anim-chart-bar" style={{animationDelay:'.6s'}}/>
          <rect x="114" y="20" width="20" height="110" fill="var(--bg)" stroke={ink} strokeWidth="2" className="anim-chart-bar" style={{animationDelay:'.9s'}}/>
          <circle cx="160" cy="40" r="18" fill={ink}/>
          <path d="M152 40l6 6 10-12" stroke={bg} strokeWidth="3" fill="none" strokeLinecap="round"/>
        </g>)}
        {k === "finance" && (<g>
          <g className="pie-spin" style={{transformOrigin:'100px 80px'}}>
            <circle cx="100" cy="80" r="42" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
            <path d="M100 80 L100 38 A42 42 0 0 1 139 95 Z" fill={ink}/>
            <path d="M100 80 L139 95 A42 42 0 0 1 76 116 Z" fill={ink} opacity=".4"/>
          </g>
          <circle cx="100" cy="80" r="16" fill={bg}/>
          <text x="100" y="86" textAnchor="middle" fontSize="14" fontWeight="700" fill={ink} fontFamily="Space Grotesk">₪</text>
        </g>)}
        {k === "sales" && (<g>
          <path d="M30 130 L70 90 L100 110 L140 50 L170 70" stroke={ink} strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" className="line-draw" style={{strokeDasharray:300, strokeDashoffset:300}}/>
          <circle cx="170" cy="70" r="8" fill={ink} className="pulse-dot"/>
          <path d="M140 50 L170 50 L170 70" stroke={ink} strokeWidth="2" strokeDasharray="4 4" fill="none"/>
          <g className="wiggle">
            <rect x="145" y="30" width="36" height="18" rx="4" fill={ink}/>
            <text x="163" y="44" textAnchor="middle" fontSize="11" fontWeight="700" fill={bg} fontFamily="Space Grotesk">+28%</text>
          </g>
        </g>)}
        {k === "hr" && (<g>
          {[0,1,2].map(i => (
            <g key={i} transform={`translate(${40+i*40}, 40)`} className="hr-check" style={{animationDelay:`${i*0.5}s`}}>
              <circle cx="20" cy="20" r="12" fill={ink}/>
              <rect x="4" y="36" width="32" height="32" rx="6" fill={ink} opacity={i===1?1:.3}/>
              {i===1 && <path d="M12 52l6 6 12-14" stroke={bg} strokeWidth="2.5" fill="none" strokeLinecap="round"/>}
            </g>
          ))}
          <rect x="40" y="110" width="120" height="8" rx="4" fill={ink} opacity=".2"/>
          <rect x="40" y="110" width="70" height="8" rx="4" fill={ink} className="hr-bar"/>
        </g>)}
        {k === "data" && (<g>
          <g className="orbit" style={{transformOrigin:'100px 80px'}}>
            <circle cx="100" cy="30" r="8" fill={ink}/>
            <circle cx="100" cy="130" r="8" fill={ink} opacity=".4"/>
          </g>
          <g className="orbit-rev" style={{transformOrigin:'100px 80px'}}>
            <circle cx="50" cy="80" r="6" fill={ink} opacity=".6"/>
            <circle cx="150" cy="80" r="6" fill={ink} opacity=".6"/>
          </g>
          <circle cx="100" cy="80" r="22" fill={ink}/>
          <text x="100" y="86" textAnchor="middle" fontSize="14" fontWeight="700" fill={bg} fontFamily="Space Grotesk">BI</text>
        </g>)}
        {k === "techsupport" && (<g>
          <rect x="44" y="40" width="112" height="70" rx="6" fill={ink}/>
          <rect x="50" y="50" width="100" height="54" rx="2" fill={bg}/>
          <text x="60" y="70" fontSize="9" fontFamily="JetBrains Mono" fill={ink}>$ fix --bug</text>
          <text x="60" y="84" fontSize="9" fontFamily="JetBrains Mono" fill={ink} opacity=".6">→ patching...</text>
          <text x="60" y="98" fontSize="9" fontFamily="JetBrains Mono" fill={ink}>✓ resolved<tspan className="blink">_</tspan></text>
          <rect x="80" y="110" width="40" height="14" rx="2" fill={ink}/>
          <rect x="70" y="124" width="60" height="4" rx="2" fill={ink} opacity=".3"/>
        </g>)}
        {k === "inventory" && (<g>
          {[0,1,2,3].map(c => [0,1,2].map(r => (
            <rect key={c+'-'+r} x={34+c*34} y={30+r*34} width="26" height="26" rx="3" fill={ink} opacity={Math.random()>.4?1:.2} className="inv-flash" style={{animationDelay:`${(c+r)*0.15}s`}}/>
          )))}
          <rect x="34" y="130" width="132" height="8" rx="4" fill={ink} opacity=".2"/>
          <rect x="34" y="130" width="90" height="8" rx="4" fill={ink}/>
        </g>)}
        {k === "collect" && (<g>
          <rect x="40" y="36" width="120" height="88" rx="10" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="50" width="70" height="6" rx="3" fill={ink}/>
          <rect x="52" y="62" width="96" height="4" rx="2" fill={ink} opacity=".3"/>
          <rect x="52" y="72" width="80" height="4" rx="2" fill={ink} opacity=".3"/>
          <rect x="52" y="92" width="40" height="20" rx="4" fill={ink}/>
          <text x="72" y="106" textAnchor="middle" fontSize="10" fontWeight="700" fill={bg} fontFamily="Space Grotesk">שלם</text>
          <circle cx="148" cy="48" r="10" fill={ink} className="wiggle"/>
          <text x="148" y="52" textAnchor="middle" fontSize="10" fontWeight="700" fill={bg}>!</text>
        </g>)}
        {k === "content" && (<g>
          <rect x="40" y="30" width="120" height="100" rx="6" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="44" width="74" height="8" rx="2" fill={ink}/>
          <rect x="52" y="60" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="70" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="80" width="72" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="96" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="106" width="60" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="114" y="106" width="10" height="14" rx="1" fill={ink} className="blink"/>
        </g>)}
        {k === "translate" && (<g>
          <g className="tx-left">
            <circle cx="70" cy="80" r="30" fill={ink}/>
            <text x="70" y="88" textAnchor="middle" fontSize="22" fontWeight="700" fill={bg} fontFamily="Space Grotesk">א</text>
          </g>
          <g className="tx-right">
            <circle cx="130" cy="80" r="30" fill={ink}/>
            <text x="130" y="88" textAnchor="middle" fontSize="22" fontWeight="700" fill={bg} fontFamily="Space Grotesk">A</text>
          </g>
          <path d="M100 80 L100 80" stroke={ink} strokeWidth="2"/>
          <path d="M82 64 L118 96 M82 96 L118 64" stroke={bg} strokeWidth="2" className="tx-cross"/>
        </g>)}
      </svg>
    </div>
  );
};

Object.assign(window, { LogoMark, AgentIllu });
