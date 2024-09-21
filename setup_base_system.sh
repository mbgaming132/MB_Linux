#!/bin/bash

# Variables
TARGET_DIR="mb_linux_base"
DEBIAN_VERSION="bookworm"
ARCH_MIRROR="https://mirror.rackspace.com/archlinux"

# Create the target directory
mkdir -p $TARGET_DIR

# Bootstrap the minimal Debian system
sudo debootstrap --arch=amd64 $DEBIAN_VERSION $TARGET_DIR http://deb.debian.org/debian/

# Mount necessary filesystems
sudo mount --bind /dev $TARGET_DIR/dev
sudo mount --bind /proc $TARGET_DIR/proc
sudo mount --bind /sys $TARGET_DIR/sys

# Copy the script to configure the chroot environment
sudo tee $TARGET_DIR/setup_chroot.sh > /dev/null <<EOF
#!/bin/bash
# Add Ubuntu 24.04 repositories
echo "deb http://archive.ubuntu.com/ubuntu/ lunar main universe" > /etc/apt/sources.list.d/ubuntu.list

# Add Arch Linux repositories
echo "[archlinux]" > /etc/pacman.d/archlinux.repo
echo "Server = $ARCH_MIRROR/\$repo/os/\$arch" >> /etc/pacman.d/archlinux.repo

# Install necessary packages
apt update
apt install -y sudo arch-install-scripts pacman

# Set up Pacman
echo "[options]" > /etc/pacman.conf
echo "Architecture = auto" >> /etc/pacman.conf
echo "Include = /etc/pacman.d/archlinux.repo" >> /etc/pacman.conf

# Install yay for AUR support
sudo pacman -Syu --noconfirm yay

# Clean up
apt clean
rm /setup_chroot.sh

exit
EOF

# Make the script executable
sudo chmod +x $TARGET_DIR/setup_chroot.sh

# Enter the chroot environment and run the configuration script
sudo chroot $TARGET_DIR /setup_chroot.sh

# Unmount filesystems
sudo umount $TARGET_DIR/dev
sudo umount $TARGET_DIR/proc
sudo umount $TARGET_DIR/sys

echo "Base system setup complete. You can now chroot into $TARGET_DIR to continue configuration."

