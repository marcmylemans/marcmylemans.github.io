---
layout: post
title: Outlook and Teams open links on Microsoft Edge
categories: office outlook
tags: office office365 outlook regkey
---

Microsoft decided to change the behavior of Outlook and Teams. From now Outlook and Teams will open hyperlinks with Edge despite if another browser has been selected as the default browser.

To change this behaviour you can download the newest Office 365 ADMX files. Or create the registry key below.

To resolve this we need to run the following Powershell:

```powershell
Set-ItemProperty -Path “HKCU:\SOFTWARE\Policies\Microsoft\Office\16.0\common\links” -Name ‘BrowserChoice’ -Value 0 -Type DWORD –Force
```

To revert back to Edge as the default browser in Outlook:

```powershell
Set-ItemProperty -Path “HKCU:\SOFTWARE\Policies\Microsoft\Office\16.0\common\links” -Name ‘BrowserChoice’ -Value 1 -Type DWORD –Force
```

After this you need to close Outlook and open it again.