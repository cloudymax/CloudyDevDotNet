# Virtual Machines w/ cloud-init

https://multipass.run/docs/launch-command

https://cloudinit.readthedocs.io/en/latest/topics/examples.html

```yaml
# cloud-config
# examples https://cloudinit.readthedocs.io/en/latest/topics/examples.html
groups:
  - ubuntu: [root,sys]
  - cloud-users
users:
  - default
  - name: someUser
    sudo:  ALL=(ALL) NOPASSWD:ALL
    no_ssh_fingerprints: true
    ssh-authorized-keys:
        - ssh-rsa someData= someUser
apt_mirror: http://archive.ubuntu.com/ubuntu
package_update: true
drivers:
  nvidia:
    license-accepted: true
disable_root: true
disable_root_opts: no-port-forwarding,no-agent-forwarding,no-X11-forwarding,command="echo 'Please login as the user \"$USER\" rather than the user \"root\".';echo;sleep 10"
phone_home:
 url: http://my.example.com/$INSTANCE_ID/
 post: [ pub_key_dsa, pub_key_rsa, pub_key_ecdsa, instance_id ]
 tries: 10

```

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
