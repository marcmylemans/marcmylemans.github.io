---
categories: Windows Server
layout: post
tags: windows server powershell hyperv
title: Find Your Hyper-V VM’s Host Name with PowerShell
---

use the powershell command below if you ever need to find out on wich Hyper-V server your vm is running.

Run as admin:

```powershell
(get-item "HKLM:\SOFTWARE\Microsoft\Virtual Machine\Guest\Parameters").GetValue("HostName")
```