import requests
import json

url = "https://api.emailjs.com/api/v1.0/email/send"
headers = {"Content-Type": "application/json"}
data = {
    "service_id": "service_ne5z4wv",
    "template_id": "template_sl4n308",
    "user_id": "7IoARO-EcljLAzrok",
    "accessToken": "qrDC3NWZhEoUpR_zFfFnC",
    "template_params": {
        "user_name": "דביר",
        "onboarding_link": "https://onstaffai.web.app/onboarding.html",
        "to_email": "dvir@onstaffai.com",
        "to_name": "דביר"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.text)
