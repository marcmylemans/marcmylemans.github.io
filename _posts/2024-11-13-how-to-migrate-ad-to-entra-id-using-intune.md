---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "How to Migrating from On-Premise Active Directory to Entra ID with Intune"
date: 2024-11-13
categories: [Cloud Computing, Endpoint Management]
tags: [Entra ID, Azure AD, Microsoft Intune, Active Directory Migration, Autopilot, Group Policy Migration, Device Enrollment, Company Portal, Application Deployment, Remote Work, Cloud Kerberos Trust, Windows Hello, OneDrive, Microsoft Edge, Modern Workplace, MDM]
---

# Guide to Setting Up Autopilot and Migrating to Entra ID with Intune

## 1. Creating an Autopilot Profile

Windows Autopilot streamlines the setup of new devices, allowing users to get up and running with minimal IT intervention.

### Step 1: Create a Dynamic Security Group

To automatically group Autopilot devices:

1. Navigate to the Azure portal and select **Azure Active Directory > Groups > New Group**.
2. Set the following:
   - **Group Type:** Security  
   - **Group Name:** `SG_AutoPilotDevices`  
   - **Membership Type:** Dynamic Device  
3. Under **Dynamic device members**, enter the following rule:

    ```plaintext
    (device.devicePhysicalIDs -any (_ -startsWith "[ZTDId]"))
    ```

   This rule ensures all Autopilot devices are automatically added to the group.

### Step 2: Create an Autopilot Deployment Profile

1. In Intune, go to **Devices > Windows > Windows enrollment > Deployment Profiles**.
2. Click **+ Create profile** and select **Windows PC**.
3. Configure the profile:
   - **Name:** `Autopilot`  
   - **Convert all targeted devices to Autopilot:** Yes  
   - **Deployment mode:** User-Driven  
   - **Join to Azure AD as:** Azure AD joined  
   - **User account type:** Standard  
   - **Language (Region):** Operating system default  
   - **Automatically configure keyboard:** No  
4. Assign the profile to **All Devices**.
5. Click **Create**.

> **Note:** The device conversion process can take up to 48 hours. To expedite, you can manually register devices using the `Get-WindowsAutopilotInfo.ps1 -Online` script.

---

## 2. Migrating Group Policies to Entra ID

Migrating your Group Policy Objects (GPOs) to Intune allows for centralized management and supports devices that are not connected to the corporate network.

### Step 1: Export Group Policy

1. Open **Group Policy Management Console** on your domain controller.
2. Right-click the desired GPO and select **Save Report**.
3. Save the report as an **XML** file.

### Step 2: Import into Intune

1. In Intune, navigate to **Devices > Group Policy analytics (preview)**.
2. Click **Import** and select the XML file.
3. Once analyzed, you'll see a compatibility report.
4. Select the policy and click **Migrate** to create an equivalent Intune policy.

### Step 3: Assign the Policy

1. Assign the new policy to the `SG_AutoPilotDevices` group.
2. Review and modify settings as necessary.

---

## 3. Configuring Applications in Intune

Deploy essential applications to devices to ensure users have the tools they need.

### Deploying Company Portal

The Company Portal app allows users to install available applications and manage their devices.

1. In Intune, go to **Apps > Windows > + Add**.
2. Select **Microsoft Store app (new)**.
3. Search for **Company Portal** and select it.
4. Configure the app information as needed.
5. Under **Assignments**, set it as **Required** for the appropriate user or device groups.
6. Click **Next** and then **Create**.

### Deploying Other Applications

Repeat the steps above to deploy:

- **Microsoft Office**
- **Microsoft Edge**

For applications that users can choose to install:

1. Set **Assignment** to **Available for enrolled devices**.
2. Assign to the relevant user groups.

---

## 4. Migrating Users to Entra ID Devices

When moving users to new devices:

1. **Inventory Applications:** Ensure all required applications are available in Intune.
2. **Backup Data:** Use OneDrive to back up user data from Desktop, Documents, and Pictures.
3. **Browser Settings:** Import bookmarks and settings to Microsoft Edge and enable synchronization.
4. **Assign User to Device:** Use Autopilot to assign the user to the new device.

### Device Setup Process

1. Connect the device to the internet via Ethernet or configure Wi-Fi during setup.
2. The user signs in with their work account.
3. **Windows Hello** is configured (PIN, fingerprint, or facial recognition).
4. Device setup completes with policies and applications applied automatically.

---

## Conclusion

Migrating from an on-premise Active Directory environment to Entra ID using Intune enhances flexibility, security, and user experience. With this setup, users can work remotely without relying on VPNs for policy updates or application installations.

For any questions or further assistance, feel free to leave a comment below. Don't forget to subscribe for more guides on modernizing your IT infrastructure.
