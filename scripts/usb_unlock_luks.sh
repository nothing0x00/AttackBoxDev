#!/bin/sh

lsblk

echo "Enter USB Device (/dev/sdb):"
read USB_DEVICE

echo "Enter Encrypted Partition (/dev/sda5):"
read LUKS_DEVICE

if [ ! -b $USB_DEVICE ]; then
    echo "USB device does not exist."
    exit
fi


if [ ! -b $LUKS_DEVICE ]; then
    echo "LUKS device does not exist." 
    exit
fi


#setup USB drive
echo ""
echo "Preparing USB File System"
echo ""
sfdisk --delete ${USB_DEVICE}
parted -a optimal ${USB_DEVICE} mkpart primary ext4 0% 100%
mkfs.ext4 -L KEY ${USB_DEVICE}1


#remove old key if exists on slot 1
echo ""
echo "If LUKS Slot 1 key exists, delete (requires Slot 0 passphrase)"
echo ""
cryptsetup luksKillSlot ${LUKS_DEVICE} 1


#setup new luks key
echo ""
echo "Create new LUKS Slot 1 Key (requires Slot 0 passphrase)"
echo ""
mkdir /root/usbkey
mount ${USB_DEVICE}1 /root/usbkey
dd if=/dev/urandom of=/root/usbkey/key.bin bs=4096 count=1
cryptsetup luksAddKey ${LUKS_DEVICE} /root/usbkey/key.bin
umount /root/usbkey


#update crypttab, modules, copy unlock_custom and initramfs
echo ""
echo "Setup crypttab and initramfs"
echo ""
cat ../configs/modules > /etc/initramfs-tools/modules
cp ../scripts/unlock_custom.sh /lib/cryptsetup/scripts/unlock_custom.sh
chmod 755 /lib/cryptsetup/scripts/unlock_custom.sh 
if [ ! -f /etc/crypttab.bak ]; then
    cp /etc/crypttab /etc/crypttab.bak
fi
sed -i "s|none luks|/dev/disk/by-label/KEY:/key.bin luks,keyscript=/lib/cryptsetup/scripts/unlock_custom.sh|g" /etc/crypttab
update-initramfs -k all -u
