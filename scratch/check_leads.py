import urllib.request
import json

url = "https://firestore.googleapis.com/v1/projects/onstaffai/databases/(default)/documents/leads?pageSize=15"
req = urllib.request.Request(url, headers={'Accept': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        documents = res.get('documents', [])
        print(f"Retrieved {len(documents)} leads:")
        for doc in documents:
            name = doc.get('name', '')
            fields = doc.get('fields', {})
            lead_id = name.split('/')[-1]
            
            lead_name = fields.get('name', {}).get('stringValue', '')
            company = fields.get('company', {}).get('stringValue', '')
            email = fields.get('email', {}).get('stringValue', '')
            phone = fields.get('phone', {}).get('stringValue', '')
            created_at = fields.get('createdAt', {}).get('timestampValue', '')
            
            print(f"- ID: {lead_id}")
            print(f"  Name: {lead_name}")
            print(f"  Company: {company}")
            print(f"  Email: {email}")
            print(f"  Phone: {phone}")
            print(f"  CreatedAt: {created_at}")
            print("-" * 30)
except Exception as e:
    print("Error:", e)
