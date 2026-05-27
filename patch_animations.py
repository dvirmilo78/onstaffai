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
    
    # 7e79941f-698d-4ffa-993c-2d7c4469260f is the UUID for illustrations.jsx
    uuid = "7e79941f-698d-4ffa-993c-2d7c4469260f"
    if uuid in manifest:
        entry = manifest[uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # 1. Patch Tech Support (Yuval)
        old_tech = '''{k === "techsupport" && (<g>
          <rect x="44" y="40" width="112" height="70" rx="6" fill={ink}/>
          <rect x="50" y="50" width="100" height="54" rx="2" fill={bg}/>
          <text x="60" y="70" fontSize="9" fontFamily="JetBrains Mono" fill={ink}>$ fix --bug</text>
          <text x="60" y="84" fontSize="9" fontFamily="JetBrains Mono" fill={ink} opacity=".6">→ patching...</text>
          <text x="60" y="98" fontSize="9" fontFamily="JetBrains Mono" fill={ink}>✓ resolved<tspan className="blink">_</tspan></text>
          <rect x="80" y="110" width="40" height="14" rx="2" fill={ink}/>
          <rect x="70" y="124" width="60" height="4" rx="2" fill={ink} opacity=".3"/>
        </g>)}'''
        
        new_tech = '''{k === "techsupport" && (<g>
          <rect x="44" y="40" width="112" height="70" rx="6" fill={ink}/>
          <rect x="50" y="50" width="100" height="54" rx="2" fill={bg}/>
          <text x="60" y="66" fontSize="9" fontFamily="JetBrains Mono" fill={ink}>$ fix --bug</text>
          <rect x="60" y="76" width="80" height="4" rx="2" fill={ink} opacity=".2"/>
          <rect x="60" y="76" width="80" height="4" rx="2" fill={ink} className="hr-bar"/>
          <text x="60" y="94" fontSize="9" fontFamily="JetBrains Mono" fill={ink} className="blink">✓ resolved_</text>
          <rect x="80" y="110" width="40" height="14" rx="2" fill={ink}/>
          <rect x="70" y="124" width="60" height="4" rx="2" fill={ink} opacity=".3"/>
          <g className="orbit" style={{transformOrigin:'130px 60px'}}>
             <circle cx="130" cy="50" r="4" fill={ink} opacity=".5"/>
          </g>
        </g>)}'''
        
        text = text.replace(old_tech, new_tech)

        # 2. Patch Collect (Avi)
        old_collect = '''{k === "collect" && (<g>
          <rect x="40" y="36" width="120" height="88" rx="10" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="50" width="70" height="6" rx="3" fill={ink}/>
          <rect x="52" y="62" width="96" height="4" rx="2" fill={ink} opacity=".3"/>
          <rect x="52" y="72" width="80" height="4" rx="2" fill={ink} opacity=".3"/>
          <rect x="52" y="92" width="40" height="20" rx="4" fill={ink}/>
          <text x="72" y="106" textAnchor="middle" fontSize="10" fontWeight="700" fill={bg} fontFamily="Space Grotesk">שלם</text>
          <circle cx="148" cy="48" r="10" fill={ink} className="wiggle"/>
          <text x="148" y="52" textAnchor="middle" fontSize="10" fontWeight="700" fill={bg}>!</text>
        </g>)}'''
        
        new_collect = '''{k === "collect" && (<g>
          <rect x="40" y="36" width="120" height="88" rx="10" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="50" width="70" height="6" rx="3" fill={ink}/>
          <rect x="52" y="62" width="96" height="4" rx="2" fill={ink} opacity=".3" className="hr-bar"/>
          <rect x="52" y="72" width="80" height="4" rx="2" fill={ink} opacity=".3" className="hr-bar" style={{animationDelay:".2s"}}/>
          <g className="wiggle">
            <rect x="52" y="92" width="40" height="20" rx="4" fill={ink}/>
            <text x="72" y="106" textAnchor="middle" fontSize="10" fontWeight="700" fill={bg} fontFamily="Space Grotesk">שלם</text>
          </g>
          <g className="pulse-dot" style={{transformOrigin:'148px 48px'}}>
            <circle cx="148" cy="48" r="12" fill={ink}/>
            <text x="148" y="53" textAnchor="middle" fontSize="12" fontWeight="700" fill={bg}>₪</text>
          </g>
        </g>)}'''
        
        text = text.replace(old_collect, new_collect)
        
        # 3. Patch Content (Shir)
        old_content = '''{k === "content" && (<g>
          <rect x="40" y="30" width="120" height="100" rx="6" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="44" width="74" height="8" rx="2" fill={ink}/>
          <rect x="52" y="60" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="70" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="80" width="72" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="96" width="96" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="52" y="106" width="60" height="3" rx="1.5" fill={ink} opacity=".4"/>
          <rect x="114" y="106" width="10" height="14" rx="1" fill={ink} className="blink"/>
        </g>)}'''
        
        new_content = '''{k === "content" && (<g>
          <rect x="40" y="30" width="120" height="100" rx="6" fill="var(--bg)" stroke={ink} strokeWidth="2"/>
          <rect x="52" y="44" width="74" height="8" rx="2" fill={ink} className="hr-bar"/>
          <rect x="52" y="60" width="96" height="3" rx="1.5" fill={ink} opacity=".4" className="hr-bar" style={{animationDelay:".2s"}}/>
          <rect x="52" y="70" width="96" height="3" rx="1.5" fill={ink} opacity=".4" className="hr-bar" style={{animationDelay:".4s"}}/>
          <rect x="52" y="80" width="72" height="3" rx="1.5" fill={ink} opacity=".4" className="hr-bar" style={{animationDelay:".6s"}}/>
          <rect x="52" y="96" width="96" height="3" rx="1.5" fill={ink} opacity=".4" className="hr-bar" style={{animationDelay:".8s"}}/>
          <rect x="52" y="106" width="60" height="3" rx="1.5" fill={ink} opacity=".4" className="hr-bar" style={{animationDelay:"1s"}}/>
          <rect x="116" y="101" width="6" height="12" rx="1" fill={ink} className="blink"/>
        </g>)}'''

        text = text.replace(old_content, new_content)
        
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Patched animations successfully.")
