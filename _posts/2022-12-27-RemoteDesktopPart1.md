---
date: 2022-12-27 09:00:00
image: https://mylemans.online/assets/img/posts/bkTFagCdycc.jpg
layout: post
categories: [Windows, Server 2022]
tags: [server 2022, rdp, remote desktop services, rds, tutorial, youtube, part1]
title: Server 2022 - Remote Desktop Services - Part 1
---

{% youtube "https://youtu.be/bkTFagCdycc" %}

---

**Update:** We've recently created a comprehensive guide that covers everything you need to know about setting up Remote Desktop Services (RDS) in **Windows Server 2022**. It consolidates all the topics from this series into one detailed post. Check it out here: [A Step-by-Step Guide - Setting Up Remote Desktop Services With FS Logix And Single Sign On!](https://mylemans.online/posts/Remote-Desktop-Services-Part1/).

---

Join us in this first part of our series on deploying Remote Desktop Services (RDS) in Windows Server 2022. This tutorial is designed for IT professionals looking to set up a robust RDS environment in their network.

---

### Deploying Key RDS Components

In Part 1 of this series, we focus on setting up the fundamental components of RDS:

1. **Remote Desktop Broker**: The central hub that manages RDS connections.
2. **Remote Desktop Host**: The server where your applications and resources run.
3. **Web Access and Gateway**: Enabling remote access to your RDS environment via the web.

---

### Prerequisites for Deployment

Before diving into the setup, ensure you have the following:

- **Two Domain-Joined Servers (Virtual Machines)**: These will serve as the backbone of your RDS setup.
- **Public Domain Name**: Essential for accessing your RDS environment externally.
- **Public Certificate**: We use a Let's Encrypt certificate for our lab, but a paid certificate is recommended for production environments.
- **Network Configuration**: One server will host the Broker/Web Access/Gateway services and will require a fixed IP with ports 80 and 443 forwarded to it in your router/firewall.

---

### Setting Up Your RDS Environment

This video will guide you through each step of the process, from initial server setup to configuring each RDS component. We’ll cover:

- **Broker/Web Access and Gateway Server Setup**: How to configure and optimize your first server for these roles.
- **RDS Host Configuration**: Setting up your second server to host your remote desktop sessions.

---

### Why RDS?

Remote Desktop Services in Server 2022 offers:

- **Flexibility**: Access your applications and data from anywhere.
- **Scalability**: Easily adjust to changing workloads and user numbers.
- **Security**: Centralized control over access and data.

---

### Concluding Thoughts

This tutorial marks the beginning of your journey to a fully functional RDS environment in Windows Server 2022. For a more detailed and comprehensive guide that covers these topics and more, check out our new post: [Link to New Blog Post].

Stay tuned for more in-depth tutorials on Windows Server 2022, and we’re eager to hear your feedback!

