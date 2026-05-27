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
