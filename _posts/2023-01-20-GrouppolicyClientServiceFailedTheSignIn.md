---
layout: post
title: FSLogix - Service group policy client prevents login
categories: Server
tags: server 2022 gpo bug error fslogix wvd
---


![Assign users](/assets/GrouppolicyClientServiceFailedTheSignIn/error.png)

If you ever encounter the following error with FSLogix that a user can't login because of the error Service group policy client prevents login.

Here is how to fix it!


Find the SID for the affected user 'Local user'

```powershell
Get-LocalUser -Name 'johndoe' | Select-Object  sid
```

Find the SID for the affected user 'Active Directory'

```powershell
Import-Module ActiveDirectory
Get-AdUser -Identity toms | Select Name, SID, UserPrincipalName
```

Open Regedit and navigate to the following regkey:

```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileService\References\<sid affected user>
```

Change the "RefCount" value to 0.


