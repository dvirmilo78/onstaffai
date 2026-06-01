import urllib.request
import json

url = "https://api.emailjs.com/api/v1.0/email/send"
service_id = 'service_ne5z4wv'
template_id = 'template_sl4n308'
user_id = '7IoARO-EcljLAzrok'
accessToken = 'qrDC3NWZhEoUpR_zFfFnC'

fields_to_test = ['email', 'to', 'user_email']

for field in fields_to_test:
    # Set only one email field
    template_params = {
        field: "dvir@onstaffai.com",
        "to_name": f"דביר מילוא (טסט {field})",
        "onboard_url": "https://onstaffai.web.app/onboarding.html?lid=test_id",
        "onboarding_link": "פרטי הליד לטסט"
    }
    
    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": user_id,
        "accessToken": accessToken,
        "template_params": template_params
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Field '{field}' succeeded! Status: {response.getcode()}")
    except urllib.error.HTTPError as e:
        print(f"Field '{field}' failed with code {e.code}: {e.read().decode('utf-8').strip()}")
    except Exception as e:
        print(f"Field '{field}' failed generic: {e}")
