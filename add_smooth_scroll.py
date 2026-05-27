import re

with open('OnStaffAI.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add html { scroll-behavior: smooth; } just after <style>
if '<style>' in html:
    html = html.replace('<style>', '<style>\nhtml { scroll-behavior: smooth; }\n')

with open('OnStaffAI.html', 'w', encoding='utf-8') as out:
    out.write(html)
    
print("Successfully added smooth scrolling.")
