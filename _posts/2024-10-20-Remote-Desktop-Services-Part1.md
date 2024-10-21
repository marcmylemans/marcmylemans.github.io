---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "A Step-by-Step Guide - Setting Up Remote Desktop Services with Windows Server 2022"
date: 2024-10-20
categories: [Windows Server, Remote Desktop Services]
tags: [windows server 2022, remote desktop services, rds, active directory, group policy, fslogix, single sign-on, sso, certificate services, let's encrypt, server manager, rds licensing]
---


**Welcome to this comprehensive guide** on setting up Remote Desktop Services (RDS) using Windows Server 2022! Whether you're managing a small business or setting up a lab environment, this tutorial will walk you through the entire process of creating a scalable, secure RDS environment that supports multiple users. By the end, you'll have everything configured for remote access, complete with security features and user-friendly interfaces.

---

## Prerequisites

Before we dive into the technical details, it's important to make sure you have the following prerequisites in place:

1. **A Domain Controller**: Ensure that Active Directory (**DC1**) is up and running. If you're not familiar with this, check out our video on [Setting up Active Directory on Server 2022]({% link _posts/2024-09-17-SettingUpActiveDirectoryServer2022.md %}).
2. **Group Policy Knowledge**: Familiarity with Group Policy is essential for this setup. We have a video on [Group Policy Essentials and Best Practices]({% link _posts/2024-09-17-GroupPolicyBestPracticesServer2022.md %}) that you can watch for more insights.
3. **Two (Virtual) Machines**: 
   - **RDS1**: Will serve as the Remote Desktop Session Host.
   - **RDGW**: Will handle the Remote Desktop Connection Broker, Web Access, Licensing, and Gateway roles.
4. **Static IP Addresses** for both VMs.
5. A Fileserver (**DC1**): Required for storing FSLogix.
6. **Public Domain Name**: Required for external access. We'll use Let's Encrypt for generating SSL certificates.
7. **Port Forwarding**: Ensure your router is configured to forward ports **80** and **443** to your environment.

For related setup videos, check out the links in the description!

---

## Part 1: Installing and Configuring Active Directory Certificate Services (AD CS)

Setting up a Certificate Authority (CA) is critical for securing your RDS environment. Here's how to install and configure AD CS.

### Step 1: Installing AD CS

1. Open **Server Manager** and select **Add Roles and Features**.
2. Choose **Active Directory Certificate Services**, and follow the setup wizard.
3. Select **Certification Authority (CA)** and complete the installation.

### Step 2: Configuring the Certificate Authority

1. Once installation is complete, select **Configure Active Directory Certificate Services**.
2. Choose **Enterprise CA** and **Root CA** during setup.
3. Set the validity period for the CA to **5 years**.
4. Complete the setup wizard.

### Step 3: Configuring Group Policies for CA

1. In **Group Policy Management**, edit the `Default Domain Policy`.
2. Navigate to: `Computer Configuration > Policies > Windows Settings > Security Settings > Public Key Policies`.
3. Enable **Certificate Services Client - Auto Enrollment** with the following options:
   - `Renew expired certificates`
   - `Update certificates that use certificate templates`
4. Repeat the process under the **User Configuration** path.
5. Navigate to: `User Configuration > Policies > Windows Settings > Security Settings > Public Key Policies`.
6. Enable **Certificate Services Client - Auto Enrollment** with the following options:
   - `Renew expired certificates`
   - `Update certificates that use certificate templates`

---

## Part 2: Installing Remote Desktop Services (RDS)

### Step 1: Adding Servers to Server Manager

1. Open **Server Manager** from the Start menu or taskbar.
2. In the left-hand pane, right-click **All Servers** and select **Add Servers**.
3. In the **Active Directory** dialog box, click **Find Now** to display a list of available servers.
4. Select the servers **RDGW** (Remote Desktop Gateway) and **RDS1** (Remote Desktop Session Host) from the list, and click **Add**.
5. Click **OK** to close the dialog box.

With both servers added to Server Manager, you’re now ready to install and configure the core RDS roles.

### Step 2: Installing RDS Roles

1. Open **Server Manager** again, and click **Add Roles and Features** from the Dashboard.
2. In the wizard, choose **Remote Desktop Services Installation** and click **Next**.
3. Select **Standard Deployment** and choose **Session-based desktop deployment** for a virtual desktop infrastructure (VDI).
4. Assign the RDS roles as follows:
   - **Connection Broker**: Assign to **RDGW** – The Connection Broker manages session connections and ensures load balancing.
   - **Web Access**: Assign to **RDGW** – This role enables users to access RemoteApp and desktop resources via a web browser.
   - **Session Host**: Assign to **RDS1** – This is the server that hosts the Remote Desktop sessions for users.

After assigning the roles, proceed with the installation and configure any additional settings as needed.


### Step 3: Configuring RDS Certificates

To secure Remote Desktop Services (RDS) traffic, you'll need an SSL certificate. Follow these steps to set it up using **[Certify The Web](https://certifytheweb.com/)**:

1. Download and install **Certify The Web** on your server.
2. Request a certificate for your **public DNS name** and apply it to **IIS**.
3. Export the certificate and import it into **Server Manager** under **Remote Desktop Services > Edit Deployment Properties**.
4. Assign the certificate to the following RDS roles:
   - **Connection Broker**: *(If you have set up your CA correctly and enabled Certificate Services Client - Auto Enrollment, you don't need to assign a certificate here manually.)*
   - **Web Access**
   - **Gateway**

By following these steps, you’ll ensure that SSL encryption is applied to your RDS environment, securing communication between the servers and clients.


### Step 4: Configuring Remote Desktop Licensing

1. Open **Edit Deployment Properties** in **Server Manager**.
2. Navigate to **RD Licensing** and select **Per User** mode for licensing.

---

## Part 3: Configuring FSLogix for User Profiles

FSLogix optimizes user profile management in RDS environments, offering faster logins and smoother session experiences.

### Step 1: Downloading and Installing FSLogix

1. Download the latest version of **[FSLogix](https://aka.ms/fslogix-latest)** from Microsoft's website.
2. Install FSLogix on each Remote Desktop Session Host server.

### Step 2: Configuring FSLogix Profiles

To properly store and manage user profiles in a Remote Desktop Services environment, you’ll use **FSLogix** for handling profiles and Office 365 data. Here’s how to set it up:

### 1. Create Shared Folders for Profiles and Containers
1. Create two shared folders to store user profiles and containers:
   - `\\DC1\FSLogix_Profiles`
   - `\\DC1\FSLogix_Containers`
2. Set appropriate folder permissions to ensure secure access for users and the system.

### Folder Permissions Setup

Here’s the recommended permission configuration for the profile folder (`FSLogix_Profiles`), which will ensure proper access for users and administrators:

| Principal               | Access                  | Applies to                      | Description                                                                                                                                  |
|-------------------------|-------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **CREATOR OWNER**        | Modify (Read / Write)   | Subfolders and files only        | Ensures the profile directory created by the user has the correct permissions, granting exclusive access to the user who owns the folder.      |
| **CONTOSO\Domain Admins**| Full Control            | This folder, subfolders, and files| Administrative group with full control over the folder and its contents. Replace with your organization's administrative group.               |
| **CONTOSO\Domain Users** | Modify (Read / Write)   | This folder only                 | Allows authorized users to create their profile directory at the top-level folder. Replace with the group that contains the users needing access.|

> Replace `CONTOSO` with your organization's domain name as necessary.

These permissions ensure that:
- Each user has exclusive access to their own profile folder (via **CREATOR OWNER** permissions).
- Admins can manage all profiles with **Full Control**.
- Regular users can create their profile folder but cannot modify or delete other users' profiles.

---

### 2. Configure FSLogix Group Policies

You will configure FSLogix settings through Group Policy to manage the profile and Office 365 containers.
Locate the two files (fslogix.admx and fslogix.adml) and copy them to a location based on a local or central store configuration.

Navigate to `Computer Configuration > Administrative Templates > FSLogix` for each of the following settings:

#### Office 365 Containers
**Enabled**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include Office cache data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include OneDrive data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include OneNote data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include Outlook data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include Outlook personalization data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include Skype data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Include Teams data in container**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**Set Outlook cached mode on successful container attach**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**

**VHD location**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**  
   - Value: `\\test.lan\DFS\O365Containers$`

**Virtual disk type**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Office 365 Containers`  
   - State: **Enabled**  
   - Value: **VHDX**

#### Profile Containers
**Delete local profile when FSLogix Profile should apply**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Profile Containers`  
   - State: **Enabled**

**Enabled**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Profile Containers`  
   - State: **Enabled**

**Set Outlook cached mode on successful container attach**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Profile Containers`  
   - State: **Enabled**

**VHD location**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Profile Containers`  
   - State: **Enabled**  
   - Value: `\\test.lan\DFS\ProfileContainers$`

**Virtual disk type**  
   - Navigate to: `Computer Configuration > Administrative Templates > FSLogix > Profile Containers > Container and Directory Naming`  
   - State: **Enabled**  
   - Value: **VHDX**

---

## Part 4: Setting Up Single Sign-On (SSO)

Single Sign-On (SSO) enhances the user experience by allowing users to sign in once and access multiple services seamlessly.

### Step 1: Configuring SSO Policies

1. Create a new Group Policy called `Computer Policy - Enable RDP SSO`.
2. Enable:
   - `Allow delegating default credentials` under `Administrative Templates > System > Credentials Delegation`.
   - Set the policy to use: `TERMSRV/*.domain.local`.
3. Create another Group Policy called `User Policy - Enable RD Gateway SSO`.
4. In this policy, configure:
   - **RD Gateway Authentication Method** to use **locally logged-on credentials**.

### Step 2: Configuring Web Feed for RemoteApp Connections

1. Create a new Group Policy named `User Policy - Enable RDP Webfeed`.
2. Set the **default connection URL** to your RDS Web Access feed:
   - Example: `https://yourdnsrecord/rdweb/feed/webfeed.aspx`.

---

## Conclusion

Congratulations! 🎉 You've successfully set up a complete Remote Desktop Services environment using Windows Server 2022. With SSL certificates for secure access, FSLogix for user profile management, and Single Sign-On for a seamless user experience, your RDS setup is now fully operational and ready to support multiple users.

This setup can easily scale for larger environments or remain efficient for small businesses. Be sure to check out the video links in the description for more detailed configurations, and don't hesitate to leave comments or questions below!
