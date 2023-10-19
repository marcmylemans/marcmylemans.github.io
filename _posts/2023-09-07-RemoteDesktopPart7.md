---
layout: post
title: Remote Desktop Services, Securing it with Azure MFA!
categories: Windows Server
tags: server 2022 rdp part7 mfa
---

In this video we will install the Azure MFA NPS Extension, with this extension we can use the Multifactor Authentication from Azure AD and securing the Remote Desktop Gateway connection for Remote Desktop.


{% youtube "https://youtu.be/b5WL7PgEmaY" %}


[Download NPS Extension](https://www.microsoft.com/en-us/download/details.aspx?id=54688)

```powershell
cd 'c:\Program Files\Microsoft\AzureMfa\Config'
```

```powershell
.\AzureMfaNpsExtnConfigSetup.ps1
```

In order for Non MFA enabled users to continue to connect to the Remote Gateway server you can add the following Regkey in the registy of the NPS installed server under the following registery path, open an elevated cmd prompt and run the following command

```
reg add HKLM\Software\Microsoft\AzureMFA /v REQUIRE_USER_MATCH /t REG_SZ /d FALSE
```

Reboot the server for it to take effect.

Be sure to check out the previous video where we configured Remote Desktop Services:

[Server 2022 - Remote Desktop Services - Part 1]({% link _posts/2022-12-27-RemoteDesktopPart1.md %})

[Server 2022 - Remote Desktop Services - Part 2]({% link _posts/2022-12-31-RemoteDesktopPart2.md %})

[Server 2022 - Remote Desktop Services - Part 3]({% link _posts/2023-01-03-RemoteDesktopPart3.md %})

[Installing Office 365 on a Remote Desktop Host!]({% link _posts/2023-01-04-RemoteDesktopPart4.md %})

[Server 2022 - Remote Desktop Services - Part 5]({% link _posts/2023-01-05-RemoteDesktopPart5.md %})

[Server 2022 - Remote Desktop Services - Part 6]({% link _posts/2023-01-23-Remote_DesktopPart6.md %})