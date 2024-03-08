---
categories: windows registery
layout: post
tags: windows register drivemapping networkdrive
title: Drivemapping with Registery key's

image: /assets/img/posts/Default.webp
---

# Configuring Drivemapping with Registeryg Keys!


Save the following as **Drivemap.reg**, make sure you replace HKEY_CURRENT_USER\Network\Z with the Driveletter you want to use, for example **Z**. take note that these settings are for the **Current User** that is logged on to the system.

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Network\Z]
"ConnectFlags"=dword:00000000
"ConnectionType"=dword:00000001
"DeferFlags"=dword:00000004
"ProviderName"="Microsoft Windows Network"
"ProviderType"=dword:00020000
"RemotePath"="\\\\servername\\folder"
"UserName"=dword:00000000

```

Run the **Drivemap.reg** as the user


You can create a **.reg** file for each Driveletter and push these to your clients.

To import multiple .reg files all at once you can use the following cmd:

```
for /f "tokens=*" %%a in ('dir /b *.reg') do (
	echo  Importing Settings: %%a
	regedit /S "%%a"
)
```