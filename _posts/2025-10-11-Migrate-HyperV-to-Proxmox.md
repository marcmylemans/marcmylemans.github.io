---
layout: post
title: "How to Migrate a Hyper-V VM to Proxmox (Step-by-Step Guide)"
date: 2025-10-11
categories: [Homelab, Virtualization]
tags: [Proxmox, Hyper-V, Migration, qemu-img, VirtIO]
image: https://mylemans.online/assets/img/posts/Migrate-HyperV-to-Proxmox.png
description: "Step-by-step tutorial on migrating a Hyper-V virtual machine to Proxmox using qemu-img and VirtIO drivers."
---

If you’re moving your home lab or production workloads from **Hyper-V** to **Proxmox**, this guide walks you through the entire migration process, including installing drivers, exporting, converting, and importing your virtual machine.

{% youtube "https://youtu.be/nYLgYg2zPHc" %}

---

## Step 1 — Prepare the VM

1. Inside your Hyper-V VM, install the latest stable **VirtIO drivers**:
   [Download VirtIO ISO](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso)

2. Mount the ISO, install all drivers, then shut down the VM.

3. Export the VM from Hyper-V:
   - Open Hyper-V Manager → right-click the VM → **Export**
   - Choose a destination folder.

---

## Step 2 — Convert the Disk

Use **qemu-img** to convert your `.vhdx` disk to `.qcow2`.

**Windows download:**
- [https://cloudbase.it/qemu-img-windows/](https://cloudbase.it/qemu-img-windows/)
- Direct ZIP: [qemu-img-win-x64-2_3_0.zip](https://cloudbase.it/downloads/qemu-img-win-x64-2_3_0.zip)

Run from Command Prompt:

```bash
qemu-img.exe convert -f vhdx -O qcow2 "C:\path\to\VM.vhdx" "C:\path\to\VM-converted.qcow2"
```

In powershell or Terminal you have to append .\ to any file.

```powershell
.\qemu-img.exe convert -f vhdx -O qcow2 "C:\path\to\VM.vhdx" "C:\path\to\VM-converted.qcow2"
```

**Linux example:**

```bash
qemu-img convert -f vhdx -O qcow2 -o preallocation=off ./Win10test.vhdx /var/lib/vz/images/101/Win10-converted.qcow2
```

---

## Step 3 — Share the Converted Disk

1. On the Hyper-V host, share the folder containing the converted file.
2. In Proxmox, go to:
   - **Datacenter → Storage → Add → SMB/CIFS**
   - Enter your Hyper-V server IP, credentials, and share name.
   - Under **Content**, select **Import**.

---

## Step 4 — Create and Import the VM in Proxmox

1. Create a new VM → choose “Do not use any media”.
2. System:
   - Machine: **q35**
   - BIOS: **OVMF (UEFI)** for Gen2 or **SeaBIOS** for Gen1
   - Deselect EFI disk and TPM .
3. Delete the default disk → click **Import Disk**.
4. Select your `.qcow2` image.

Once done, start your VM and enjoy your new Proxmox environment!

---

## Summary

- Install VirtIO drivers  
- Export VM  
- Convert VHDX → QCOW2  
- Mount SMB share  
- Import & boot in Proxmox

---

### Related Video

Watch the full tutorial on YouTube:  
[https://youtube.com/@MylemansOnline](https://youtube.com/@MylemansOnline)

---
