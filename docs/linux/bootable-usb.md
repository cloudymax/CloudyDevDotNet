# Bootable usb drive

1. download the iso of your choice somehwere

    ```bash
    export IMAGE_DIR="/home/max/Desktop/image_files/ubuntu"
    export IMAGE_FILE="ubuntu-18.04.5-desktop-amd64.iso"
    ```

2. burning the image

    ```bash
    # disk configuration

    sudo fdisk -l |grep "Disk /dev/"

    export DISK_NAME="/dev/sdb"

    sudo umount "$DISK_NAME"

    sudo dd bs=4M if=$IMAGE_DIR/$IMAGE_FILE of="$DISK_NAME" status=progress oflag=sync

    ```
