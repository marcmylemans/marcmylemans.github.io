---
layout: post
title: Installing the Remote Desktop Web Client!
categories: Windows Server
tags: server 2022 rdp part5 html5 browser
---

In this video we will configure the Remote Desktop Web Client. This way our users can use any device/browser (For Example a Smartphone/Tablet/...) that supports HTML5 to open a connection to the Remote Desktop host.

{% youtube "https://youtu.be/i87spvTzR6w" %}

[Source](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-web-client-admin)

Run powershell as an Administrator
```powershell
Install-Module -Name PowerShellGet -Force
```
Close Powershell!
Run powershell as an Administrator
```powershell
Install-Module -Name RDWebClientManagement
```
```powershell
Install-RDWebClientPackage
```
```powershell
Import-RDWebClientBrokerCert <.cer file path>
```
```powershell
Publish-RDWebClientPackage -Type Production -Latest
```
Be sure to check out the previous video where we configured Remote Desktop Services:

[Server 2022 - Remote Desktop Services - Part 1]({% link _posts/2022-12-27-RemoteDesktopPart1.md %})

[Server 2022 - Remote Desktop Services - Part 2]({% link _posts/2022-12-31-RemoteDesktopPart2.md %})

[Server 2022 - Remote Desktop Services - Part 3]({% link _posts/2023-01-03-RemoteDesktopPart3.md %})

[Installing Office 365 on a Remote Desktop Host!]({% link _posts/2023-01-04-RemoteDesktopPart4.md %})


