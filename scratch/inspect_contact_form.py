import re

def inspect_file(filename):
    print(f"--- Inspecting {filename} ---")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Search for company input elements
        matches = list(re.finditer(r'<input[^>]*name=["\']company["\'][^>]*>', content))
        if not matches:
            print("No matching company input found.")
        for m in matches:
            start = max(0, m.start() - 100)
            end = min(len(content), m.end() + 100)
            print(f"Match found at position {m.start()}:\n{content[start:end]}\n")
    except Exception as e:
        print("Error:", e)

inspect_file("index.html")
inspect_file("OnStaffAI.html")
inspect_file("onboarding.html")
inspect_file("admin.html")
