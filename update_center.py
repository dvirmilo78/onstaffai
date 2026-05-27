import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

NEW_CHARTS_ANIM = r"""const ChartsAnim = ({ lang }) => {
  const isHe = lang === "he";

  const [interactions, setInteractions] = React.useState(4821);
  const [resolved,     setResolved]     = React.useState(3904);
  const [avgResp,      setAvgResp]      = React.useState(1.4);
  const [revenue,      setRevenue]      = React.useState(182350);

  const agentNames = ["מאיה","רוני","דנה","איתן","עומר","טל","מיכל"];
  const [agentTasks, setAgentTasks] = React.useState([210,185,240,198,220,175,260]);

  const allActions = [
    { agent:"מאיה", action:"פתרה פנייה #5002",        color:"#22d3a0" },
    { agent:"איתן", action:"גבה ₪8,750 מ-3 לקוחות",  color:"#f97316" },
    { agent:"עומר", action:"עדכן מלאי — 200 יח'",    color:"#38bdf8" },
    { agent:"טל",   action:"סגר עסקה ₪12,000",       color:"#f97316" },
    { agent:"מיכל", action:'סיננה 14 קו"ח',           color:"#818cf8" },
    { agent:"דנה",  action:"שלחה 500 מיילים",         color:"#818cf8" },
    { agent:"רוני", action:"תיאם 8 פגישות היום",      color:"#38bdf8" },
    { agent:"מאיה", action:"ענתה ל-32 שיחות",        color:"#22d3a0" },
    { agent:"טל",   action:"הגדיל המרה ב-18%",       color:"#f97316" },
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
  const ink    = "var(--ink)";
  const card   = "var(--card)";

  const kpiW = 186, kpiH = 82;
  const kpiItems = [
    { label: isHe ? "אינטראקציות" : "Interactions", val: fmt(interactions), color: green,  x: 16  },
    { label: isHe ? "נפתרו"       : "Resolved",     val: fmt(resolved),     color: orange, x: 210 },
    { label: isHe ? "זמן תגובה"   : "Avg Response", val: `${avgResp}s`,    color: blue,   x: 404 },
    { label: isHe ? "הכנסות היום" : "Revenue Today",val: fmtR(revenue),    color: orange, x: 598 },
  ];

  const barAreaX = 16, barAreaY = 210, barAreaW = 490, barAreaH = 220;
  const barCount = agentTasks.length;
  const barW = Math.floor((barAreaW - 20) / barCount) - 8;
  const barGap = Math.floor((barAreaW - 20 - barW * barCount) / (barCount - 1));

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%"
         preserveAspectRatio="xMidYMid meet" direction="ltr"
         style={{ display:"block" }}>

      {/* ── KPI cards — all content centered ── */}
      {kpiItems.map((k, i) => (
        <g key={i} transform={`translate(${k.x}, 8)`}>
          <rect width={kpiW} height={kpiH} rx="12"
                fill={card} stroke={k.color} strokeWidth="1.5" strokeOpacity="0.5"/>
          {/* pulsing dot centered top */}
          <circle cx={kpiW/2} cy="14" r="5" fill={k.color}>
            <animate attributeName="r" values="5;7;5" dur="1.8s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="1;0.5;1" dur="1.8s" repeatCount="indefinite"/>
          </circle>
          {/* label centered */}
          <text x={kpiW/2} y="30" textAnchor="middle" fontSize="11" fill={ink} opacity=".6"
                fontFamily="'Heebo',sans-serif" fontWeight="600">{k.label}</text>
          {/* big value centered */}
          <text x={kpiW/2} y="58" textAnchor="middle" fontSize="24" fontWeight="900" fill={k.color}
                fontFamily="'Space Grotesk',sans-serif" letterSpacing="-0.02em"
                direction="ltr">{k.val}</text>
          {/* live badge centered */}
          <rect x={kpiW/2 - 26} y="64" width="52" height="14" rx="7" fill={k.color} opacity="0.15"/>
          <text x={kpiW/2} y="74" textAnchor="middle" fontSize="9" fontWeight="800"
                fill={k.color} fontFamily="'JetBrains Mono',monospace">↑ LIVE</text>
        </g>
      ))}

      {/* ── Bar chart card ── */}
      <g transform={`translate(${barAreaX}, ${barAreaY - 10})`}>
        <rect width={barAreaW + 4} height={barAreaH + 30} rx="14"
              fill={card} stroke={orange} strokeWidth="1" strokeOpacity="0.25"/>

        <circle cx="16" cy="18" r="5" fill={green}>
          <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
        </circle>
        <text x={barAreaW/2} y="23" textAnchor="middle" fontSize="13" fontWeight="700" fill={ink}
              fontFamily="'Heebo',sans-serif">
          {isHe ? "משימות שהושלמו לפי סוכן" : "Tasks completed by agent"}
        </text>
        <rect x={barAreaW - 50} y="8" width="50" height="18" rx="9" fill={orange} opacity="0.15"/>
        <text x={barAreaW - 25} y="21" textAnchor="middle" fontSize="9" fontWeight="800"
              fill={orange} fontFamily="'JetBrains Mono',monospace">LIVE ↑</text>

        {[0,1,2,3].map(i => (
          <line key={i} x1="10" x2={barAreaW - 6}
                y1={38 + i * 42} y2={38 + i * 42}
                stroke={ink} strokeWidth="0.5" strokeDasharray="3 6" opacity=".1"/>
        ))}

        {agentTasks.map((h, i) => {
          const x = 14 + i * (barW + barGap);
          const maxH = barAreaH - 50;
          const scaledH = Math.max(8, Math.min(maxH, (h / (maxTask * 1.05)) * maxH));
          const isPeak = h === maxTask;
          const barColor = isPeak ? orange : (i % 2 === 0 ? blue : "#6b7280");
          const yBase = barAreaH - 18;
          return (
            <g key={i}>
              <rect x={x} y={yBase - scaledH} width={barW} height={scaledH} rx="5"
                    fill={barColor} opacity={isPeak ? 1 : 0.6}
                    style={{ transition: "all 0.7s cubic-bezier(0.4,0,0.2,1)" }}/>
              <text x={x + barW/2} y={yBase - scaledH - 5}
                    textAnchor="middle" fontSize="11" fontWeight="800"
                    fill={isPeak ? orange : ink} opacity={isPeak ? 1 : 0.75}
                    fontFamily="'Space Grotesk',sans-serif" direction="ltr">{h}</text>
              {isPeak && (
                <g transform={`translate(${x + barW/2 - 18}, ${yBase - scaledH - 22})`}>
                  <rect width="36" height="14" rx="7" fill={orange} opacity="0.2"/>
                  <text x="18" y="11" textAnchor="middle" fontSize="8" fontWeight="800"
                        fill={orange} fontFamily="'JetBrains Mono',monospace">PEAK</text>
                </g>
              )}
              <text x={x + barW/2} y={yBase + 14} textAnchor="middle"
                    fontSize="11" fill={isPeak ? orange : ink} opacity={isPeak ? 1 : 0.55}
                    fontWeight={isPeak ? "700" : "400"}
                    fontFamily="'Heebo',sans-serif">{agentNames[i]}</text>
            </g>
          );
        })}
      </g>

      {/* ── Live feed card — centered content ── */}
      <g transform="translate(526, 200)">
        <rect width="258" height="230" rx="14"
              fill={card} stroke={orange} strokeWidth="1" strokeOpacity="0.25"/>

        {/* header centered */}
        <circle cx="129" cy="16" r="5" fill={orange}>
          <animate attributeName="opacity" values="1;0.3;1" dur="1.2s" repeatCount="indefinite"/>
        </circle>
        <text x="129" y="33" textAnchor="middle" fontSize="13" fontWeight="700" fill={ink}
              fontFamily="'Heebo',sans-serif">
          {isHe ? "פעילות בזמן אמת" : "Real-time feed"}
        </text>

        {feed.map((f, i) => (
          <g key={i} transform={`translate(0, ${44 + i * 46})`} opacity={1 - i * 0.2}>
            <rect x="8" width="242" height="38" rx="8"
                  fill={f.color} fillOpacity="0.08"/>
            {/* avatar circle centered on card */}
            <circle cx="30" cy="19" r="12" fill={f.color} opacity="0.9"/>
            <text x="30" y="23" textAnchor="middle" fontSize="10" fill="#fff"
                  fontFamily="'Heebo',sans-serif" fontWeight="700">
              {f.agent.charAt(0)}
            </text>
            {/* agent name + action centered in remaining space */}
            <text x="145" y="14" textAnchor="middle" fontSize="11" fontWeight="700" fill={f.color}
                  fontFamily="'Heebo',sans-serif">{f.agent}</text>
            <text x="145" y="28" textAnchor="middle" fontSize="10" fill={ink} opacity=".75"
                  fontFamily="'Heebo',sans-serif">{f.action}</text>
          </g>
        ))}
      </g>

      {/* ── Revenue ticker — centered ── */}
      <g transform="translate(16, 448)">
        <rect width="768" height="44" rx="12"
              fill={card} stroke={orange} strokeWidth="1.5" strokeOpacity="0.4"/>
        <text x="384" y="20" textAnchor="middle" fontSize="11" fontWeight="600" fill={ink} opacity=".6"
              fontFamily="'Heebo',sans-serif">
          {isHe ? "💰 הכנסות מצטברות — היום" : "💰 Revenue generated today"}
        </text>
        <text x="384" y="38" textAnchor="middle" fontSize="20" fontWeight="900"
              fill={orange} fontFamily="'Space Grotesk',sans-serif" direction="ltr">
          {fmtR(revenue)}
        </text>
      </g>
    </svg>
  );
};"""

for uuid, entry in manifest.items():
    if entry.get('mime') not in ['text/javascript', 'application/javascript']:
        continue
    data = base64.b64decode(entry['data'])
    if entry.get('compressed'):
        data = gzip.decompress(data)
    text = data.decode('utf-8', errors='ignore')

    if 'const ChartsAnim = ({ lang }) => {' in text:
        start = text.find('const ChartsAnim = ({ lang }) => {')
        end   = text.find('\nconst OrbitAnim', start)
        if start != -1 and end != -1:
            text = text[:start] + NEW_CHARTS_ANIM + "\n\n" + text[end:]
            print(f"Replaced ChartsAnim in {uuid}")
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

new_manifest_json = json.dumps(manifest, separators=(',', ':'))
new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
    out.write(new_html)
print("Done!")
