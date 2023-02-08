---
layout: post
title: AAD Connect / Cloud Sync with existing cloud users
categories: Azure Connect
tags: azuread ad sync
---

If you already have users in your Azure/Office 365 tenant and want to setup AD Connect or Cloud Sync, then you will notice that it can happen that you get duplicate users from your Active Directory environment.

To prevent this from happening you can link the existing immutableid from Active Directory to the user in Azure Directory.
it is also important that every proxyaddress (alias e-mail) in Office 365 is present in Active Directory.

First we will have to get an Export from Office 365 for all the information and also as a backup.
The following script will create an export of all the Users in Office 365.

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

The following script will do the same from Active Directory.

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

With the following script you can do a compare to both the file to see the difference

```powershell
$Data_AD = Import-CSV c:\temp\Users_AD.csv -Delimiter ","
$Data_AAD = Import-CSV c:\temp\Users_AAD.csv -Delimiter ","

#Echo "Not Matching ImmutableID's: (AD VS AAD)"
Compare-Object -ReferenceObject $Data_AD -DifferenceObject $Data_AAD -Property ImmutableID -IncludeEqual -PassThru | Where-Object {$_.SideIndicator -Notlike "=="}

#Echo "Not Matching ProxyAddresses:(AD VS AAD)"
Compare-Object -ReferenceObject $Data_AD -DifferenceObject $Data_AAD -Property ProxyAddresses -IncludeEqual -PassThru | Where-Object {$_.SideIndicator -Notlike "=="}

```

After comparing everything you can use the following script to import all the proxyAddresses in Active Directory
this is an important step, because Active Directory will overwrite everything in AAD.

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

To create a hardlink between an Active Directory User and an Azure Directory User we will be using the following script.
This script will take the ObjectID from Active Directory and Write it to the corresponding user in Azure Directory. 

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