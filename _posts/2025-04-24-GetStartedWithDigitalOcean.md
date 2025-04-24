---
image: https://mylemans.online/assets/img/posts/7c4285c92df0.png
layout: post
title: "How to Get Started with DigitalOcean (and Get $200 Free Credit!)"
date: 2025-04-24
categories: [Cloud Hosting, Digital Ocean]
---

# How to Get Started with DigitalOcean (and Get $200 Free Credit!)

Are you ready to launch your own VPS, website, or app but don’t want to break the bank?  
**DigitalOcean** is one of the easiest and most affordable cloud platforms to get started with — and with my referral link, you’ll receive **$200 in free credits** to use over 60 days!

Whether you're a developer, freelancer, or just curious about hosting your server, here's a step-by-step guide to get going.

---

## Claim Your Free Credit

Use this link to sign up and get started with $200 in credit:

👉 **[Sign up to DigitalOcean here](https://m.do.co/c/e03b740d65fb)**

Or use the badge below:

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=e03b740d65fb&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

---

## Step 1: Create Your DigitalOcean Account

1. Click the referral link above and register for a free account.
2. You'll be asked to verify your email and add a payment method (credit card or PayPal) to prevent abuse — **you won’t be charged upfront**.
3. Once verified, your **$200 in credits** will be automatically applied.

---

## Step 2: Create Your First Droplet (VPS)

A "Droplet" is what DigitalOcean calls its VPS instances. To create one:

1. Go to the **Droplets** tab and click **Create Droplet**.
2. Choose your OS (Ubuntu is great for most users).
3. Select a data center close to your audience.
4. Pick a plan (start with the $5/month plan — it's free with your credits!).
5. Set up authentication (SSH key or password).
6. Click **Create Droplet**.

That's it! Your server will be ready in less than a minute.

---

## Step 3: Secure & Configure Your Droplet

To keep your server secure and performing well, follow these steps right after creating your droplet:

### Connect via SSH

```bash
ssh root@your_droplet_ip
```

> Replace `your_droplet_ip` with the actual IP address of your droplet.

---

### Update Your Packages

```bash
apt update && apt upgrade -y
```

---

### Configure the Firewall

Enable UFW (Uncomplicated Firewall) and allow only essential services:

```bash
ufw allow OpenSSH
ufw enable
ufw status
```

#### (Optional) Also allow web traffic (if you plan to host web services)

```bash
ufw allow 80/tcp
ufw allow 443/tcp
```

---

### Install and Enable Fail2Ban

Step 1: Install Fail2Ban

```bash
apt install fail2ban -y
```

Step 2: Create a local configuration file:

```bash
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```
Edit the **jail.local** file:

```bash
nano /etc/fail2ban/jail.local
```

Ensure the following lines are present and uncommented:

```
[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 5
```

Step 3: Start and Enable Fail2Ban

```bash
systemctl enable fail2ban
systemctl start fail2ban
```

Fail2Ban helps protect against brute-force attacks by banning IPs with too many failed login attempts.

To unban an IP address:

```bash
fail2ban-client set sshd unbanip <IP_ADDRESS>
```

---

### Install Docker & Docker Compose (Optional) 

```bash
apt install docker.io docker-compose -y
systemctl enable docker
systemctl start docker
```

---

If you'd like me to set this up for you, [check out my Fiverr gig](https://www.fiverr.com/share/XYZ) — I’ll handle everything so you can focus on building your project.


---

## What Can You Do with DigitalOcean?

- Host websites and blogs (WordPress, static sites)
- Run your own VPN or cloud storage
- Deploy web apps or APIs
- Set up developer environments
- Much more!

---

## Final Thoughts

DigitalOcean is a fantastic platform to learn, build, and deploy. And with the free $200 credit, you’ve got **zero risk** to get started.

👉 [![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=e03b740d65fb&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)  
Let me know if you need help — I’d be happy to assist!

