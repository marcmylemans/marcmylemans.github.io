---
layout: post
title: AutoPilot - Hybrid Azure AD
date: 2023-01-02 09:00:00
categories: Azure Intune
tags: server 2022 azure hybrid autopilot
---

In this video we will be using the power of Autopilot / Intune / Active Directory Group Policy's to create a Hybrid Azure Joined Device.

What will be included in this video:
- Installing Intune connector for Active Directory.
- Create a specific Organisational Unit for our Autopilot Devices.
- Create a Dynamic Security Group for our Autopilot Devices.
- Create an Hybrid Azure AD joined Autopilot profile and Domain Join configuration in Intune. You can also change this to Azure AD Joined and skip the Domain Join Configuration if you only want to Azure AD Join your devices.
- Azure AD join our new device to enroll(*) them into Intune. 
Reset the new device so autopilot can automatilcy Hybrid join our new device into Active Directory.

(*)You can enroll your devices into Auto Pilot in other (more automated ways). Please let me know in the comments of this is something you would like to see.

Source:
(https://learn.microsoft.com/en-us/mem/autopilot/windows-autopilot-hybrid)

{% youtube "https://youtu.be/Jp_kmppB_Fk" %}
