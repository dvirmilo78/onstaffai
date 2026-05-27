with open("OnStaffAI.html", "r", encoding="utf-8") as f:
    html = f.read()

# Inject JS for smooth scrolling just before </body>
smooth_scroll_js = """
<script>
document.addEventListener('click', function(e) {
  const target = e.target.closest('a[href^="#"]');
  if (target) {
    const id = target.getAttribute('href');
    if (id !== '#') {
      const element = document.querySelector(id);
      if (element) {
        e.preventDefault();
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }
});
</script>
"""

if smooth_scroll_js not in html:
    html = html.replace("</body>", smooth_scroll_js + "</body>")

with open("OnStaffAI.html", "w", encoding="utf-8") as out:
    out.write(html)
print("Injected smooth scroll JS.")
