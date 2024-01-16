---
layout: post
title: Find Your Hyper-V VM’s Host Name with PowerShell
categories: Windows Server
tags: windows server powershell hyperv
---

use the powershell command below if you ever need to find out on wich Hyper-V server your vm is running.

Run as admin:

```powershell
(get-item "HKLM:\SOFTWARE\Microsoft\Virtual Machine\Guest\Parameters").GetValue("HostName")
```


