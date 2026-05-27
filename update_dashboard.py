import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

for uuid, entry in manifest.items():
    if entry.get('mime') not in ['text/javascript', 'application/javascript']:
        continue
    data = base64.b64decode(entry['data'])
    if entry.get('compressed'):
        data = gzip.decompress(data)
    text = data.decode('utf-8', errors='ignore')
    changed = False

    # 1) Switch default animKind from "flow" to "charts"
    if 'animKind = "flow", lang = "he"' in text:
        text = text.replace('animKind = "flow", lang = "he"', 'animKind = "charts", lang = "he"')
        print(f'Switched animKind default in {uuid}')
        changed = True

    # 2) Replace entire ChartsAnim with a rich busy dashboard
    if 'const ChartsAnim = ({ lang }) => {' in text:
        OLD = re.search(r'const ChartsAnim = \(\{ lang \}\) => \{.*?^\};', text, re.DOTALL | re.MULTILINE)
        if OLD:
            old_str = OLD.group(0)
            new_str = r"""const ChartsAnim = ({ lang }) => {
  const ink = "var(--ink)";

  // KPI counters - always incrementing
  const [interactions, setInteractions] = React.useState(4821);
  const [resolved, setResolved] = React.useState(3904);
  const [avgResp, setAvgResp] = React.useState(1.4);
  const [revenue, setRevenue] = React.useState(182);

  // Bar chart: tasks completed per agent (always grows)
  const agentNames = ["מאיה","רוני","דנה","איתן","עומר","טל","מיכל"];
  const [agentTasks, setAgentTasks] = React.useState([210,185,240,198,220,175,260]);

  // Agent status feed
  const [feed, setFeed] = React.useState([
    { agent:"מאיה", action:"סגרה פנייה #4821", color:"var(--mint)" },
    { agent:"איתן", action:"שלח חשבונית ₪3,200", color:"var(--butter)" },
    { agent:"דנה",  action:"יצרה קמפיין חדש",   color:"var(--violet)" },
    { agent:"רוני", action:"תיאם פגישה למחר",    color:"var(--sky)" },
  ]);

  const allActions = [
    { agent:"מאיה", action:"פתרה תקלה #5002",    color:"var(--mint)" },
    { agent:"איתן", action:"גבה ₪8,750 מ-3 לקוחות", color:"var(--butter)" },
    { agent:"עומר", action:"עדכן מלאי - 200 יח'", color:"var(--sky)" },
    { agent:"טל",   action:"סגר עסקה חדשה",       color:"var(--accent)" },
    { agent:"מיכל", action:"סיננה 14 קורות חיים", color:"var(--violet)" },
    { agent:"דנה",  action:"שלחה 500 מיילים",      color:"var(--violet)" },
    { agent:"רוני", action:"תיאם 8 פגישות היום",  color:"var(--sky)" },
    { agent:"מאיה", action:"ענתה ל-32 שיחות",    color:"var(--mint)" },
  ];

  React.useEffect(() => {
    const id = setInterval(() => {
      setInteractions(v => v + Math.floor(Math.random() * 6) + 1);
      setResolved(v => v + Math.floor(Math.random() * 5) + 1);
      setAvgResp(v => Math.max(0.8, +(v - 0.01 + (Math.random() * 0.04 - 0.02)).toFixed(2)));
      setRevenue(v => v + Math.floor(Math.random() * 3));
      setAgentTasks(arr => arr.map(t => t + Math.floor(Math.random() * 8) + 2));
      setFeed(f => {
        const next = allActions[Math.floor(Math.random() * allActions.length)];
        return [next, ...f.slice(0, 3)];
      });
    }, 1800);
    return () => clearInterval(id);
  }, []);

  const fmt = n => n.toLocaleString("en-US");
  const maxTask = Math.max(...agentTasks);

  const kpis = [
    { label: lang === "he" ? "אינטראקציות" : "Interactions", val: fmt(interactions), color: "var(--mint)", delta: "↑ LIVE" },
    { label: lang === "he" ? "נפתרו" : "Resolved",     val: fmt(resolved),     color: "var(--accent)", delta: "↑ LIVE" },
    { label: lang === "he" ? "זמן תגובה" : "Avg. Response", val: `${avgResp}s`, color: "var(--butter)", delta: "↓ FAST" },
  ];

  const chartInnerTop = 20, chartInnerBottom = 130, barW = 36, barGap = 10;

  return (
    <svg viewBox="0 0 520 440" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" direction="ltr">
      {/* Background panel */}
      <rect width="520" height="440" rx="16" fill="var(--card)" opacity="0.6"/>

      {/* Title bar */}
      <rect width="520" height="38" rx="16" fill="var(--card)"/>
      <rect y="22" width="520" height="16" fill="var(--card)"/>
      <circle cx="18" cy="19" r="5" fill="var(--mint)">
        <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="30" y="24" fontSize="11" fontWeight="700" fill={ink} fontFamily="'Heebo',sans-serif">
        {lang === "he" ? "לוח בקרה — סוכנים פעילים" : "Live Agent Control Panel"}
      </text>
      <rect x="380" y="8" width="48" height="20" rx="10" fill="var(--accent)" opacity="0.15"/>
      <text x="404" y="22" textAnchor="middle" fontSize="9" fontWeight="700" fill="var(--accent)" fontFamily="'JetBrains Mono',monospace">LIVE</text>
      <text x="454" y="22" fontSize="9" fill={ink} opacity="0.5" fontFamily="'JetBrains Mono',monospace">{`${agentNames.length} agents`}</text>

      {/* KPI cards row */}
      {kpis.map((k, i) => (
        <g key={i} transform={`translate(${10 + i * 168}, 46)`}>
          <rect width="158" height="64" rx="10" fill="var(--card)" stroke={k.color} strokeWidth="1" strokeOpacity="0.4"/>
          <circle cx="12" cy="14" r="4" fill={k.color}/>
          <text x="22" y="18" fontSize="10" fill={ink} opacity=".6" fontFamily="'Heebo',sans-serif" fontWeight="500">{k.label}</text>
          <text x="10" y="44" fontSize="22" fontWeight="800" fill={k.color} fontFamily="'Space Grotesk',sans-serif" letterSpacing="-0.02em" direction="ltr">{k.val}</text>
          <rect x="10" y="50" width="44" height="12" rx="6" fill={k.color} opacity="0.12"/>
          <text x="32" y="59" textAnchor="middle" fontSize="8" fontWeight="700" fill={k.color} fontFamily="'JetBrains Mono',monospace">{k.delta}</text>
        </g>
      ))}

      {/* Bar chart: tasks per agent */}
      <g transform="translate(10 120)">
        <rect width="310" height="160" rx="10" fill="var(--card)" opacity="0.7"/>
        <text x="10" y="18" fontSize="10" fontWeight="600" fill={ink} opacity=".6" fontFamily="'Heebo',sans-serif">
          {lang === "he" ? "משימות שהושלמו לפי סוכן" : "Tasks completed by agent"}
        </text>
        {/* gridlines */}
        {[0,1,2,3].map(i => (
          <line key={i} x1="14" x2="300" y1={chartInnerTop + 28 + i*28} y2={chartInnerTop + 28 + i*28}
            stroke={ink} strokeWidth="0.5" strokeDasharray="2 4" opacity=".1"/>
        ))}
        {agentTasks.map((h, i) => {
          const x = 18 + i * (barW + barGap);
          const scaledH = Math.min(100, (h / (maxTask * 1.1)) * (chartInnerBottom - chartInnerTop));
          const isPeak = h === maxTask;
          return (
            <g key={i}>
              <rect x={x} y={chartInnerTop + 28 + (100 - scaledH)} width={barW} height={scaledH} rx="4"
                fill={isPeak ? "var(--accent)" : ink}
                opacity={isPeak ? 1 : 0.55}
                style={{ transition: "all 0.6s cubic-bezier(0.4,0,0.2,1)" }}/>
              <text x={x + barW/2} y={chartInnerTop + 25 + (100 - scaledH)} textAnchor="middle"
                fontSize="8" fontWeight="700" fill={isPeak ? "var(--accent)" : ink} opacity="0.7"
                fontFamily="'JetBrains Mono',monospace" direction="ltr">{h}</text>
              <text x={x + barW/2} y="148" textAnchor="middle" fontSize="8" fill={ink} opacity=".5"
                fontFamily="'Heebo',sans-serif">{agentNames[i]}</text>
            </g>
          );
        })}
      </g>

      {/* Live activity feed */}
      <g transform="translate(328 120)">
        <rect width="182" height="160" rx="10" fill="var(--card)" opacity="0.7"/>
        <text x="10" y="18" fontSize="10" fontWeight="600" fill={ink} opacity=".6" fontFamily="'Heebo',sans-serif">
          {lang === "he" ? "פעילות בזמן אמת" : "Real-time activity"}
        </text>
        {feed.map((f, i) => (
          <g key={i} transform={`translate(0 ${28 + i * 32})`} opacity={1 - i * 0.2}>
            <rect x="8" width="166" height="26" rx="6" fill={f.color} fillOpacity="0.1"/>
            <circle cx="20" cy="13" r="4" fill={f.color}/>
            <text x="30" y="10" fontSize="9" fontWeight="700" fill={f.color} fontFamily="'Heebo',sans-serif">{f.agent}</text>
            <text x="30" y="21" fontSize="8" fill={ink} opacity=".7" fontFamily="'Heebo',sans-serif">{f.action}</text>
          </g>
        ))}
      </g>

      {/* Revenue ticker bottom */}
      <g transform="translate(10 290)">
        <rect width="500" height="36" rx="10" fill="var(--card)" opacity="0.7"/>
        <text x="14" y="22" fontSize="11" fontWeight="600" fill={ink} opacity=".6" fontFamily="'Heebo',sans-serif">
          {lang === "he" ? "הכנסות מצטברות היום" : "Revenue generated today"}
        </text>
        <text x="490" y="22" textAnchor="end" fontSize="16" fontWeight="800" fill="var(--butter)" fontFamily="'Space Grotesk',sans-serif" direction="ltr">
          {`₪${fmt(revenue * 1000)}`}
        </text>
      </g>
    </svg>
  );
};"""
            text = text.replace(old_str, new_str)
            print(f'Replaced ChartsAnim in {uuid}')
            changed = True
        else:
            print(f'Could not match old ChartsAnim block in {uuid}')

    if changed:
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

new_manifest_json = json.dumps(manifest, separators=(',', ':'))
new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
    out.write(new_html)
print("Done!")
