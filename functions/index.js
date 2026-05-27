const { onSchedule } = require("firebase-functions/v2/scheduler");
const admin = require("firebase-admin");
const axios = require("axios");
const cheerio = require("cheerio");
admin.initializeApp();

// ── EmailJS Credentials (need to be filled later via ENV or hardcoded) ──
const EMAILJS_SERVICE_ID = process.env.EMAILJS_SERVICE_ID || "service_ne5z4wv";
const EMAILJS_PUBLIC_KEY = process.env.EMAILJS_PUBLIC_KEY || "7IoARO-EcljLAzrok";
const EMAILJS_PRIVATE_KEY = process.env.EMAILJS_PRIVATE_KEY || "qrDC3NWZhEoUpR_zFfFnC";
const EMAILJS_TEMPLATE_REMINDER = process.env.EMAILJS_TEMPLATE_REMINDER || "template_p9xm8ll";
const EMAILJS_TEMPLATE_DIGEST = process.env.EMAILJS_TEMPLATE_DIGEST || "YOUR_DIGEST_TPL";
const EMAILJS_TEMPLATE_2FA = process.env.EMAILJS_TEMPLATE_2FA || "template_stdgvar";
const ADMIN_EMAIL = "dvir@onstaffai.com";

// ── Vonage SMS Credentials ──
const VONAGE_API_KEY = process.env.VONAGE_API_KEY || "342c70be";
const VONAGE_API_SECRET = process.env.VONAGE_API_SECRET || "bKRjzkC8Ujr3Z20i";
const VONAGE_FROM = "OnStaffAI";

// Helper function to send email via EmailJS REST API
async function sendEmailJSEmail(templateId, templateParams) {
    if (EMAILJS_SERVICE_ID === "YOUR_SERVICE_ID") {
        console.log("EmailJS not configured. Skipping email send:", templateParams);
        return false;
    }
    
    try {
        await axios.post("https://api.emailjs.com/api/v1.0/email/send", {
            service_id: EMAILJS_SERVICE_ID,
            template_id: templateId,
            user_id: EMAILJS_PUBLIC_KEY,
            accessToken: EMAILJS_PRIVATE_KEY,
            template_params: templateParams
        });
        return true;
    } catch (error) {
        console.error("Error sending EmailJS email:", error.response ? error.response.data : error.message);
        return false;
    }
}

// Runs every day at 08:00 AM Jerusalem time
exports.dailyOnboardingCheck = onSchedule({
    schedule: "0 8 * * *",
    timeZone: "Asia/Jerusalem",
}, async (event) => {
    const db = admin.firestore();
    const now = new Date();
    
    // Calculate timestamp for 48 hours ago
    const twoDaysAgo = new Date();
    twoDaysAgo.setDate(now.getDate() - 2);
    
    // We will collect data for the digest
    const stuckLeads = []; // step 1
    const inProgressLeads = []; // step 2-4
    
    try {
        const leadsSnapshot = await db.collection("leads").get();
        
        for (const doc of leadsSnapshot.docs) {
            const lead = doc.data();
            
            // Treat Firestore Timestamps vs ISO strings
            let lastActivityDate = lead.lastActivity;
            if (lastActivityDate && typeof lastActivityDate.toDate === 'function') {
                lastActivityDate = lastActivityDate.toDate();
            } else if (typeof lastActivityDate === 'string') {
                lastActivityDate = new Date(lastActivityDate);
            } else {
                continue; // invalid date
            }

            const isInactive = lastActivityDate < twoDaysAgo;
            
            if (lead.step === 1) {
                stuckLeads.push({ id: doc.id, ...lead });
            } else if (lead.step > 1 && lead.step < 5) {
                inProgressLeads.push({ id: doc.id, ...lead });
            }

            // --- Reminder Logic (Max 3 reminders, sent when inactive for > 2 days) ---
            if (lead.step < 5 && isInactive) {
                const reminderCount = lead.reminderCount || 0;
                if (reminderCount < 3) {
                    console.log(`Sending reminder ${reminderCount + 1} to ${lead.email}`);
                    
                    const onboardUrl = `https://onstaffai.web.app/onboarding.html?lid=${doc.id}`;
                    
                    const emailSent = await sendEmailJSEmail(EMAILJS_TEMPLATE_REMINDER, {
                        to_email: lead.email, email: lead.email, to: lead.email, user_email: lead.email,
                        to_name: lead.name,
                        company: lead.company,
                        onboard_url: onboardUrl, onboarding_link: onboardUrl
                    });
                    
                    if (emailSent) {
                        // Update lead with new activity date so it waits another 2 days
                        await doc.ref.update({
                            reminderCount: reminderCount + 1,
                            lastActivity: admin.firestore.FieldValue.serverTimestamp()
                        });
                    }
                }
            }
        }
        
        // --- Daily Digest Logic ---
        console.log(`Sending daily digest. Stuck: ${stuckLeads.length}, In-Progress: ${inProgressLeads.length}`);
        
        // Format the tables for the email
        let digestHtml = "<h3>לידים תקועים (שלב 1 - לא התחילו):</h3>";
        if (stuckLeads.length === 0) digestHtml += "<p>אין לידים תקועים כרגע.</p>";
        else {
            digestHtml += "<ul>";
            stuckLeads.forEach(l => {
                digestHtml += `<li><b>${l.name}</b> (${l.company}) - ${l.email} - סוכנים: ${l.agents}</li>`;
            });
            digestHtml += "</ul>";
        }
        
        digestHtml += "<h3>לידים בתהליך (שלבים 2-4):</h3>";
        if (inProgressLeads.length === 0) digestHtml += "<p>אין לידים בתהליך כרגע.</p>";
        else {
            digestHtml += "<ul>";
            inProgressLeads.forEach(l => {
                digestHtml += `<li><b>${l.name}</b> (${l.company}) - מונחים בשלב ${l.step}</li>`;
            });
            digestHtml += "</ul>";
        }

        await sendEmailJSEmail(EMAILJS_TEMPLATE_DIGEST, {
            to_email: ADMIN_EMAIL, email: ADMIN_EMAIL, to: ADMIN_EMAIL, user_email: ADMIN_EMAIL,
            to_name: "דביר",
            digest_html: digestHtml,
            date: now.toLocaleDateString('he-IL')
        });
        
    } catch (error) {
        console.error("Error running daily cron:", error);
    }
});

const { onCall, HttpsError } = require("firebase-functions/v2/https");

// HTTP Callable function to generate and send 2FA code
exports.request2FA = onCall({ region: "us-central1" }, async (request) => {
    const { username, email, phone } = request.data;
    if (!username || !email) {
        throw new HttpsError('invalid-argument', 'The function must be called with a username and email.');
    }

    const code = Math.floor(100000 + Math.random() * 900000).toString(); // 6 digits
    const expiresAt = new Date(Date.now() + 5 * 60000); // 5 minutes TTL

    const db = admin.firestore();
    
    try {
        await db.collection("authCodes").doc(username).set({
            code: code,
            expiresAt: admin.firestore.Timestamp.fromDate(expiresAt),
            email: email,
            phone: phone || null
        });

        // 1. Send via EmailJS
        const emailSent = await sendEmailJSEmail(EMAILJS_TEMPLATE_2FA, {
            to_email: email, email: email, to: email, user_email: email,
            message: `Your OnStaffAI login code is: ${code}`,
            code: code
        });
        console.log(`Email 2FA sent to ${email}: ${emailSent}`);

        // 2. Send via SMS (Vonage)
        if (phone) {
            try {
                // Format phone number to E.164 without '+' (e.g. 972501234567)
                let formattedPhone = phone.replace(/[^0-9]/g, '');
                if (formattedPhone.startsWith('0')) {
                    formattedPhone = '972' + formattedPhone.substring(1);
                }
                
                if (VONAGE_API_SECRET !== "YOUR_VONAGE_API_SECRET") {
                    const smsRes = await axios.post('https://rest.nexmo.com/sms/json', {
                        api_key: VONAGE_API_KEY,
                        api_secret: VONAGE_API_SECRET,
                        to: formattedPhone,
                        from: VONAGE_FROM,
                        text: `לקוחות יקרים, קוד הכניסה שלכם למערכת הוא: ${code}`,
                        type: "unicode"
                    });
                    
                    if (smsRes.data && smsRes.data.messages && smsRes.data.messages[0].status === "0") {
                        console.log(`Vonage SMS sent to ${formattedPhone}`);
                    } else {
                        console.error(`Vonage SMS error:`, smsRes.data.messages ? smsRes.data.messages[0]['error-text'] : 'Unknown error');
                    }
                } else {
                    console.log(`[SMS MOCK] Missing Vonage API Secret. Would have sent: ${code} to ${formattedPhone}`);
                }
            } catch (smsErr) {
                console.error(`Failed to send Vonage SMS:`, smsErr.message);
            }
        }

        return { success: true, message: "Code sent successfully" };
    } catch (error) {
        console.error("Error setting 2FA code:", error);
        throw new HttpsError('internal', 'Unable to process 2FA request.');
    }
});

// Runs every 5 minutes to check for inactive agent sessions
exports.checkInactiveSessions = onSchedule({
    schedule: "every 5 minutes",
    timeZone: "Asia/Jerusalem"
}, async (event) => {
    const db = admin.firestore();
    const now = new Date();
    
    try {
        const snapshot = await db.collection("agentSessions").where("status", "in", ["active", "human_active"]).get();
        for (const doc of snapshot.docs) {
            const session = doc.data();
            let lastUpdate = session.lastUpdate;
            if (lastUpdate && typeof lastUpdate.toDate === 'function') {
                lastUpdate = lastUpdate.toDate();
            } else if (typeof lastUpdate === 'string') {
                lastUpdate = new Date(lastUpdate);
            } else {
                continue;
            }
            
            const diffMinutes = (now.getTime() - lastUpdate.getTime()) / 60000;
            
            if (!session.followUpSent && diffMinutes >= 60) {
                // Send follow-up
                const msgText = "אני רואה שלא התקבלה ממך שום תגובה , האם יש משהו נוסף שאני יכול לעזור בו או לאפשר לסגור את השיחה";
                await db.collection("agentMessages").doc(doc.id).collection("messages").add({
                    text: msgText,
                    sender: session.status === "human_active" ? "human" : "agent",
                    ts: admin.firestore.FieldValue.serverTimestamp()
                });
                await doc.ref.update({
                    followUpSent: true,
                    lastUpdate: admin.firestore.FieldValue.serverTimestamp(),
                    lastUserMsg: msgText,
                    unread: false
                });
                console.log(`Sent follow-up for session ${doc.id}`);
            } else if (session.followUpSent && diffMinutes >= 10) {
                // Close session
                const msgText = "השיחה הסתיימה , במידה ויש שאלות נוספות יש להתחיל שיחה חדשה";
                await db.collection("agentMessages").doc(doc.id).collection("messages").add({
                    text: msgText,
                    sender: session.status === "human_active" ? "human" : "agent",
                    ts: admin.firestore.FieldValue.serverTimestamp()
                });
                await doc.ref.update({
                    status: "closed",
                    followUpSent: admin.firestore.FieldValue.delete(),
                    lastUpdate: admin.firestore.FieldValue.serverTimestamp(),
                    lastUserMsg: msgText,
                    unread: false
                });
                console.log(`Closed inactive session ${doc.id}`);
            }
        }
    } catch(e) {
        console.error("Error checking inactive sessions", e);
    }
});

// ── Web Scraper for RAG ──
async function doScrape(targetUrl) {
    if (!targetUrl.startsWith('http')) targetUrl = 'https://' + targetUrl;

    const visited = new Set();
    const toVisit = [targetUrl];
    const maxPages = 30; // limit to 30 pages to capture full site structure while avoiding massive payloads
    
    let combinedText = '';
    const baseUrlObj = new URL(targetUrl);
    const baseDomain = baseUrlObj.hostname;

    while (toVisit.length > 0 && visited.size < maxPages) {
        const currentUrl = toVisit.shift();
        if (visited.has(currentUrl)) continue;
        visited.add(currentUrl);
        
        try {
            console.log(`Scraping: ${currentUrl}`);
            const resp = await axios.get(currentUrl, {
                timeout: 5000,
                headers: { 'User-Agent': 'Mozilla/5.0 (compatible; OnStaffAIBot/1.0;)' }
            });
            const $ = cheerio.load(resp.data);
            
            // Remove unnecessary elements
            $('script, style, noscript, iframe, img, svg, video, audio, nav, footer, header').remove();
            
            // Format links so LLM can see them before extracting text
            $('a').each((_, el) => {
                const linkText = $(el).text().trim();
                const href = $(el).attr('href');
                if (linkText && href && !href.startsWith('javascript:') && !href.startsWith('tel:')) {
                    try {
                        const absHref = new URL(href, currentUrl).href;
                        $(el).text(` ${linkText} [קישור: ${absHref}] `);
                    } catch(e) {}
                }
            });
            
            // Add newlines to block elements to preserve visual structure
            $('br, p, div, tr, li, h1, h2, h3, h4, h5, h6').append('\n');

            // Extract text
            let text = $('body').text();
            
            // Replace multiple spaces with a single space, but preserve newlines
            text = text.replace(/[ \t]+/g, ' ').replace(/\n\s*\n/g, '\n').trim();
            
            if (text) {
                combinedText += `\n\n--- דף: ${currentUrl} ---\n${text}`;
            }

            // Find internal links for crawling
            $('a').each((_, el) => {
                let href = $(el).attr('href');
                if (href) {
                    try {
                        const resolvedUrl = new URL(href, currentUrl);
                        // Only add internal links (same domain) and not already queued
                        if (resolvedUrl.hostname === baseDomain && !resolvedUrl.hash) {
                            let cleanUrl = resolvedUrl.origin + resolvedUrl.pathname;
                            if (!visited.has(cleanUrl) && !toVisit.includes(cleanUrl)) {
                                toVisit.push(cleanUrl);
                            }
                        }
                    } catch (e) {
                        // invalid url, ignore
                    }
                }
            });
        } catch (e) {
            console.error(`Failed to scrape ${currentUrl}:`, e.message);
        }
    }
    
    return {
        url: targetUrl,
        content: combinedText,
        pagesScraped: visited.size
    };
}

exports.scrapeWebsite = onCall({ timeoutSeconds: 300 }, async (request) => {
    const data = request.data;
    let targetUrl = data.url;
    if (!targetUrl) throw new HttpsError('invalid-argument', 'Missing URL');
    return await doScrape(targetUrl);
});

// Runs every day at 08:00 AM Jerusalem time to rescan all URLs
exports.dailyUrlRescan = onSchedule({
    schedule: "0 8 * * *",
    timeZone: "Asia/Jerusalem",
    timeoutSeconds: 540
}, async (event) => {
    const db = admin.firestore();
    
    try {
        console.log("Starting daily URL rescan...");
        let totalScanned = 0;
        
        // Helper to process a global data document that has a .urls array
        async function processRagDoc(docRef) {
            const docSnap = await docRef.get();
            if (!docSnap.exists) return;
            const data = docSnap.data();
            if (!data.urls || !Array.isArray(data.urls)) return;
            
            let updated = false;
            for (let i = 0; i < data.urls.length; i++) {
                const urlItem = data.urls[i];
                if (urlItem && urlItem.url) {
                    console.log(`Rescanning URL: ${urlItem.url} for doc: ${docRef.path}`);
                    try {
                        const result = await doScrape(urlItem.url);
                        data.urls[i].content = result.content;
                        // Save lastScanned as ISO string because arrays can't hold FieldValue.serverTimestamp easily
                        data.urls[i].lastScanned = new Date().toISOString(); 
                        updated = true;
                        totalScanned++;
                    } catch (scrapeErr) {
                        console.error(`Error rescanning ${urlItem.url}:`, scrapeErr);
                    }
                }
            }
            
            if (updated) {
                await docRef.update({ urls: data.urls });
            }
        }

        // 1. Process Admin's global knowledge
        const adminDocRef = db.collection("globalKnowledge").doc("data");
        await processRagDoc(adminDocRef);
        
        // 2. Process all clients' global knowledge and agent-specific knowledge
        const companiesSnap = await db.collection("companies").get();
        for (const companyDoc of companiesSnap.docs) {
            // Global
            const clientDocRef = companyDoc.ref.collection("globalData").doc("rag");
            await processRagDoc(clientDocRef);
            
            // Agent-specific
            const agentsSnap = await companyDoc.ref.collection("agentData").get();
            for (const agentDoc of agentsSnap.docs) {
                await processRagDoc(agentDoc.ref);
            }
        }
        
        console.log(`Finished daily URL rescan. Total URLs updated: ${totalScanned}`);
    } catch(e) {
        console.error("Error in daily URL rescan task", e);
    }
});
