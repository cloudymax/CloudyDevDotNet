# why can I never remeber this

1. place to save the Host private key the Host private key stays secret

    ```bash
    export KEY_FILE="/Users/4008575/.ssh/BigBradley"
    yes |ssh-keygen -b 2048 -f "${KEY_FILE}" -t rsa -q -N ""
    ```

2. copy the host's PUBLIC key into the clients

    ```bash
    export LOCAL_USER="xxxxxx"
    export REMOTE_USER="xxx"
    export REMOTE_HOST="xxx.xxx.xxx.xxx"

    ssh-copy-id -i $KEY_FILE \
    -o StrictHostKeyChecking=no \
    -o ControlMaster=no \
    -o ControlPath=none \
    $REMOTE_USER@$REMOTE_HOST

    ssh -i $KEY_FILE \
    -o StrictHostKeyChecking=no \
    -o ControlMaster=no \
    -o ControlPath=none \
    $REMOTE_USER@$REMOTE_HOST
    ```

3. the long way

    ```bash
    cat $KEY_FILE | ssh -i $REMOTE_USER@$REMOTE_HOST "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
    
    #push
    scp -i $KEY_FILE $KEY_FILE $REMOTE_USER@$REMOTE_HOST:~/.ssh/authorized_keys
    
    #pull
    scp $REMOTE_USER@$REMOTE_HOST:/home/$REMOTE_USER/.ssh/id_rsa.pub /home/$LOCAL_USER/.ssh/authorized_keys
    
    
    yes |ssh-keygen -b 2048 -f "${KEY_FILE}" -t rsa -q -N ""
    touch ./cloud-init.yaml
    cat $KEY_FILE.pub
    ssh-keygen -R $IP_ADDRESS
    
    ```
