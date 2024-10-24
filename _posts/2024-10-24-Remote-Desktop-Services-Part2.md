---
image: https://mylemans.online/assets/img/posts/a803d385944d.png
layout: post
title: "A Step-by-Step Guide - Installing and Configuring Office on RemoteAPP/Desktop Services"
date: 2024-10-24
categories: [Windows Server, Remote Desktop Services]
tags: [windows server 2022, remote desktop services, rds, microsoft office, group policy, admx, office 365, office deployment tool, remote apps, fslogix]
---

# A Step-by-Step Guide to Installing and Configuring Office on Remote Desktop Services

Hey there! 🎉 Welcome to our follow-up guide on Remote Desktop Services (RDS). If you've already set up your RDS environment with Windows Server 2022 from our previous tutorial, congrats—you've laid a solid foundation! Now, we’re going to make your setup even more productive by installing and configuring Office applications. And hey, we’ll even throw in a few power tips using ADMX files for Group Policy, so you can enhance productivity with minimal manual work. Let’s dive in!

## Prerequisites

Before we get started, make sure you’ve got a working Remote Desktop Services environment. If not, no worries! We’ve got you covered with our [Step-by-Step RDS Guide](https://mylemans.online/posts/Remote-Desktop-Services-Part1/).

### What you need:
- **Group Policy Knowledge**: You’ll need a basic understanding of Group Policy. If you need a quick refresher, check out our [Group Policy Best Practices guide](https://mylemans.online/posts/GroupPolicyBestPracticesServer2022/).
- **(Optional)**: An extra virtual machine (VM) for deploying Remote Apps. I like to call mine **RDS2**.

---

## Part 1: Installing Office on Your Remote Desktop Host Server

First things first, we’ll install Microsoft Office on your remote desktop host. Let’s make sure your users can work remotely without skipping a beat.

### Step 1: Download the Office Deployment Tool

1. Download the **Office Deployment Tool** from the official Microsoft website [here](https://www.microsoft.com/en-us/download/details.aspx?id=49117).
2. Once downloaded, extract the contents to a folder on your server. I suggest using a directory like `c:\temp` for easy access.

### Step 2: Create and Configure Your Office Installation

1. Head over to [config.office.com](https://config.office.com) to create a custom configuration file for your Office installation.
   - Select **Microsoft 365 Apps for Enterprise** (or **Business**, depending on your license).
   - Choose the applications you want to install. Maybe you're a fan of Word and Excel but don’t need PowerPoint—your choice!
   - Don’t forget to add all the languages you need. Office will default to the operating system’s language, but you can install multiple languages and proofing tools.

2. Select **Office Content Delivery Network (CDN)** as your source location. This ensures you’re always installing the latest version. You can also set up a local source as a fallback if bandwidth is an issue.

3. Enable **automatic architecture upgrades** (like from 32-bit to 64-bit). If you’ve still got some 32-bit installations hanging around, this is your chance to upgrade!

4. Under **Licensing and Activation**:
   - Accept the EULA.
   - Make sure to select **Shared Computer Licensing**—crucial for remote desktop environments.

5. Once you’ve tweaked all the settings, **export the configuration**. Save the `.xml` file alongside the Office setup files you downloaded earlier.

### Step 3: Install Office on the RDS Host

Now that we’ve got the configuration ready, let’s get Office installed!

1. Open **Control Panel**, set the view to "Small Icons" (trust me, it makes life easier), and select **Install Applications on Remote Desktop**.
   
2. Navigate to your Office setup file and run the command below, making sure to point it to your configuration file:
   ```bash
   c:\temp\setup.exe /configure c:\temp\yourconfigfile.xml
   ```
3. Wait for the installation to finish, and don’t close the wizard until you’re done!

### Step 4: Add Shortcuts for Users

Since you’re in a multi-user environment, it’s handy to put application shortcuts on the desktop for all users.

1. Navigate to the Start Menu shortcuts, copy them, and drop them in the public desktop folder (%public%\desktop). This way, every user gets easy access, and since they don’t have admin rights, they can’t delete them. 🎉

## Part 2: Configuring Office Using Administrative Templates (ADMX Files)

Time to unlock the real power of Group Policy and ADMX files! This step will help you manage Office settings across all users like a pro.

### Step 1: Download and Set Up ADMX Files

You can grab the latest ADMX files for Office [here](https://www.microsoft.com). Copy these files to your central store or a local folder on your server.

Need a refresher on setting up a central store? Check out our [Group Policy Best Practices guide](https://mylemans.online/posts/GroupPolicyBestPracticesServer2022/).

### Step 2: Configure Policies for Office
Here are a few policies I love configuring to enhance user experience:
- **Disable the First Run Movie**: Let’s skip that awkward “Welcome to Office” video.
   - Path: `User Configuration > Administrative Templates > Microsoft Office 2016 > First Run`
   - Set to **Enabled**.
  
- **Configure Default Office Settings**: For smooth sailing, set default options for Word, Excel, and other Office apps. You can tweak everything from default file locations to user privacy settings.

Create a Group Policy called **User Policy - Office - Default Settings** and go wild. Your users will thank you!

---

## Part 3: Optional - Deploying RemoteApps

If you want to streamline the experience and save server resources, **RemoteApps** might be your jam. Instead of offering full desktops, you can let users access individual applications as if they were installed locally. Here’s how you do it:

1. Open **Server Manager**, right-click **All Servers**, and add **RDS2** (or your chosen VM).
2. Go to **Remote Desktop Services** and create a **Session Collection**. Name it something snazzy like "Remote Applications."
3. Assign a security group (default: **Domain Users**), and make sure to **deselect user profile disks**. We’ll use **FS Logix** instead for profile management.
4. Publish your desired apps through the wizard.

Now your users can access Office (or any other app) directly from their local desktops, without the overhead of a full desktop session. 

---

## Wrapping Up

And there you have it! You’ve now installed and configured Microsoft Office on a Remote Desktop Services host, set up Group Policies using ADMX files, and optionally deployed RemoteApps for a sleek, lightweight user experience.

If you’re looking for more tips, tricks, or need help troubleshooting, check out our other [guides](https://mylemans.online/posts) or drop us a comment below. We’re here to help!

Happy configuring!