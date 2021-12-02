# 🧨 firecracker microVMs 💻

[Firecracker](https://firecracker-microvm.github.io/)microVM's using [KVM](https://www.redhat.com/en/topics/virtualization/what-is-KVM) are an interesting contender in this space as they provide the full machine via KVM directly to metal but can be overprovisioned.

Firecraker was developed by Amazon for use w/ AWS EC2 Fargate and Lambda to sol the following problems:

- High overhead for dedicated VM's per-tenant
- Under-Uitilization of metal assets
- Multi-tenant cluster security
- Ephemerality for Serverless systems

__Pros__:

- __Fast__. __as__. __hell__. Instantiates in ~__125ms__, throughput of __150VMs__ per second, __*per host*__.
- Multi-tenant __secure__ by running in a VM using KVM instad of a container.
- __Over provisionable__ so thousands fit on a single node
- __Compatible w/ containrd__ to be managed like a container [firecracker-containerd](https://github.com/firecracker-microvm/firecracker-containerd)

__Cons__:

- No GPU support/ passthrough. __ever__. That requires pinning memory addresses, which negates the ability to over-provision

__Thoughs__:

- If you're processing lots of databse queries, small data transformations or messaging - firecraker is an incrible way to achieve
high-density workload saturation. It's fast, efficient, and it's a tailor-made solution for serverless systems.

- If youre workloads need GPU acceleration, lifecycle management, high uptime, or consume lots of resources over a longer duration, I dont think firecracker is your best option here.


```bash
export RELEASE_URL="https://github.com/firecracker-microvm/firecracker/releases"
export LATEST=$(basename $(curl -fsSLI -o /dev/null -w  %{url_effective} ${RELEASE_URL}/${LATEST}))
export ARCH=`uname -m`

curl -L ${RELEASE_URL}/download/${LATEST}/firecracker-${LATEST}-${ARCH}.tgz \
| tar -xz
mv release-${LATEST}/firecracker-${$LATEST}-$(uname -m) firecracker

# uncompressed Linux kernel binary
curl -O https://s3.amazonaws.com/spec.ccfc.min/img/quickstart_guide/x86_64/kernels/vmlinux.bin

# ext4 file system image
curl -O https://s3.amazonaws.com/spec.ccfc.min/img/hello/fsfiles/hello-rootfs.ext4

# Now, let's open up two shell prompts:
# one to run Firecracker,
# and another one to control it (by writing to the API socket)

# Shell A:
# clear the socket
rm -f /tmp/firecracker.socket

# start Firecracker
./firecracker --api-sock /tmp/firecracker.socket

#Shell B:
uname -m
#>x86_64

export kernel_path=$(pwd)"/hello-vmlinux.bin"

curl --unix-socket /tmp/firecracker.socket -i \
   -X PUT 'http://localhost/boot-source'   \
   -H 'Accept: application/json'           \
   -H 'Content-Type: application/json'     \
   -d "{
             \"kernel_image_path\": \"${kernel_path}\",
         \"boot_args\": \"console=ttyS0 reboot=k panic=1 pci=off\"
    }"

rootfs_path=$(pwd)"/hello-rootfs.ext4"
curl --unix-socket /tmp/firecracker.socket -i \
  -X PUT 'http://localhost/drives/rootfs' \
  -H 'Accept: application/json'           \
  -H 'Content-Type: application/json'     \
  -d "{
        \"drive_id\": \"rootfs\",
        \"path_on_host\": \"${rootfs_path}\",
        \"is_root_device\": true,
        \"is_read_only\": false
   }"

curl --unix-socket /tmp/firecracker.socket -i \
  -X PUT 'http://localhost/actions'       \
  -H  'Accept: application/json'          \
  -H  'Content-Type: application/json'    \
  -d '{
      "action_type": "InstanceStart"
   }'
```
