# Bootable usb drive

1. download the iso of your choice somehwere

    ```bash
    export IMAGE_DIR="/home/max/Desktop/image_files/ubuntu"
    export IMAGE="jammy-live-server-amd64.iso"
    export ISO_URL="https://cdimage.ubuntu.com/ubuntu-server/daily-live/current/$IMAGE"

    wget -N -c -O Ubuntu.iso "${ISO_URL}"
    ```

2. burning the image

    ```bash
    # disk configuration
    sudo fdisk -l |grep "Disk /dev/"

    # im making the assumption that it will be the only other disk
    export DISK_NAME="/dev/sdb"
  
    # unmount the disk
    sudo umount "$DISK_NAME"

    ## dd the image to the drive

    sudo dd \
      bs=4M \
      if="$IMAGE_DIR"/"$IMAGE_FILE" \
      of="$DISK_NAME" \
      status=progress \
      oflag=sync

    ```
