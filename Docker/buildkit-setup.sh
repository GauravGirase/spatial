#!/bin/bash
# =========================================
# BuildKit Server Bootstrap Script
# =========================================
# Usage: sudo bash bootstrap-buildkit.sh <EBS_DEVICE>
# Example: sudo bash bootstrap-buildkit.sh /dev/nvme1n1
# =========================================

set -e

EBS_DEVICE="$1"
MOUNT_POINT="/mnt/buildkit-cache"

if [ -z "$EBS_DEVICE" ]; then
    echo "Usage: sudo $0 <EBS_DEVICE> (e.g., /dev/nvme1n1)"
    exit 1
fi

echo "=== Updating OS ==="
apt update && apt upgrade -y

echo "=== Installing Docker ==="
apt install -y docker.io

echo "=== Adding current user to docker group ==="
usermod -aG docker $USER
newgrp docker

echo "=== Enabling BuildKit ==="
export DOCKER_BUILDKIT=1

echo "=== Installing Buildx (if not present) ==="
docker buildx version >/dev/null 2>&1 || docker buildx install

echo "=== Setting up cache volume: $EBS_DEVICE ==="
# Format volume if not already formatted
if ! blkid $EBS_DEVICE >/dev/null 2>&1; then
    mkfs.ext4 $EBS_DEVICE
fi

# Create mount point
mkdir -p $MOUNT_POINT
mount $EBS_DEVICE $MOUNT_POINT
chown -R $USER:$USER $MOUNT_POINT

# Get UUID for fstab
UUID=$(blkid -s UUID -o value $EBS_DEVICE)

# Add to /etc/fstab if not already present
grep -q "$UUID" /etc/fstab || echo "UUID=$UUID $MOUNT_POINT ext4 defaults,nofail 0 2" >> /etc/fstab

echo "=== Creating per-language cache directories ==="
for lang in python node java go; do
    mkdir -p $MOUNT_POINT/$lang
    chown -R $USER:$USER $MOUNT_POINT/$lang
done

echo "=== Installing BuildKit daemon ==="
apt install -y buildkit

echo "=== Creating BuildKit config ==="
CONFIG_FILE="/etc/buildkit/buildkitd.toml"
mkdir -p /etc/buildkit
cat <<EOF > $CONFIG_FILE
debug = false

[worker.oci]
  gc = true
  gckeepstorage = 80000000000

[[worker.oci.gcpolicy]]
  keepBytes = 20000000000
  keepDuration = 604800

[[worker.oci.gcpolicy]]
  keepBytes = 20000000000
EOF

echo "=== Starting BuildKit daemon ==="
nohup buildkitd --config $CONFIG_FILE > /var/log/buildkitd.log 2>&1 &

echo "=== Creating Buildx builder ==="
docker buildx create --name shared-builder --use

echo "=== BuildKit Server Bootstrap Completed ==="
echo "Cache mount: $MOUNT_POINT"
echo "Per-language directories: python, node, java, go"
echo "Buildx builder name: shared-builder"
