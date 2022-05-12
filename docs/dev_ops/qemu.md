# [QEMU](https://www.qemu.org/)

QEMU is a generic and open source machine emulator and virtualizer. It can be used for __system emulation__, where it provides a virtual model of an entire machine to run a guest OS or it may work with a hypervisor such as KVM, Xen, Hax or Hypervisor.

The second supported way to use QEMU is __user mode emulation__, where QEMU can launch processes compiled for one CPU on another CPU. In this mode the CPU is always emulated.


## Sources

- [Improving the performance of a Windows Guest on KVM/QEMU](https://leduccc.medium.com/improving-the-performance-of-a-windows-10-guest-on-qemu-a5b3f54d9cf5) - leduccc

- [My Magical Adventure With cloud-init](https://christine.website/blog/cloud-init-2021-06-04) - Xe Iaso

- [Faster Virtual Machines in Linux](https://adamgradzki.com/2020/04/06/faster-virtual-machines-linux/)

- [gpu-virtualization-with-kvm-qemu](https://medium.com/@calerogers/gpu-virtualization-with-kvm-qemu-63ca98a6a172)
 by Cale Rogers

- [vfio-gpu-how-to-series](http://vfio.blogspot.com/2015/05/vfio-gpu-how-to-series-part-1-hardware.html) by Alex Williamson

- [virtualization-hypervisors-explaining-qemu-kvm-libvirt](https://sumit-ghosh.com/articles/virtualization-hypervisors-explaining-qemu-kvm-libvirt/) by Sumit Ghosh

## usage in kubernetes

- [Schedule GPUs in K8s](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/#deploying-amd-gpu-device-plugin)

## installation of Nvidia Container Toolkit

- [install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Basic cloud-init backed VM

```bash
#!/bin/bash
############
# Script to launch qemu-kvm guest VMs on a headless remote host
# This script utilizes qemu-system-x86_64 to create the VM instead of
# using virt-manager to prevent the need to create XML config files
# as well as to be able to manage the VMs without a UI/GUI
#
# This bash script is a proof-of-concept that ports the previous 
# VMM work found here: https://www.cloudydev.net/dev_ops/multipass/
# from multipass to QEMU/KVM
#
# The need to remove multipass derives from the fact that multipas 
# does not easliy work with non-ubuntu images, nor will it work to
# test .iso live usb images, which I need.
# 
# Multipass also cannot provide hardware accelerated (GPU) windows
# guest VMs, which I also need.
#
# Depends on grub-pc-bin, nmap, net-tools, cloud-image-utils, whois

# VM metadata
export_metatdata(){
  export IMAGE_TYPE="img" #img or iso
  export HOST_ADDRESS="192.168.50.100"
  export HOST_SSH_PORT="22"
  export VM_NAME="testvm"
  export VM_USER="vmadmin"
  export VM_SSH_PORT="1234"
  export DISK_NAME="boot.img"
  export DISK_SIZE="60G"
  export ISO_FILE="ubuntu-22.04-live-server-amd64.iso"
  export UBUNTU_CODENAME="jammy"
  export CLOUD_IMAGE_NAME="${UBUNTU_CODENAME}-server-cloudimg-amd64"
  export CLOUD_IMAGE_URL="https://cloud-images.ubuntu.com/jammy/current"
  export MEMORY="8G"
  export PHYSICAL_CORES="4"
  export VGA="std"
  export VM_KEY=""
  export VM_KEY_FILE="$VM_USER"
}

# create a directory to hold the VM assets
create_dir(){
  mkdir "$VM_NAME"
  cd "$VM_NAME"
}

# download a cloud image as .img
download_cloud_image(){
  wget -c -O "$CLOUD_IMAGE_NAME".img \
  "$CLOUD_IMAGE_URL"/"$CLOUD_IMAGE_NAME".img
}

# Create and expanded image
expand_cloud_image(){
  qemu-img create -b ${CLOUD_IMAGE_NAME}.img -f qcow2 \
        -F qcow2 ${CLOUD_IMAGE_NAME}-new.img \
        "$DISK_SIZE"
}

# convert the .img to qcow2 to use as base layer
img_to_qcow(){
  qemu-img convert -f raw \
    -O qcow2 "$CLOUD_IMAGE_NAME"_original.img \
    "$CLOUD_IMAGE_NAME".qcow2
}

# create the next layer on the image
create_qcow_image(){
  qemu-img create -f qcow2 \
    -F qcow2 \
    -o backing_file="$CLOUD_IMAGE_NAME"_base.qcow2 \
    "$VM_NAME".qcow2
}

# create a ssh key for the user and save as a file w/ prompt
create_ssh_key(){
  ssh-keygen -C "$VM_USER" \
    -f "$VM_KEY_FILE" \
    -N '' \
    -t rsa

  VM_KEY_FILE=$(find "$(cd ..; pwd)" -name $VM_USER)
  VM_KEY=$(cat "$VM_KEY_FILE".pub)
}

create_user_data(){
cat > user-data <<EOF
#cloud-config
#vim:syntax=yaml
cloud_config_modules:
 - runcmd
cloud_final_modules:
 - [users-groups, always]
 - [scripts-user, once-per-instance]
users:
  - name: ${VM_USER}
    groups: [ wheel ]
    shell: /bin/bash
    sudo: [ "ALL=(ALL) NOPASSWD:ALL" ]
    ssh-authorized-keys:
      - ${VM_KEY}
EOF
}


# create a disk
create_virtual_disk(){
  qemu-img create -f qcow2 \
    -F qcow2 \
    -b "$CLOUD_IMAGE_NAME"_base.qcow2 \
    hdd.qcow2 "$DISK_SIZE"
}

# Generate an ISO image
generate_seed_iso(){
  cloud-localds seed.img user-data
}

# start the VM
start_ubuntu_cloud_vm(){
  tmux new-session -d -s "${VM_NAME}_session"
  tmux send-keys -t "${VM_NAME}_session" "sudo qemu-system-x86_64  \
    -machine accel=kvm,type=q35 \
    -cpu host \
    -smp "$PHYSICAL_CORES" \
    -m "$MEMORY" \
    -nographic \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
    -drive if=virtio,format=qcow2,file="$CLOUD_IMAGE_NAME"-new.img \
    -drive if=virtio,format=raw,file=seed.img \
    -vnc :0 \
    $@" ENTER
}

attach_to_vm_tmux(){
  export_metatdata
  tmux attach-session -t "${VM_NAME}_session"
}

ssh_to_vm(){
  export_metatdata
  ssh-keygen -f "/home/${USER}/.ssh/known_hosts" -R "[${HOST_ADDRESS}]:${VM_SSH_PORT}"
  ssh -o "StrictHostKeyChecking no" \
    -i testvm/"$VM_USER" \
    -p "$VM_SSH_PORT" "$VM_USER"@"$HOST_ADDRESS"
}


# TODO 
# create an iso image https://quantum-integration.org/posts/install-cloud-guest-with-virt-install-and-cloud-init-configuration.html
#qemu-img create -f qcow2 -o \
#    backing_file=./master/centos-7-cloud.qcow2 \
#    example.qcow2

# luanch the VM to install from ISO to Disk
create_vm_from_iso(){
  sudo qemu-system-x86_64 -enable-kvm \
          -cpu host,nx \
          -smp 2 \
          -drive file="$CLOUD_IMAGE_NAME"_base.img,if=virtio \
          -net nic -net user,hostfwd=::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
          -m "$MEMORY" \
          -vga "$VGA" \
          -monitor stdio \
          -vnc :0 \
          $@
}

main(){
  export_metatdata
  create_dir
  download_cloud_image
  expand_cloud_image
  create_ssh_key
  create_user_data
  generate_seed_iso
  start_ubuntu_cloud_vm
}

"$@"

#
#
#  Connecting to the VM after install is done
#  1. SSH from the Host to Guest
#   ssh -X -Y -p "$VM_SSH_PORT" localhost
#
#  2. SSH from remote client to host and be redirected to guest
#   ssh -X -Y -p "$VM_SSH_PORT" max@"$HOST_ADDRESS"
#
#  3. Connect to Guest using QEMU's VNC server
#   "$HOST_ADDRESS":"$VM_SSH_PORT"
#  Get status of port
#
#  nmap -p 1234 localhost
#
#  VNC tunnel https://gist.github.com/chriszarate/bc34b7378d309f6c3af5
#
#
#  ssh -o "StrictHostKeyChecking no" \
#    -N -L 5001:"$HOST_ADDRESS":5900 \
#    -p "$VM_SSH_PORT" "VM_USER"@"HOST_ADDRESS" 
```

# QEMU + KVM GPU IOMMU passthrough with Debian Linux Host and Windows 10 Guest


## Getting the GPU PCI Information

Your GPU that you wish to pass through to the VM will often have other devices in its IOMMU group.
If this is the case, ALL devices in that IOMMU group should be passed through to your VM.
This shouldnt be too much of a problem, as those companion devices will likely be audio or busses that 
are attached to the GPU as well. 
This is only really an issue if your GPU for the Host and the GPU for the Guest are in the same IOMMU Group.
If that's the case, you need a patched kernel[idk how to do it yet] or to put the GPU in a differient PCI-e slot on your motherboard.


This script will gather all the PCI devices and sort them cleanly based on their IOMMU Group:

```zsh

cat << EOF > iommu-finder.sh
#!/bin/bash
# change the 999 if needed
shopt -s nullglob
for d in /sys/kernel/iommu_groups/{0..999}/devices/*; do
    n=${d#*/iommu_groups/*}; n=${n%%/*}
    printf 'IOMMU Group %s ' "$n"
    lspci -nns "${d##*/}"
done;
EOF

chmod +x iommu-finder
```

Example script output

```zsh
...
...
IOMMU Group 0 00:00.0 Host bridge [0600]: Intel Corporation 4th Gen Core Processor DRAM Controller [8086:0c00] (rev 06)
IOMMU Group 1 00:01.0 PCI bridge [0604]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor PCI Express x16 Controller [8086:0c01] (rev 06)
IOMMU Group 1 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP104 [GeForce GTX 1070 Ti] [10de:1b82] (rev a1)
IOMMU Group 1 01:00.1 Audio device [0403]: NVIDIA Corporation GP104 High Definition Audio Controller [10de:10f0] (rev a1)
IOMMU Group 2 00:02.0 VGA compatible controller [0300]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor Integrated Graphics Controller [8086:0412] (rev 06)
IOMMU Group 3 00:03.0 Audio device [0403]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor HD Audio Controller [8086:0c0c] (rev 06)
...
...

```

From the above output I found the PCI Bus and Device ID of the NVIDIA GPU and its related devices. 

```yaml
Nvidia:
  - GUEST_GPU: GTX 1070ti
    IOMMU_Group: '1'
  - Name: PCI Bridge
    Bus: '00:01.0'
    DeviceId: '8086:0c01'
  - Name: VGA-compatible-controller
    Bus: '01:00.0'
    DeviceId": '10de:1b82'
  - Name: Audio_Device
    Bus: '01:00.1'
    DeviceId": '10de:10f0'
```

Fortunately, all needed of these devices were already in separate IOMMU groups, or bundeled together in [group 1]


To apply these values im going modify kernel modules via scripts.
that will same effect as a kernel mod line in /etc/defaul/grub like:

```zsh

GRUB_CMDLINE_LINUX_DEFAULT="amd_iommu=on iommu=pt kvm.ignore_msrs=1 vfio-pci.ids=<someID-0>,<someID-1>"

```


Creating /etc/initramfs-tools/scripts/init-top/vfio.sh

```zsh

cat << EOF > /etc/initramfs-tools/scripts/init-top/vfio.sh
#!/bin/sh

# VGA-compatible-controller
PCIbusID0="01:00.0"

# audio-device
PCIbusID1="01:00.1"

PREREQ=""

prereqs()
{
   echo "$PREREQ"
}

case $1 in
prereqs)
   prereqs
   exit 0
   ;;
esac

for dev in 0000:"$PCIbusID0" 0000:"$PCIbusID1"
do 
 echo "vfio-pci" > /sys/bus/pci/devices/$dev/driver_override 
 echo "$dev" > /sys/bus/pci/drivers/vfio-pci/bind 
done

exit 0

EOF

```
Make it executable:

```zsh
chmod +x vfio.sh
```

Setting the kernel module options by creating a replacement config file for: "/etc/initramfs-tools/modules"


Create the file in the local dir

```zsh

cat << EOF > modules
# List of modules that you want to include in your initramfs.
# They will be loaded at boot time in the order below.
#
# Syntax:  module_name [args ...]
#
# You must run update-initramfs(8) to effect this change.
#
# Examples:
#
# raid1
# sd_mod
options kvm ignore_msrs=1
EOF

```

Move it into place and correct the ownership and pemrissions

```
sudo mv /etc/initramfs-tools/modules /etc/initramfs-tools/modules.bak
sudo mv modules /etc/initramfs-tools/
sudo chown root:root /etc/initramfs-tools/modules 
sudo chmod 644 /etc/initramfs-tools/modules 
```


CPU Pinning
 <vcpu placement='static'>14</vcpu>
 <iothreads>1</iothreads>
 <cputune>
    <vcpupin vcpu='0' cpuset='1'/>
    <vcpupin vcpu='1' cpuset='2'/>
    <vcpupin vcpu='2' cpuset='3'/>
    <vcpupin vcpu='3' cpuset='4'/>
    <vcpupin vcpu='4' cpuset='5'/>
    <vcpupin vcpu='5' cpuset='6'/>
    <vcpupin vcpu='6' cpuset='7'/>
    <vcpupin vcpu='7' cpuset='9'/>
    <vcpupin vcpu='8' cpuset='10'/>
    <vcpupin vcpu='9' cpuset='11'/>
    <vcpupin vcpu='10' cpuset='12'/>
    <vcpupin vcpu='11' cpuset='13'/>
    <vcpupin vcpu='12' cpuset='14'/>
    <vcpupin vcpu='13' cpuset='15'/>
    <emulatorpin cpuset='0,8'/>
    <iothreadpin iothread='1' cpuset='0,8'/>
 </cputune>
 
 
# simple launch to get into the gui

Once we can get into the GUI we must update some group policy values to set the proper GPU for use with RDP connections

```zsh
qemu-system-x86_64 \
    -hda win10.img \
    -boot c \
    -machine type=q35,accel=kvm \
    -cpu host,kvm="off" \
    -smp sockets=1,cores=2,threads=2 \
    -m 8G \
    -vga std
    -serial none \
    -parallel none \
    -device vfio-pci,host=01:00.0,multifunction=on \
    -device vfio-pci,host=01:00.1 \
    -net nic,model=e1000 \
    -net user 
```

We also need to record the ip address for the vm. 
For this example is "10.0.2.15"

Now we can connect via rdp

# Set up a networking bridge, before RDP will work
Make sure bridge-utils is installed:
`sudo apt install bridge-utils`


edit `/etc/network/interfaces`:

```
auto lo
iface lo inet loopback

auto br0
iface br0 inet static
        address 192.168.50.23
        network 192.168.50.0
        netmask 255.255.255.0
        broadcast 192.168.50.255
        gateway 192.168.50.1
        dns-nameservers 192.168.50.1 1.1.1.1
        bridge_ports eth0
        bridge_stp off
        bridge_fd 0
        bridge_maxwait 0
```

Restart networking? :shrug: maybe reboot if you can't figure that out :shrug:

The XML for the networking in virtual manager:
```xml
<interface type="network">
  <mac address="52:54:00:1b:70:45"/>
  <source network="default"/>
  <model type="e1000e"/>
  <address type="pci" domain="0x0000" bus="0x01" slot="0x00" function="0x0"/>
</interface>
```

What we're gonna change it to:
```xml
<interface type="bridge">
  <mac address="52:54:00:1b:70:45"/>
  <source brdige="br0"/>
</interface>
```


# with vnc
```zsh
qemu-system-x86_64 \
  -drive id=disk0,if=virtio,cache=none,format=raw,file=Win10-AlternateInstall.img \
  -drive file=Win10_21H2_EnglishInternational_x64.iso,index=1,media=cdrom \
  -boot c \
  -machine type=q35,accel=kvm \
  -cpu host,kvm="off" \
  -smp sockets=1,cores=2,threads=2 \
  -m 8G \
  -vga none -nographic -serial none -parallel none \
  -device vfio-pci,host=01:00.0,multifunction=on \
  -device vfio-pci,host=01:00.1 \
  -device virtio-net,netdev=vmnic \
  -netdev user,id=vmnic \
  -net nic,model=e1000 \
  -net user \
  -vnc 127.0.0.1:2
```

To get to bios, this worked, and spits you into a shell, which you then hit exit on and select boot manager.
  
```zsh
sudo qemu-system-x86_64 \
   # primary hard disk \
   -drive id=disk0,if=virtio,cache=none,format=raw,file=Win10-AlternateInstall.img \
   # Windows Installer ISO Image \
   -drive file=Win10_21H2_EnglishInternational_x64.iso,index=1,media=cdrom \
   # Driver installer ISO \
   #-drive file=virtio-win-0.1.141.iso,index=0,media=cdrom \
   -boot c \
   -machine type=q35,accel=kvm \
   -cpu host,kvm="off" \
   -smp sockets=1,cores=2,threads=2 \
   -m 8G \
   -serial none \
   -parallel none \
   # GTX 1070 TI \
   -device vfio-pci,host=01:00.0,multifunction=on \
   # GTX 1070 TI HDMI Audio \
   -device vfio-pci,host=01:00.1 \
   -net nic,model=e1000 \
   -net user \
   -bios /usr/share/qemu/OVMF.fd \
   # if you need a remote connection
   -vnc 127.0.0.1:2


sudo qemu-system-x86_64 \
   -hda Win10-AlternateInstall.img \
   -boot c \
   -machine type=q35,accel=kvm \
   -cpu host,kvm="off" \
   -smp sockets=1,cores=2,threads=2 \
   -m 8G \
   -serial none \
   -parallel none \
   -device vfio-pci,host=01:00.0,multifunction=on \
   -device vfio-pci,host=01:00.1 \
   -device virtio-net,netdev=vmnic \
   -netdev user,id=vmnic \
   -net nic,model=e1000 \
   -net user \
   -bios /usr/share/qemu/OVMF.fd
```