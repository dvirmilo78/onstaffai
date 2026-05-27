import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'r') as f:
    idx_content = f.read()

# Fix index.html to ensure onboarding_link is passed to EmailJS
idx_content = idx_content.replace('onboard_url: onboardUrl,', 'onboard_url: onboardUrl,\n                        onboarding_link: onboardUrl,')
with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'w') as f:
    f.write(idx_content)

# Same for functions/index.js
with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/functions/index.js', 'r') as f:
    js_content = f.read()
js_content = js_content.replace('onboard_url: onboardUrl', 'onboard_url: onboardUrl, onboarding_link: onboardUrl')
with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/functions/index.js', 'w') as f:
    f.write(js_content)

html_content = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OnStaffAI | אשף הקמת חשבון</title>
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png?v=2">
    <link rel="apple-touch-icon" href="/assets/favicon.png?v=2">
    <link rel="stylesheet" href="style.css">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        body { 
            background: var(--bg-dark); 
            display: flex; flex-direction: column; min-height: 100vh;
            align-items: center; justify-content: center;
            padding: 2rem 0;
        }
        
        .header-logo { margin-bottom: 2rem; text-align: center; }
        .header-logo img { height: 44px; filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.2)); }

        .wizard-container { 
            width: 90%; max-width: 760px;
            background: var(--surface-color); 
            border: 1px solid var(--surface-border);
            border-radius: 24px; 
            padding: 2.5rem;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }

        .step-indicator { 
            display: flex; gap: 8px; margin-bottom: 2.5rem; 
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 1.5rem; overflow-x: auto;
        }
        
        .modal-tab { 
            padding: 10px 18px; border-radius: 12px; border: none; 
            background: transparent; color: var(--text-secondary); 
            font-weight: 600; cursor: default; white-space: nowrap; 
            font-size: 15px; transition: all 0.3s; display: flex; align-items: center; gap: 8px;
        }
        .modal-tab.active { background: rgba(56, 189, 248, 0.1); color: var(--accent-primary); border: 1px solid rgba(56, 189, 248, 0.2); }
        .modal-tab.done { color: #fff; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
        .modal-tab i { font-size: 1.25rem; }

        .step-content { display: none; animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        .step-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        h2 { font-size: 1.8rem; margin-bottom: 1.5rem; color: #fff; font-weight: 700; letter-spacing: -0.02em; }

        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 8px; font-size: 0.95rem; font-weight: 500; color: var(--text-secondary); }
        .form-control { 
            width: 100%; padding: 1rem 1.2rem; border-radius: 12px; 
            border: 1px solid var(--surface-border); background: rgba(0,0,0,0.2); 
            color: #fff; font-size: 1rem; font-family: inherit; outline: none; transition: all 0.2s; box-sizing: border-box;
        }
        .form-control:focus { border-color: var(--accent-primary); background: rgba(0,0,0,0.4); box-shadow: 0 0 0 3px rgba(56,189,248,0.1); }

        .nav-buttons { display: flex; justify-content: space-between; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--surface-border); }

        .plan-card { 
            border: 1px solid var(--surface-border); border-radius: 16px; 
            padding: 1.5rem; cursor: pointer; transition: all 0.2s; 
            text-align: center; background: rgba(0,0,0,0.2); 
        }
        .plan-card.selected { border-color: var(--accent-primary); background: rgba(56, 189, 248, 0.08); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .plan-price { font-size: 2rem; font-weight: 800; color: #fff; margin: 0.5rem 0; font-family: 'Outfit', sans-serif;}

        .agent-toggle { 
            padding: 1rem; border: 1px solid var(--surface-border); 
            border-radius: 14px; cursor: pointer; display: flex; align-items: center; gap: 12px; 
            transition: all 0.2s; background: rgba(0,0,0,0.2); margin-bottom: 0.8rem; 
        }
        .agent-toggle.active { border-color: var(--accent-primary); background: rgba(56, 189, 248, 0.08); }
        .agent-toggle .icon-box { 
            width: 42px; height: 42px; border-radius: 10px; background: rgba(255,255,255,0.05);
            display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: var(--text-primary); transition: all 0.2s;
        }
        .agent-toggle.active .icon-box { background: var(--accent-primary); color: #000; }
        
        .btn-primary { background: #fff; color: #000; padding: 0.8rem 2rem; font-weight: 700; border-radius: 99px; cursor: pointer; border: none; font-size: 1rem; transition: all 0.2s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255,255,255,0.2); }
        .btn-outline { background: transparent; color: #fff; border: 1px solid var(--surface-border); padding: 0.8rem 2rem; border-radius: 99px; cursor: pointer; font-size: 1rem; transition: all 0.2s; }
        .btn-outline:hover { background: rgba(255,255,255,0.05); }

        .success-circle {
            width: 80px; height: 80px; border-radius: 50%; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;
            display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2.5rem; color: #10b981;
        }
    </style>
</head>
<body>
    <div class="noise-overlay"></div>
    <div class="orb-1"></div>
    <div class="orb-2"></div>

    <div class="header-logo">
        <a href="index.html"><img src="assets/onstaff_logo.png" alt="OnStaffAI"></a>
    </div>

    <div class="wizard-container">
        <div class="step-indicator" id="step-indicator">
            <!-- Filled by JS -->
        </div>

        <div id="steps-container">
            <!-- Step 1: Company -->
            <div class="step-content active" id="step-1">
                <h2>פרטי החברה</h2>
                <div class="form-group">
                    <label>שם החברה *</label>
                    <input type="text" id="ob-company" class="form-control" placeholder="לדוגמה: חברה בע&quot;מ">
                </div>
                <div class="form-group">
                    <label>מספר חברה / ח.פ.</label>
                    <input type="text" id="ob-company-num" class="form-control" placeholder="51-xxxxxxx-x">
                </div>
                <div class="form-group">
                    <label>אתר אינטרנט</label>
                    <input type="url" id="ob-website" class="form-control" placeholder="https://">
                </div>
            </div>

            <!-- Step 2: Contact -->
            <div class="step-content" id="step-2">
                <h2>איש קשר ראשי</h2>
                <div class="form-group">
                    <label>שם מלא *</label>
                    <input type="text" id="ob-name" class="form-control" placeholder="ישראל ישראלי">
                </div>
                <div class="form-group">
                    <label>אימייל *</label>
                    <input type="email" id="ob-email" class="form-control" placeholder="info@example.com">
                </div>
                <div class="form-group">
                    <label>טלפון *</label>
                    <input type="tel" id="ob-phone" class="form-control" placeholder="05x-xxxxxxx">
                </div>
            </div>

            <!-- Step 3: Plan -->
            <div class="step-content" id="step-3">
                <h2>בחירת תוכנית</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div class="plan-card" onclick="selectPlan('starter')" id="plan-starter">
                        <h3 style="color:var(--text-primary);margin-bottom:4px;font-weight:700;">Starter</h3>
                        <div class="plan-price">₪490</div>
                        <p style="font-size: 0.9rem; color: var(--text-secondary);">עד 3 סוכנים</p>
                    </div>
                    <div class="plan-card selected" onclick="selectPlan('growth')" id="plan-growth">
                        <h3 style="color:var(--text-primary);margin-bottom:4px;font-weight:700;">Growth</h3>
                        <div class="plan-price">₪990</div>
                        <p style="font-size: 0.9rem; color: var(--text-secondary);">עד 6 סוכנים</p>
                    </div>
                    <div class="plan-card" onclick="selectPlan('business')" id="plan-business">
                        <h3 style="color:var(--text-primary);margin-bottom:4px;font-weight:700;">Business</h3>
                        <div class="plan-price">₪1990</div>
                        <p style="font-size: 0.9rem; color: var(--text-secondary);">עד 10 סוכנים</p>
                    </div>
                </div>
                <input type="hidden" id="ob-plan" value="growth">
            </div>

            <!-- Step 4: Agents -->
            <div class="step-content" id="step-4">
                <h2>אילו סוכנים להפעיל?</h2>
                <p style="margin-bottom: 1.5rem; color: var(--text-secondary);">בחרנו עבורך סוכנים מומלצים, ניתן לערוך בחירה זו תמיד.</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;" id="ob-agents-container">
                    <!-- Checkboxes generated by JS -->
                </div>
            </div>

            <!-- Step 5: Payment Placeholder -->
            <div class="step-content" id="step-5">
                <h2>אמצעי תשלום</h2>
                <p style="margin-bottom: 2rem; color: var(--text-secondary);">כדי להשלים את ההתקנה, יש להזין אמצעי תשלום. לא נחייב אותך עד סיום תקופת הניסיון (14 ימים).</p>
                
                <div style="background: rgba(0,0,0,0.3); border: 1px dashed var(--surface-border); border-radius: 16px; padding: 3rem 2rem; text-align: center;">
                    <i class="ph ph-credit-card" style="font-size: 3.5rem; color: var(--text-secondary); margin-bottom: 1rem;"></i>
                    <p style="font-weight: 500; color: var(--text-secondary);">(כאן תשולב מערכת סליקה מאובטחת - Stripe / משולם)</p>
                </div>
            </div>
            
            <!-- Step 6: Done -->
            <div class="step-content" id="step-6" style="text-align: center; padding: 4rem 0;">
                <div class="success-circle">
                    <i class="ph ph-check-bold"></i>
                </div>
                <h2 style="font-size: 2.2rem;">הכל מוכן! סוכני ה-AI בדרך.</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2.5rem; font-size: 1.1rem; max-width: 400px; margin-inline: auto;">פרטי ההתחברות לפורטל נשלחו לכתובת המייל שלך.</p>
                <a href="client_portal.html" class="btn btn-primary">היכנס לפורטל הניהול</a>
            </div>
        </div>

        <div class="nav-buttons" id="nav-buttons">
            <button class="btn btn-outline" id="btn-prev" onclick="prevStep()" style="visibility: hidden;">חזור</button>
            <button class="btn btn-primary" id="btn-next" onclick="nextStep()">המשך לשלב הבא</button>
        </div>
    </div>

    <!-- Firebase SDK -->
    <script type="module">
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
        import { getFirestore, doc, updateDoc, serverTimestamp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

        const firebaseConfig = {
            apiKey: "AIzaSyBExample-ReplaceWithYourKey",
            authDomain: "onstaffai.firebaseapp.com",
            projectId: "onstaffai"
        };
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        window._db = db;
        window._updateDoc = updateDoc;
        window._doc = doc;
        window._serverTimestamp = serverTimestamp;
    </script>

    <!-- EmailJS -->
    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
    
    <script>
        const EMAILJS_PUBLIC_KEY  = '7IoARO-EcljLAzrok';
        const EMAILJS_SERVICE_ID  = 'service_ne5z4wv';
        const EMAILJS_TEMPLATE_STEP = 'template_sl4n308'; // Template for step completion

        if (EMAILJS_PUBLIC_KEY !== 'YOUR_PUBLIC_KEY') {
            emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
        }

        const TOTAL_STEPS = 5;
        let currentStep = 1;
        let leadId = null;

        const STEPS_DATA = [
            { num: 1, id: 'company', label: 'פרטי חברה', icon: 'ph-buildings' },
            { num: 2, id: 'contact', label: 'איש קשר', icon: 'ph-user' },
            { num: 3, id: 'plan', label: 'תוכנית', icon: 'ph-star' },
            { num: 4, id: 'agents', label: 'סוכנים', icon: 'ph-robot' },
            { num: 5, id: 'payment', label: 'תשלום', icon: 'ph-credit-card' }
        ];

        const AGENT_TYPES = [
            { id: 'customer-service', label: 'שירות לקוחות', icon: 'ph-headphones' },
            { id: 'tech-support', label: 'תמיכה טכנית', icon: 'ph-wrench' },
            { id: 'marketing', label: 'שיווק ומכירות', icon: 'ph-megaphone' },
            { id: 'finance', label: 'כספים', icon: 'ph-currency-dollar' },
            { id: 'operations', label: 'תפעול', icon: 'ph-cube' },
            { id: 'onboarding', label: 'מלווה לקוחות', icon: 'ph-rocket-launch' },
            { id: 'hr', label: 'HR וגיוס', icon: 'ph-users-three' },
            { id: 'pm', label: 'מנהל פרויקטים', icon: 'ph-kanban' }
        ];

        function init() {
            // Render agents toggle
            const agc = document.getElementById('ob-agents-container');
            agc.innerHTML = AGENT_TYPES.map(a => `
                <div class="agent-toggle" id="ag-tog-${a.id}" onclick="toggleAgent('${a.id}')">
                    <div class="icon-box"><i class="ph ${a.icon}"></i></div>
                    <span style="font-weight:600; font-size:1.05rem; color:#fff; flex:1;">${a.label}</span>
                    <div id="ag-chk-${a.id}" style="width:22px;height:22px;border-radius:6px;border:1.5px solid var(--surface-border);display:flex;align-items:center;justify-content:center;transition:all 0.2s;"></div>
                </div>
            `).join('');

            // Parse URL params to prefill
            const params = new URLSearchParams(window.location.search);
            if (params.get('company')) document.getElementById('ob-company').value = params.get('company');
            if (params.get('name')) document.getElementById('ob-name').value = params.get('name');
            if (params.get('email')) document.getElementById('ob-email').value = params.get('email');
            if (params.get('phone')) document.getElementById('ob-phone').value = params.get('phone');
            if (params.get('lid')) leadId = params.get('lid');
            
            // Prefill selected agents
            const selectedAgents = params.get('agents') ? params.get('agents').split(',') : ['customer-service'];
            selectedAgents.forEach(aid => {
                if(aid && document.getElementById(`ag-tog-${aid}`)) toggleAgent(aid);
            });
            
            // Prefill selected plan
            const pPlan = params.get('plan');
            if(pPlan) {
                const planKey = pPlan.toLowerCase();
                if(['starter','growth','business'].includes(planKey)) selectPlan(planKey);
            }

            updateUI();
        }

        function toggleAgent(id) {
            const el = document.getElementById(`ag-tog-${id}`);
            const chk = document.getElementById(`ag-chk-${id}`);
            el.classList.toggle('active');
            if (el.classList.contains('active')) {
                chk.innerHTML = '<i class="ph ph-check" style="color:#000;font-weight:bold;font-size:14px;"></i>';
                chk.style.borderColor = 'var(--accent-primary)';
                chk.style.background = 'var(--accent-primary)';
            } else {
                chk.innerHTML = '';
                chk.style.borderColor = 'var(--surface-border)';
                chk.style.background = 'transparent';
            }
        }

        window.selectPlan = function(plan) {
            document.querySelectorAll('.plan-card').forEach(el => el.classList.remove('selected'));
            document.getElementById(`plan-${plan}`).classList.add('selected');
            document.getElementById('ob-plan').value = plan;
        }

        function validateStep() {
            if (currentStep === 1) {
                if (!document.getElementById('ob-company').value.trim()) return alert('יש להזין שם חברה');
            }
            if (currentStep === 2) {
                if (!document.getElementById('ob-name').value.trim()) return alert('יש להזין שם איש קשר');
                if (!document.getElementById('ob-email').value.trim()) return alert('יש להזין אימייל');
            }
            return true;
        }

        window.nextStep = async function() {
            if (!validateStep()) return;
            
            const btn = document.getElementById('btn-next');
            btn.disabled = true;
            btn.textContent = 'מעדכן...';

            // Sync with Firebase & Send Email
            if (leadId && window._db && window._updateDoc && window._doc) {
                try {
                    const docRef = window._doc(window._db, 'leads', leadId);
                    await window._updateDoc(docRef, {
                        step: currentStep + 1,
                        lastActivity: window._serverTimestamp ? window._serverTimestamp() : new Date().toISOString()
                    });
                    
                    // Send step completion email via EmailJS
                    if (EMAILJS_PUBLIC_KEY !== 'YOUR_PUBLIC_KEY') {
                        emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_STEP, {
                            to_email: document.getElementById('ob-email').value,
                            to_name: document.getElementById('ob-name').value,
                            completed_step: currentStep,
                            next_step: currentStep + 1
                        });
                    }
                } catch(e) {
                    console.error("Failed to update lead", e);
                }
            }

            btn.disabled = false;
            
            if (currentStep === TOTAL_STEPS) {
                finishOnboarding();
            } else {
                currentStep++;
                updateUI();
            }
        }

        window.prevStep = function() {
            if (currentStep > 1) {
                currentStep--;
                updateUI();
            }
        }

        function updateUI() {
            // Update steps visibility
            for (let i = 1; i <= 6; i++) {
                const el = document.getElementById(`step-${i}`);
                if(el) {
                    if (i === currentStep) el.classList.add('active');
                    else el.classList.remove('active');
                }
            }
            
            // Update buttons
            const btnPrev = document.getElementById('btn-prev');
            const btnNext = document.getElementById('btn-next');
            
            if (currentStep === 1) btnPrev.style.visibility = 'hidden';
            else btnPrev.style.visibility = 'visible';
            
            if (currentStep === TOTAL_STEPS) {
                btnNext.textContent = 'סיום והפעלת סוכנים';
                btnNext.style.background = '#10b981';
                btnNext.style.color = '#fff';
            } else {
                btnNext.textContent = 'המשך לשלב הבא';
                btnNext.style.background = '#fff';
                btnNext.style.color = '#000';
            }

            // Update indicator tabs
            const ind = document.getElementById('step-indicator');
            ind.innerHTML = STEPS_DATA.map((s, i) => `
                <div class="modal-tab ${currentStep === s.num ? 'active' : ''} ${currentStep > s.num ? 'done' : ''}">
                    <i class="ph ${s.icon}"></i> ${s.label}
                </div>
            `).join('');
        }
        
        function finishOnboarding() {
            document.getElementById('nav-buttons').style.display = 'none';
            document.getElementById('step-indicator').style.display = 'none';
            
            // Show step 6 (Done)
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`step-${i}`).classList.remove('active');
            }
            document.getElementById('step-6').classList.add('active');
        }

        // Initialize on load
        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/onboarding.html', 'w') as f:
    f.write(html_content)

