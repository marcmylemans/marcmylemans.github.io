---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "Dynamic User Language Switching in Active Directory Using PowerShell"
date: 2024-10-25
categories: [Active Directory, PowerShell]
tags: [active directory, powerShell, group policy, automation, language settings]
---

Managing language preferences in a diverse organization is more than just a nice-to-have; it’s about creating an efficient and user-friendly environment. In this post, we’ll dive into how to automatically apply language settings for users in Active Directory (AD) based on their preferences using PowerShell. This solution saves time, minimizes errors, and ensures each user interacts with Windows in their preferred language.
Imagine a workplace with employees who speak different languages—some prefer English, others French or Dutch. Configuring language settings for each person individually? That’s tedious and prone to mistakes. Instead, we can automate this process using Active Directory attributes and Group Policy Objects (GPOs). By letting a PowerShell script handle the heavy lifting, we ensure everyone gets the right settings consistently and with minimal effort from IT.
Ready to simplify your admin life? Let’s break it down.


## Prerequisites

Before we jump into the fun part, here’s what you’ll need:

- **Active Directory Environment**: A working AD setup with user accounts.
- **Group Policy Management**: Three GPOs tailored to French (FR), English (EN), and Dutch (NL) language settings.
- **Security Groups**: You’ll need three security groups, each corresponding to a language policy:
  - `User Policy Language FR`
  - `User Policy Language EN`
  - `User Policy Language NL`
- **PowerShell Access**: You’ll be running a PowerShell script on your AD server.


## Creating Language-Specific GPOs in Active Directory

In a multilingual organization, managing user preferences for regional and language settings can be streamlined by creating dedicated GPOs for each language. This setup allows users to interact with their Windows environment in their preferred language, enhancing productivity and comfort. Here’s how to create GPOs for **English (EN)**, **Dutch (NL)**, and **French (FR)** in Active Directory.

### Step 1: Open Group Policy Management Console

1. **Log into your domain controller** with an account that has permissions to create and manage Group Policy Objects.
2. Open the **Group Policy Management Console (GPMC)** by searching for "Group Policy Management" in the Start menu or running `gpmc.msc`.

### Step 2: Create a New GPO for Each Language

We’ll create three separate GPOs for the languages **English (EN)**, **Dutch (NL)**, and **French (FR)**. Each GPO will be configured with the necessary settings to enforce language-specific regional options.

1. In the **Group Policy Management Console**, navigate to your **domain** (e.g., `domain.local`) in the left pane.
2. Right-click on the **Group Policy Objects** folder, select **New**, and name your GPO according to the language. For example:
   - **User Policy - Language EN** for English
   - **User Policy - Language NL** for Dutch
   - **User Policy - Language FR** for French

3. Click **OK** to create each GPO.

### Step 3: Edit the GPO and Configure Language Settings

Now, we’ll configure the settings for each GPO individually to apply the correct regional and language options for each target language.

#### 1. Configure Regional Options for Each Language

For each GPO (**User Policy - Language EN**, **User Policy - Language NL**, **User Policy - Language FR**), follow these steps:

1. Right-click on the newly created GPO (e.g., **User Policy - Language EN**) and select **Edit**.
2. In the Group Policy Management Editor, navigate to: User Configuration > Policies > Administrative Templates > Control Panel > Regional and Language Options

3. Double-click **Restrict selection of Windows menus and dialogs language** and configure it as follows:
- **State**: Enabled
- **Restrict users to the following language**: Set the language according to the GPO:
  - **English (EN)**: Select **English**
  - **Dutch (NL)**: Select **Dutch**
  - **French (FR)**: Select **French**
- Click **Apply** and **OK**.

#### 2. Configure Office Language Settings

If you are also managing Microsoft Office language preferences, you can set the Office display and editing languages for each GPO.

1. In the Group Policy Management Editor for each language-specific GPO, navigate to: User Configuration > Policies > Administrative Templates > Microsoft Office 2016 > Language Preferences


2. Configure the following settings:

- **Display menus and dialog boxes in**:
  - **State**: Enabled
  - **Display menus and dialog boxes in**: Select the appropriate language
    - **English (EN)**: Set to **English**
    - **Dutch (NL)**: Set to **Dutch**
    - **French (FR)**: Set to **French**

- **Primary Editing Language**:
  - **State**: Enabled
  - **Primary Editing Language**: Select the appropriate language
    - **English (EN)**: Set to **English**
    - **Dutch (NL)**: Set to **Dutch (Belgium)**
    - **French (FR)**: Set to **French (France)**

3. Click **Apply** and **OK** for each setting.

> **Note:** These Office-specific settings require that users have Microsoft Office 2016 or later. The settings are applied when Office applications are launched and can be used to ensure users see Office in their preferred language.

### Step 4: Link the GPOs to the Appropriate Organizational Units (OUs)

Now that each GPO is configured, we need to link them to the appropriate OUs in Active Directory.

1. In the **Group Policy Management Console**, locate the **Organizational Unit (OU)** where your users are stored. This might be a departmental OU or a specific OU for users.
2. Right-click on the target OU, select **Link an Existing GPO**, and choose the appropriate GPO:
- Link **User Policy - Language EN** for users who prefer English.
- Link **User Policy - Language NL** for users who prefer Dutch.
- Link **User Policy - Language FR** for users who prefer French.
3. Repeat this process for each OU or group of users that needs a specific language policy applied.

### Step 5: Assign Users to Language-Based Security Groups

To ensure that users are only affected by the GPOs that match their language preference, assign them to language-specific security groups in Active Directory.

1. Create three security groups in Active Directory, for example:
- `User Policy Language EN`
- `User Policy Language NL`
- `User Policy Language FR`
2. Add users to the appropriate group based on their language preference.
3. Modify the **Security Filtering** of each GPO to apply only to the corresponding group:
- Open each GPO in the **Group Policy Management Console**.
- In the **Scope** tab, under **Security Filtering**, add the relevant security group (e.g., `User Policy Language EN` for **User Policy - Language EN**).
- Remove **Authenticated Users** from the Security Filtering list to restrict the GPO to only the specified group.

### Step 6: Test and Verify

1. Log in as a test user for each language group and verify that the language and regional settings are correctly applied.
2. Open Windows and check that system menus, dialogs, and regional settings reflect the language specified in the GPO.
3. For Office users, open an Office application (such as Word or Excel) and confirm that the interface language and editing language match the settings specified in the GPO.

---

By following these steps, you can create dedicated GPOs that apply language and regional settings based on user preferences. This approach ensures consistency across your organization and allows users to work in the language that suits them best, while automating the process for IT administrators. 

For more information on language codes and locale settings, refer to the [official Microsoft documentation on language locale settings](https://learn.microsoft.com/en-us/previous-versions/commerce-server/ee825488(v=cs.20)?redirectedfrom=MSDN).


## Implementation Strategy

Here’s the game plan: we’ll use the `preferredLanguage` attribute in AD to assign users to specific language groups, which in turn link to GPOs for language settings. This way, as user language preferences change, AD will automatically handle the adjustments.

Here’s how it works:

1. **Retrieve Users**: Pull all AD users who have a `preferredLanguage` attribute set.
2. **Determine Language**: For each user, extract the language code from their `preferredLanguage` attribute.
3. **Assign to Group**: Add the user to the corresponding security group based on their language code.
4. **Remove from Other Groups**: Make sure they’re not in any other language groups to avoid conflicts.
5. **Handle Undefined/Unsupported Languages**: If a user’s `preferredLanguage` isn’t set or isn’t supported, remove them from all language groups.

Automating these steps with PowerShell means language settings stay up-to-date, hassle-free.

## The PowerShell Script

Here’s the PowerShell script that does it all. This script should be saved (e.g., as `Update-UserLanguageGroups.ps1`) on your AD server and run as a scheduled task.

```powershell
# Script Name: Update-UserLanguageGroups.ps1
# Description: Assigns users to language-specific security groups based on the language portion of their preferredLanguage attribute in Active Directory.
# Author: Your Name
# Date: YYYY-MM-DD

# Import Active Directory module
Import-Module ActiveDirectory

# Define the security groups corresponding to each language policy
$languageGroups = @{
    "FR" = "User Policy Language FR"
    "EN" = "User Policy Language EN"
    "NL" = "User Policy Language NL"
}

# Define the distinguished names of the security groups
$groupDNs = @{
    "FR" = (Get-ADGroup -Filter { Name -eq $languageGroups["FR"] }).DistinguishedName
    "EN" = (Get-ADGroup -Filter { Name -eq $languageGroups["EN"] }).DistinguishedName
    "NL" = (Get-ADGroup -Filter { Name -eq $languageGroups["NL"] }).DistinguishedName
}

# Function to remove user from all language groups
function Remove-FromAllLanguageGroups {
    param (
        [Parameter(Mandatory = $true)]
        [string]$UserDN
    )
    foreach ($groupDN in $groupDNs.Values) {
        Remove-ADGroupMember -Identity $groupDN -Members $UserDN -ErrorAction SilentlyContinue
    }
}

# Get all users with the 'preferredLanguage' attribute
$users = Get-ADUser -Filter { preferredLanguage -like "*" } -Properties preferredLanguage, DistinguishedName

foreach ($user in $users) {
    # Extract the language code from the preferredLanguage attribute (e.g., 'en' from 'en-US')
    $preferredLanguageFull = $user.preferredLanguage
    $preferredLanguageCode = $preferredLanguageFull.Split('-')[0].ToUpper()
    $userDN = $user.DistinguishedName

    if ($languageGroups.ContainsKey($preferredLanguageCode)) {
        $targetGroupDN = $groupDNs[$preferredLanguageCode]
        
        # Add user to the target group if not already a member
        if (-not (Get-ADGroupMember -Identity $targetGroupDN -Recursive | Where-Object { $_.DistinguishedName -eq $userDN })) {
            Add-ADGroupMember -Identity $targetGroupDN -Members $userDN
            Write-Output "Added $($user.SamAccountName) to $($languageGroups[$preferredLanguageCode])"
        }

        # Remove user from other language groups
        foreach ($lang in $languageGroups.Keys) {
            if ($lang -ne $preferredLanguageCode) {
                $otherGroupDN = $groupDNs[$lang]
                Remove-ADGroupMember -Identity $otherGroupDN -Members $userDN -ErrorAction SilentlyContinue
                Write-Output "Removed $($user.SamAccountName) from $($languageGroups[$lang])"
            }
        }
    }
    else {
        # If preferredLanguage is not set correctly, remove from all language groups
        Remove-FromAllLanguageGroups -UserDN $userDN
        Write-Output "Removed $($user.SamAccountName) from all language groups due to undefined or unsupported preferredLanguage: $preferredLanguageFull"
    }
}

# Optional: Log the script execution time
Write-Output "Language group update completed at $(Get-Date)"
```

## Setting Up the Scheduled Task

1. **Open Task Scheduler** on your AD server.
2. **Create a New Task** and give it a name like “User Language Group Update.”
3. **Set the Trigger** to run daily or weekly, depending on how frequently you need updates.
4. **Set the Action** to run `PowerShell.exe` with the argument pointing to your script’s location (e.g., `-File "C:\Scripts\Update-UserLanguageGroups.ps1"`).
5. **Configure the Task** to run with the highest privileges and to use a service account that has permissions to modify AD groups.

## Testing and Validation

Before rolling this out, test it on a few user accounts to make sure everything is working as expected:

1. **Assign test values** to the `preferredLanguage` attribute for sample users.
2. **Run the script manually** and observe the output to verify users are being added to the correct groups.
3. **Check the Group Membership** of test users in AD to confirm changes.

Once you’re confident it’s working, schedule the task to automate the process!

## Changing the preferredLanguage Attribute

To make sure each user is assigned the correct language settings, you’ll need to set the `preferredLanguage` attribute in Active Directory for each user. This attribute follows the [RFC 1766](https://tools.ietf.org/html/rfc1766) format, such as `"en-US"` for English (United States) or `"fr-FR"` for French (France). 

Here’s how to update this attribute for a user in Active Directory Users and Computers (ADUC).

### Using Active Directory Users and Computers (ADUC)

1. **Open ADUC** and find the user you want to modify.
2. Right-click the user and select **Properties**.
3. Go to the **Attribute Editor** tab. (If you don’t see this tab, you may need to enable **Advanced Features** in the **View** menu.)
4. Find the `preferredLanguage` attribute in the list, select it, and click **Edit**.
5. Enter the desired language code (e.g., `"en-US"` for English or `"nl-NL"` for Dutch).
6. Click **OK** to save your changes.

### Supported Values

The `preferredLanguage` attribute uses language codes specified in [Microsoft's official documentation for locale settings](https://learn.microsoft.com/en-us/previous-versions/commerce-server/ee825488(v=cs.20)?redirectedfrom=MSDN). Make sure to use the correct language codes for your organization’s requirements.

This allows you to set a wide range of languages based on user preferences, making your environment more inclusive and tailored to individual needs.


## Conclusion

This PowerShell-based approach makes it easy to keep user language settings aligned with their preferences without manual intervention. It’s a set-it-and-forget-it solution that adapts as your organization grows and changes. Automating tasks like this is a great way to free up your time for more strategic IT initiatives.

Happy automating!

