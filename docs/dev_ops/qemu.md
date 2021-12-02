# [QEMU](https://www.qemu.org/)

QEMU is a generic and open source machine emulator and virtualizer. It can be used for __system emulation__, where it provides a virtual model of an entire machine to run a guest OS or it may work with a hypervisor such as KVM, Xen, Hax or Hypervisor.

The second supported way to use QEMU is __user mode emulation__, where QEMU can launch processes compiled for one CPU on another CPU. In this mode the CPU is always emulated.

After enabling GVT-g in QEMU you must also recompile QEMU with the 60 fps fix to get smooth video. There is no way around this issue as of the time of publishing. I describe how to get this working in the the section “Fix QEMU graphics refresh rate.”

## Sources

- [Faster Virtual Machines in Linux](https://adamgradzki.com/2020/04/06/faster-virtual-machines-linux/)

- [gpu-virtualization-with-kvm-qemu](https://medium.com/@calerogers/gpu-virtualization-with-kvm-qemu-63ca98a6a172)
 by Cale Rogers

- [vfio-gpu-how-to-series](http://vfio.blogspot.com/2015/05/vfio-gpu-how-to-series-part-1-hardware.html) by Alex Williamson

- [virtualization-hypervisors-explaining-qemu-kvm-libvirt](https://sumit-ghosh.com/articles/virtualization-hypervisors-explaining-qemu-kvm-libvirt/) by Sumit Ghosh

## usage in kubernetes

- [Schedule GPUs in K8s](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/#deploying-amd-gpu-device-plugin)

## installation of Nvidia Container Toolkit

- [install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## installation with intel GVT-g

```bash
# in /etc/default/grub
i915.enable_gvt=1 intel_iommu=igfx_off kvm.ignore_msrs=1 kvm.report_ignored_msrs=0

#if you do not use a bootloader.
# boot with EFISTUB so you efibootmgr commandline looks like this:
efibootmgr --disk /dev/nvme0n1 --part 1 --create --label "Arch Linux" /
--loader /vmlinuz-linux --unicode 'root=/dev/nvme0n1p2 rw initrd=\initramfs-linux.img i915.enable_gvt=1  intel_iommu=igfx_off kvm.ignore_msrs=1 kvm.report_ignored_msrs=0' --verbose

#Create a dedicated folder for your virtual machine assets, including virtual disks and UEFI variable stores.

mkdir ~/vms
cd ~/vms

# Generate a random UUID for the next step
uuidgen

# Create Intel GVT-g device
# This step must be run each time you reboot your Linux host
# If i915-GVTg_V5_2 is not available you must go to BIOS settings and even potentially change Thunderbolt security settings to allow the GPU to address more memory
sudo su -c "echo 5b9fa453-8b2f-413c-aa19-cfba99ffbed9 > /sys/devices/pci0000\:00/0000\:00\:02.0/mdev_supported_types/i915-GVTg_V5_2/create"

# Create disk for Windows 10 installation
qemu-img create -f qcow2 win10.qcow2 40G

# Convert the qemu disk image to a compressed image and replace the original
qemu-img convert win10.qcow2 -O qcow2 win10.c.qcow2 -c
mv -v win10.c.qcow2 win10.qcow2

# Create a writable UEFI variable store based on the UEFI defaults
cp /usr/share/ovmf/x64/OVMF_VARS.fd my_uefi_vars.bin

# Download Windows 10 virtio drivers
curl -LO https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Create a memory pool for the virtual machine using Linux hugepages.
# 2000 hugepages is enough for ~4000 RAM allocated in QEMU if each is ~2MB
sudo su -c "echo 2000 > /proc/sys/vm/nr_hugepages"

# Check to make sure we actually have the number of huge pages we want
sudo grep -i hugepages /proc/meminfo
```

## VM installation execution

```bash
sudo qemu-system-x86_64 \
-cpu host \
-enable-kvm \
-smp cores=$(nproc),threads=1,sockets=1 \
-rtc clock=host,base=localtime \
-device virtio-rng-pci \
-drive if=pflash,format=raw,readonly,file=/usr/share/ovmf/x64/OVMF_CODE.fd \
-drive if=pflash,format=raw,file=my_uefi_vars.bin \
-drive file=win10.qcow2,if=virtio \
-drive file=virtio-win.iso,media=cdrom \
-nic user,model=virtio-net-pci,smb="$(realpath shared)" \
-m 4000M \
-mem-path /dev/hugepages \
-mem-prealloc \
-k en-us \
-machine kernel_irqchip=on \
-global PIIX4_PM.disable_s3=1 -global PIIX4_PM.disable_s4=1 \
-parallel none -serial none \
-vga none \
-display gtk,gl=on \
-device vfio-pci-nohotplug,sysfsdev=/sys/bus/pci/devices/0000\:00\:02.0/5b9fa453-8b2f-413c-aa19-cfba99ffbed9,x-igd-opregion=on,romfile=vbios_gvt_uefi.rom,ramfb=on,display=off

```

Navigate to D:\NetKVM\w10\amd64, and right click on the netkvm (setup information) file where D:\ is the disk drive associated with the virtio disk. Select the “Install” option from the context menu. When installing drivers such as the virtio drivers from the Fedora CDROM the VM may appear to completely lock-up for a few minutes. Be patient!

After installation and after first boot, install the network virtio driver from the CDROM as well for internet access. Also install the RNG and Balloon virtio drivers.

After setup is complete, go to Windows Device Manager. I expanded the “Display Adapters” section and left it open for two minutes while doing nothing. Out of nowhere the first display adapter was replaced with “Intel UHD Graphics 620.” I did not have to manually install it.

If Windows does not automatically install the Intel driver, wait up to 15 minutes with the Device Manager open to the Display Adapter section then manually force the driver installation. Find the display adapter with the triangle and exclamation point and right click on it. Select “Update Driver” to download and install the Intel graphics driver. This froze up my entire virtual machine UI for a few minutes. If the driver download part succeeds be patient with the installation. It will unfreeze after a few minutes.

**Do not proceed unless you can see Intel UHD Graphics listed in the Display Adapters section of the Windows Device Manager.**

## normal execution

```bash
sudo qemu-system-x86_64 \
-cpu host \
-enable-kvm \
-smp cores=$(nproc),threads=1,sockets=1 \
-rtc clock=host,base=localtime \
-device virtio-rng-pci \
-drive if=pflash,format=raw,readonly,file=/usr/share/ovmf/x64/OVMF_CODE.fd \
-drive if=pflash,format=raw,file=my_uefi_vars.bin \
-drive file=win10.qcow2,if=virtio \
-drive file=virtio-win.iso,media=cdrom \
-nic user,model=virtio-net-pci,smb="$(realpath shared)" \
-m 4000M \
-mem-path /dev/hugepages \
-mem-prealloc \
-k en-us \
-machine kernel_irqchip=on \
-global PIIX4_PM.disable_s3=1 -global PIIX4_PM.disable_s4=1 \
-parallel none -serial none \
-vga none \
-display gtk,gl=on \
-device vfio-pci-nohotplug,sysfsdev=/sys/bus/pci/devices/0000\:00\:02.0/5b9fa453-8b2f-413c-aa19-cfba99ffbed9,x-igd-opregion=on,romfile=vbios_gvt_uefi.rom,ramfb=on,display=on
```

## Fix QEMU graphics refresh rate

Despite enabling graphics acceleration our virtual machine graphics are fixed to a low framerate which makes interaction with the virtual machine very choppy and generally unpleasant.

```git
diff --unified --recursive --text qemu-4.2.0/include/ui/console.h qemu-4.2.0.new/include/ui/console.h
--- qemu-4.2.0/include/ui/console.h     2019-12-12 13:20:48.000000000 -0500
+++ qemu-4.2.0.new/include/ui/console.h 2020-04-07 14:50:19.995242274 -0400
@@ -26,7 +26,7 @@
 #define QEMU_CAPS_LOCK_LED   (1 << 2)

 /* in ms */
-#define GUI_REFRESH_INTERVAL_DEFAULT    30
+#define GUI_REFRESH_INTERVAL_DEFAULT    16
 #define GUI_REFRESH_INTERVAL_IDLE     3000

 /* Color number is match to standard vga palette */
```

## Additional remarks and gotchas

Hyper-V CPU flags for QEMU cause issues with the Intel Graphics Driver so do not use them.

QEMU Hyper-V flags look like this:

```bash
-cpu host,hv_spinlocks=0x1fff,hv_vapic,hv_time,hv_reset,hv_vpindex,hv_runtime,hv_relaxed,hv_synic,hv_stimer,hv_tlbflush,hv_ipi

# USB support - may cause stuttering - root causes not known
-device qemu-xhci \
```

QEMU file sharing requires you to pass an absolute path to the right side of smb=

Use realpath to resolve relative path to the corresponding absolute path.

```bash
smb="$(realpath shared)"
```


__linux__

__mac__
