#!/bin/sh

lsblk

echo "Enter USB Device (/dev/sda):"
read USB_DEVICE

echo "Enter Encrypted Partition (/dev/nvme0n1p3):"
read LUKS_DEVICE

if [ ! -b $USB_DEVICE ]; then
    echo "USB device does not exist."
    exit
fi


if [ ! -b $LUKS_DEVICE ]; then
    echo "LUKS device does not exist." 
    exit
fi


#remove old key if exists on slot 1
echo ""
echo "If LUKS Slot 1 key exists, delete (requires Slot 0 passphrase)"
echo ""
cryptsetup luksKillSlot ${LUKS_DEVICE} 1


#setup new luks key
echo ""
echo "Create new LUKS Slot 1 Key (requires Slot 0 passphrase)"
echo ""
rmdir /root/usbkey
mkdir /root/usbkey
mount ${USB_DEVICE}1 /root/usbkey
shred -u /root/usbkey/key.bin
umount /root/usbkey
