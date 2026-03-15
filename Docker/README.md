# BuildKit server configuration
Turning a single EC2 into a dedicated BuildKit server that supports your multi-language builds with per-language caches. This will use local NVMe storage but is also compatible with optional EBS persistence.

We’ll cover:
- OS and Docker setup
- BuildKit configuration (buildkitd.toml)
- Cache directories per technology
- Buildx builder creation
- Bootstrap command for CI SSH usage

## Step 1: Launch EC2
**Instance type:** c6i.xlarge (or any NVMe-supported instance)
**OS:** Ubuntu 22.04 LTS (or your preferred Linux)
**Storage:**
- Primary NVMe instance store for BuildKit cache → 400GB
- Optional EBS if you want persistence

### SSH into the instance:
```bash
ssh ubuntu@<EC2_IP>
```

## Step 2: Install Docker and BuildKit
```bash
# Update OS
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker
docker version

# Enable BuildKit
export DOCKER_BUILDKIT=1
```
## Step 3: Create cache directories
**Create per-language cache on NVMe (or EBS mount):**
```bash
# Suppose the volume is /dev/nvme1n1
sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir -p /mnt/buildkit-cache
sudo mount /dev/nvme1n1 /mnt/buildkit-cache
sudo chown -R ubuntu:ubuntu /mnt/buildkit-cache
```
**Mount permanently**
```bash
lsblk
```
Example output:
```bash
NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
nvme0n1      259:0    0    8G  0 disk 
└─nvme0n1p1  259:1    0    8G  0 part /
nvme1n1      259:1    0  400G  0 disk 
```
**Get UUID of the volume**
```bash
sudo blkid /dev/nvme1n1

# Example output:
/dev/nvme1n1: UUID="f1a2b3c4-d5e6-7890-ab12-34567890cdef" TYPE="ext4"
```
**Edit /etc/fstab**
```bash
sudo vi /etc/fstab
UUID=f1a2b3c4-d5e6-7890-ab12-34567890cdef /mnt/buildkit-cache ext4 defaults,nofail 0 2
```
**Explanation:**
- UUID: Volume UUID from blkid
- Mount point: /mnt/buildkit-cache
- FS type: ext4
- Options: defaults,nofail → mount automatically, but don’t fail boot if missing
- Dump: 0 (unused)
- Pass: 2 (fsck order)
### Test the fstab entry
- No errors → fstab entry works
```bash
sudo mount -a
```
- Check mount:
```bash
df -h | grep buildkit
```
**Expected o/p:**
```bash
/dev/nvme1n1  400G   1G  399G  1% /mnt/buildkit-cache
```

```bash
sudo mkdir -p /mnt/buildkit-cache/python
sudo mkdir -p /mnt/buildkit-cache/node
sudo mkdir -p /mnt/buildkit-cache/java
sudo mkdir -p /mnt/buildkit-cache/go
sudo chown -R $USER:$USER /mnt/buildkit-cache
```
## Step 4: Configure buildkitd
**Create /etc/buildkit/buildkitd.toml:**
```bash
debug = false

[worker.oci]
  gc = true
  gckeepstorage = 80000000000  # max 80GB per worker (adjust as needed)

[[worker.oci.gcpolicy]]
  keepBytes = 20000000000      # ~20GB per cache scope
  keepDuration = 604800        # 7 days

[[worker.oci.gcpolicy]]
  keepBytes = 20000000000
```
**Explanation:**
- gc = true → enables automatic garbage collection
- gckeepstorage → max disk usage for cache
- gcpolicy → keep ~20GB per cache scope (Python, Node, Java, Go)

**Start BuildKit daemon:**
```bash
sudo buildkitd --config /etc/buildkit/buildkitd.toml &
```
**Verify BuildKit is running:**
```bash
ps aux | grep buildkitd
```
## Step 5: Create Buildx builder
```bash
docker buildx create --name shared-builder --use
docker buildx ls
```
**Note:** This ensures all builds go through BuildKit.
## Step 5: CI bootstrap command (SSH)
From your CI server, you can SSH and run builds directly:
```bash
ssh ubuntu@<EC2_IP> << 'EOF'
export DOCKER_BUILDKIT=1

docker buildx create --use

# Example: Node build
docker buildx build \
  --cache-from type=local,src=/mnt/buildkit-cache/node \
  --cache-to type=local,dest=/mnt/buildkit-cache/node,mode=max \
  -t demo-node .

# Example: Python build
docker buildx build \
  --cache-from type=local,src=/mnt/buildkit-cache/python \
  --cache-to type=local,dest=/mnt/buildkit-cache/python,mode=max \
  -t demo-python .
EOF
```
- --cache-from → pull previous cache for that language
- --cache-to → push new cache after build
- mode=max → keep maximum cache possible for reuse

## Step 6: Dockerfile best practice
Use BuildKit cache mounts for dependencies:
**Node.js example:**
```bash
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm install
COPY . .
CMD ["node","server.js"]
```
**Python example:**
```bash
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY . .
CMD ["python","app.py"]
```
This ensures dependency caches don’t blow up your 20GB limit and reuse layers efficiently.
