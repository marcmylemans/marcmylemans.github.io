---
layout: page
title: "mediakit"
icon: fas fa-address-card
order: 99
permalink: /mediakit/
---

<div class="text-center">
  <img src="https://mylemans.online/assets/img/favicons/mstile-150x150.png" alt="Mylemans Online Logo" width="180" style="margin-bottom: 1rem;">
  <h1>Mylemans Online — Media Kit</h1>
  <p>Tech • Homelab • Tutorials</p>
</div>

---

## About Mylemans Online

Hi! I’m **Marc Mylemans**, a Belgian IT systems engineer and content creator.  
Through my YouTube channel, blog, and community, I share **practical tutorials** on Proxmox, Active Directory, Homelabs, and real-world IT setups — all with a personal touch.

My goal is to make complex tech **accessible, fun, and hands-on** for enthusiasts and professionals alike.

---

## 🧰 Collaboration Opportunities

I’m open to **honest, long-term collaborations** that align with my audience’s interests.

**Options include:**
- Sponsored videos or mentions  
- Affiliate partnerships  
- Product reviews (hardware/software)  
- Long-term ambassador roles  
- Giveaway collaborations  

---

## 🎥 Example Content

| Video | Topic | Link |
|-------|--------|------|
| Proxmox Cluster Setup | Homelab Virtualization | [Watch on YouTube](https://youtube.com/@mylemansonline) |
| AD to Entra ID Sync | Hybrid Identity | [Watch on YouTube](https://youtube.com/@mylemansonline) |
| DeskPi Rack Setup | 10-inch Homelab Build | [Watch on YouTube](https://youtube.com/@mylemansonline) |

---

## 🌍 Audience Snapshot

**Top Countries:** Belgium, Netherlands, Germany, US, UK  
**Audience Interests:** Proxmox, Active Directory, Windows Server, Home IT setups  
**Engagement:** High retention on tutorials and setup videos  

---

## 🧩 Contact

📧 **marc@mylemans.online**  
🌐 [mylemans.online](https://mylemans.online)  
🎥 [YouTube — Mylemans Online](https://youtube.com/@mylemansonline)  
🦋 [Bluesky](https://bsky.app/profile/mylemansonline.bsky.social)

---

<div class="text-center" style="margin-top:2rem;">
  <button onclick="window.print()" class="btn btn-primary">📄 Download as PDF</button>
</div>

---
<table>
  <tr><th>Website users (period)</th><td id="ga-users">—</td></tr>
  <tr><th>New users</th><td id="ga-new">—</td></tr>
  <tr><th>Avg. engagement / active user</th><td id="ga-eng">—</td></tr>
  <tr><th>Events</th><td id="ga-events">—</td></tr>
</table>

<ul id="ga-top-pages"></ul>

<script defer>
async function loadGA(){
  try{
    const res = await fetch('https://mylemans.online/assets/data/ga-site.json?v=' + Date.now(), {cache:'no-store'});
    const j = await res.json();
    const k = j.kpis || {};
    const p = j.period ? ` (${j.period.start} → ${j.period.end})` : '';
    const fmt = n => (n==null||n==='') ? '—' : Number(n).toLocaleString();
    document.getElementById('ga-users').textContent = fmt(k.active_users) + p;
    document.getElementById('ga-new').textContent   = fmt(k.new_users);
    // format seconds to mm:ss
    const s = Number(k.avg_engagement_seconds_per_active_user||0);
    const mm = Math.floor(s/60), ss = Math.round(s%60).toString().padStart(2,'0');
    document.getElementById('ga-eng').textContent   = s ? `${mm}:${ss}` : '—';
    document.getElementById('ga-events').textContent= fmt(k.event_count);

    const ul = document.getElementById('ga-top-pages');
    (j.top_pages||[]).forEach(row=>{
      const li = document.createElement('li');
      const parts = [];
      if (row.title) parts.push(row.title);
      if (row.views!=null) parts.push(`${row.views.toLocaleString()} views`);
      if (row.active_users!=null) parts.push(`${row.active_users.toLocaleString()} users`);
      li.textContent = parts.join(' — ');
      ul.appendChild(li);
    });
  }catch(e){ console.error('GA load error', e); }
}
document.addEventListener('DOMContentLoaded', loadGA);
</script>

