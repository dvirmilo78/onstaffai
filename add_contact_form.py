import json
import base64
import gzip
import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

# New Component Code
contact_form_code = """
const ContactForm = ({ lang }) => {
  const [status, setStatus] = React.useState('idle');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    data.timestamp = new Date().toISOString();
    
    // Placeholder Webhook URL for Make.com / Zapier
    // TODO: User needs to replace this with their actual webhook URL
    const webhookUrl = 'https://hook.us1.make.com/PLACEHOLDER_WEBHOOK_URL';
    
    try {
      // We will try to send to the webhook. In a real scenario, this might fail due to CORS if the webhook is not configured correctly, 
      // but Make/Zapier usually accept no-cors or simple POST requests.
      await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).catch(e => console.warn('Webhook warning (expected if no-cors or placeholder):', e));
      
      // We also save it to localStorage for the simple admin dashboard
      const existingLeads = JSON.parse(localStorage.getItem('onstaff_leads') || '[]');
      existingLeads.push({...data, status: 'New', id: Date.now()});
      localStorage.setItem('onstaff_leads', JSON.stringify(existingLeads));

      setStatus('success');
      e.target.reset();
    } catch (error) {
      console.error('Error submitting form:', error);
      setStatus('error');
    }
  };

  const isHe = lang === 'he';

  return (
    <section id="contact" style={{ padding: '60px 20px', background: 'var(--bg)', borderTop: '1px solid var(--line)' }}>
      <div className="wrap" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
        <h2 style={{ fontSize: '32px', marginBottom: '16px', color: 'var(--ink)' }}>
          {isHe ? 'יצירת קשר ותחילת תהליך' : 'Contact Us & Onboarding'}
        </h2>
        <p style={{ color: 'var(--mute)', marginBottom: '32px' }}>
          {isHe 
            ? 'השאירו פרטים ואחד מסוכני ה-AI שלנו יצור איתכם קשר וידריך אתכם לאורך כל תהליך ההטמעה.'
            : 'Leave your details and one of our AI agents will contact you and guide you through the onboarding process.'}
        </p>
        
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px', textAlign: isHe ? 'right' : 'left' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'שם מלא *' : 'Full Name *'}</label>
            <input type="text" name="fullName" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'טלפון *' : 'Phone *'}</label>
            <input type="tel" name="phone" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'דוא"ל *' : 'Email *'}</label>
            <input type="email" name="email" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>
          
          <button type="submit" disabled={status === 'loading'} className="btn btn-primary" style={{ padding: '14px', fontSize: '16px', marginTop: '10px' }}>
            {status === 'loading' ? (isHe ? 'שולח...' : 'Sending...') : (isHe ? 'שלח פרטים' : 'Submit')}
          </button>
          
          {status === 'success' && <div style={{ color: 'var(--mint)', marginTop: '16px' }}>{isHe ? 'הפרטים נשלחו בהצלחה! סוכן חכם יצור איתך קשר בקרוב.' : 'Details sent successfully! A smart agent will contact you shortly.'}</div>}
          {status === 'error' && <div style={{ color: 'var(--rose)', marginTop: '16px' }}>{isHe ? 'אירעה שגיאה. נסה שוב.' : 'An error occurred. Please try again.'}</div>}
        </form>
      </div>
    </section>
  );
};

"""

uuid_target = "4a6fb28c-5e65-4bc9-ba76-50164d056976"

if uuid_target in manifest:
    entry = manifest[uuid_target]
    data = base64.b64decode(entry['data'])
    if entry.get('compressed'):
        data = gzip.decompress(data)
    text = data.decode('utf-8', errors='ignore')
    
    # Inject ContactForm component definition right before the App component
    app_idx = text.find("const App =")
    if app_idx != -1:
        text = text[:app_idx] + contact_form_code + text[app_idx:]
        
    # Inject <ContactForm lang={lang} /> before <Footer
    footer_idx = text.find("<Footer t={L.footer}/>")
    if footer_idx != -1:
        text = text[:footer_idx] + "<ContactForm lang={lang}/>\n      " + text[footer_idx:]

    new_data = text.encode('utf-8')
    if entry.get('compressed'):
        new_data = gzip.compress(new_data)
    entry['data'] = base64.b64encode(new_data).decode('utf-8')

    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    new_html = html[:manifest_match.start(1)] + new_manifest_json + html[manifest_match.end(1):]
    
    with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    print("Injected Contact Form into OnStaffAI.html")
else:
    print("Could not find the target chunk.")
