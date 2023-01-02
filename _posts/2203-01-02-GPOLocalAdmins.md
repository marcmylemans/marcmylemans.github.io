---
layout: post
title: Manage Local Admins with Group Policy on Workstations
date: 2023-01-02 10:00:00
categories: Windows Server
tags: server 2022 ad gpo admin
---

In this video we will be managing our Local Admins with Group Policy's.
In the first part i will show you how to delete all die local administrators and only leave the Domain Admins.
In the second part we will be using the Managed By field in Active directory to assign a 'Primary User' to the workstation. With this the 'Primary User' has local admin rights only on that assigned workstation.

{% youtube "https://youtu.be/FrRasK5DQiY" %}

Adding the Users to the Local Administrators group:

![Assign users](/assets/primaryuserlocaladmin/primaryuserlocaladmin_assign.jpg)

Item Level targeting:
![Item Level targeting](/assets/primaryuserlocaladmin/primaryuserlocaladmin_itemlvltargeting.jpg)

LDAP Query:

![LDAP Query](/assets/primaryuserlocaladmin/primaryuserlocaladmin_itemlvltargeting.jpg)

1st LDAP Query
```Filter
(&(objectCategory=computer)(objectClass=computer)(name=%COMPUTERNAME%))
```
```Attribute
managedby
```
```Environment variable name
PrimaryUser
```

2nd LDAP Query
```Filter
(&(|(objectClass=group)(objectClass=user))(distinguishedName=%PrimaryUser%))
```
```Attribute
sAMAccountName
```
```Environment variable name
PrimaryUser
```


