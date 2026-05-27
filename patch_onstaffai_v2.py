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

# The old text has window.emailjs.send
old_email_code = """if (window.emailjs) {
        await window.emailjs.send('service_ne5z4wv', 'template_sl4n308', {
          to_email: data.email,
          to_name: data.fullName,
          onboard_url: onboardUrl,
          onboarding_link: onboardUrl
        });
      }"""

new_email_code = """const emailRes = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
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
            plan: selectedPlan,
            agents: selectedAgents.join(','),
            onboard_url: onboardUrl,
            onboarding_link: onboardUrl
          }
        })
      });
      if (!emailRes.ok) {
        const errText = await emailRes.text();
        console.error('EmailJS Error:', errText);
        throw new Error('EmailJS failed: ' + errText);
      }"""

if old_email_code in text:
    text = text.replace(old_email_code, new_email_code)
    
    comp_data = gzip.compress(text.encode('utf-8'))
    manifest[file_id]['data'] = base64.b64encode(comp_data).decode('utf-8')
    new_manifest_json = json.dumps(manifest)
    new_html = html.replace(manifest_json, new_manifest_json)

    with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/OnStaffAI.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("Patch V2 applied to OnStaffAI.html successfully!")
else:
    print("Could not find the old email code string.")
