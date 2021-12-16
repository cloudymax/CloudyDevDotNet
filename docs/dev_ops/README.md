# Cloud-init

> Cloud-init is the MUCH needed replacement for Ubuntu Pre-Seed.
Ubuntu pre-seed was the way to automate the initial setup of ubuntu images and it was literally the worst. CLoud-init replaces it with a system integrated into the Ubuntu (and other linux distro) boot process directly (similar to old-timey hacking on rc.local but better). It uses YAML and has great documentation. 10/10
>
>[Cloud Init Docs and Examples](https://cloudinit.readthedocs.io/en/latest/topics/examples.html)
>
>[Multipass launch command docs](https://multipass.run/docs/launch-command)


1. Example Cloud-Init yaml config file:

    ??? Example "cloudinit cloud-config"
      
        ```yaml
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
    
2. Creating a multipass VM using cloud init


    ??? Example "Multipass w/ Cloud-init"

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

        # creating a ssh key
        ssh-keygen -C $VM_USER -f $VM_KEY

        #add to cloud init
        # write a cloud-init file that provisions the base VM/container etc..
        cat << EOF > cloud-init.yaml
        #cloud-config
        groups:
          - ubuntu: [root,sys]
          - docker
        users:
          - default
          - name: ${VM_USER}
            sudo: ALL=(ALL) NOPASSWD:ALL
            shell: /bin/bash
            groups: docker, admin, sudo, users
            no_ssh_fingerprints: true
            ssh-authorized-keys:
              - ${VM_KEY}
        apt:
          primary:
            - arches: [default]
              uri: http://us.archive.ubuntu.com/ubuntu/
          sources:
            docker.list:
              source: deb [arch=amd64] https://download.docker.com/linux/ubuntu ${VM_IMAGE} stable
              keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88
            kubectl.list:
              source: deb [arch=amd64] https://apt.kubernetes.io/ kubernetes-xenial main
              keyid: 59FE0256827269DC81578F928B57C5C2836F4BEB
        packages:
          - apt-transport-https
          - ca-certificates
          - curl
          - cpu-checker
          - rsync
        package_update: true
        package_upgrade: true
        package_reboot_if_required: true
        runcmd:
          - [ sed , -i , "s/#PermitRootLogin prohibit-password/PermitRootLogin no/g" , /etc/ssh/sshd_config ]
        EOF
        }

        # Stop, delete, purge previous versions of the VM
        multipass stop -all
        multipass delete -all
        multipass purge

        # Start the new VM using the cloud-init.yaml we created

        multipass launch --name $VM_NAME \
            --cpus $VM_CPUS \
            --disk $VM_DISK \
            --mem $VM_MEM \
            --cloud-init $VM_INIT \
            $VERBOSITY

        # export info about the VM and filter to get the IP

        export VM_IP=$(multipass info $VM_NAME | grep IPv4 |awk '{print $2}')

        # ssh to your vm using the ssh key we created

        ssh -i $VM_KEY $VM_USER@$VM_IP -o StrictHostKeyChecking=no -vvvv

        # Or on systems without custom security:

        multipass shell VirtualBradley

        ```

3. Using a multipass VM with ansible via Cloud-Init <3

    ??? Example "Ansible + Cloud-init"

        1. create a ssh key for the user and save as a file w/ prompt
        
            ```zsh
            ssh-keygen -C "$VM_USER" \
                -f "$VM_KEY_FILE" \
                -N '' \
                -t rsa
            ```

        2. write a cloud-init file that will insert out ssh key into the VM as it boots.
        
            ```zsh
            cat << EOF > cloud-init.yaml
            #cloud-config
            groups:
              - ubuntu: [root,sys]
              - docker
            users:
              - default
              - name: <SOME USER>
                sudo: ALL=(ALL) NOPASSWD:ALL
                shell: /bin/bash
                groups: docker, admin, sudo, users
                no_ssh_fingerprints: true
                ssh-authorized-keys:
                  - <SOME SSH KEY>
            apt:
              sources:
                docker.list:
                  source: deb [arch=amd64] https://download.docker.com/linux/ubuntu ${VM_IMAGE} stable
                  keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88
            packages:
              - apt-transport-https
              - ca-certificates
              - curl
            package_update: true
            package_upgrade: true
            package_reboot_if_required: true
            runcmd:
              - [ sed , -i , "s/#PermitRootLogin prohibit-password/PermitRootLogin no/g" , /etc/ssh/sshd_config ]
            EOF
            }
            ```

        3. Create the base VM
            
            ```zsh
            multipass launch --name $VM_NAME \
                --cpus $VM_CPUS \
                --disk $VM_DISK \
                --mem $VM_MEM \
                $VM_IMAGE \
                --cloud-init $VM_INIT \
                $VERBOSITY
            ```

        4. grab the new VM's IP
        
            ```zsh
            multipass start $VM_NAME
            VM_IP=$(multipass list |grep "${VM_NAME}" |awk '{print $3}')
            multipass exec -vvvv $VM_NAME -- sudo ufw allow 22/tcp
            multipass exec -vvvv $VM_NAME -- sudo systemctl reload sshd
            ```

        5. Create the ansible inventory file
        
            ```zsh
            cat << EOF > inventory.yaml
            webservers:
              hosts:
                ${VM_NAME}:
                  ansible_connection: ssh
                  ansible_host: ${VM_IP}
                  ansible_ssh_user: ${VM_USER}
                  ansible_ssh_port: ${SSH_PORT}
                  ansible_ssh_common_args: "-o StrictHostKeyChecking=no -o ControlMaster=auto -o"
                  ansible_ssh_private_key_file: ${VM_KEY_FILE}
            EOF
            ```

        6. open a ssh connections into the VM
        
            ```zsh
            ssh -i $VM_KEY_FILE \
                $VM_USER@$VM_IP \
                -o StrictHostKeyChecking=no \
                -p $SSH_PORT \
                -vvvv -t \
                /bin/bash
            ```