import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'r') as f:
    content = f.read()

# Add plan selector HTML right after Agent count
plan_html = """
                    <!-- Plan selector -->
                    <div style="margin-bottom:1.2rem;">
                        <label style="font-size:0.8rem;color:rgba(255,255,255,0.5);display:block;margin-bottom:6px;">
                            באיזו תוכנית תמחור אתה מעוניין?
                            <span style="color:#ea580c;font-size:0.72rem;margin-right:6px;">לא חובה, אך יעזור לנו להתאים עבורך את השירות</span>
                        </label>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            <label id="plan-starter" onclick="selectPlan(this,'Starter')" style="cursor:pointer;padding:7px 18px;border-radius:20px;border:1px solid rgba(255,255,255,0.15);font-size:0.85rem;color:rgba(255,255,255,0.7);transition:all 0.2s;user-select:none;">Starter</label>
                            <label id="plan-pro" onclick="selectPlan(this,'Pro')" style="cursor:pointer;padding:7px 18px;border-radius:20px;border:1px solid rgba(255,255,255,0.15);font-size:0.85rem;color:rgba(255,255,255,0.7);transition:all 0.2s;user-select:none;">Pro</label>
                            <label id="plan-enterprise" onclick="selectPlan(this,'Enterprise')" style="cursor:pointer;padding:7px 18px;border-radius:20px;border:1px solid rgba(255,255,255,0.15);font-size:0.85rem;color:rgba(255,255,255,0.7);transition:all 0.2s;user-select:none;">Enterprise</label>
                        </div>
                        <input type="hidden" id="cf-plan">
                    </div>
"""

# Insert plan_html after cf-agent-count
content = content.replace('<input type="hidden" id="cf-agent-count">\n                    </div>', '<input type="hidden" id="cf-agent-count">\n                    </div>\n' + plan_html)

# Add selectPlan JS function
js_plan = """
        let _selectedPlan = '';
        function selectPlan(el, val) {
            document.querySelectorAll('[id^="plan-"]').forEach(function(l) {
                l.style.background = 'transparent';
                l.style.color = 'rgba(255,255,255,0.7)';
                l.style.borderColor = 'rgba(255,255,255,0.15)';
            });
            el.style.background   = 'rgba(234,88,12,0.18)';
            el.style.color        = '#fff';
            el.style.borderColor  = '#ea580c';
            _selectedPlan = val;
            document.getElementById('cf-plan').value = val;
        }
"""
content = content.replace('let _selectedCount = \'\';', js_plan + '\n        let _selectedCount = \'\';')
content = content.replace('window.selectAgentCount    = selectAgentCount;', 'window.selectAgentCount    = selectAgentCount;\n        window.selectPlan          = selectPlan;')

# Add 'plan' to handleContactSubmit and Firestore saving
content = content.replace("const agents  = document.getElementById('cf-agents').value;", "const agents  = document.getElementById('cf-agents').value;\n            const plan    = document.getElementById('cf-plan').value;")
content = content.replace("agents: agents", "agents: agents,\n                        plan: plan")
content = content.replace("agentCount: count,", "agentCount: count,\n                        plan: plan,")

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/index.html', 'w') as f:
    f.write(content)
