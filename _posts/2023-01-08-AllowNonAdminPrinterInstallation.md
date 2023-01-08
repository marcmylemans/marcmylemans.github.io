---
layout: post
title: Allow (Print) Driver installation (Non Admins)
categories: Windows Server
tags: server 2022 printer gpo
---

In this video we will configure a Group Policy to allow our 'Non Administrator' users to install Printer Drivers to their workstations.

{% youtube "https://youtu.be/sTIjM9f8e1Q" %}

[Sources - Driver Installation Prevention](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/devices-prevent-users-from-installing-printer-drivers)

[Sources - Manage Device Installation with Group Policy](https://learn.microsoft.com/en-us/windows/client-management/manage-device-installation-with-group-policy)

Class = Printer
```
{4658ee7e-f050-11d1-b6bd-00c04fa372a7};
```

Class = PNPPrinters 
```
{4d36e979-e325-11ce-bfc1-08002be10318}
```

