---
layout: post
title: Uninstall Azure AD Connect
categories: Windows Server
tags: azure domaincontroller adconnect sync
---

In this article we are going to uninstall AD Connect because the customer is fully migrated to the cloud.

On the server where AD Connect is installed run the following powershell commands:

```powershell
Import-Module ADSync
Set-ADSyncScheduler -SyncCycleEnabled $false
```

Verify that the sync is disabled:

```powershell
Get-ADSyncScheduler | ft SyncCycleEnabled
```

Then connect to the Azure tenant:


```powershell
Connect-MsolService
```

Turn off DirSync:

```powershell
Set-MsolDirSyncEnabled -EnableDirSync $false
```

Verify that the sync is disabled:

```powershell
(Get-MSOLCompanyInformation).DirectorySynchronizationEnabled
```

Next:

Uninstall Azure AD Connect from server

1. Click on Start > Control Panel > Programs and Features.
2. Click on Microsoft Azure AD Connect and press on Uninstall.
3. The Uninstall Azure AD Connect wizard shows up. Check the checkbox Also uninstall supporting components. Click Remove