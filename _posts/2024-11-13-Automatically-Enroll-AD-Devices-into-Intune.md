---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "Automatically Enroll Active Directory Devices into Intune via Group Policy and Deploy Apps with Company Portal"
date: 2024-11-13
categories: [Cloud, Endpoint Management]
tags: [Microsoft Intune, Active Directory, Group Policy, Device Enrollment, Company Portal, Application Deployment, Remote Work, Microsoft 365, Entra ID, Azure AD, Device Management, MDM]
---


Managing devices remotely has become essential for modern workplaces, especially with so many users working from home or in hybrid setups. If you’re looking to streamline device enrollment and make application deployment easy for your users, this guide is for you. We’ll walk through how to automatically enroll Active Directory (AD) devices into **Microsoft Intune** using **Group Policy**, and how to deploy applications via the **Company Portal**.

This setup not only simplifies device management but also gives your users more control, enabling them to install approved applications as needed. Let’s dive in!

## Why Use Intune for Device Management?

Microsoft Intune provides a robust set of tools for managing devices across your organization, allowing you to enforce policies, deploy applications, and ensure compliance—all through a single cloud-based platform. When you enroll AD devices into Intune, you can manage them remotely, apply security configurations, and push software updates without requiring a VPN connection to your corporate network.

## Prerequisites

Before starting, make sure you have the following:

- **Active Directory** on-premises.
- **Entra ID (formerly Azure AD)** connected to your AD environment.
- A **Microsoft Intune** license (Microsoft Business Premium or similar) that includes device management capabilities.
- Basic understanding of **Group Policy** in Windows Server.

Once you have these prerequisites in place, you’re ready to start.

## Step 1: Enable Automatic Enrollment into Intune via Group Policy

First, we’ll use Group Policy to configure automatic enrollment into Intune for your AD-joined devices. This setup will allow devices to connect to Intune whenever they have an internet connection, making management easier even for remote workers.

1. **Open Group Policy Management Console** on your domain controller.
2. Create a new **Group Policy Object (GPO)** and link it to the **Organizational Unit (OU)** containing the devices you want to enroll.
3. Edit the GPO and navigate to: Computer Configuration > Administrative Templates > Windows Components > MDM
4. Enable the policy **Enable automatic MDM enrollment using default Azure AD credentials**.

> **Note:** In some versions, this policy may appear as "Enable automatic MDM enrollment using default Microsoft Entra credentials."

5. Set the policy to **Enabled** and select **User Credential** as the enrollment method.

This Group Policy configuration will create a scheduled task on each targeted machine that attempts to enroll in Intune every 5 minutes. If Multi-Factor Authentication (MFA) is required by your organization, users may see an MFA prompt when enrolling.

## Step 2: Verify Device Enrollment

After configuring the Group Policy, it’s important to verify that devices are enrolling in Intune as expected. Here’s how to check on a client machine:

1. Go to **Start > Settings > Accounts > Access work or school**.
2. Select your **domain account**.
3. Click **Info** and look for MDM enrollment information.

If you see that the device is managed by your organization’s MDM service, enrollment was successful. This setup ensures that your devices are connected to Intune and ready to receive policies and applications.

## Step 3: Deploy the Company Portal App via Intune

The **Company Portal** app is the gateway for users to install and manage applications approved by your organization. Once devices are enrolled in Intune, you can deploy the Company Portal app to make it easy for users to access company resources.

1. Go to the **Microsoft Endpoint Manager Admin Center**: [https://intune.microsoft.com](https://intune.microsoft.com).
2. In the left-hand menu, select **Apps**.
3. Click **Add** and choose **Microsoft Store app (new)** as the app type.
4. In the search bar, type **Company Portal** and select it from the results.

### Assigning the Company Portal App

When configuring the Company Portal app, you’ll have several assignment options:

- **Required**: Installs the app automatically on devices that meet your assignment criteria (e.g., all users, all devices, or specific security groups).
- **Available for enrolled devices**: Makes the app available in the Company Portal, allowing users to install it on demand.
- **Uninstall**: Removes the app if it was previously installed as "Required" or "Available."

For this setup, assign **Company Portal** as **Required** so it installs automatically on all enrolled devices.

## Step 4: Deploy Microsoft 365 and Other Essential Apps

With the Company Portal deployed, you can now push other essential applications, like **Microsoft Office** and **Microsoft Edge**, directly to users' devices.

1. In **Microsoft Endpoint Manager**, go to **Apps** and click **Add**.
2. Select **Microsoft 365 Apps** if you’re deploying Office, and configure it to match your organization’s needs.
3. Assign the app as **Required** for the relevant groups.
4. Repeat similar steps to add **Microsoft Edge** or other necessary apps from the Microsoft Store.

By setting applications as “Required,” they will automatically install on all devices that meet your assignment criteria. This makes it easy to ensure that users have the tools they need, no matter where they’re working from.

## Step 5: Empower Users with Self-Service Application Access

With the Company Portal in place, users now have a self-service option to install approved applications whenever they need them. This approach reduces the burden on your IT team by allowing users to:

- Open the **Company Portal** on their device.
- Browse and install available applications.
- Manage their enrolled devices directly from the app.

This self-service model not only saves time for IT support but also empowers users by giving them control over their work devices.

## Key Benefits of Automatic Intune Enrollment and Company Portal

By automatically enrolling AD devices in Intune and deploying applications through the Company Portal, your organization gains:

- **Simplified Device Management**: Manage all devices and applications from a single cloud-based console, even for remote users.
- **Remote Work Ready**: Devices only need an internet connection to receive policies and updates, eliminating the need for VPN access.
- **Enhanced Security**: Enforce compliance and security policies on all enrolled devices.
- **User Empowerment**: Allow users to install necessary apps themselves, reducing helpdesk requests.

## Conclusion

By following this guide, you’ve successfully configured Group Policy to automatically enroll Active Directory devices in Intune and set up the Company Portal for streamlined application deployment. This setup makes device management easier for your IT team and gives users a smooth experience, especially for those working remotely.

For more advanced configurations, such as setting up conditional access policies or enabling Azure Multi-Factor Authentication, stay tuned for our next posts. 

Got questions? Drop a comment below, and we’ll be happy to help!
