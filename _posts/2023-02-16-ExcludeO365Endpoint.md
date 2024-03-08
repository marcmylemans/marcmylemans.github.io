---
categories: Azure Exchange
layout: post
tags: exchange office365 migration azure
title: Unexpected Autodiscover behavior when you have registry settings under the
  \Autodiscover key
---

During a migration from an Onpremise Exchange to O365 i encountered the issue that Outlook would ask for the credentials from O365.
Because the mailbox was still on the Onpremise Exchange Outlook could not find a mailbox.

To resolve this we need to run the following Powershell:

```powershell
Set-ItemProperty -Path “HKCU:\Software\Microsoft\Office\16.0\Outlook\AutoDiscover” -Name ‘ExcludeExplicitO365Endpoint’ -Value 1 -Type DWORD –Force
```

```powershell
Set-ItemProperty -Path “HKCU:\Software\Policies\Microsoft\Office\16.0\Outlook\AutoDiscover” -Name ‘ExcludeExplicitO365Endpoint’ -Value 1 -Type DWORD –Force
```

After this you need to close Outlook and open it again, sometimes it can take a few minutes.