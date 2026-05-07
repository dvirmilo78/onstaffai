"""
OnStaffAI Backend — FastAPI
Handles OAuth for Gmail, Google Calendar, Microsoft (Outlook + Calendar), WhatsApp Business API
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import httpx, os, json, base64, hmac, hashlib, time
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="OnStaffAI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ENV VARS (set in Railway / .env) ────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
MS_CLIENT_ID         = os.getenv("MS_CLIENT_ID", "")
MS_CLIENT_SECRET     = os.getenv("MS_CLIENT_SECRET", "")
WA_PHONE_ID          = os.getenv("WA_PHONE_ID", "")
WA_ACCESS_TOKEN      = os.getenv("WA_ACCESS_TOKEN", "")
WA_VERIFY_TOKEN      = os.getenv("WA_VERIFY_TOKEN", "onstaffai_webhook_2025")
ANTHROPIC_API_KEY    = os.getenv("ANTHROPIC_API_KEY", "")
BASE_URL             = os.getenv("BASE_URL", "https://your-app.railway.app")
FRONTEND_URL         = os.getenv("FRONTEND_URL", "https://your-frontend.com")

# ─── IN-MEMORY TOKEN STORE (replace with Redis/DB in production) ─────────────
tokens: dict = {}  # {"company_service": {access_token, refresh_token, expiry, email}}


# ══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/")
def root():
    return {"status": "OnStaffAI Backend running", "version": "1.0.0"}

@app.get("/health")
def health():
    services = {
        "google": bool(GOOGLE_CLIENT_ID),
        "microsoft": bool(MS_CLIENT_ID),
        "whatsapp": bool(WA_ACCESS_TOKEN),
        "anthropic": bool(ANTHROPIC_API_KEY),
    }
    return {"status": "ok", "configured": services}


# ══════════════════════════════════════════════════════════════════════════════
# GOOGLE OAUTH  (Gmail + Google Calendar — same OAuth flow, different scopes)
# ══════════════════════════════════════════════════════════════════════════════
GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO  = "https://www.googleapis.com/oauth2/v2/userinfo"

GOOGLE_SCOPES_GMAIL = " ".join([
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
])
GOOGLE_SCOPES_CALENDAR = " ".join([
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
])


@app.get("/auth/google/{service}")
def google_oauth_start(service: str, company: str = "default"):
    """Start Google OAuth — service = 'gmail' or 'calendar'"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(400, "Google OAuth not configured — set GOOGLE_CLIENT_ID")
    scopes = GOOGLE_SCOPES_GMAIL if service == "gmail" else GOOGLE_SCOPES_CALENDAR
    state = f"{company}:{service}"
    params = {
        "client_id":     GOOGLE_CLIENT_ID,
        "redirect_uri":  f"{BASE_URL}/auth/google/callback",
        "response_type": "code",
        "scope":         scopes,
        "access_type":   "offline",
        "prompt":        "consent",
        "state":         state,
    }
    url = GOOGLE_AUTH_URL + "?" + "&".join(f"{k}={httpx.utils.quote(str(v))}" for k,v in params.items())
    return RedirectResponse(url)


@app.get("/auth/google/callback")
async def google_oauth_callback(code: str, state: str = "", error: str = ""):
    """Google OAuth callback — exchanges code for tokens"""
    if error:
        return RedirectResponse(f"{FRONTEND_URL}?auth_error=google:{error}")

    company, service = (state.split(":", 1) + ["gmail"])[:2]

    async with httpx.AsyncClient() as c:
        # Exchange code for tokens
        r = await c.post(GOOGLE_TOKEN_URL, data={
            "code":          code,
            "client_id":     GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri":  f"{BASE_URL}/auth/google/callback",
            "grant_type":    "authorization_code",
        })
        t = r.json()
        if "error" in t:
            return RedirectResponse(f"{FRONTEND_URL}?auth_error={t['error']}")

        # Get user email
        ui = await c.get(GOOGLE_USERINFO,
            headers={"Authorization": f"Bearer {t['access_token']}"})
        user = ui.json()

    key = f"{company}_{service}_google"
    tokens[key] = {
        "access_token":  t["access_token"],
        "refresh_token": t.get("refresh_token", ""),
        "expires_at":    time.time() + t.get("expires_in", 3600),
        "email":         user.get("email", ""),
        "name":          user.get("name", ""),
        "service":       service,
        "provider":      "google",
    }
    return RedirectResponse(f"{FRONTEND_URL}?auth_success=google_{service}&company={company}&email={user.get('email','')}")


async def get_google_token(company: str, service: str) -> str:
    """Get valid Google access token, refresh if needed"""
    key = f"{company}_{service}_google"
    t = tokens.get(key)
    if not t:
        raise HTTPException(401, f"Google {service} not connected for {company}")
    if time.time() > t["expires_at"] - 60:
        # Refresh
        async with httpx.AsyncClient() as c:
            r = await c.post(GOOGLE_TOKEN_URL, data={
                "client_id":     GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "refresh_token": t["refresh_token"],
                "grant_type":    "refresh_token",
            })
            new = r.json()
            if "access_token" in new:
                t["access_token"] = new["access_token"]
                t["expires_at"]   = time.time() + new.get("expires_in", 3600)
    return t["access_token"]


# ── Gmail endpoints ───────────────────────────────────────────────────────────
@app.get("/gmail/{company}/messages")
async def get_gmail_messages(company: str, max_results: int = 10, query: str = "is:unread"):
    """Fetch Gmail messages"""
    token = await get_google_token(company, "gmail")
    async with httpx.AsyncClient() as c:
        r = await c.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers={"Authorization": f"Bearer {token}"},
            params={"maxResults": max_results, "q": query},
        )
        msgs = r.json().get("messages", [])
        result = []
        for m in msgs[:5]:  # Fetch details for first 5
            dr = await c.get(
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{m['id']}",
                headers={"Authorization": f"Bearer {token}"},
                params={"format": "metadata", "metadataHeaders": ["Subject","From","Date"]},
            )
            d = dr.json()
            headers = {h["name"]: h["value"] for h in d.get("payload",{}).get("headers",[])}
            result.append({
                "id":      m["id"],
                "subject": headers.get("Subject","(no subject)"),
                "from":    headers.get("From",""),
                "date":    headers.get("Date",""),
                "snippet": d.get("snippet",""),
            })
    return {"messages": result}


@app.post("/gmail/{company}/send")
async def send_gmail(company: str, body: dict):
    """Send email via Gmail — body: {to, subject, text}"""
    token = await get_google_token(company, "gmail")
    msg = f"To: {body['to']}\r\nSubject: {body['subject']}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body['text']}"
    raw = base64.urlsafe_b64encode(msg.encode()).decode().rstrip("=")
    async with httpx.AsyncClient() as c:
        r = await c.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={"Authorization": f"Bearer {token}"},
            json={"raw": raw},
        )
    return r.json()


# ── Google Calendar endpoints ─────────────────────────────────────────────────
@app.get("/gcal/{company}/events")
async def get_gcal_events(company: str, days_ahead: int = 7):
    """Get upcoming calendar events"""
    token = await get_google_token(company, "calendar")
    now = datetime.utcnow()
    end = now + timedelta(days=days_ahead)
    async with httpx.AsyncClient() as c:
        r = await c.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "timeMin":      now.isoformat() + "Z",
                "timeMax":      end.isoformat() + "Z",
                "singleEvents": True,
                "orderBy":      "startTime",
                "maxResults":   20,
            },
        )
    events = r.json().get("items", [])
    return {"events": [{
        "id":       e["id"],
        "summary":  e.get("summary","(ללא כותרת)"),
        "start":    e["start"].get("dateTime", e["start"].get("date","")),
        "end":      e["end"].get("dateTime",   e["end"].get("date","")),
        "attendees":[a["email"] for a in e.get("attendees",[])],
        "meet_link": e.get("hangoutLink",""),
    } for e in events]}


@app.post("/gcal/{company}/events")
async def create_gcal_event(company: str, body: dict):
    """Create calendar event — body: {summary, start_datetime, end_datetime, attendee_email, description}"""
    token = await get_google_token(company, "calendar")
    event = {
        "summary":     body["summary"],
        "description": body.get("description",""),
        "start":  {"dateTime": body["start_datetime"], "timeZone": "Asia/Jerusalem"},
        "end":    {"dateTime": body["end_datetime"],   "timeZone": "Asia/Jerusalem"},
        "attendees":   [{"email": body["attendee_email"]}] if body.get("attendee_email") else [],
        "conferenceData": {"createRequest": {"requestId": f"meet-{int(time.time())}"}},
    }
    async with httpx.AsyncClient() as c:
        r = await c.post(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers={"Authorization": f"Bearer {token}"},
            params={"conferenceDataVersion": 1, "sendNotifications": True},
            json=event,
        )
    created = r.json()
    return {
        "id":        created.get("id"),
        "htmlLink":  created.get("htmlLink"),
        "meet_link": created.get("hangoutLink",""),
        "status":    "created",
    }


@app.delete("/gcal/{company}/events/{event_id}")
async def delete_gcal_event(company: str, event_id: str):
    token = await get_google_token(company, "calendar")
    async with httpx.AsyncClient() as c:
        r = await c.delete(
            f"https://www.googleapis.com/calendar/v3/calendars/primary/events/{event_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    return {"status": "deleted" if r.status_code == 204 else "error", "code": r.status_code}


# ══════════════════════════════════════════════════════════════════════════════
# MICROSOFT OAUTH  (Outlook + Microsoft Calendar — same tenant, different scopes)
# ══════════════════════════════════════════════════════════════════════════════
MS_AUTH_URL  = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

MS_SCOPES = " ".join([
    "openid", "profile", "email", "offline_access",
    "Mail.ReadWrite", "Mail.Send",
    "Calendars.ReadWrite",
    "User.Read",
])


@app.get("/auth/microsoft")
def ms_oauth_start(company: str = "default", service: str = "both"):
    """Start Microsoft OAuth"""
    if not MS_CLIENT_ID:
        raise HTTPException(400, "Microsoft OAuth not configured — set MS_CLIENT_ID")
    state = f"{company}:{service}"
    params = {
        "client_id":     MS_CLIENT_ID,
        "redirect_uri":  f"{BASE_URL}/auth/microsoft/callback",
        "response_type": "code",
        "scope":         MS_SCOPES,
        "response_mode": "query",
        "state":         state,
    }
    url = MS_AUTH_URL + "?" + "&".join(f"{k}={httpx.utils.quote(str(v))}" for k,v in params.items())
    return RedirectResponse(url)


@app.get("/auth/microsoft/callback")
async def ms_oauth_callback(code: str, state: str = "", error: str = ""):
    if error:
        return RedirectResponse(f"{FRONTEND_URL}?auth_error=microsoft:{error}")

    company, service = (state.split(":", 1) + ["both"])[:2]

    async with httpx.AsyncClient() as c:
        r = await c.post(MS_TOKEN_URL, data={
            "client_id":     MS_CLIENT_ID,
            "client_secret": MS_CLIENT_SECRET,
            "code":          code,
            "redirect_uri":  f"{BASE_URL}/auth/microsoft/callback",
            "grant_type":    "authorization_code",
            "scope":         MS_SCOPES,
        })
        t = r.json()
        if "error" in t:
            return RedirectResponse(f"{FRONTEND_URL}?auth_error={t['error']}")

        # Get user info
        ui = await c.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {t['access_token']}"},
        )
        user = ui.json()

    for svc in ["outlook", "calendar"]:
        key = f"{company}_{svc}_microsoft"
        tokens[key] = {
            "access_token":  t["access_token"],
            "refresh_token": t.get("refresh_token", ""),
            "expires_at":    time.time() + t.get("expires_in", 3600),
            "email":         user.get("mail") or user.get("userPrincipalName",""),
            "name":          user.get("displayName",""),
            "provider":      "microsoft",
        }
    email = user.get("mail") or user.get("userPrincipalName","")
    return RedirectResponse(f"{FRONTEND_URL}?auth_success=microsoft&company={company}&email={email}")


async def get_ms_token(company: str, service: str) -> str:
    key = f"{company}_{service}_microsoft"
    t = tokens.get(key)
    if not t:
        raise HTTPException(401, f"Microsoft not connected for {company}")
    if time.time() > t["expires_at"] - 60:
        async with httpx.AsyncClient() as c:
            r = await c.post(MS_TOKEN_URL, data={
                "client_id":     MS_CLIENT_ID,
                "client_secret": MS_CLIENT_SECRET,
                "refresh_token": t["refresh_token"],
                "grant_type":    "refresh_token",
                "scope":         MS_SCOPES,
            })
            new = r.json()
            if "access_token" in new:
                t["access_token"] = new["access_token"]
                t["expires_at"]   = time.time() + new.get("expires_in", 3600)
    return t["access_token"]


# ── Outlook endpoints ─────────────────────────────────────────────────────────
@app.get("/outlook/{company}/messages")
async def get_outlook_messages(company: str, top: int = 10):
    token = await get_ms_token(company, "outlook")
    async with httpx.AsyncClient() as c:
        r = await c.get(
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages",
            headers={"Authorization": f"Bearer {token}"},
            params={"$top": top, "$select": "subject,from,receivedDateTime,bodyPreview,isRead"},
        )
    msgs = r.json().get("value", [])
    return {"messages": [{
        "id":       m["id"],
        "subject":  m.get("subject",""),
        "from":     m["from"]["emailAddress"]["address"],
        "date":     m.get("receivedDateTime",""),
        "snippet":  m.get("bodyPreview",""),
        "isRead":   m.get("isRead", True),
    } for m in msgs]}


@app.post("/outlook/{company}/send")
async def send_outlook(company: str, body: dict):
    token = await get_ms_token(company, "outlook")
    msg = {
        "message": {
            "subject": body["subject"],
            "body":    {"contentType": "Text", "content": body["text"]},
            "toRecipients": [{"emailAddress": {"address": body["to"]}}],
        }
    }
    async with httpx.AsyncClient() as c:
        r = await c.post(
            "https://graph.microsoft.com/v1.0/me/sendMail",
            headers={"Authorization": f"Bearer {token}"},
            json=msg,
        )
    return {"status": "sent" if r.status_code == 202 else "error", "code": r.status_code}


# ── Microsoft Calendar endpoints ──────────────────────────────────────────────
@app.get("/mscal/{company}/events")
async def get_ms_events(company: str, days_ahead: int = 7):
    token = await get_ms_token(company, "calendar")
    now = datetime.utcnow()
    end = now + timedelta(days=days_ahead)
    async with httpx.AsyncClient() as c:
        r = await c.get(
            "https://graph.microsoft.com/v1.0/me/calendarView",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "startDateTime": now.isoformat() + "Z",
                "endDateTime":   end.isoformat() + "Z",
                "$top":          20,
                "$select":       "subject,start,end,attendees,onlineMeeting,bodyPreview",
                "$orderby":      "start/dateTime",
            },
        )
    events = r.json().get("value", [])
    return {"events": [{
        "id":       e["id"],
        "summary":  e.get("subject",""),
        "start":    e["start"]["dateTime"],
        "end":      e["end"]["dateTime"],
        "attendees":[a["emailAddress"]["address"] for a in e.get("attendees",[])],
        "teams_link": (e.get("onlineMeeting") or {}).get("joinUrl",""),
    } for e in events]}


@app.post("/mscal/{company}/events")
async def create_ms_event(company: str, body: dict):
    token = await get_ms_token(company, "calendar")
    event = {
        "subject":  body["summary"],
        "body":     {"contentType": "Text", "content": body.get("description","")},
        "start":    {"dateTime": body["start_datetime"], "timeZone": "Israel Standard Time"},
        "end":      {"dateTime": body["end_datetime"],   "timeZone": "Israel Standard Time"},
        "attendees":[{"emailAddress":{"address":body["attendee_email"]},"type":"required"}] if body.get("attendee_email") else [],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness",
    }
    async with httpx.AsyncClient() as c:
        r = await c.post(
            "https://graph.microsoft.com/v1.0/me/events",
            headers={"Authorization": f"Bearer {token}"},
            json=event,
        )
    created = r.json()
    return {
        "id":         created.get("id"),
        "webLink":    created.get("webLink",""),
        "teams_link": (created.get("onlineMeeting") or {}).get("joinUrl",""),
        "status":     "created",
    }


# ══════════════════════════════════════════════════════════════════════════════
# WHATSAPP BUSINESS API (Meta Cloud API)
# ══════════════════════════════════════════════════════════════════════════════
WA_API = f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}"
WA_SESSIONS: dict = {}  # phone_number -> conversation history


@app.get("/webhooks/whatsapp")
def wa_verify(request: Request):
    """Meta webhook verification"""
    params = dict(request.query_params)
    if params.get("hub.verify_token") == WA_VERIFY_TOKEN:
        return int(params.get("hub.challenge", 0))
    raise HTTPException(403, "Invalid verify token")


@app.post("/webhooks/whatsapp")
async def wa_webhook(request: Request):
    """Receive WhatsApp messages and reply with Claude"""
    body = await request.json()
    try:
        entry  = body["entry"][0]["changes"][0]["value"]
        if "messages" not in entry:
            return {"ok": True}

        msg    = entry["messages"][0]
        phone  = msg["from"]
        text   = msg.get("text", {}).get("body", "")
        if not text:
            return {"ok": True}

        # Get/create session
        history = WA_SESSIONS.get(phone, [])
        history.append({"role": "user", "content": text})

        # Claude API
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key":         ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json",
                },
                json={
                    "model":      "claude-sonnet-4-20250514",
                    "max_tokens": 500,
                    "system":     WA_SYSTEM_PROMPT,
                    "messages":   history[-10:],
                },
            )
            data  = r.json()
            reply = data["content"][0]["text"]

        history.append({"role": "assistant", "content": reply})
        WA_SESSIONS[phone] = history[-20:]  # Keep last 20 messages

        # Send reply
        async with httpx.AsyncClient() as c:
            await c.post(
                f"{WA_API}/messages",
                headers={"Authorization": f"Bearer {WA_ACCESS_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "to":   phone,
                    "type": "text",
                    "text": {"body": reply},
                },
            )
    except Exception as e:
        print(f"WhatsApp error: {e}")

    return {"ok": True}


WA_SYSTEM_PROMPT = """
אתה נציג שירות לקוחות ותיאום פגישות של OnStaffAI.
ענה בעברית בצורה ידידותית וקצרה (עד 3 משפטים).
OnStaffAI מציעה סוכני AI לעסקים — שירות לקוחות, תיאום פגישות, שיווק, גבייה ועוד.
מחירים: Starter ₪499, Growth ₪1,299, Business ₪1,999, Enterprise ₪2,999.
אם הלקוח מעוניין — תאם פגישת דמו: info@onstaffai.com
"""


@app.post("/whatsapp/send")
async def wa_send_manual(body: dict):
    """Send WhatsApp message manually — body: {to, text}"""
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{WA_API}/messages",
            headers={"Authorization": f"Bearer {WA_ACCESS_TOKEN}"},
            json={
                "messaging_product": "whatsapp",
                "to":   body["to"],
                "type": "text",
                "text": {"body": body["text"]},
            },
        )
    return r.json()


# ══════════════════════════════════════════════════════════════════════════════
# TOKEN STATUS endpoint (for frontend to check connection state)
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/connections/{company}")
def get_connections(company: str):
    """Return which services are connected for a company"""
    result = {}
    for key, t in tokens.items():
        if key.startswith(company + "_"):
            parts = key.split("_", 1)[1]  # e.g. "gmail_google" or "calendar_microsoft"
            result[parts] = {
                "connected": True,
                "email":     t.get("email",""),
                "provider":  t.get("provider",""),
                "expires_at": t.get("expires_at",0),
            }
    return {"company": company, "connections": result}
