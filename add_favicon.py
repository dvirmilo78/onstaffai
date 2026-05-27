import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if a favicon is already present
    if '<link rel="icon"' in html:
        # Replace the existing favicon link
        html = re.sub(r'<link rel="icon".*?>', '<link rel="icon" type="image/png" href="assets/favicon.png">', html)
    elif '<head>' in html:
        # Add the favicon link right after <head>
        html = html.replace('<head>', '<head>\n  <link rel="icon" type="image/png" href="assets/favicon.png">', 1)
    else:
        print(f"Warning: Could not find <head> in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

update_file('OnStaffAI.html')
update_file('index.html')

print("Successfully added favicon.")
