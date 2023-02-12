---
layout: post
title: Upgrade domain controllers to a newer version of Windows Server
categories: Windows Server
tags: upgrade domaincontroller AD
---

For an in-place upgrade of an existing DC, you must run adprep /forestprep and adprep /domainprep manually. You need to run Adprep /forestprep only once in the forest for each newer version of Windows Server. Run Adprep /domainprep once in each domain in which you have DCs that you're upgrading for each newer version of Windows Server.

In this table you can see the supported upgrade paths, based on the version you're currently on.

Upgrade from / to|Windows Server 2008 R2|Windows Server 2012|Windows Server 2012 R2|Windows Server 2016|Windows Server 2019|Windows Server 2022
Windows Server 2008|Yes|Yes|-|-|-|-
Windows Server 2008 R2|-|Yes|Yes|-|-|-
Windows Server 2012|-|-|Yes|Yes|-|-
Windows Server 2012 R2|-|-|-|Yes|Yes|-
Windows Server 2016|-|-|-|-|Yes|Yes
Windows Server 2019|-|-|-|-|-|Yes

So we need to run the following command to prepare the Forest:

```powershell

adprep /forestprep

```

And then for each Domain controller we want to upgrade:

```powershell

Adprep /domainprep

```