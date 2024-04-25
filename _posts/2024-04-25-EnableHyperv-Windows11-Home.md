---
categories: Windows Server 2022
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
tags: hyper-v virtualisation home
title: Enable Hyper-V on Windows 10/11 Home Edition!
---


# Exciting Update: Enable Hyper-V on Windows 10/11 Home Edition!

Welcome back to our blog! As you know, we've been exploring various ways to enhance your home lab experience using Hyper-V, which typically requires a Windows Pro or Server environment. Today, I'm thrilled to share a workaround that enables Hyper-V on Windows 10/11 Home editions!

### Discovering the Workaround

A script developed by the Microsoft Virtualization team can activate Hyper-V on systems running Home editions of Windows 10 or Windows 11. While this script is an unofficial method and not guaranteed to work in perpetuity (especially through system updates), it presents a valuable opportunity for home users to engage with virtualization technology without the need for an immediate system upgrade.

### How to Check if Virtualization is Enabled

Before proceeding, ensure your system supports virtualization:
1. Open `Command Prompt`.
2. Type `systeminfo` and press Enter.
3. Look for `Virtualization Enabled in Firmware`. If it says `No`, you'll need to enable this in your BIOS settings.

### Running the Hyper-V Enabling Script

To enable Hyper-V using the script:
1. **Create a Batch File**: Paste the provided script into a text file and save it as `Enable-Hyper-V.bat`.
2. **Run as Administrator**: Right-click the batch file and select 'Run as Administrator'. This is crucial, as the script requires elevated privileges to make changes to your system.

```
pushd "%~dp0"
dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt
for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
del hyper-v.txt
Dism /online /enable-feature /featurename:Microsoft-Hyper-V -All /LimitAccess /ALL
pause
```

This script will install necessary components and enable Hyper-V on your machine. Please make sure to restart your computer once the script completes its execution.

### Recommended Hardware

For those starting with Hyper-V:
- **RAM**: At least 8 GB.
- **Storage**: An SSD for better performance.

### Moving Forward

For long-term and stable use of Hyper-V, upgrading from Windows Home to Pro is advisable, as it provides official support and stability for Hyper-V.

For more detailed instructions on enabling Hyper-V using the script and other virtualization tips, check out the [original guide on The Windows Club](https://www.thewindowsclub.com/how-to-install-and-enable-hyper-v-on-windows-10-home) and [CloudBytes](https://cloudbytes.dev/snippets/enable-hyper-v-on-windows-1011-home).

