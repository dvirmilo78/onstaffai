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
            
            if "const ChartsAnim = ({ lang }) => {" in text:
                
                # Replace the setBars logic
                old_setBars = """setBars(b => {
         const newBars = [...b.slice(1)];
         const last = newBars[newBars.length - 1];
         let next = last + (Math.random() * 40 - 20);
         if (next < 20) next = 20;
         if (next > 160) next = 160;
         newBars.push(Math.round(next));
         return newBars;
      });"""
                new_setBars = """setBars(b => {
         const newBars = [...b];
         for (let i=0; i<3; i++) {
            const idx = Math.floor(Math.random() * newBars.length);
            newBars[idx] += Math.floor(Math.random() * 15) + 5;
         }
         return newBars.map(val => val + Math.floor(Math.random() * 3));
      });"""
                text = text.replace(old_setBars, new_setBars)

                # Replace chart title
                old_title = '{lang === "he" ? "פעילות סוכנים" : "Agent activity · 12 hours"}'
                new_title = '{lang === "he" ? "משימות שהושלמו לפי סוכן" : "Tasks completed by agents"}'
                text = text.replace(old_title, new_title)

                # Replace x-axis
                old_xaxis = """{["08","10","12","14","16","18","20"].map((h, i) => (
            <text key={i} x={20 + 40 + i * 70} textAnchor="middle">{h}:00</text>
          ))}"""
                new_xaxis = """{bars.map((_, i) => {
            const barW = 24;
            const gap = (chartW - 40 - bars.length * barW) / (bars.length - 1);
            const x = 20 + i * (barW + gap);
            return <text key={i} x={x + barW/2} textAnchor="middle">A{i+1}</text>;
          })}"""
                text = text.replace(old_xaxis, new_xaxis)

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
