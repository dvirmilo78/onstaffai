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
    
    app_uuid = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
    if app_uuid in manifest:
        entry = manifest[app_uuid]
        data = base64.b64decode(entry['data'])
        if entry.get('compressed'):
            data = gzip.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        
        # Replace the H2 title
        old_h2_content = "{isHe ? 'מהפכת ה AI כבר כאן , עכשיו הזמן שלהם שתצטרפו אליה' : 'The AI revolution is here, time to join it'}"
        new_h2_content = """{isHe ? (
          <React.Fragment>
            <strong style={{ color: 'var(--primary, #ea580c)' }}>מהפכת ה AI</strong> כבר כאן , עכשיו הזמן שלכם <strong style={{ color: 'var(--primary, #ea580c)' }}>להצטרף</strong> אליה
          </React.Fragment>
        ) : (
          <React.Fragment>
            The <strong style={{ color: 'var(--primary, #ea580c)' }}>AI revolution</strong> is here, time to <strong style={{ color: 'var(--primary, #ea580c)' }}>join</strong> it
          </React.Fragment>
        )}"""
        
        text = text.replace(old_h2_content, new_h2_content)
        
        # Replace the button
        old_btn_regex = r'<button type="submit" disabled=\{status === \'loading\'\} className="btn btn-primary" style=\{\{ padding: \'14px\', fontSize: \'16px\', marginTop: \'10px\' \}\}>\s*\{status === \'loading\' \? \(isHe \? \'שולח...\' : \'Sending...\'\) : \(isHe \? \'שלח פרטים\' : \'Submit\'\)\}\s*</button>'
        
        new_btn = """<style>{`
          .contact-btn-highlight {
            animation: pulse-orange 2s infinite;
            transition: all 0.3s ease;
          }
          .contact-btn-highlight:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.6);
          }
          @keyframes pulse-orange {
            0% { box-shadow: 0 0 0 0 rgba(234, 88, 12, 0.7); }
            70% { box-shadow: 0 0 0 12px rgba(234, 88, 12, 0); }
            100% { box-shadow: 0 0 0 0 rgba(234, 88, 12, 0); }
          }
        `}</style>
        <button type="submit" disabled={status === 'loading'} className="btn btn-primary contact-btn-highlight" style={{ padding: '16px', fontSize: '22px', marginTop: '15px', textAlign: 'center', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', fontWeight: '900', borderRadius: '12px' }}>
          {status === 'loading' ? (isHe ? 'מצטרף...' : 'Joining...') : (isHe ? 'הצטרפו עכשיו!' : 'Join Now!')}
        </button>"""
        
        text = re.sub(old_btn_regex, new_btn, text)
        
        new_data = text.encode('utf-8')
        if entry.get('compressed'):
            new_data = gzip.compress(new_data)
        entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Successfully updated Contact form title and button.")
