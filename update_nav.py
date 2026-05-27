import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
data = base64.b64decode(manifest[file_id]['data'])
if manifest[file_id].get('compressed'):
    data = gzip.decompress(data)
text = data.decode('utf-8')

# The current nav block
old_nav = """      <nav className="nav">
        <div className="wrap nav-inner">
          <div className="brand"><div style={{display: "flex", alignItems: "center", gap: "clamp(4px, 1.5vw, 10px)"}}><img src="assets/onstaff_icon.png" alt="OnStaffAI Icon" style={{height: "clamp(35px, 8vw, 65px)", width: "auto"}}/><img src="assets/onstaff_text.png" alt="OnStaffAI Text" style={{height: "clamp(24px, 5.5vw, 45px)", width: "auto"}}/></div></div>
          <div className="nav-links">
            <a href="#agents">{L.nav.agents}</a>
            <a href="#how">{L.nav.how}</a>
            <a href="#roi">{L.nav.roi}</a>
            <a href="#demo">{L.nav.demo}</a>
            <a href="#pricing">{L.nav.pricing}</a>
          </div>
          <div className="nav-right">
            <div className="lang-toggle">
              <button className={lang === "he" ? "on" : ""} onClick={() => setLang("he")}>עב</button>
              <button className={lang === "en" ? "on" : ""} onClick={() => setLang("en")}>EN</button>
            </div>
            <a href="#contact" className="btn btn-primary" style={{ padding: "9px 16px", fontSize: 14 }}>{L.cta.primary}</a>
          </div>
        </div>
      </nav>"""

new_nav = """      <nav className="nav">
        <div className="wrap nav-inner">
          <div className="brand"><div style={{display: "flex", alignItems: "center", gap: "clamp(4px, 1.5vw, 10px)"}}><img src="assets/onstaff_icon.png" alt="OnStaffAI Icon" style={{height: "clamp(35px, 8vw, 65px)", width: "auto"}}/><img src="assets/onstaff_text.png" alt="OnStaffAI Text" style={{height: "clamp(24px, 5.5vw, 45px)", width: "auto"}}/></div></div>
          
          <div className="nav-links desktop-only">
            <a href="#agents">{L.nav.agents}</a>
            <a href="#how">{L.nav.how}</a>
            <a href="#roi">{L.nav.roi}</a>
            <a href="#demo">{L.nav.demo}</a>
            <a href="#pricing">{L.nav.pricing}</a>
          </div>
          
          <div className="nav-right desktop-only">
            <div className="lang-toggle">
              <button className={lang === "he" ? "on" : ""} onClick={() => setLang("he")}>עב</button>
              <button className={lang === "en" ? "on" : ""} onClick={() => setLang("en")}>EN</button>
            </div>
            <a href="client_portal.html" className="btn" style={{ padding: "9px 16px", fontSize: 14, background: "transparent", border: "1px solid var(--line)", color: "var(--ink)", borderRadius: "999px" }}>{isHe ? 'כבר לקוח? התחבר' : 'Login'}</a>
            <a href="#contact" className="btn btn-primary" style={{ padding: "9px 16px", fontSize: 14 }}>{L.cta.primary}</a>
          </div>

          <div className={`hamburger ${menuOpen ? 'active' : ''}`} onClick={() => setMenuOpen(!menuOpen)}>
             <span className="bar"></span>
             <span className="bar"></span>
             <span className="bar"></span>
          </div>
        </div>
        
        <div className={`mobile-menu ${menuOpen ? 'open' : ''}`}>
          <div className="mobile-menu-inner">
            <a href="#agents" onClick={() => setMenuOpen(false)}>{L.nav.agents}</a>
            <a href="#how" onClick={() => setMenuOpen(false)}>{L.nav.how}</a>
            <a href="#roi" onClick={() => setMenuOpen(false)}>{L.nav.roi}</a>
            <a href="#demo" onClick={() => setMenuOpen(false)}>{L.nav.demo}</a>
            <a href="#pricing" onClick={() => setMenuOpen(false)}>{L.nav.pricing}</a>
            
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <a href="#contact" className="btn btn-primary" onClick={() => setMenuOpen(false)} style={{ textAlign: 'center', padding: '12px' }}>{L.cta.primary}</a>
              <a href="client_portal.html" className="btn" onClick={() => setMenuOpen(false)} style={{ textAlign: 'center', padding: '12px', background: "transparent", border: "1px solid var(--line)", color: "var(--ink)", borderRadius: "12px", fontWeight: "900" }}>{isHe ? 'כבר לקוח? התחבר' : 'Login'}</a>
            </div>
            
            <div className="lang-toggle" style={{ marginTop: '20px', justifyContent: 'center' }}>
              <button className={lang === "he" ? "on" : ""} onClick={() => { setLang("he"); setMenuOpen(false); }}>עב</button>
              <button className={lang === "en" ? "on" : ""} onClick={() => { setLang("en"); setMenuOpen(false); }}>EN</button>
            </div>
          </div>
        </div>
      </nav>"""

# We also need to add menuOpen to the state variables.
old_state = """  const [lang, setLang] = useState("he");
  const [tweaks, setTweaks] = useState(defaults);
  const [tweaksOpen, setTweaksOpen] = useState(false);"""

new_state = """  const [lang, setLang] = useState("he");
  const [tweaks, setTweaks] = useState(defaults);
  const [tweaksOpen, setTweaksOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);"""

if old_state in text and old_nav in text:
    text = text.replace(old_state, new_state)
    text = text.replace(old_nav, new_nav)
    print("Replaced navigation in JSX successfully.")
else:
    print("Could not find blocks to replace in the bundle.")
    print("Did we find state?", old_state in text)
    print("Did we find nav?", old_nav in text)
    exit(1)

# Now, we also want to remove the JS injection snippet from OnStaffAI.html
# The string is `(function injectClientLink() {` to `})();`
# It's better to just regex it out.
import re
new_html = html
new_html = re.sub(r'<script>\s*// Wait for React to render.*?injectClientLink\(\);\s*</script>', '', new_html, flags=re.DOTALL)

comp_data = gzip.compress(text.encode('utf-8'))
manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
new_manifest_json = json.dumps(manifest)
new_html = new_html.replace(manifest_json, new_manifest_json)

with open('OnStaffAI.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✅ Nav updated, OnStaffAI.html written.")
