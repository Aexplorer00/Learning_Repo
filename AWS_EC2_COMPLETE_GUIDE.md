# 🖥️ AWS EC2 Complete Deep Dive

**2-Hour Session: Everything about EC2**

---

# Part 1: EC2 Fundamentals

## What is EC2?
- **Elastic Compute Cloud** - Virtual servers in AWS
- You rent compute capacity by the hour/second
- Full control over OS, software, configuration

---

## EC2 Instance Lifecycle

```
Launch → Pending → Running → Stopping → Stopped → Terminated
                       ↓
                  Rebooting
```

| State | Description | Billing |
|-------|-------------|---------|
| **Pending** | Starting up | No |
| **Running** | Active | Yes |
| **Stopping** | Shutting down | No |
| **Stopped** | Off, can restart | No (EBS charged) |
| **Terminated** | Deleted permanently | No |

**Key Point:** Stopped ≠ Terminated. Stopped instances can be started again!

---

# Part 2: Instance Types

## Naming Convention
```
m5.large
│ │  │
│ │  └── Size (nano, micro, small, medium, large, xlarge, 2xlarge...)
│ └──── Generation (5th gen of M family)
└────── Family
```

## Instance Families

| Family | Optimized For | Example Use Case |
|--------|---------------|------------------|
| **T** (t3, t4g) | Burstable, general | Dev/test, small web |
| **M** (m5, m6i) | Balanced | App servers, backends |
| **C** (c5, c6i) | Compute (CPU) | Batch processing, ML |
| **R** (r5, r6i) | Memory | Databases, caching |
| **I** (i3) | Storage IOPS | NoSQL, data warehousing |
| **G/P** (g4, p4) | GPU | ML training, video |
| **X** (x2) | Extreme memory | SAP HANA, in-memory DBs |

## T-Series Burstable Explained

T instances have **CPU credits**:
- Baseline: ~20% CPU usage
- Earn credits when idle
- Spend credits when bursting (up to 100% CPU)
- Credits depleted → throttled to baseline

**T3 Unlimited:** Pay for extra credits (no throttling)

### Interview Question:
> "When would you NOT use a T instance?"
> 
> "When workload needs **consistent** high CPU. T instances are for sporadic bursts. For steady high CPU, use C-series."

---

# Part 3: Launching an Instance

## Step-by-Step Process

### 1. Choose AMI (Amazon Machine Image)
- **What:** Template with OS and software
- **Types:**
  - **Amazon Linux 2** - AWS optimized, free
  - **Ubuntu** - Popular Linux
  - **Windows Server** - Windows workloads
  - **Custom AMI** - Your own image

### 2. Choose Instance Type
- Match to workload (see above)

### 3. Configure Instance
- **Number of instances:** How many to launch
- **Network:** VPC and Subnet
- **IAM Role:** Permissions for AWS services
- **Placement Group:** Optional clustering
- **User Data:** Bootstrap script

### 4. Add Storage
- **Root Volume:** OS disk
- **Additional Volumes:** Data disks
- **Delete on Termination:** Yes/No

### 5. Add Tags
- Key-value pairs for organization
- Example: `Name=WebServer`, `Environment=Prod`

### 6. Configure Security Group
- Firewall rules (ports)

### 7. Review and Select Key Pair
- SSH access (Linux) or RDP password (Windows)

---

## CLI: Launch Instance

```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --count 1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'
```

---

# Part 4: Key Pairs

## What They Are
- **Public Key:** Stored in AWS, placed on instance
- **Private Key (.pem):** YOU keep, used to SSH

## Create Key Pair
```bash
# Create and save
aws ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text > my-key.pem

# Set permissions (Linux/Mac)
chmod 400 my-key.pem
```

## Connect via SSH
```bash
ssh -i my-key.pem ec2-user@<public-ip>
# For Ubuntu: ubuntu@<public-ip>
# For Amazon Linux 2: ec2-user@<public-ip>
```

## CRITICAL: Lost Key Recovery

**You CANNOT recover a lost .pem file!**

**Recovery Steps:**
1. Stop the instance
2. Detach root EBS volume
3. Attach to recovery instance
4. Mount volume: `sudo mount /dev/xvdf1 /mnt`
5. Add new public key: `echo "ssh-rsa AAAA..." >> /mnt/home/ec2-user/.ssh/authorized_keys`
6. Unmount: `sudo umount /mnt`
7. Detach volume
8. Reattach to original instance as root
9. Start instance

---

# Part 5: Security Groups

## What They Are
- Virtual firewall for EC2 instances
- Control inbound and outbound traffic
- **Stateful:** If inbound allowed, response auto-allowed

## Default Behavior
- **Inbound:** Deny all
- **Outbound:** Allow all

## Rules Structure
```
Type     | Protocol | Port Range | Source/Destination
---------|----------|------------|-------------------
SSH      | TCP      | 22         | My IP (x.x.x.x/32)
HTTP     | TCP      | 80         | 0.0.0.0/0 (anywhere)
HTTPS    | TCP      | 443        | 0.0.0.0/0
Custom   | TCP      | 5000       | sg-0123456 (another SG)
```

## CLI: Create Security Group
```bash
# Create SG
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Web server SG" \
  --vpc-id vpc-0123456789abcdef0

# Add SSH rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/24

# Add HTTP rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

## Best Practices
- ✅ Use least privilege (only open needed ports)
- ✅ Use source SG instead of IP when possible
- ✅ Don't use 0.0.0.0/0 for SSH (use your IP)
- ❌ Don't open all ports (0-65535)

---

# Part 6: EBS (Elastic Block Store)

## What It Is
- Network-attached storage for EC2
- Persists independently of instance
- Can attach/detach to different instances

## Volume Types

| Type | IOPS | Throughput | Use Case |
|------|------|------------|----------|
| **gp3** | 3,000-16,000 | 125-1,000 MB/s | General (default) |
| **gp2** | Burst 3,000 | - | Legacy general |
| **io1/io2** | Up to 64,000 | 1,000 MB/s | Databases |
| **st1** | 500 | 500 MB/s | Big data (HDD) |
| **sc1** | 250 | 250 MB/s | Cold data (HDD) |

## Root Volume vs Data Volume

| Aspect | Root Volume | Data Volume |
|--------|-------------|-------------|
| Purpose | OS | Application data |
| Delete on termination | Yes (default) | No (default) |
| Device name | /dev/xvda | /dev/xvdf, etc. |

## CLI: EBS Operations

### Create Volume
```bash
aws ec2 create-volume \
  --volume-type gp3 \
  --size 100 \
  --availability-zone us-east-1a
```

### Attach Volume
```bash
aws ec2 attach-volume \
  --volume-id vol-0123456789abcdef0 \
  --instance-id i-0123456789abcdef0 \
  --device /dev/sdf
```

### On EC2: Format and Mount (NEW VOLUME ONLY!)
```bash
# Check device
lsblk

# Format (ONLY for NEW volumes - destroys data!)
sudo mkfs -t ext4 /dev/xvdf

# Create mount point
sudo mkdir /data

# Mount
sudo mount /dev/xvdf /data

# Persist across reboots (add to fstab)
echo '/dev/xvdf /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

### Resize Volume (NO DOWNTIME!)
```bash
# 1. Modify volume in AWS
aws ec2 modify-volume --volume-id vol-xxx --size 200

# 2. Check modification progress
aws ec2 describe-volumes-modifications --volume-id vol-xxx

# 3. Extend partition (on EC2)
sudo growpart /dev/xvda 1

# 4. Extend filesystem
sudo resize2fs /dev/xvda1   # ext4
sudo xfs_growfs /data       # xfs
```

### Create Snapshot
```bash
aws ec2 create-snapshot \
  --volume-id vol-0123456789abcdef0 \
  --description "Daily backup"
```

---

# Part 7: User Data

## What It Is
- Script that runs on **first boot only**
- Used to bootstrap instances
- Runs as root

## Example: Install and Start Apache
```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from $(hostname)</h1>" > /var/www/html/index.html
```

## CLI: Launch with User Data
```bash
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type t3.micro \
  --user-data file://setup.sh
```

## View User Data
```bash
aws ec2 describe-instance-attribute --instance-id i-xxx --attribute userData
```

---

# Part 8: Instance Metadata

## What It Is
- Information about the running instance
- Available from INSIDE the instance only
- URL: `http://169.254.169.254/latest/meta-data/`

## Common Metadata

```bash
# Instance ID
curl http://169.254.169.254/latest/meta-data/instance-id

# Public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Private IP
curl http://169.254.169.254/latest/meta-data/local-ipv4

# Instance type
curl http://169.254.169.254/latest/meta-data/instance-type

# Availability Zone
curl http://169.254.169.254/latest/meta-data/placement/availability-zone

# IAM Role credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
```

## IMDSv2 (Secure Metadata)
```bash
# Get token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Use token
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id
```

---

# Part 9: Placement Groups

## Types

| Type | What | Use Case |
|------|------|----------|
| **Cluster** | Same rack, low latency | HPC, tightly coupled |
| **Spread** | Different hardware | Critical instances |
| **Partition** | Separate partitions | HDFS, HBase, Cassandra |

## CLI: Create Cluster Placement Group
```bash
aws ec2 create-placement-group \
  --group-name my-cluster \
  --strategy cluster
```

---

# Part 10: Pricing Models

| Model | Description | Savings | Best For |
|-------|-------------|---------|----------|
| **On-Demand** | Pay by hour/second | 0% | Variable workloads |
| **Reserved** | 1-3 year commitment | 30-75% | Steady workloads |
| **Spot** | Bid for unused capacity | Up to 90% | Fault-tolerant, flexible |
| **Savings Plans** | Commit $/hour | Similar to RI | Flexible |

## Spot Instances
- Can be interrupted with 2-minute warning
- Great for: Batch jobs, CI/CD, data analysis
- Not for: Databases, critical apps

---

# Part 11: Common CLI Commands

```bash
# List instances
aws ec2 describe-instances

# Filter running instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

# Start instance
aws ec2 start-instances --instance-ids i-xxx

# Stop instance
aws ec2 stop-instances --instance-ids i-xxx

# Terminate instance
aws ec2 terminate-instances --instance-ids i-xxx

# Reboot instance
aws ec2 reboot-instances --instance-ids i-xxx

# Get console output
aws ec2 get-console-output --instance-id i-xxx

# Create AMI from instance
aws ec2 create-image --instance-id i-xxx --name "My AMI"
```

---

# Part 12: Troubleshooting

## Instance Not Accessible via SSH

| Check | How |
|-------|-----|
| Instance running? | Console: State = running |
| Public IP? | Check if instance has public IP |
| Security Group? | Port 22 open from your IP? |
| Key pair correct? | `ssh -i right-key.pem` |
| Key permissions? | `chmod 400 key.pem` |
| Route table? | Subnet has route to IGW? |
| NACL? | Allows port 22? |

## Instance Not Connecting to Internet

| Check | Solution |
|-------|----------|
| Public subnet? | Must have route to IGW |
| Private subnet? | Needs NAT Gateway |
| Security Group | Outbound rules allow? |
| DNS? | VPC DNS enabled? |

## Check Instance Logs
```bash
# Console output (boot logs)
aws ec2 get-console-output --instance-id i-xxx

# System log (on instance)
journalctl -xe

# Cloud-init logs
cat /var/log/cloud-init-output.log
```

---

# Summary: Interview Cheat Sheet

| Topic | Key Points |
|-------|------------|
| **Instance Types** | T=burst, C=CPU, R=memory, M=balanced |
| **States** | Running (billing), Stopped (no billing), Terminated (gone) |
| **Security Groups** | Stateful firewall, instance level |
| **EBS** | gp3 default, resize with growpart+resize2fs |
| **Key Pairs** | Cannot recover lost .pem! Use volume swap |
| **User Data** | First boot only, runs as root |
| **Metadata** | 169.254.169.254, get instance info |
| **Pricing** | On-Demand, Reserved (1-3yr), Spot (up to 90% off) |

---

*Practice launching, connecting, and managing EC2 instances!*

---

# ✅ Hands-On Practice Completed (Jan 21, 2026)

## Session Summary
**Duration:** ~2 hours | **Region:** ap-south-1

---

## Exercises Completed

### 1. Launch EC2 Instance
```bash
# Created key pair
aws ec2 create-key-pair --key-name practice-key --query "KeyMaterial" --output text > practice-key.pem

# Got latest AMI
aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --query "Parameters[0].Value" --output text

# Launched t2.micro (Free Tier)
aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro --key-name practice-key
```

### 2. Connected via SSH (MobaXterm)
- Used MobaXterm with .pem key
- Username: `ec2-user`

### 3. Queried Instance Metadata
```bash
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/public-ipv4
curl http://169.254.169.254/latest/meta-data/placement/availability-zone
curl http://169.254.169.254/latest/meta-data/instance-type
```

### 4. EBS Volume - Create, Attach, Format, Mount
```bash
# Create volume (PowerShell)
aws ec2 create-volume --size 1 --volume-type gp2 --availability-zone ap-south-1a

# Attach (PowerShell)
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf

# Format (EC2 - MobaXterm)
lsblk
sudo mkfs -t ext4 /dev/xvdf

# Mount
sudo mkdir /data
sudo mount /dev/xvdf /data

# Create test file
echo "Hello from EBS" | sudo tee /data/hello.txt
cat /data/hello.txt
```

### 5. EBS Resize (NO DOWNTIME!) ⭐
```bash
# Resize from 1GB to 2GB (PowerShell)
aws ec2 modify-volume --volume-id vol-xxx --size 2

# Extend filesystem (EC2 - MobaXterm)
sudo resize2fs /dev/xvdf

# Verify
df -h /data  # Shows 2.0G now!
```

### 6. Snapshot & Restore
```bash
# Create snapshot
aws ec2 create-snapshot --volume-id vol-xxx --description "Practice backup"

# Create volume from snapshot
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone ap-south-1a --volume-type gp2
```

### 7. Clean Up
```bash
aws ec2 terminate-instances --instance-ids i-xxx
aws ec2 delete-volume --volume-id vol-xxx
aws ec2 delete-snapshot --snapshot-id snap-xxx
aws ec2 delete-key-pair --key-name practice-key

# Verify cleanup
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].InstanceId"
# Output: []

aws ec2 describe-volumes --query "Volumes[*].VolumeId"
# Output: []
```

---

## Key Learnings

| Skill | Interview Answer |
|-------|------------------|
| **EBS Resize** | "Online resize with `modify-volume` then `resize2fs` - no downtime" |
| **Format vs Mount** | "Format creates filesystem (new volumes only), mount connects to directory" |
| **Snapshot** | "Point-in-time backup, incremental after first, stored in S3" |
| **Metadata** | "169.254.169.254 - standard link-local IP for instance info" |

---

## Interview-Ready Topics ✅

- [x] Launch EC2 with CLI
- [x] SSH via key pair
- [x] Query instance metadata
- [x] Create, attach, format, mount EBS
- [x] Resize EBS without downtime
- [x] Create and restore from snapshot
- [x] Clean up resources
