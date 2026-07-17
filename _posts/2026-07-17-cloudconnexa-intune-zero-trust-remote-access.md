---
title: "CloudConnexa + Intune: Zero-Trust Remote Access"
description: "Build identity-driven remote access with CloudConnexa, wire SAML to Entra ID, then deploy OpenVPN Connect through Intune with the Cloud ID pre-filled."
categories: [Security, Networking]
tags: [cloudconnexa, openvpn, zero-trust, intune, entra-id, saml, nis2, tutorial, youtube]
date: 2026-07-17 09:00:00 +0200
image:
  path: /assets/img/posts/cloudconnexa-intune/13-network-topology.jpg
  alt: CloudConnexa network topology showing the connector, network, and connected devices
---

## Your remote access is fine, until someone leaves

Most small-business remote access is a shared VPN config that has been sitting in a Teams chat for three years, an RDP port someone swears is safe because it is not the default one, and no clean way to answer the one question that matters when a person walks out the door: what can they still get into?

In this post I build the fix. You will stand up identity-driven, segmented remote access with CloudConnexa, tie sign-in to Microsoft Entra ID over SAML, and then deploy the OpenVPN Connect client across a Windows fleet through Intune, with the CloudConnexa Cloud ID already filled in so users never type a server URL. I will show the SSO error I hit on the first try, and the single Intune detection setting that quietly breaks the whole rollout.

> **The short version:** Create a CloudConnexa network and install a connector on a server inside it. Switch authentication to SAML and register CloudConnexa as an Entra ID enterprise app, mapping the group claim so access follows group membership. Install OpenVPN Connect with `winget` for a single machine, or for a fleet deploy it as two Intune Win32 apps: the MSI in system context, then a user-context script that pre-fills the Cloud ID. Offboarding then becomes one move at the identity layer.
{: .prompt-tip }

## Why this instead of a classic VPN

A classic VPN drops you onto the office network and trusts you with everything on it. The model here is a doorman: it checks who you are at the entrance, walks you to exactly the resource you are allowed to reach, and writes down that you went there. Identity at the front, access scoped to one thing instead of the whole network, and a log of it. That is what people mean by zero-trust access.

The tool is CloudConnexa. Yes, it is from OpenVPN, the same name behind the open-source protocol, but CloudConnexa is a different product: a cloud-managed access service, not a point-to-point tunnel. Keeping remote access identity-bound, segmented, and logged maps directly onto the NIS2 risk-management measures around access control and secured communications.

![CloudConnexa pricing tiers, free versus Essential](/assets/img/posts/cloudconnexa-intune/01-pricing.jpg)
_The free tier is genuinely complete for one person. The SAML and team features in this guide need Essential._

## Step 1: Create your network

A network in CloudConnexa is the private side you want people to reach: your lab, an office subnet, whatever sits behind the connector. Open the Networks section, add a network, give it a name and region, and define the subnet or route it should serve.

![Creating a network in the CloudConnexa admin portal](/assets/img/posts/cloudconnexa-intune/03-networks.jpg)

## Step 2: Install the connector

The connector is the piece that links CloudConnexa to that private network. CloudConnexa generates a deployment command for you, and you paste it into a terminal on a server that already has access to the network. I run it on a Linux box: copy the command from the Connectors page, run it, and it pulls down and starts the connector service.

![Installing the CloudConnexa connector from the command line](/assets/img/posts/cloudconnexa-intune/04-connector-cli.jpg)

Wait for the connector to report online in the portal before moving on. If it never comes up, it is almost always that the host cannot reach the subnet you told CloudConnexa it serves, or outbound 443 is blocked from that box.

## Step 3: Turn on SAML single sign-on

Go to Settings, then User Authentication. By default CloudConnexa uses its own username and password. Switch on SAML (Single Sign-On). This is the change that ties access to your company directory instead of a hand-maintained user list.

![CloudConnexa User Authentication set to SAML](/assets/img/posts/cloudconnexa-intune/05-user-auth-saml.jpg)

## Step 4: Register CloudConnexa in Microsoft Entra ID

In the Microsoft Entra admin center go to Enterprise applications, then New application, then browse the gallery. Register CloudConnexa as the application Entra hands identities to, then open its Single sign-on settings and choose SAML.

![Browsing the Microsoft Entra app gallery](/assets/img/posts/cloudconnexa-intune/06-entra-app-gallery.jpg)

Entra asks for the identifier and reply URL from CloudConnexa, and hands you back its own metadata: the login URL, the Entra identifier, and a signing certificate. Keep that tab open.

## Step 5: Configure and map the SAML connection

Back in CloudConnexa's SAML configuration, paste the identity-provider details from Entra: the sign-on URL, the issuer or entity ID, and the signing certificate.

![SAML configuration in CloudConnexa](/assets/img/posts/cloudconnexa-intune/07-saml-config.jpg)

Then set the attribute mapping. This tells CloudConnexa which claims from Entra map to email, first name, last name, and the one that does the real work, group membership. Map the group claim and access follows an Entra security group: put someone in the group and they get the access that group allows, automatically.

![SAML attribute and group mapping](/assets/img/posts/cloudconnexa-intune/08-attribute-mapping.jpg)

## The blocker everyone hits: the first SSO test fails

Here is the part most guides skip. The first sign-in test will very likely fail, and the error is deliberately vague.

![CloudConnexa Single Sign-On Error after a failed SAML test](/assets/img/posts/cloudconnexa-intune/09-sso-error.jpg)
_"Request validation failed." Almost always a mismatch in the SAML config, not a deeper problem._

When you see "Single Sign-On Error, we cannot authenticate you because of an issue with the SSO provider," do not start ripping things out. Use the "Copy Details to Clipboard" link on that error, then check three things, in order: the reply URL in Entra matches the assertion consumer URL CloudConnexa expects, the identifier or entity ID is identical on both sides (a trailing slash counts), and the attribute CloudConnexa reads for the username actually exists in the Entra claim. In my build it was the reply URL. Fix the mismatch, hit "Try To Sign In Again," and you are through.

![Signed in and connected through SSO](/assets/img/posts/cloudconnexa-intune/10-sso-signin.jpg)
_The payoff: authenticated against Entra and connected._

## Step 6: Install the client (one machine)

On a single machine, the fastest route is `winget`. Open an elevated terminal and run:

```powershell
winget install OpenVPNTechnologies.OpenVPNConnect
```
{: file="PowerShell (Administrator)" }

Launch it, import the connection profile, sign in, done. For one box that is the whole story. The rest of this post is about doing it for fifty boxes without touching any of them.

## Step 7: Deploy to a fleet with Intune, Cloud ID pre-filled

This is the section worth bookmarking, because the official guidance leaves out the part that actually bites.

You want users to install the app, open it, and connect, with no server URL to type and no Cloud ID to paste out of an email. The catch that shapes the entire design: the MSI installs the app machine-wide, in SYSTEM context, but the URL pre-fill is a per-user app setting that has to be applied in the logged-in user's context. You cannot do both in one app. So this is a two-app deployment, with the config app depending on the install app.

Three small scripts do it. One does the work, two are Intune detection rules. Grab them here:

- [Apply-OpenVPNConfig.ps1](/assets/scripts/Apply-OpenVPNConfig.ps1) - generates the config, accepts GDPR, applies it, drops a detection marker
- [Detect-OpenVPNConnect.ps1](/assets/scripts/Detect-OpenVPNConnect.ps1) - detection rule for the MSI (App 1)
- [Detect-OpenVPNConfig.ps1](/assets/scripts/Detect-OpenVPNConfig.ps1) - detection rule for the config (App 2)

### App 1: the MSI (system context)

Wrap the OpenVPN Connect MSI with the [Win32 Content Prep Tool](https://github.com/microsoft/Microsoft-Win32-Content-Prep-Tool):

```text
IntuneWinAppUtil.exe -c "C:\Packaging\OpenVPNConnect" -s "OpenVPN-Connect.msi" -o "C:\Packaging\Output"
```

Then in the admin center go to **Apps > Windows > Add > Windows app (Win32)** and upload the `.intunewin`. Intune reads the MSI and pre-fills most fields. I make the install fully silent:

| Field | Value |
| --- | --- |
| Install command | `msiexec /i "OpenVPN-Connect.msi" /qn /norestart` |
| Uninstall command | `msiexec /x "{product-code}" /qn /norestart` (auto-filled) |
| Install behavior | **System** |
| Detection | MSI product code, or `Detect-OpenVPNConnect.ps1` for a minimum version |
| Requirements | Windows 64-bit |

![Adding the OpenVPN Connect Win32 app in Intune](/assets/img/posts/cloudconnexa-intune/11-intune-add-app.jpg)

### App 2: the config (user context)

App 2 carries only the apply script. The config file is generated at runtime, so nothing else is bundled. Wrap the script the same way, add a second Win32 app, and this is where your Cloud ID goes, on the install command line:

| Field | Value |
| --- | --- |
| Install command | `powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "Apply-OpenVPNConfig.ps1" -Url https://yourID.openvpn.com -CloseWhenDone` |
| Uninstall command | `cmd /c del "%LOCALAPPDATA%\OpenVPN Connect\ocfg-applied.tag"` |
| Install behavior | **User** |
| Detection | Custom script: `Detect-OpenVPNConfig.ps1` |

Before you upload the detection script, open it and set `$expectedUrl` to the same URL you put on the install command line. Detection scripts cannot take parameters, so that one value lives in two places. Keep them in sync or App 2 loops trying to reinstall.

### The dependency is what enforces order

On **App 2**, open **Dependencies**, add **App 1** with **Automatically install** enabled. Now the MSI always lands before the config tries to apply, and assigning App 2 to a group pulls App 1 along with it.

> **The setting that silently breaks everything:** on any PowerShell detection script, leave **Run script as 32-bit process on 64-bit clients** set to **No**. Flip it to Yes and WOW64 redirection points the 64-bit `Program Files` lookup at the x86 path, so a perfectly good install reads as missing and Intune reinstalls forever. This is the single most common reason these deployments fail, and nothing in the UI warns you.
{: .prompt-warning }

### The success dialog, and the honest workaround

OpenVPN Connect has no real headless mode yet, so applying a config pops an informational "App configuration was successfully applied" dialog with no supported flag to suppress it. The `-CloseWhenDone` switch is the workaround: the config is already saved by the time the dialog appears, so quitting the app tears the dialog down with it. Worst case a user sees a brief flash, and only if they happen to be looking at the screen mid-sync.

### The pro check: confirm it, do not assume it

Do not trust "I assigned it." On a test machine after the sync, confirm the marker file exists at `%LOCALAPPDATA%\OpenVPN Connect\ocfg-applied.tag` and that its contents match your URL, open OpenVPN Connect and check the Cloud ID is pre-filled, and confirm both apps report **Installed** in Intune.

![Intune app install status for OpenVPN Connect](/assets/img/posts/cloudconnexa-intune/12-intune-install-result.jpg)
_An assignment that has not landed yet shows no device data. Wait for the real "Installed" before you call it done._

When something misbehaves, the logs are in `C:\ProgramData\Microsoft\IntuneManagementExtension\Logs\`. `IntuneManagementExtension.log` covers app processing; `AgentExecutor.log` covers the script runs.

## The apply script, in full

Generating the config JSON at runtime means PowerShell handles the escaping, which sidesteps the backslash trap in OpenVPN's own documented example. Write the file as UTF-8 with no BOM, because a leading BOM trips the config parser.

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Url,
    [hashtable]$Settings,
    [int]$LaunchWaitSeconds = 8,
    [switch]$CloseWhenDone
)

$ErrorActionPreference = 'Stop'

# Normalise the URL
$Url = $Url.Trim().TrimEnd('/')
if ($Url -notmatch '^[a-zA-Z][a-zA-Z0-9+.-]*://') { $Url = "https://$Url" }

# Locate the OpenVPN Connect binary
$connect = @(
    "$env:ProgramFiles\OpenVPN Connect\OpenVPNConnect.exe",
    "${env:ProgramFiles(x86)}\OpenVPN Connect\OpenVPNConnect.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $connect) {
    throw "OpenVPN Connect not found. Install the MSI before running this script."
}

# Build the .ocfg (JSON generation handles escaping)
$config = [ordered]@{ "import-url" = $Url }
if ($Settings) { $config["settings"] = $Settings }

$json     = $config | ConvertTo-Json -Depth 5
$ocfgPath = Join-Path $env:TEMP ("openvpn-connect-{0}.ocfg" -f ([guid]::NewGuid().ToString('N')))

# UTF-8 with NO BOM. A leading BOM trips the config parser.
[System.IO.File]::WriteAllText($ocfgPath, $json, (New-Object System.Text.UTF8Encoding $false))

try {
    Start-Process -FilePath $connect `
        -ArgumentList '--accept-gdpr', '--skip-startup-dialogs', '--minimize' `
        -WindowStyle Hidden
    Start-Sleep -Seconds $LaunchWaitSeconds

    $output = & $connect "--import-config=$ocfgPath" 2>&1 | Out-String
    Write-Verbose $output

    if ($output -notmatch '"status"\s*:\s*"success"') {
        throw "Config import did not report success. Output: $output"
    }

    if ($CloseWhenDone) {
        Start-Sleep -Seconds 2
        & $connect '--quit' 2>&1 | Out-Null
    }
}
finally {
    Remove-Item $ocfgPath -ErrorAction SilentlyContinue
}

# Marker for Intune detection (stores the URL so you can re-detect)
$tagDir = Join-Path $env:LOCALAPPDATA "OpenVPN Connect"
New-Item -Path $tagDir -ItemType Directory -Force | Out-Null
Set-Content -Path (Join-Path $tagDir "ocfg-applied.tag") -Value $Url -Encoding UTF8

Write-Output "Applied import URL: $Url"
```
{: file="Apply-OpenVPNConfig.ps1" }

To change the Cloud ID later, update it in two places: the `-Url` on App 2's install command and `$expectedUrl` in its detection script. On the next sync the device sees the old value in the tag, fails detection, re-runs App 2, and the new URL is written. Clean re-push, no manual cleanup. `[VERIFY: OpenVPN Connect CLI flags (--import-config, --accept-gdpr, --quit) and that CLI support is 3.3+ on the build you deploy]`

## See the whole thing

Back in CloudConnexa, the network view lays out the connector, the network, and the connected devices together. This is your confirmation that traffic flows the way you intended and access is scoped, not wide open.

![CloudConnexa network topology view](/assets/img/posts/cloudconnexa-intune/13-network-topology.jpg)

This build pairs naturally with a properly run Microsoft 365 tenant, since the offboarding only works if the identity side is solid. If you have not done that groundwork, see the M365-as-MSP tenant build `[SLOT: internal link to the existing "Set Up M365 Like an MSP" post]`, and the connector here runs happily on the home server from the Proxmox build `[SLOT: internal link to the existing Proxmox home-server post]`.

## FAQ

**Is the CloudConnexa free tier enough for me?**
If you are a solo operator, a freelancer, or running a homelab, yes. The free tier is a real product, not a trial that expires. You grow into the paid tier the day you add people, because that is when offboarding has to be one clean move and survive an audit. `[VERIFY: current free-tier limits]`

**Why two Intune apps instead of one?**
Because the MSI installs machine-wide in SYSTEM context, but pre-filling the Cloud ID is a per-user setting applied in the user's context. One app cannot run in both. App 2 (user context) depends on App 1 (system context) so the order is enforced.

**My Intune app reinstalls on every sync. Why?**
Two usual causes. Either the detection script is running as 32-bit (set "Run script as 32-bit process on 64-bit clients" to No), or the `-Url` on App 2 and `$expectedUrl` in its detection script do not match after normalisation, usually a stray trailing slash or a missing scheme.

**Why does the first SAML sign-in fail?**
Almost always a config mismatch, not a real fault. Check the reply URL, the identifier or entity ID, and the username attribute on both the Entra and CloudConnexa sides. Use "Copy Details to Clipboard" on the error to see exactly what failed.

**Does this make me NIS2 compliant?**
It covers access control, multi-factor, secured transport, and the logging that supports incident handling. It does not back up your data, manage vulnerabilities, train your staff, or govern encryption policy, so do not treat it as NIS2 in a box.

## Recap

You built identity-driven, segmented remote access: a CloudConnexa network with a connector inside it, sign-in tied to Entra ID over SAML with access following group membership, and the OpenVPN Connect client deployed to a Windows fleet through Intune with the Cloud ID pre-filled and confirmed. The day someone leaves, you pull them from the Entra group and access closes everywhere at once, with a log to prove it.


> **Make it a skill, not a one-off.** I built a free, no-signup learning path on Mylemans Labs that walks you through securing remote access for a small environment in the right order. Start here: [Mylemans Labs remote-access path](https://labs.mylemans.online)
{: .prompt-info }
