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
    
    for uuid, entry in manifest.items():
        if entry.get('mime') in ['text/javascript', 'application/javascript']:
            data = base64.b64decode(entry['data'])
            if entry.get('compressed'):
                data = gzip.decompress(data)
            
            text = data.decode('utf-8', errors='ignore')
            
            # Find the ChartsAnim block
            if "const ChartsAnim = ({ lang }) => {" in text:
                print(f"Found ChartsAnim in {uuid}")
                
                old_block = """const ChartsAnim = ({ lang }) => {
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
  const chartW = 480, chartH = 220, chartInnerTop = 40, chartInnerBottom = 200;"""

                new_block = """const ChartsAnim = ({ lang }) => {
  const ink = "var(--ink)";
  const [revenue, setRevenue] = React.useState(248);
  const [calls, setCalls] = React.useState(1247);
  const [saved, setSaved] = React.useState(82);
  const [bars, setBars] = React.useState([38,55,72,48,86,68,100,92,118,88,140,112,96]);

  React.useEffect(() => {
    const id = setInterval(() => {
      setRevenue(r => r + Math.floor(Math.random() * 4));
      setCalls(c => c + Math.floor(Math.random() * 8));
      setSaved(s => s + Math.floor(Math.random() * 2));
      setBars(b => {
         const newBars = [...b.slice(1)];
         const last = newBars[newBars.length - 1];
         let next = last + (Math.random() * 40 - 20);
         if (next < 20) next = 20;
         if (next > 160) next = 160;
         newBars.push(Math.round(next));
         return newBars;
      });
    }, 2000);
    return () => clearInterval(id);
  }, []);

  const fmt = (n) => n.toLocaleString("en-US");
  const kpis = [
    { label: lang === "he" ? "הכנסות" : "Revenue", val: lang === "he" ? `${fmt(revenue)}K ₪` : `$${fmt(revenue<68?revenue:68)}K`, delta: "+12%", color: "var(--butter)" },
    { label: lang === "he" ? "שיחות" : "Calls", val: fmt(calls), delta: "+34%", color: "var(--mint)" },
    { label: lang === "he" ? "חיסכון" : "Saved", val: lang === "he" ? `${fmt(saved)}K ₪` : `$${fmt(saved<23?saved:23)}K`, delta: "+8%", color: "var(--sky)" },
  ];
  const maxBar = Math.max(...bars);
  const chartW = 480, chartH = 220, chartInnerTop = 40, chartInnerBottom = 200;"""

                # Replace the block
                if old_block in text:
                    text = text.replace(old_block, new_block)
                    print("Replaced block successfully.")
                else:
                    print("Could not find the exact old block.")
                    # Try a regex replace just in case formatting slightly differs
                    # But the string matched exactly earlier.

                # Now replace the rect to add smooth transition
                old_rect = 'rx="4" fill={isPeak ? "var(--accent)" : ink} opacity={isPeak ? 1 : 0.78}/>'
                new_rect = 'rx="4" fill={isPeak ? "var(--accent)" : ink} opacity={isPeak ? 1 : 0.78} style={{ transition: "all 0.5s ease" }}/>'
                
                if old_rect in text:
                    text = text.replace(old_rect, new_rect)
                    print("Replaced rect successfully.")
                else:
                    print("Could not find old rect.")

                # Encode back
                new_data = text.encode('utf-8')
                if entry.get('compressed'):
                    new_data = gzip.compress(new_data)
                entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated OnStaffAI.html")
else:
    print("Manifest not found")
