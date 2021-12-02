# [multipass](https://multipass.run/)

Multipass is a lightweight VM manager for Linux, Windows and macOS. It's designed for developers who want a fresh Ubuntu environment with a single command. It uses KVM on Linux, Hyper-V on Windows and HyperKit on macOS to run the VM with minimal overhead. It can also use VirtualBox on Windows and macOS. Multipass will fetch images for you and keep them up to date.

Since it supports metadata for cloud-init, you can simulate a small cloud deployment on your laptop or workstation.

- [github.com/canonical/multipass](https://github.com/canonical/multipass)
- [KVM](https://www.redhat.com/en/topics/virtualization/what-is-KVM)

__What makes it unique versus other VM solutions?__

- It's very minimal, it only makes Ubuntu cloud-compatible VMs
- provides a consistent Ubuntu experince w/ the benefit of cliud-init.
- SSH disabled by default, you use cloud-init to place keys and bootstrap your users
- much more analogous to a cloud-native workflow - especially GCP
- installs natively w/ package manegers to mac/linux/windows
- can be managed by Oracle Virtual Box for more customization

__Thoughts__:

- fastest option for getting a Ubuntu LTS virtual machine up and running

- not very automation friendly - ansible seems to hate it - WIP though: update - cloud init was the issue, and its working now :)

- potentially a good solution for getting around [Docker for MacOS's horrible IO issues](https://github.com/docker/for-mac/issues/3677) w/ mount points

## install

Linux:

```bash
sudo snap install multipass
```

Windows:
Download from [link](https://multipass.run/download/windows) or use WSL

MacOS:
Download from [link](https://multipass.run/download/macos)

or

```bash
curl -O https://multipass.run/download/macos
```

[multipass launch docs](https://multipass.run/docs/launch-command)
[cloud init](https://cloudinit.readthedocs.io/en/latest/topics/examples.html)

```bash
export FORMAT="yaml" \
export VM_NAME="BeautifulBradley" \
export VM_CPUS="4" \
export VM_DISK="4G" \
export VM_MEM="4G" \
export VERBOSITY="-vvvvvv" \
export VM_INIT="cloud-init.yaml" \
export VM_KEY="cloudymax" \
export VM_IP="none" \
export VM_USER="vmadmin"

ssh-keygen -C $VM_USER -f $VM_KEY

#add to cloud init

multipass stop -all
multipass delete -all
multipass purge

multipass launch --name $VM_NAME \
    --cpus $VM_CPUS \
    --disk $VM_DISK \
    --mem $VM_MEM \
    --cloud-init $VM_INIT \
    $VERBOSITY

export VM_IP=$(multipass info $VM_NAME | grep IPv4 |awk '{print $2}')

ssh -i $VM_KEY $VM_USER@$VM_IP -o StrictHostKeyChecking=no -vvvv

```

```bash
multipass shell VirtualBradley
```

## VirtualBox integration

```bash
# enable
sudo multipass set local.driver=virtualbox

# disable
sudo multipass set local.driver=hyperkit

#other backends
libvirt|hyperv
```
