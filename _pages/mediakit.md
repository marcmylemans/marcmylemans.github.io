---
layout: page
title: "Media Kit"
permalink: /mediakit/
description: "Mylemans Online — YouTube & Tech Creator Media Kit"
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

## 📊 Channel Overview

| Metric | Current | Source |
|---------|----------|--------|
| **Subscribers** | <span id="yt-subs">Loading...</span> | YouTube API |
| **Monthly Views** | <span id="yt-views">Loading...</span> | YouTube API |
| **Watch Time (hours)** | <span id="yt-watch">Loading...</span> | YouTube API |
| **Top Audience** | 25–44 y/o, tech-savvy men (EU & US) | Analytics |
| **Main Topics** | Homelab • Proxmox • Windows Server • Automation |

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

<script>
async function loadYouTubeStats() {
  const channelId = "UC1y0Dtbzss2I3mm45xPMm1Q"; // replace with your channel ID
  const apiKey = "AIzaSyAnBMaJPMo2xftoApMPWlt0D3PFWG2JLus";
  const response = await fetch(`https://www.googleapis.com/youtube/v3/channels?part=statistics&id=${channelId}&key=${apiKey}`);
  const data = await response.json();
  const stats = data.items[0].statistics;
  document.getElementById("yt-subs").innerText = Number(stats.subscriberCount).toLocaleString();
  document.getElementById("yt-views").innerText = Number(stats.viewCount).toLocaleString();
  document.getElementById("yt-watch").innerText = "—"; // optional: custom estimate
}
loadYouTubeStats();
</script>
