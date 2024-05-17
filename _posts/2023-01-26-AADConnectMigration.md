---
layout: post
title: AAD Connect / Cloud Sync with Existing Cloud Users
categories: [Azure, Connect]
tags: [azuread, ad, sync, aad connect, cloud sync, powershell, tutorial]
---

# Tackling Duplicate Users in AAD Connect / Cloud Sync

Integrating your existing Active Directory with Azure AD using AD Connect or Cloud Sync can sometimes result in duplicate user entries. This video demonstrates how to link existing ImmutableIDs from Active Directory to Azure Directory users and ensure that all proxy addresses in Office 365 are present in Active Directory.

# Disclaimer for Script Usage

Please note that these scripts are provided for informational purposes and should be used with caution. Always test scripts in a non-production environment first, and ensure you have backups of your data. I am not responsible for any issues that may arise from the use of these scripts. Users should have an understanding of PowerShell and Active Directory operations before proceeding.

### Step 1: Exporting User Data from Office 365

The following PowerShell script will export all user data from Office 365, which serves as both an information source and a backup.


```powershell
#Check for Existing c:\Temp folder and if needed create the c:\Temp folder
$FolderName = "C:\Temp"

if([System.IO.Directory]::Exists($FolderName))
{
    Write-Host "Folder Exists"
    Get-ChildItem -Path $FolderName | Where-Object {$_.CreationTime -gt (Get-Date).Date}   
}
else
{
    Write-Host "Folder Doesn't Exists"
    
    #PowerShell Create directory if not exists
    New-Item $FolderName -ItemType Directory
}

Connect-AzureAD


$reportoutput=@()
$users = Get-AzureADUser -All $true
$users | Foreach-Object {
 
    $user = $_
    $SMTP_Addresses = $user.ProxyAddresses
    $SMTP_List = $SMTP_Addresses -join ";"

    $report = New-Object -TypeName PSObject
    $report | Add-Member -MemberType NoteProperty -Name 'UserPrincipalName' -Value $user.UserPrincipalName
    $report | Add-Member -MemberType NoteProperty -Name 'SamAccountName' -Value $user.samaccountname
    $report | Add-Member -MemberType NoteProperty -Name 'ImmutableID' -Value $user.immutableid
    $report | Add-Member -MemberType NoteProperty -Name 'DisplayName' -Value $user.displayname
    $report | Add-Member -MemberType NoteProperty -Name 'ProxyAddresses' -Value $SMTP_List
    $reportoutput += $report
}
 # Report
$reportoutput | Export-Csv -Path c:\temp\Users_AAD.csv -NoTypeInformation -Encoding UTF8

```

### Step 2: Exporting Data from Active Directory

This script performs a similar export from Active Directory.

```powershell
#Check for Existing c:\Temp folder and if needed create the c:\Temp folder
$FolderName = "C:\Temp"

if([System.IO.Directory]::Exists($FolderName))
{
    Write-Host "Folder Exists"
    Get-ChildItem -Path $FolderName | Where-Object {$_.CreationTime -gt (Get-Date).Date}   
}
else
{
    Write-Host "Folder Doesn't Exists"
    
    #PowerShell Create directory if not exists
    New-Item $FolderName -ItemType Directory
}


$reportoutput=@()
$users = Get-ADUser -Filter * -Properties *
$users | Foreach-Object {
 
    $user = $_
    $objectid = $user.ObjectGUID
    $immutableid = [Convert]::ToBase64String([guid]::New($objectid).ToByteArray())

    $SMTP_Addresses = $user.ProxyAddresses
    $SMTP_List = $SMTP_Addresses -join ";" 

    $report = New-Object -TypeName PSObject
    $report | Add-Member -MemberType NoteProperty -Name 'UserPrincipalName' -Value $user.UserPrincipalName
    $report | Add-Member -MemberType NoteProperty -Name 'SamAccountName' -Value $user.samaccountname
    $report | Add-Member -MemberType NoteProperty -Name 'ImmutableID' -Value $immutableid
    $report | Add-Member -MemberType NoteProperty -Name 'ProxyAddresses' -Value $SMTP_List
    $reportoutput += $report
}
 # Report
$reportoutput | Export-Csv -Path c:\temp\Users_AD.csv -NoTypeInformation -Encoding UTF8

```

### Step 3: Comparing Data Between AD and AAD

To identify differences, use this script to compare the exported data:

```powershell
$Data_AD = Import-CSV c:\temp\Users_AD.csv -Delimiter ","
$Data_AAD = Import-CSV c:\temp\Users_AAD.csv -Delimiter ","

#Echo "Not Matching ImmutableID's: (AD VS AAD)"
Compare-Object -ReferenceObject $Data_AD -DifferenceObject $Data_AAD -Property ImmutableID -IncludeEqual -PassThru | Where-Object {$_.SideIndicator -Notlike "=="}

#Echo "Not Matching ProxyAddresses:(AD VS AAD)"
Compare-Object -ReferenceObject $Data_AD -DifferenceObject $Data_AAD -Property ProxyAddresses -IncludeEqual -PassThru | Where-Object {$_.SideIndicator -Notlike "=="}

```

### Step 4: Importing Proxy Addresses into Active Directory

It's crucial that Active Directory's data reflects all proxyAddresses in AAD. Use the following script to import these addresses:

```powershell
#Check for Existing c:\Temp folder and if needed create the c:\Temp folder
$FolderName = "C:\Temp"

if([System.IO.Directory]::Exists($FolderName))
{
    Write-Host "Folder Exists"
    Get-ChildItem -Path $FolderName | Where-Object {$_.CreationTime -gt (Get-Date).Date}   
}
else
{
   Write-Host "Folder Doesn't Exists"
    
#PowerShell Create directory if not exists
   New-Item $FolderName -ItemType Directory
}


$Data_AD = Import-CSV c:\temp\Users_AD_FR.csv -Delimiter ","
foreach ($AD_User in $Data_AD) {
$UPN = $AD_User.Userprincipalname
$ProxyAddresses = $AD_User.Proxyaddresses
Get-ADUser -Filter "userPrincipalName -like '*$UPN'" | Set-ADUser -replace @{ProxyAddresses=$ProxyAddresses -split ";"}
}
```

### Step 5: Creating a Hard Link Between AD and AAD Users

Finally, this script will write the ObjectID from Active Directory to the corresponding user in Azure Directory.

```powershell
#Check for Existing c:\Temp folder and if needed create the c:\Temp folder
$FolderName = "C:\Temp"

if([System.IO.Directory]::Exists($FolderName))
{
    Write-Host "Folder Exists"
    Get-ChildItem -Path $FolderName | Where-Object {$_.CreationTime -gt (Get-Date).Date}   
}
else
{
    Write-Host "Folder Doesn't Exists"
    
    #PowerShell Create directory if not exists
    New-Item $FolderName -ItemType Directory
}


Connect-MsolService

$Data_AD = Import-CSV c:\temp\Users_AD.csv -Delimiter ","
foreach ($User in $Data_AD) {
$UPN = $User.UserPrincipalName
$ImmutableID = $user.ImmutableId

Echo -userprincipalname $UPN -ImmutableID $ImmutableID
set-msoluser -userprincipalname $UPN -ImmutableID $ImmutableID
}
```

# Closing Thoughts

Successfully merging existing Azure/Office 365 tenant users with your Active Directory environment requires careful planning and execution. This tutorial is designed to guide you through this process, helping you avoid the common pitfall of duplicate user entries.

Your experiences, insights, or any questions about this process are invaluable. Please share them in the comments below. Your input helps us all learn and grow in our understanding of Azure AD and Active Directory integrations.

Stay tuned for more informative guides and tutorials!
