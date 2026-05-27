with open("OnStaffAI.html", "r", encoding="utf-8") as f:
    html = f.read()

target = "<style>\nhtml { scroll-behavior: smooth; }\n"
replacement = "<style>"

# Split by the target string
parts = html.split(target)

# We want to keep the FIRST target (which is the main style tag in the head), and revert the rest.
# Actually, the very first <style> in the file is the right one.
# So we join the first two parts with the target, and the rest with the replacement.
if len(parts) > 2:
    new_html = parts[0] + target + replacement.join(parts[1:])
    with open("OnStaffAI.html", "w", encoding="utf-8") as out:
        out.write(new_html)
    print("Fixed newlines in JSON.")
else:
    print("No need to fix.")
