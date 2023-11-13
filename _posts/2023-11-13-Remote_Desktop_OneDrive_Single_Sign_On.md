---
layout: post
title: Remote Desktop - OneDrive Single Sign On
categories: Windows Server
tags: server 2022 rdp onedrive sso
---
In this video, we will Install OneDrive and configure Single Sign On with a Group Policy.

Let me know in the comments if you like to see a follow-up video on this because in this setup you have to download/install Onedrive the first time per user account. In the next video we can automate this process.

{% youtube "https://youtu.be/GFqTZh6xxb4" %}

# Instructions

[Download OneDrive](https://support.microsoft.com/en-us/office/onedrive-release-notes-845dcf18-f921-435e-bf28-4e24b95e5fc0?ui=en-us&rs=en-us&ad=us)

How to install the OneDrive Policy's please visit [manage-onedrive-using-group-policy](https://learn.microsoft.com/en-us/sharepoint/use-group-policy#manage-onedrive-using-group-policy).

Follow the [per-machine](https://learn.microsoft.com/en-us/sharepoint/per-machine-installation#deployment-instructions) instructions if you want to install OneDrive for **All Users**.

Configure the group policy for **All Users**

You will find the new Policy under **Computer Configuration\Policies\Administrative Templates\OneDrive**

I **enabled** the following:

* Use OneDrive Files On-Demand

* Silently move Windows known folders to OneDrive

* Silently sign in users to the OneDrive sync app with their Windows credentials