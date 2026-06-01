import urllib.request
import json
import sys

lead_id = "5wkmpJOCsPAWkUToufOA"
if len(sys.argv) > 1:
    lead_id = sys.argv[1]

url = f"https://firestore.googleapis.com/v1/projects/onstaffai/databases/(default)/documents/leads/{lead_id}"
req = urllib.request.Request(url, headers={'Accept': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        doc = json.loads(response.read().decode('utf-8'))
        print(json.dumps(doc, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
