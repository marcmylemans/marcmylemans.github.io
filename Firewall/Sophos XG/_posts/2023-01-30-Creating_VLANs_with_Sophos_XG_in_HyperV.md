---
layout: post
title: Creating VLAN's with Sophos XG in Hyper-V!
image: https://i9.ytimg.com/vi/1GrQDet3XlU/mqdefault.jpg?v=63d0173a&sqp=CMzFq68G&rs=AOn4CLDm4esjcFZW8fwzvwSOurOZwd4-Bg
---

In this video we continue our Sophos XG series. In the previous video we installed Sophos XG in Hyper-V as a virtual machine.
Now we are creating Vlan's and allowing Hyper-v to 'Trunk' the vlan's.

{% youtube "https://www.youtube.com/watch?v=1GrQDet3XlU" %}


Below are the powershell commands used in this video.

Lookup the Network Adapters for your Virtual Machine:
```powershell
Get-VMNetworkAdapter -vmname SophosXG
```

Run the following to rename your Network Adapters, where 0 would be your LAN Network Adapter and 1 your WAN Network Adapter in this example:
```powershell
$VMNET = Get-VMNetworkAdapter -vmname SophosXG
Rename-VMNetworkAdapter -VMNetworkAdapter $VMNET[0] -NewName LAN
Rename-VMNetworkAdapter -VMNetworkAdapter $VMNET[1] -NewName WAN
```

Set your LAN Network Adapter to a trunk port to allow Tagged VLAN 1 to 254 and set the Untagged interface to vlan 0:
```powershell
Set-VMNetworkAdapter -VMName "SophosXG" -VMNetworkAdapterName "LAN" -Trunk -Allowedvlanidlist 1-254 -nativevlanid 0
```
