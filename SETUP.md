# OnStaffAI Backend — מדריך הקמה מלא

## מה הבאקנד הזה עושה
- Google OAuth → Gmail קריאה + שליחה, Google Calendar קריאה + יצירת פגישות
- Microsoft OAuth → Outlook קריאה + שליחה, Microsoft Calendar קריאה + יצירת פגישות
- WhatsApp Business API → קבלת הודעות נכנסות + תשובות אוטומטיות עם Claude

---

## שלב 1 — Google Cloud Console (Gmail + Calendar)

1. כנס ל: https://console.cloud.google.com
2. צור פרויקט חדש: "OnStaffAI"
3. **APIs & Services → Enable APIs:**
   - Gmail API
   - Google Calendar API
   - Google People API
4. **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID:**
   - Application type: **Web application**
   - Name: OnStaffAI Backend
   - Authorized redirect URIs: `https://YOUR_APP.railway.app/auth/google/callback`
5. הורד את ה-JSON ושמור את:
   - `client_id` → GOOGLE_CLIENT_ID
   - `client_secret` → GOOGLE_CLIENT_SECRET
6. **OAuth consent screen:**
   - App name: OnStaffAI
   - Scopes: gmail.modify, gmail.send, calendar.events
   - Test users: הוסף את המייל שלך

---

## שלב 2 — Azure Portal (Outlook + Calendar)

1. כנס ל: https://portal.azure.com
2. **Azure Active Directory → App registrations → New registration:**
   - Name: OnStaffAI
   - Supported account types: Accounts in any organizational directory + personal
   - Redirect URI (Web): `https://YOUR_APP.railway.app/auth/microsoft/callback`
3. **Certificates & secrets → New client secret** → שמור את הערך
4. **API permissions → Add a permission → Microsoft Graph → Delegated:**
   - Mail.ReadWrite
   - Mail.Send
   - Calendars.ReadWrite
   - User.Read
   - offline_access
5. **Grant admin consent**
6. שמור:
   - Application (client) ID → MS_CLIENT_ID
   - Client secret value → MS_CLIENT_SECRET

---

## שלב 3 — Meta / WhatsApp Business

1. כנס ל: https://developers.facebook.com
2. **Create App → Business → Next**
3. **Add Product → WhatsApp**
4. **WhatsApp → Getting Started:**
   - בחר Meta Business Account
   - Phone Number ID → WA_PHONE_ID
   - Access Token (temporary) → לצורך בדיקה
5. **For permanent token:**
   - Business Settings → System Users → Create System User
   - Add Assets → Apps → Add your app
   - Generate Token → בחר whatsapp_business_messaging + whatsapp_business_management
6. **Webhooks → Configure:**
   - Callback URL: `https://YOUR_APP.railway.app/webhooks/whatsapp`
   - Verify Token: `onstaffai_webhook_2025`
   - Subscribe to: messages, message_reads

---

## שלב 4 — פריסה על Railway (חינם)

```bash
# 1. התקן Railway CLI
npm install -g @railway/cli

# 2. התחבר
railway login

# 3. צור פרויקט
cd onstaffai-backend
railway init

# 4. הגדר משתני סביבה
railway variables set GOOGLE_CLIENT_ID=xxx
railway variables set GOOGLE_CLIENT_SECRET=xxx
railway variables set MS_CLIENT_ID=xxx
railway variables set MS_CLIENT_SECRET=xxx
railway variables set WA_PHONE_ID=xxx
railway variables set WA_ACCESS_TOKEN=xxx
railway variables set WA_VERIFY_TOKEN=onstaffai_webhook_2025
railway variables set ANTHROPIC_API_KEY=xxx
railway variables set BASE_URL=https://YOUR_APP.railway.app
railway variables set FRONTEND_URL=https://YOUR_FRONTEND.com

# 5. פרוס
railway up

# 6. קבל URL
railway domain
```

**חלופה — Render.com (חינם):**
```bash
# הוסף render.yaml לתיקייה
# Push to GitHub → connect on render.com → auto deploy
```

---

## שלב 5 — חבר לפרונטנד (OnStaffAI Platform)

ב-platform שלך, עדכן את כפתורי החיבור להפנות ל:

```
Gmail:              GET /auth/google/gmail?company=COMPANY_NAME
Google Calendar:    GET /auth/google/calendar?company=COMPANY_NAME
Microsoft (שניהם): GET /auth/microsoft?company=COMPANY_NAME
```

לאחר OAuth, הדפדפן יחזיר ל-FRONTEND_URL עם:
```
?auth_success=google_gmail&company=שופינג פלוס&email=user@gmail.com
```

---

## API Endpoints מלאים

### Gmail
- `GET  /gmail/{company}/messages?query=is:unread` — הודעות
- `POST /gmail/{company}/send` — `{to, subject, text}`

### Google Calendar
- `GET  /gcal/{company}/events?days_ahead=7` — אירועים
- `POST /gcal/{company}/events` — `{summary, start_datetime, end_datetime, attendee_email}`
- `DELETE /gcal/{company}/events/{event_id}` — מחק אירוע

### Outlook
- `GET  /outlook/{company}/messages` — הודעות
- `POST /outlook/{company}/send` — `{to, subject, text}`

### Microsoft Calendar
- `GET  /mscal/{company}/events?days_ahead=7` — אירועים
- `POST /mscal/{company}/events` — `{summary, start_datetime, end_datetime, attendee_email}`

### WhatsApp
- `POST /whatsapp/send` — `{to, text}` — שלח הודעה ידנית
- `POST /webhooks/whatsapp` — Meta webhook (אוטומטי)
- `GET  /webhooks/whatsapp` — Meta verification

### Status
- `GET  /connections/{company}` — בדוק אילו שירותים מחוברים
- `GET  /health` — בריאות הבאקנד

---

## זמן הקמה משוער
- Google OAuth: ~20 דקות
- Microsoft OAuth: ~20 דקות  
- WhatsApp: ~30 דקות (דורש אימות Meta Business)
- פריסה על Railway: ~5 דקות
- **סה"כ: ~75 דקות**
