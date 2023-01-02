---
layout: post
title: Server 2022 - Remote Desktop Services - Part 1
date: 2022-12-27 09:00:00
categories: Windows Server
tags: server 2022 rdp part1
---

In this video we will deploying Remote Desktop Services.
In Part 1 we deploy a Broker,Host, Web Access and a Gateway. 

You will be needing at least 2 Domain Joined (Virtual Machines) Servers. A public domain name a Public certificate (For our lab environment we will be using a Lets Encrypt certificate, for production environments an paid Certificate is recommended).

1 Server will be needed for our Broker/Web Acces and Gateway services. This server will have to be configured with a fixed ip and ports 80,433 will need to be port forwarded in your Router/firewall to this server.

1 Server will be needed for our RDS Host.

{% youtube "https://youtu.be/bkTFagCdycc" %}
