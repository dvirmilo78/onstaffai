import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'r') as f:
    content = f.read()

content = content.replace(
    '<span style="color:#ea580c;font-size:0.72rem;margin-right:6px;">מומלץ לסמן</span>',
    '<span style="color:#ea580c;font-size:0.72rem;margin-right:6px;">לא חובה, אך יעזור לנו להתאים עבורך את השירות</span>'
)
content = content.replace(
    '<span style="color:#ea580c;font-size:0.72rem;margin-right:6px;">מומלץ למלא</span>',
    '<span style="color:#ea580c;font-size:0.72rem;margin-right:6px;">לא חובה, אך יעזור לנו להתאים עבורך את השירות</span>'
)

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'w') as f:
    f.write(content)
