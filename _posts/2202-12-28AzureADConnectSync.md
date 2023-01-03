---
layout: post
title: Server 2022 - Azure AD Connect sync
date: 2022-12-28 09:00:00
categories: Windows Server
tags: server 2022 azure
---

In this video we are connecting our Server 2022 Active Directory with Azure AD.
After this we will AD Sync our selected User and Security Group Ou's. 

First step:
We will create a security group for a controlled test Sync. 
To automate things further we will create a GPO for Seamless Sign On for our clients and create a Security Group to automate assigning licenses to our AAD Synced users.

Second step:
After our 'testing phase' we will disconnect the security group so everybody withing our OU structure will automticly sync. 


Try O365:
(https://learn.microsoft.com/en-us/microsoft-365/commerce/try-or-buy-microsoft-365?view=o365-worldwide)

Download Link Azure AD Connect
(https://www.microsoft.com/en-us/download/details.aspx?id=47594)

Deploy Single Sign On:
(https://learn.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-sso-quick-start#deploy-seamless-single-sign-on)

{% youtube "https://youtu.be/2XeRcNKzuUM" %}
