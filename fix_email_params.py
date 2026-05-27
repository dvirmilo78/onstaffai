import re

files = [
    "/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html",
    "/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/onboarding.html",
    "/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/functions/index.js"
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # index.html
    if filepath.endswith("index.html"):
        content = content.replace("to_email: email,", "to_email: email, email: email, to: email, user_email: email,")
        content = content.replace("to_email: email\n", "to_email: email,\nemail: email,\nto: email,\nuser_email: email\n")
    
    # onboarding.html
    elif filepath.endswith("onboarding.html"):
        content = content.replace("to_email: leadData.email,", "to_email: leadData.email, email: leadData.email, to: leadData.email, user_email: leadData.email,")
    
    # index.js
    elif filepath.endswith("index.js"):
        content = content.replace("to_email: lead.email,", "to_email: lead.email, email: lead.email, to: lead.email, user_email: lead.email,")
        content = content.replace("to_email: ADMIN_EMAIL,", "to_email: ADMIN_EMAIL, email: ADMIN_EMAIL, to: ADMIN_EMAIL, user_email: ADMIN_EMAIL,")

    with open(filepath, 'w') as f:
        f.write(content)
