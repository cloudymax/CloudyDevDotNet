# [Virtual Box](https://www.virtualbox.org/wiki/Downloads)

VirtualBox is Oracle’s x86 and AMD64/Intel64 virtualization software. It is a free, open-source virtualization product, distributed under the GNU General Public License (GPL) version 2.

The software allows you to run virtual machines on your host operating system. Additionally, it lets you establish a managed connection between the VMs and even the host if needed.

You can run VirtualBox on Linux, Windows, Mac OS, and Oracle Solaris.

In 2010, Oracle introduced the VirtualBox Extension Pack, a closed-source complemental package with additional features. It included features such as support for USB2/USB3 and RDP.

- [virtualbox-vs-vmware](https://phoenixnap.com/kb/virtualbox-vs-vmware#ftoc-heading-13)
- [KVM](https://www.redhat.com/en/topics/virtualization/what-is-KVM)

---------------------------------

## important variables

```bash
export DOWNLOAD_URL="https://download.virtualbox.org/virtualbox"
export VIRTUALBOX_VERSION="6.1.22"
export HOST_OS_PACKAGE="OSX.dmg" #Win.exe for windows
```

## Installation

### [extension-pack](https://download.virtualbox.org/virtualbox/6.1.22/Oracle_VM_VirtualBox_Extension_Pack-6.1.22.vbox-extpack)

```bash
# for pipelines
curl -O $DOWNLOAD_URL/${VIRTUALBOX_VERSION}/Oracle_VM_VirtualBox_Extension_Pack-${VIRTUALBOX_VERSION}.vbox-extpack
```

### [Windows](https://download.virtualbox.org/virtualbox/6.1.22/VirtualBox-6.1.22-144080-Win.exe)

```bash
# for pipelines
curl -O $DOWNLOAD_URL/${VIRTUALBOX_VERSION}/VirtualBox-${VIRTUALBOX_VERSION}-${HOST_OS_PACKAGE}
```

### [MacOS](https://download.virtualbox.org/virtualbox/6.1.22/VirtualBox-6.1.22-144080-OSX.dmg)

```bash
# for pipelines
curl -O $DOWNLOAD_URL/${VIRTUALBOX_VERSION}/VirtualBox-${VIRTUALBOX_VERSION}-${HOST_OS_PACKAGE}
```

### Linux

```bash

# Easy way
sudo apt-get install virtualbox
sudo apt-get install virtualbox—ext–pack

# Long way
# add to /etc/apt/sources.list:
deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian <mydist> contrib

# apt key:
curl -O https://www.virtualbox.org/download/oracle_vbox_2016.asc
sudo apt-key add oracle_vbox_2016.asc

# install
sudo apt-get update
sudo apt-get install virtualbox-6.1

# What to do when experiencing The following signatures were invalid: BADSIG ... when refreshing the packages from the repository?
sudo -s -H
apt-get clean
rm /var/lib/apt/lists/*
rm /var/lib/apt/lists/partial/*
apt-get clean
apt-get update

```

---------------------------------

## 3D acceleration

VirtualBox 6.1 introduced an improved 3D acceleration support; \
thanks to the huge work done by the VirtualBox engineering team \
we're now able to have improved performance for 3D on Virtual Machines running on VirtualBox.

```text
 The 3D acceleration feature currently has the following preconditions:
    - It is only available for certain Windows, Linux, and Oracle Solaris guests.
    - OpenGL on Linux requires kernel 2.6.27 or later, as well as X.org server version 1.5 or later.

```

- [Blogpost](https://blogs.oracle.com/scoter/oracle-vm-virtualbox-61-3d-acceleration-for-ubuntu-1804-and-2004-virtual-machines)

---------------------------------

## Seamless windows

```text
With the seamless windows feature of Oracle VM VirtualBox, \
 you can have the windows that are displayed within a virtual machine appear side by side next to the windows of your host. \
 This feature is supported for the following guest operating systems, provided that the Guest Additions are installed:

    - Windows guests.
    - Supported Linux or Oracle Solaris guests running the X Window System.
```

---------------------------------

## CLI

```bash
VBoxManage --version
-q|--nologo

# yeah Im not typing that out all day...
alias vbm="VBoxManage"

# the cli is HUGE, some handy references
vbm -q|--nologo
vbm list
vbm showvminfo --details
vbm showvminfo --logs

export NAME="VirtualBradley"
export PATH_TO_FILE="my_vm"
export GROUPS=""
export OS_TYPE=""
export REGISTER="True"
export BASE_FOLDER="pwd"
export UUID=""
export DEFAULT=""
export MEMORY="1024"
export VRAM="128"
export NICL="nat"
export IOAPIC="on"




# register VM
vbm registervm $PATH_TO_FILE
vb, unregister $VM_NAME

# create a VM
vbm createvm --name $VM_NAME \
--groups $GROUPS \
--ostype $OS_TYPE \
$REGISTER \
--basefolder $BASE_FOLDER \
--uuid $UUID \
--default $DEFAULT

vbm modifyvm $VM_NAME \
--ioapic $IOAPIC
--memory $MEMORY \
--vram $VRAM
--nicl $NICL

# start a VM
vbm startvm $VM_NAME \
-type $VM_TYPE \
-putenv <NAME>[=<VALUE>]

# modify a VM
vbm controlvm
vbm storageattach
vbm storagectl

# clones a dvd/disk/floppy
vbm createmedium
vbm modifymedium
vbm clonemedium

```

---------------------------------

todo:
I should make a script that caches all these links downloads to prevent linkrot
