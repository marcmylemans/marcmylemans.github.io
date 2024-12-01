---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "Simplifying MFA Setup for Remote Desktop Gateway with Microsoft Entra ID"
date: 2024-12-01
categories: [Remote Desktop Services, Security]
tags: [Multi-Factor Authentication, MFA, Microsoft Entra ID, Azure Active Directory, NPS Extension, Remote Desktop Gateway, RD Gateway, Network Policy Server, NPS, RADIUS, Step-by-Step Guide, Remote Access, Secure Remote Access, Authentication, IT Infrastructure, Windows Server, Azure MFA]
---


## Simplify Your Remote Work Security: Set Up MFA for RD Gateway with Microsoft Entra ID

Securing remote work access doesn't have to be complicated. Multi-Factor Authentication (MFA) is one of the most effective ways to protect your Remote Desktop Gateway (RD Gateway). This guide will walk you through how to integrate Microsoft Entra ID (formerly Azure Active Directory) with RD Gateway using the Network Policy Server (NPS) extension. No jargon—just clear steps to get you up and running with confidence.

---

### Why This Matters  

In a world of remote work, safeguarding sensitive company data is crucial. By adding MFA to your RD Gateway, you add an essential extra layer of defense. This setup not only protects against unauthorized access but also enhances trust within your IT ecosystem.

Here’s what you’ll achieve by the end of this guide:

- **MFA-Enabled RD Gateway:** More secure remote connections.
- **Optimized NPS Configuration:** Seamless MFA integration.
- **Peace of Mind:** A safer remote access experience for users and administrators.

---

### Ready to Get Started?  

Before diving in, make sure you have:

1. **An RD Gateway Server:** Installed and operational.  
2. **Microsoft Entra ID:** With user accounts synced via Azure AD Connect.  
3. **Microsoft Entra P1 or P2 License:** Required for MFA functionality.  
4. **NPS Role:** Installed on a domain member server or controller.  
5. **Administrator Access:** To configure server settings and Microsoft Entra ID.  

---

### Step 1: Prepping Your Environment  

#### 1. Install the NPS Role  
1. Open **Server Manager** on your NPS-designated server.  
2. Select **Add roles and features** and proceed to **Server Roles**.  
3. Check **Network Policy and Access Services**, then complete the wizard.  

#### 2. Sync Users with Microsoft Entra ID  
Ensure your on-premises Active Directory users are synced with Microsoft Entra ID using **Azure AD Connect**. This allows seamless integration of existing accounts.  

---

### Step 2: Setting Up MFA in Microsoft Entra ID  

#### 1. Enable MFA for Users  
1. Log in to the [Microsoft Entra admin center](https://entra.microsoft.com).  
2. Navigate to **Users** > **All Users**, then select the desired accounts.  
3. Click **Multi-Factor Authentication** and enable MFA for selected users.  

#### 2. Guide Users to Register for MFA  
1. Have users visit [https://aka.ms/mfasetup](https://aka.ms/mfasetup).  
2. Walk them through setting up their preferred MFA method (e.g., the Microsoft Authenticator app).

> **Important:**
> The sign-in behavior for Remote Desktop Gateway doesn't provide the option to enter a verification code with Microsoft Entra multifactor authentication. Users must be configured for phone verification or the Microsoft Authenticator App with **Approve**/**Deny** push notifications.
>
> - If neither phone verification nor the Microsoft Authenticator App with **Approve**/**Deny** push notifications is configured for a user, they won't be able to complete the Microsoft Entra multifactor authentication challenge and sign in to Remote Desktop Gateway.
> - The SMS text method doesn't work with Remote Desktop Gateway because it doesn't provide the option to enter a verification code.


---

### Step 3: Installing the NPS Extension  

#### 1. Download & Install  
- Download the NPS extension for Microsoft Entra ID [here](https://aka.ms/npsmfa).  
- Run the installer on your NPS server and follow the prompts.  

#### 2. Configure the Extension  
1. Open **PowerShell** as an administrator.  
2. Navigate to the config folder:  
   ```powershell
   cd "C:\Program Files\Microsoft\AzureMfa\Config"
   ```
 3. Run the setup script:
   ```powershell
   .\AzureMfaNpsExtnConfigSetup.ps1
   ```
 4. When prompted, sign in with your Microsoft Entra ID admin credentials.
 5. Enter your Tenant ID when prompted (you can find this in the Microsoft Entra admin center under Azure Active Directory > Properties > Tenant ID).


---

### Step 4: Linking RD Gateway with NPS  

#### 1. Enable NPS on RD Gateway  
1. In **Remote Desktop Gateway Manager**, open **Properties** for your server.  
2. Under **RD CAP Store**, select **Central server running NPS**.  
3. Add your NPS server’s name or IP address, along with a shared secret.  

#### 2. Adjust Timeout Settings  
1. Open **Network Policy Server** on your RD Gateway server.  
2. Expand **RADIUS Clients and Servers** > **Remote RADIUS Server Groups**.  
3. Double-click **TS GATEWAY SERVER GROUP**.  
4. Edit the entry for your NPS server.  
5. On the **Load Balancing** tab, set the **Response timeout** to **30 seconds**.  
6. Set the **Unresponsive timeout** to **30 seconds** or more for stability.  

---

### Step 5: Testing Your Setup  

#### 1. Simulate a Remote Desktop Connection  
1. On a client machine, open **Remote Desktop Connection**.  
2. Enter your RD Gateway settings:  
   - Go to **Show Options** > **Advanced** > **Settings**.  
   - Configure RD Gateway settings with your server details.  
3. Attempt to connect and follow the MFA prompt (e.g., via the Authenticator app).  

#### 2. Confirm Everything Works  
A successful MFA prompt means your setup is good to go. If not, double-check shared secrets, NPS configurations, and user MFA registration.  

---

### Troubleshooting Like a Pro  

If users are not receiving the MFA prompt or the connection fails during authentication, you may need to adjust the NPS extension settings to support your authentication methods.

**Solution:**

1. On the NPS server, open the **Registry Editor**.
2. Navigate to the following key:
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\AzureMfa
   ```
3. If the `AzureMfa` key doesn't exist, create it.
4. Within the `AzureMfa` key, create a new **String Value** with the following details:
- **Name**: `OVERRIDE_NUMBER_MATCHING_WITH_OTP`
- **Value**: `FALSE`

This configuration disables the number matching feature, which can interfere with certain authentication methods like TOTP codes when used with RD Gateway.

5. Close the Registry Editor.
6. Restart the **Network Policy Server (NPS)** service for the changes to take effect.

**Explanation:**

This registry setting tells the NPS extension not to enforce number matching, which can cause issues with RD Gateway connections if users are registered for certain MFA methods like TOTP codes. Setting the value to `FALSE` allows the NPS extension to fallback to push notifications or phone call methods that are compatible with RD Gateway.

If you run into issues:  
- **Event Logs:** Check **Event Viewer** > **Microsoft** > **AzureMfa** for errors.  
- **Verify MFA Registration:** Ensure users are correctly set up in [https://aka.ms/mfasetup](https://aka.ms/mfasetup).  
- **Network Connectivity:** Confirm RD Gateway can reach your NPS server over the required ports.



---

### Conclusion  

Congrats! You've added a powerful layer of security to your RD Gateway with Microsoft Entra ID. Your organization’s remote access is now safer, and your users can work confidently knowing their data is protected.  

---

### Pro Tips for Continued Success  

- Regularly audit MFA settings and encourage users to update their methods.  
- Monitor logs for any suspicious activity.  
- Explore Conditional Access policies for even greater security.  

---

### Watch the Video Guide  

Need a visual walkthrough? Check out our detailed step-by-step video [here](https://www.youtube.com/watch?v=YourVideoID).  

[![Watch on YouTube](https://img.youtube.com/vi/YourVideoID/0.jpg)](https://www.youtube.com/watch?v=YourVideoID)  

---

We’d love to hear from you! Did this guide help? Drop us a comment or connect with us on social media.  

---

**Secure your future—one step at a time.**
