---
categories: Windows 11
layout: post
tags: windows 10 11 powershell hello
title: Windows hello - Disable PIN
---

By default Windows 10/11 will enable Windows Hello and ask you to configure a PIN.
If you want to remove the PIN after enabling run the following in Powershell as an Administrator.

```powershell
#Disable pin requirement
$path = "HKLM:\SOFTWARE\Policies\Microsoft"
$key = "PassportForWork"
$name = "Enabled"
$value = "0"
 
New-Item -Path $path -Name $key –Force
 
New-ItemProperty -Path $path\$key -Name $name -Value $value -PropertyType DWORD -Force
 
#Delete existing pins
$passportFolder = "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Ngc"
 
if(Test-Path -Path $passportFolder)
{
Takeown /f $passportFolder /r /d "Y"
ICACLS $passportFolder /reset /T /C /L /Q
 
Remove-Item –path $passportFolder –recurse -force
}
```