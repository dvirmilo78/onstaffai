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

file_id = "4a6fb28c-5e65-4bc9-ba76-50164d056976"
data = base64.b64decode(manifest[file_id]['data'])
data = gzip.decompress(data)
text = data.decode('utf-8')

old_contact_form = re.search(r'const ContactForm = \(\{ lang \}\) => \{.*?(?=const App = \(\) => \{)', text, re.DOTALL).group(0)

new_contact_form = r"""const ContactForm = ({ lang }) => {
  const [status, setStatus] = React.useState('idle');
  const [selectedPlan, setSelectedPlan] = React.useState('growth');
  const [selectedAgents, setSelectedAgents] = React.useState([]);

  const isHe = lang === 'he';

  const plans = [
    { id: 'starter', name: isHe ? 'Starter' : 'Starter', price: '₪490', agents: 3, desc: isHe ? 'לסטארטאפים ועסקים קטנים' : 'For startups and small businesses' },
    { id: 'growth', name: isHe ? 'Growth' : 'Growth', price: '₪990', agents: 6, desc: isHe ? 'לעסקים בצמיחה מהירה' : 'For fast-growing businesses' },
    { id: 'business', name: isHe ? 'Business' : 'Business', price: '₪1990', agents: 10, desc: isHe ? 'לארגונים וחברות מבוססות' : 'For established organizations' }
  ];

  const agentTypes = [
    { id: 'customer-service', name: isHe ? 'שירות לקוחות' : 'Customer Service' },
    { id: 'tech-support', name: isHe ? 'תמיכה טכנית' : 'Tech Support' },
    { id: 'sales', name: isHe ? 'מכירות' : 'Sales' },
    { id: 'marketing', name: isHe ? 'שיווק' : 'Marketing' },
    { id: 'operations', name: isHe ? 'תיאום פגישות' : 'Scheduling' },
    { id: 'finance', name: isHe ? 'כספים' : 'Finance' },
    { id: 'hr', name: isHe ? 'משאבי אנוש' : 'HR' },
    { id: 'pm', name: isHe ? 'מנהל פרויקטים' : 'Project Manager' }
  ];

  const currentPlan = plans.find(p => p.id === selectedPlan);

  const handlePlanChange = (planId) => {
    setSelectedPlan(planId);
    const newPlan = plans.find(p => p.id === planId);
    if (selectedAgents.length > newPlan.agents) {
      setSelectedAgents(selectedAgents.slice(0, newPlan.agents));
    }
  };

  const toggleAgent = (agentId) => {
    if (selectedAgents.includes(agentId)) {
      setSelectedAgents(selectedAgents.filter(a => a !== agentId));
    } else {
      if (selectedAgents.length < currentPlan.agents) {
        setSelectedAgents([...selectedAgents, agentId]);
      } else {
        alert(isHe ? `הגעת למכסת הסוכנים בחבילת ${currentPlan.name} (${currentPlan.agents} סוכנים)` : `You reached the agent limit for the ${currentPlan.name} plan (${currentPlan.agents} agents)`);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
      const queryRes = await fetch('https://firestore.googleapis.com/v1/projects/onstaffai/databases/(default)/documents:runQuery', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          structuredQuery: {
            from: [{ collectionId: 'leads' }],
            where: {
              fieldFilter: {
                field: { fieldPath: 'email' },
                op: 'EQUAL',
                value: { stringValue: data.email }
              }
            }
          }
        })
      });
      const queryJson = await queryRes.json();
      
      if (Array.isArray(queryJson)) {
        const activeLeads = queryJson.filter(item => item.document && item.document.fields && (!item.document.fields.status || item.document.fields.status.stringValue !== 'deleted'));
        if (activeLeads.length > 0) {
          setStatus('duplicate');
          return;
        }
      }

      const agentNames = selectedAgents.map(id => agentTypes.find(a => a.id === id).name).join(', ');

      const docData = {
        fields: {
          name: { stringValue: data.fullName || '' },
          company: { stringValue: data.company || '' },
          email: { stringValue: data.email || '' },
          phone: { stringValue: data.phone || '' },
          plan: { stringValue: currentPlan.name },
          agents: { stringValue: agentNames },
          status: { stringValue: "new" },
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
        plan: currentPlan.name,
        agents: agentNames,
        lid: leadId
      });
      const onboardUrl = window.location.origin + '/onboarding.html?' + params.toString();

      const emailRes = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_id: 'service_ne5z4wv',
          template_id: 'template_sl4n308',
          user_id: '7IoARO-EcljLAzrok',
          accessToken: 'qrDC3NWZhEoUpR_zFfFnC',
          template_params: {
            to_email: data.email,
            email: data.email,
            to: data.email,
            user_email: data.email,
            to_name: data.fullName,
            company: data.company,
            plan: currentPlan.name,
            agents: agentNames,
            onboard_url: onboardUrl,
            onboarding_link: onboardUrl
          }
        })
      });
      if (!emailRes.ok) {
        throw new Error('EmailJS failed');
      }

      setStatus('success');
      e.target.reset();
      setSelectedAgents([]);
    } catch (error) {
      console.error(error);
      setStatus('error');
    }
  };

  return (
    <section id="contact" style={{ padding: '80px 20px', background: 'var(--bg)', borderTop: '1px solid var(--line)' }}>
      <div className="wrap" style={{ maxWidth: '680px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <h2 style={{ fontSize: 'clamp(28px, 4vw, 40px)', marginBottom: '16px', color: 'var(--ink)' }}>
            {isHe ? (
            <React.Fragment>
                הזמן שלכם <strong style={{ color: 'var(--primary, #ea580c)' }}>להצטרף</strong> למהפכת ה-AI
            </React.Fragment>
            ) : (
            <React.Fragment>
                Time to <strong style={{ color: 'var(--primary, #ea580c)' }}>join</strong> the AI revolution
            </React.Fragment>
            )}
            </h2>
            <p style={{ color: 'var(--mute)', fontSize: '18px' }}>
            {isHe 
                ? 'בנו לכם צוות חכם, ייעלו תהליכים וחסכו זמן יקר. בחרו את המסלול והסוכנים שלכם:'
                : 'Build a smart team, streamline processes and save valuable time. Choose your plan:'}
            </p>
        </div>
        
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px', textAlign: isHe ? 'right' : 'left' }}>
          
          <div style={{ background: 'var(--bg-2)', padding: '24px', borderRadius: '16px', border: '1px solid var(--line)' }}>
              <label style={{ display: 'block', marginBottom: '16px', color: 'var(--ink)', fontSize: '18px', fontWeight: 'bold' }}>
                <span style={{ display: 'inline-block', width: '24px', height: '24px', background: 'var(--primary, #ea580c)', color: '#fff', borderRadius: '50%', textAlign: 'center', lineHeight: '24px', fontSize: '14px', marginInlineEnd: '8px' }}>1</span>
                {isHe ? 'בחרו מסלול התחברות ' : 'Choose a plan '}
                <span style={{color:'var(--primary, #ea580c)', fontSize:'14px', fontWeight: 'normal'}}>{isHe ? '(לא חובה)' : '(Optional)'}</span>
              </label>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
                  {plans.map(p => (
                      <div key={p.id} onClick={() => handlePlanChange(p.id)} style={{ cursor: 'pointer', padding: '16px', borderRadius: '12px', border: '2px solid', borderColor: selectedPlan === p.id ? 'var(--primary, #ea580c)' : 'var(--line)', background: selectedPlan === p.id ? 'rgba(234, 88, 12, 0.05)' : 'var(--bg)', transition: 'all 0.2s', position: 'relative' }}>
                          <div style={{ fontWeight: 'bold', fontSize: '18px', color: 'var(--ink)', marginBottom: '4px' }}>{p.name}</div>
                          <div style={{ color: 'var(--primary, #ea580c)', fontWeight: 'bold', fontSize: '20px', marginBottom: '8px' }}>{p.price}<span style={{fontSize:'12px', color:'var(--mute)'}}> / חודש</span></div>
                          <div style={{ fontSize: '13px', color: 'var(--mute)', marginBottom: '12px' }}>{p.desc}</div>
                          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', background: 'var(--bg-2)', padding: '4px 8px', borderRadius: '6px', fontSize: '12px', fontWeight: 'bold' }}>
                              <span style={{ color: 'var(--primary, #ea580c)' }}>{p.agents}</span> סוכנים
                          </div>
                      </div>
                  ))}
              </div>
          </div>

          <div style={{ background: 'var(--bg-2)', padding: '24px', borderRadius: '16px', border: '1px solid var(--line)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <label style={{ color: 'var(--ink)', fontSize: '18px', fontWeight: 'bold', margin: 0 }}>
                    <span style={{ display: 'inline-block', width: '24px', height: '24px', background: 'var(--primary, #ea580c)', color: '#fff', borderRadius: '50%', textAlign: 'center', lineHeight: '24px', fontSize: '14px', marginInlineEnd: '8px' }}>2</span>
                    {isHe ? 'אילו סוכנים מעניינים אתכם? ' : 'Which agents do you need? '}
                    <span style={{color:'var(--primary, #ea580c)', fontSize:'14px', fontWeight: 'normal'}}>{isHe ? '(לא חובה)' : '(Optional)'}</span>
                </label>
                <div style={{ fontSize: '14px', color: 'var(--mute)', background: 'var(--bg)', padding: '4px 10px', borderRadius: '20px', border: '1px solid var(--line)' }}>
                    נבחרו <strong style={{color: 'var(--primary, #ea580c)'}}>{selectedAgents.length}</strong> מתוך <strong>{currentPlan.agents}</strong>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px' }}>
              {agentTypes.map(agent => {
                  const isSelected = selectedAgents.includes(agent.id);
                  const isFull = !isSelected && selectedAgents.length >= currentPlan.agents;
                  return (
                      <div key={agent.id} onClick={() => toggleAgent(agent.id)} style={{ cursor: isFull ? 'not-allowed' : 'pointer', padding: '12px', borderRadius: '10px', border: '1px solid', borderColor: isSelected ? 'var(--primary, #ea580c)' : 'var(--line)', background: isSelected ? 'var(--primary, #ea580c)' : 'var(--bg)', color: isSelected ? '#fff' : 'var(--ink)', opacity: isFull ? 0.5 : 1, transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px', fontWeight: '500' }}>
                          <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '24px', height: '24px', background: isSelected ? 'rgba(255,255,255,0.2)' : 'var(--bg-2)', borderRadius: '6px' }}>
                              {isSelected ? '✓' : '+'}
                          </span>
                          {agent.name}
                      </div>
                  );
              })}
            </div>
            {selectedAgents.length >= currentPlan.agents && (
                <div style={{ marginTop: '12px', fontSize: '13px', color: 'var(--primary, #ea580c)', textAlign: 'center' }}>
                    {isHe ? 'הגעתם למקסימום הסוכנים בחבילה זו. שדרגו חבילה כדי להוסיף עוד סוכנים.' : 'You have reached the maximum agents for this plan.'}
                </div>
            )}
          </div>

          <div style={{ background: 'var(--bg-2)', padding: '24px', borderRadius: '16px', border: '1px solid var(--line)' }}>
              <label style={{ display: 'block', marginBottom: '20px', color: 'var(--ink)', fontSize: '18px', fontWeight: 'bold' }}>
                <span style={{ display: 'inline-block', width: '24px', height: '24px', background: 'var(--primary, #ea580c)', color: '#fff', borderRadius: '50%', textAlign: 'center', lineHeight: '24px', fontSize: '14px', marginInlineEnd: '8px' }}>3</span>
                {isHe ? 'השאירו פרטים ליצירת קשר' : 'Contact Details'}
              </label>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div>
                    <label style={{ display: 'block', marginBottom: '8px', color: 'var(--mute)', fontSize: '14px' }}>{isHe ? 'שם מלא *' : 'Full Name *'}</label>
                    <input type="text" name="fullName" required placeholder="ישראל ישראלי" style={{ width: '100%', padding: '14px', borderRadius: '10px', border: '1px solid var(--line)', background: 'var(--bg)', color: 'var(--ink)', outline: 'none' }} />
                  </div>
                  <div>
                    <label style={{ display: 'block', marginBottom: '8px', color: 'var(--mute)', fontSize: '14px' }}>{isHe ? 'שם חברה *' : 'Company Name *'}</label>
                    <input type="text" name="company" required placeholder="חברה בע״מ" style={{ width: '100%', padding: '14px', borderRadius: '10px', border: '1px solid var(--line)', background: 'var(--bg)', color: 'var(--ink)', outline: 'none' }} />
                  </div>
                  <div>
                    <label style={{ display: 'block', marginBottom: '8px', color: 'var(--mute)', fontSize: '14px' }}>{isHe ? 'טלפון *' : 'Phone *'}</label>
                    <input type="tel" name="phone" required placeholder="05X-XXXXXXX" style={{ width: '100%', padding: '14px', borderRadius: '10px', border: '1px solid var(--line)', background: 'var(--bg)', color: 'var(--ink)', outline: 'none' }} />
                  </div>
                  <div>
                    <label style={{ display: 'block', marginBottom: '8px', color: 'var(--mute)', fontSize: '14px' }}>{isHe ? 'דוא"ל *' : 'Email *'}</label>
                    <input type="email" name="email" required placeholder="example@company.co.il" style={{ width: '100%', padding: '14px', borderRadius: '10px', border: '1px solid var(--line)', background: 'var(--bg)', color: 'var(--ink)', outline: 'none' }} />
                  </div>
              </div>
          </div>
          
          <button type="submit" disabled={status === 'loading'} className="btn btn-primary" style={{ padding: '20px', fontSize: '24px', marginTop: '8px', textAlign: 'center', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', fontWeight: '900', borderRadius: '16px', border: 'none', cursor: 'pointer', boxShadow: '0 8px 25px rgba(234, 88, 12, 0.4)', transition: 'transform 0.2s' }} onMouseOver={e => e.currentTarget.style.transform='translateY(-2px)'} onMouseOut={e => e.currentTarget.style.transform='translateY(0)'}>
            {status === 'loading' ? (isHe ? 'שולח נתונים...' : 'Sending...') : (isHe ? 'יאללה, בואו נתחיל!' : "Let's Start!")}
          </button>
          
          {status === 'success' && <div style={{ color: '#10B981', marginTop: '16px', fontWeight: '900', fontSize: '18px', padding: '16px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.2)', textAlign: 'center' }}>{isHe ? 'הפרטים נשלחו בהצלחה! סוכן AI שלנו יצור איתך קשר בקרוב עם כל המידע.' : 'Details sent successfully! An AI agent will contact you shortly.'}</div>}
          {status === 'error' && <div style={{ color: 'var(--rose)', marginTop: '16px', fontWeight: 'bold', textAlign: 'center' }}>{isHe ? 'אירעה שגיאה. נסה שוב.' : 'An error occurred. Please try again.'}</div>}
          {status === 'duplicate' && <div style={{ color: '#F59E0B', marginTop: '16px', fontWeight: 'bold', fontSize: '18px', padding: '16px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '12px', border: '1px solid rgba(245, 158, 11, 0.2)', textAlign: 'center' }}>{isHe ? 'כתובת המייל הזו כבר קיימת אצלנו במערכת. נציג יחזור אליכם בהקדם!' : 'This email already exists in our system. An agent will contact you shortly!'}</div>}
        </form>
      </div>
    </section>
  );
};
"""

text = text.replace(old_contact_form, new_contact_form)

comp_data = gzip.compress(text.encode('utf-8'))
manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
new_manifest_json = json.dumps(manifest)
new_html = html.replace(manifest_json, new_manifest_json)

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Patch V5 applied to OnStaffAI.html successfully!")
