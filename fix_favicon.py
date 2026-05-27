import re

def update_html_favicon(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove the old favicon link I added
    html = re.sub(r'<link rel="icon" type="image/png" href="assets/favicon\.png">\n?', '', html)
    # Remove any other old links if they exist
    html = re.sub(r'<link rel="icon".*?>\n?', '', html)
    html = re.sub(r'<link rel="shortcut icon".*?>\n?', '', html)

    # Insert the new robust tags right after <head>
    new_tags = """<head>
  <link rel="icon" type="image/x-icon" href="/favicon.ico?v=2">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png?v=2">
  <link rel="apple-touch-icon" href="/assets/favicon.png?v=2">"""
    
    html = html.replace('<head>', new_tags, 1)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

update_html_favicon('OnStaffAI.html')
update_html_favicon('index.html')

print("Successfully fixed favicons.")
