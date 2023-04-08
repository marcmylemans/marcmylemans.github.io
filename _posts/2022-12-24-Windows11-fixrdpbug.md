---
layout: post
title: Windows 11 - Fix 22H2 Remote Desktop issues!
date: 2022-12-24 09:00:00
categories: Windows 11
tags: windows 11 rdp bugfix register
---

In this video we will create a specific Group Policy for Windows 11 22H2 clients. With this policy we will disable the usage of UDP with rdp clients and force them to use TCP.

Because UDP is normally faster then TCP we only want to apply this Policy to our affected Windows 11 22H2 Devices. We will be using WMI Filters for this.

[Source](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-firewall/create-wmi-filters-for-the-gpo)

To disable UDP connections:
In regedit go to:
```
HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\Client
```
Create a new DWORD entry named: 
```
fClientDisableUDP
```
With a value of 1, and restart the device.

{% youtube "https://youtu.be/FDcCoxioSp8" %}
