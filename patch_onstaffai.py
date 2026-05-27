import json
import base64
import zlib
import gzip
import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

manifest_match = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
manifest_json = manifest_match.group(1)
manifest = json.loads(manifest_json)

# 1. Update the React Bundle (App.jsx)
file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
data = base64.b64decode(manifest[file_id]['data'])
data = gzip.decompress(data)
text = data.decode('utf-8')

old_contact_form = re.search(r'const ContactForm = \(\{ lang \}\) => \{.*?(?=const App = \(\) => \{)', text, re.DOTALL)

new_contact_form = """const ContactForm = ({ lang }) => {
  const [status, setStatus] = React.useState('idle');
  const [selectedPlan, setSelectedPlan] = React.useState('growth');
  const [selectedAgents, setSelectedAgents] = React.useState([]);

  const isHe = lang === 'he';

  const toggleAgent = (agent) => {
    setSelectedAgents(prev => prev.includes(agent) ? prev.filter(a => a !== agent) : [...prev, agent]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
      const docData = {
        fields: {
          name: { stringValue: data.fullName || '' },
          company: { stringValue: data.company || '' },
          email: { stringValue: data.email || '' },
          phone: { stringValue: data.phone || '' },
          plan: { stringValue: selectedPlan },
          agents: { stringValue: selectedAgents.join(',') },
          status: { stringValue: "New" },
          step: { integerValue: 1 },
          createdAt: { timestampValue: new Date().toISOString() },
          lastActivity: { timestampValue: new Date().toISOString() }
        }
      };
      
      const fbRes = await fetch('https://firestore.googleapis.com/v1/projects/onstaffai/databases/(default)/documents/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(docData)
      });
      const fbJson = await fbRes.json();
      const leadId = fbJson.name ? fbJson.name.split('/').pop() : '';

      const params = new URLSearchParams({
        name: data.fullName || '',
        company: data.company || '',
        email: data.email || '',
        phone: data.phone || '',
        plan: selectedPlan,
        agents: selectedAgents.join(','),
        lid: leadId
      });
      const onboardUrl = window.location.origin + '/onboarding.html?' + params.toString();

      if (window.emailjs) {
        await window.emailjs.send('service_ne5z4wv', 'template_sl4n308', {
          to_email: data.email,
          to_name: data.fullName,
          onboard_url: onboardUrl,
          onboarding_link: onboardUrl
        });
      }

      setStatus('success');
      e.target.reset();
      setSelectedAgents([]);
    } catch (error) {
      console.error('Error submitting form:', error);
      setStatus('error');
    }
  };

  return (
    <section id="contact" style={{ padding: '60px 20px', background: 'var(--bg)', borderTop: '1px solid var(--line)' }}>
      <div className="wrap" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
        <h2 style={{ fontSize: '32px', marginBottom: '16px', color: 'var(--ink)' }}>
          {isHe ? (
          <React.Fragment>
            <strong style={{ color: 'var(--primary, #ea580c)' }}>מהפכת ה AI</strong> כבר כאן , עכשיו הזמן שלכם <strong style={{ color: 'var(--primary, #ea580c)' }}>להצטרף</strong> אליה
          </React.Fragment>
        ) : (
          <React.Fragment>
            The <strong style={{ color: 'var(--primary, #ea580c)' }}>AI revolution</strong> is here, time to <strong style={{ color: 'var(--primary, #ea580c)' }}>join</strong> it
          </React.Fragment>
        )}
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
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'שם חברה *' : 'Company Name *'}</label>
            <input type="text" name="company" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'טלפון *' : 'Phone *'}</label>
            <input type="tel" name="phone" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>{isHe ? 'דוא"ל *' : 'Email *'}</label>
            <input type="email" name="email" required style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)' }} />
          </div>

          <div style={{ marginTop: '10px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>
              {isHe ? 'כמה סוכנים תרצו להפעיל? ' : 'How many agents do you need? '}
              <span style={{color:'var(--primary, #ea580c)', fontSize:'12px'}}>{isHe ? '(לא חובה, אך יעזור לנו להתאים עבורך את השירות)' : '(Optional)'}</span>
            </label>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {['1', '2-3', '4-6', '7+'].map(agentCount => (
                <div key={agentCount} onClick={() => toggleAgent(agentCount)} style={{ cursor: 'pointer', padding: '8px 16px', borderRadius: '20px', border: '1px solid var(--line)', background: selectedAgents.includes(agentCount) ? 'var(--primary, #ea580c)' : 'var(--bg-2)', color: selectedAgents.includes(agentCount) ? '#fff' : 'var(--ink)', transition: 'all 0.2s', fontSize: '14px' }}>
                  {agentCount}
                </div>
              ))}
            </div>
          </div>

          <div style={{ marginTop: '10px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--ink)' }}>
              {isHe ? 'באיזה מסלול אתם מעוניינים? ' : 'Which plan are you interested in? '}
              <span style={{color:'var(--primary, #ea580c)', fontSize:'12px'}}>{isHe ? '(לא חובה)' : '(Optional)'}</span>
            </label>
            <select value={selectedPlan} onChange={e => setSelectedPlan(e.target.value)} style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--line)', background: 'var(--bg-2)', color: 'var(--ink)', appearance: 'auto' }}>
              <option value="starter">{isHe ? 'Starter - ₪490' : 'Starter - ₪490'}</option>
              <option value="growth">{isHe ? 'Growth - ₪990' : 'Growth - ₪990'}</option>
              <option value="business">{isHe ? 'Business - ₪1990' : 'Business - ₪1990'}</option>
            </select>
          </div>
          
          <style>{`
          .contact-btn-highlight {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(234, 88, 12, 0.3);
          }
          .contact-btn-highlight::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%);
            transform: skewX(-25deg);
            transition: all 0.7s ease;
          }
          .contact-btn-highlight:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.6);
          }
          .contact-btn-highlight:hover::after {
            left: 150%;
            transition: left 0.7s ease-in-out;
          }
        `}</style>
        <button type="submit" disabled={status === 'loading'} className="btn btn-primary contact-btn-highlight" style={{ padding: '16px', fontSize: '22px', marginTop: '15px', textAlign: 'center', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', fontWeight: '900', borderRadius: '12px', border: 'none', cursor: 'pointer' }}>
          {status === 'loading' ? (isHe ? 'שולח...' : 'Sending...') : (isHe ? 'הצטרפו עכשיו!' : 'Join Now!')}
        </button>
          
          {status === 'success' && <div style={{ color: '#10B981', marginTop: '16px', fontWeight: '900', fontSize: '18px', padding: '10px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>{isHe ? 'הפרטים נשלחו בהצלחה! סוכן חכם יצור איתך קשר בקרוב.' : 'Details sent successfully! A smart agent will contact you shortly.'}</div>}
          {status === 'error' && <div style={{ color: 'var(--rose)', marginTop: '16px', fontWeight: 'bold' }}>{isHe ? 'אירעה שגיאה. נסה שוב.' : 'An error occurred. Please try again.'}</div>}
        </form>
      </div>
    </section>
  );
};
"""

text = text.replace(old_contact_form.group(0), new_contact_form)

comp_data = gzip.compress(text.encode('utf-8'))
manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
new_manifest_json = json.dumps(manifest)
new_html = html.replace(manifest_json, new_manifest_json)

# 2. Add EmailJS SDK to the HTML string itself
emailjs_script = """<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>emailjs.init({publicKey: "7IoARO-EcljLAzrok"});</script>
</head>"""
new_html = new_html.replace('</head>', emailjs_script)

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Patch applied to OnStaffAI.html successfully!")
