import urllib.request
import json

url = "https://firestore.googleapis.com/v1/projects/onstaffai/databases/(default)/documents/leads"
doc_data = {
    "fields": {
        "name": { "stringValue": "טסט בוט" },
        "company": { "stringValue": "" },
        "email": { "stringValue": "test@onstaffai.com" },
        "phone": { "stringValue": "050-0000000" },
        "plan": { "stringValue": "starter" },
        "agents": { "stringValue": "customer-service" },
        "status": { "stringValue": "new" },
        "step": { "integerValue": 1 },
        "createdAt": { "timestampValue": "2026-06-01T12:00:00Z" },
        "lastActivity": { "timestampValue": "2026-06-01T12:00:00Z" }
    }
}

req = urllib.request.Request(
    url, 
    data=json.dumps(doc_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("Success! Created document:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
