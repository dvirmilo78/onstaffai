import re

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/admin.html', 'r') as f:
    content = f.read()

# Add column to table header
content = content.replace(
    '<th>טלפון</th>\n                            <th>סטטוס</th>',
    '<th>טלפון</th>\n                            <th>סוכנים ותוכנית</th>\n                            <th>סטטוס</th>'
)

# Replace loadLeads function
new_load_leads = """
        // Fetch Leads Data from Firebase
        async function loadLeads() {
            const tbody = document.getElementById('leads-body');
            tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">טוען נתונים...</td></tr>';
            
            try {
                const snapshot = await _db.collection('leads').orderBy('lastActivity', 'desc').get();
                tbody.innerHTML = '';
                
                if (snapshot.empty) {
                    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">אין לידים עדיין</td></tr>';
                    return;
                }
                
                snapshot.forEach(doc => {
                    const lead = doc.data();
                    let badgeClass = 'new';
                    let statusText = 'חדש';
                    
                    if(lead.step === 1) statusText = 'השאיר פרטים';
                    else if(lead.step > 1 && lead.step < 5) {
                        statusText = 'תהליך אונבורדינג';
                        badgeClass = 'progress';
                    }
                    else if (lead.step >= 5) {
                        statusText = 'לקוח קיים';
                        badgeClass = 'active';
                    }

                    // Format date
                    let dateStr = '';
                    if (lead.lastActivity && lead.lastActivity.toDate) {
                        const d = lead.lastActivity.toDate();
                        dateStr = d.toLocaleDateString('he-IL') + ' ' + d.toLocaleTimeString('he-IL', {hour: '2-digit', minute:'2-digit'});
                    }

                    // Format plan and agents
                    const planText = lead.plan ? `<span style="display:inline-block;padding:2px 6px;background:rgba(234,88,12,0.1);color:var(--primary-color);border-radius:4px;font-size:11px;margin-bottom:4px;">${lead.plan}</span><br>` : '';
                    let agentsText = lead.agents ? lead.agents : '';
                    if(agentsText && agentsText.length > 30) agentsText = agentsText.substring(0,30) + '...';

                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${dateStr}</td>
                        <td>${lead.name || ''}</td>
                        <td>${lead.company || ''}</td>
                        <td>${lead.email || ''}</td>
                        <td>${lead.phone || ''}</td>
                        <td>${planText}<span style="font-size:11px;color:var(--text-secondary);">${agentsText}</span></td>
                        <td><span class="badge ${badgeClass}">${statusText}</span></td>
                        <td style="display:flex;gap:6px;align-items:center;">
                            <button onclick="convertLeadToClient({name:'${lead.name || ''}',company:'${lead.company || ''}',email:'${lead.email || ''}',phone:'${lead.phone || ''}'})"
                                style="padding:5px 10px;background:rgba(234,88,12,0.1);color:var(--primary-color);border:1px solid rgba(234,88,12,0.3);border-radius:7px;cursor:pointer;font-size:12px;font-weight:600;white-space:nowrap;font-family:Heebo,sans-serif;display:flex;align-items:center;gap:4px;">
                                <i class="ph ph-user-plus"></i> צור לקוח (אשף)
                            </button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (error) {
                console.error("Error loading leads:", error);
                tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:red;">שגיאה בטעינת הנתונים</td></tr>';
            }
        }
"""

old_load_leads_start = "        // Mock Leads Data (CRM)\n        function loadLeads() {"
old_load_leads_end = "        function convertLeadToClient(lead) {"
idx_start = content.find(old_load_leads_start)
idx_end = content.find(old_load_leads_end)

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + new_load_leads + content[idx_end:]

with open('/Users/dvirmilo/.gemini/antigravity/scratch/AgentFlow/admin.html', 'w') as f:
    f.write(content)
