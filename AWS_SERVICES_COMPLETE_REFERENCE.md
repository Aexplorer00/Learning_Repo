# 📚 AWS Services Complete Reference

**Everything you need to know about each AWS service - what, why, how, and when.**

---

# 🌐 VPC (Virtual Private Cloud)

## What It Is
Your own isolated network in AWS where you deploy resources.

## Key Components

### CIDR Block
- **What:** IP address range for your VPC
- **Options:** /16 (65,536 IPs) to /28 (16 IPs)
- **Common:** `10.0.0.0/16` for large VPCs
- **Rule:** Cannot change after creation. Plan carefully!

### Subnets
| Type | Has Route To | Use For |
|------|--------------|---------|
| **Public** | Internet Gateway | Web servers, bastion hosts |
| **Private** | NAT Gateway (optional) | Databases, app servers |

- **AZ-specific:** Each subnet lives in ONE Availability Zone
- **Best practice:** Create subnets in at least 2 AZs for HA

### Internet Gateway (IGW)
- **What:** Allows public subnet resources to reach internet
- **How:** Attach to VPC, add route `0.0.0.0/0 → IGW` in route table
- **Limit:** One per VPC
- **Stateful:** Responses automatically allowed

### NAT Gateway
- **What:** Allows private subnet resources to reach internet (outbound only)
- **Why:** Install updates, call external APIs without being publicly accessible
- **Cost:** ~$0.045/hour + data processing fees
- **HA:** Create NAT in each AZ for high availability

### Route Tables
- **What:** Rules that direct network traffic
- **Main route table:** Default for all subnets
- **Custom:** Associate with specific subnets

```
Destination     | Target
10.0.0.0/16     | local (within VPC)
0.0.0.0/0       | igw-xxx (public) OR nat-xxx (private)
```

### Security Groups (SG)
- **What:** Virtual firewall for EC2 instances
- **Level:** Instance-level
- **Stateful:** If inbound allowed, outbound response auto-allowed
- **Default:** Deny all inbound, allow all outbound

```
# Example: Web server SG
Inbound:  80 (HTTP),  443 (HTTPS) from 0.0.0.0/0
          22 (SSH) from YOUR_IP only
Outbound: All traffic allowed
```

### Network ACLs (NACLs)
- **What:** Firewall at subnet level
- **Stateless:** Must allow BOTH inbound AND outbound
- **Order:** Rules evaluated by number (lowest first)
- **Use case:** Block specific IPs at subnet level

| Aspect | Security Group | NACL |
|--------|---------------|------|
| Level | Instance | Subnet |
| Stateful | Yes | No |
| Rules | Allow only | Allow + Deny |
| Default | Deny all in | Allow all |

### VPC Endpoints
- **What:** Private connection to AWS services without internet
- **Interface Endpoint:** ENI with private IP (most services)
- **Gateway Endpoint:** Route table entry (S3, DynamoDB only)
- **Why:** Security, lower latency, no NAT costs

### VPC Peering
- **What:** Connect two VPCs privately
- **Transitive:** NO! A↔B and B↔C doesn't mean A↔C
- **Cross-region:** Yes, supported
- **Use case:** Connect prod and monitoring VPCs

---

# 💻 EC2 (Elastic Compute Cloud)

## What It Is
Virtual servers in the cloud.

## Instance Types

| Family | Optimized For | Examples |
|--------|---------------|----------|
| **T** | Burstable, general | t3.micro, t3.medium |
| **M** | Balanced | m5.large |
| **C** | Compute (CPU) | c5.xlarge |
| **R** | Memory | r5.large |
| **I** | Storage IOPS | i3.large |
| **G/P** | GPU | g4dn.xlarge |

## Instance States

```
pending → running → stopping → stopped → terminated
                  ↓
              shutting-down → terminated
```

- **Stopped:** No charges for compute (still pay for EBS)
- **Terminated:** Gone forever (unless termination protection on)

## Key Pairs
- **What:** SSH key for Linux access
- **AWS stores:** Public key only
- **You keep:** Private key (.pem file)
- **Lost key:** Cannot recover! Must create new key via volume recovery

## User Data
- **What:** Script that runs on FIRST boot
- **Use:** Install packages, configure software

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
```

## Instance Metadata
- **What:** Info about running instance
- **Access:** `curl http://169.254.169.254/latest/meta-data/`
- **Get instance ID:** `curl http://169.254.169.254/latest/meta-data/instance-id`

## Placement Groups
| Type | What | Use Case |
|------|------|----------|
| **Cluster** | Same rack, low latency | HPC |
| **Spread** | Different hardware | Critical instances |
| **Partition** | Logical partitions | Hadoop, Kafka |

---

# 💾 EBS (Elastic Block Store)

## What It Is
Network-attached storage for EC2. Like a hard drive.

## Volume Types

| Type | IOPS | Use Case |
|------|------|----------|
| **gp3** | 3,000-16,000 | General purpose (default) |
| **gp2** | Burst to 3,000 | Legacy general purpose |
| **io1/io2** | Up to 64,000 | Databases, critical apps |
| **st1** | 500 | Big data, logs (HDD) |
| **sc1** | 250 | Cold data, infrequent access |

## Key Operations

### Attach Volume
```bash
# AWS CLI
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf

# On EC2 - format (ONLY for new volumes!)
sudo mkfs -t ext4 /dev/xvdf

# Mount
sudo mkdir /data
sudo mount /dev/xvdf /data
```

### Resize Volume (NO DOWNTIME!)
```bash
# 1. Modify in AWS
aws ec2 modify-volume --volume-id vol-xxx --size 100

# 2. Extend partition (on EC2)
sudo growpart /dev/xvda 1

# 3. Extend filesystem
sudo resize2fs /dev/xvda1   # ext4
sudo xfs_growfs /data       # xfs
```

### Snapshots
- **What:** Point-in-time backup of EBS volume
- **Incremental:** Only changed blocks stored
- **Cross-region:** Can copy for DR
- **From snapshot:** Create new volume or AMI

```bash
aws ec2 create-snapshot --volume-id vol-xxx --description "Backup"
```

## Root Volume vs Data Volume
- **Root:** OS, deleted on termination by default
- **Data:** Persists after termination (if configured)

---

# 🚀 EKS (Elastic Kubernetes Service)

## What It Is
AWS-managed Kubernetes control plane.

## AWS Manages
- Control plane (API server, etcd, scheduler)
- Control plane HA across AZs
- Kubernetes version upgrades

## You Manage
- Worker nodes
- Applications
- Networking configuration

## Connect to Cluster
```bash
# Update kubeconfig
aws eks update-kubeconfig --name my-cluster --region us-east-1

# Verify
kubectl get nodes
```

## Node Types

| Type | Description | Best For |
|------|-------------|----------|
| **Managed Node Groups** | AWS manages EC2 lifecycle | Most workloads |
| **Self-managed** | You manage EC2 | Custom AMIs |
| **Fargate** | Serverless, per-pod | Variable workloads |

## Add-ons (AWS Managed Components)
| Add-on | Purpose |
|--------|---------|
| **CoreDNS** | DNS for service discovery |
| **kube-proxy** | Network routing to pods |
| **VPC CNI** | Pod networking (assigns VPC IPs) |
| **EBS CSI** | Persistent volume support |

```bash
aws eks list-addons --cluster-name my-cluster
```

## Debugging Pods
```bash
kubectl get pods -A                     # All pods
kubectl describe pod <name>             # Events, status
kubectl logs <pod>                      # App logs
kubectl logs <pod> --previous           # Previous container
kubectl exec -it <pod> -- /bin/sh       # Shell into pod
kubectl get events --sort-by='.lastTimestamp'
```

## Common Issues

| Symptom | Likely Cause |
|---------|--------------|
| Pending | Insufficient resources |
| ImagePullBackOff | Wrong image or no pull secret |
| CrashLoopBackOff | App crashing (check logs) |
| OOMKilled | Out of memory (increase limits) |

---

# 🗄️ RDS (Relational Database Service)

## What It Is
Managed relational databases.

## Supported Engines
MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora

## Deployment Options

### Single-AZ
- One DB instance
- Cheaper, no HA
- Good for dev/test

### Multi-AZ
- Primary + Standby in different AZ
- Automatic failover (60-120 sec)
- Synchronous replication
- Use for: Production

### Read Replicas
- Async replication
- Scale read traffic
- Can be cross-region
- Can promote to standalone

## Connecting to RDS
RDS is typically in **private subnet**. Connect via:

1. **From EC2 in same VPC:** Direct connection
2. **From internet:** Use bastion host

```bash
# SSH to bastion (public subnet)
ssh -i key.pem ec2-user@bastion-ip

# From bastion, connect to RDS
mysql -h mydb.xxxxx.rds.amazonaws.com -u admin -p
```

## Backups
- **Automated:** Daily, retention 0-35 days
- **Manual snapshots:** Kept until you delete
- **Restore:** Creates NEW instance (not replace)

## Parameter Groups
- Configure database settings (max_connections, buffer_pool_size)
- Apply changes: Some require reboot

## Security
- **Encryption at rest:** KMS (must enable at creation)
- **Encryption in transit:** SSL/TLS
- **Security Groups:** Control who can access

---

# 📦 S3 (Simple Storage Service)

## What It Is
Object storage for any type of data.

## Storage Classes

| Class | Access | Use Case |
|-------|--------|----------|
| **Standard** | Frequent | Active data |
| **Standard-IA** | Infrequent | Backups accessed monthly |
| **One Zone-IA** | Infrequent, single AZ | Reproducible data |
| **Glacier Instant** | Rarely, instant retrieval | Archives |
| **Glacier Flexible** | Rarely, mins-hours retrieval | Compliance |
| **Glacier Deep** | Rarely, 12-48 hrs retrieval | Long-term |

## Key Features

### Versioning
- Keep all versions of objects
- Protect against accidental deletes
- **Delete marker:** Shows as deleted but recoverable

### Lifecycle Rules
```
Day 0:   Standard
Day 30:  Transition to Standard-IA
Day 90:  Transition to Glacier
Day 365: Delete
```

### Encryption
| Type | Key Managed By |
|------|---------------|
| SSE-S3 | AWS (default) |
| SSE-KMS | You (in KMS) |
| SSE-C | Customer-provided |

### Bucket Policies
- **What:** JSON policy attached to bucket
- **Use:** Public access, cross-account, IP restrictions

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

### Static Website Hosting
```bash
aws s3 website s3://my-bucket --index-document index.html
```
URL: `http://my-bucket.s3-website-us-east-1.amazonaws.com`

### Cross-Region Replication
- Replicate objects to another region
- Requires versioning on both buckets
- Use for: DR, compliance, lower latency

---

# 🔐 IAM (Identity and Access Management)

## What It Is
Control who can do what in AWS.

## Key Components

### Users
- **What:** Person or application
- **Credentials:** Password (console), Access Keys (CLI/API)
- **Best practice:** Never use root user

### Groups
- **What:** Collection of users
- **Policies attached to group:** Applied to all members

### Roles
- **What:** Identity that can be ASSUMED
- **No credentials:** Uses temporary tokens
- **Trust policy:** Who can assume this role

```json
{
  "Effect": "Allow",
  "Principal": {"Service": "ec2.amazonaws.com"},
  "Action": "sts:AssumeRole"
}
```

### Policies
- **What:** JSON document defining permissions
- **Types:** AWS managed, Customer managed, Inline

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

## When to Use What

| Scenario | Use |
|----------|-----|
| Human accessing console | IAM User |
| EC2 accessing S3 | IAM Role attached to EC2 |
| Lambda accessing DynamoDB | IAM Role for Lambda |
| Cross-account access | IAM Role with trust policy |
| CI/CD pipeline | OIDC (no long-term keys) |

## STS (Security Token Service)
- **What:** Issues temporary credentials
- **AssumeRole:** Get temp creds for a role
- **Duration:** 15 min - 12 hours

---

# 📊 CloudWatch

## What It Is
Monitoring and observability.

## Components

### Metrics
- **What:** Time-series data points
- **Default:** EC2 (CPU, Network), RDS, ELB
- **Custom:** Send your own via API

### Logs
- **Log Groups:** Container for log streams
- **Log Streams:** Sequence of log events
- **Retention:** Set 1 day to forever

### Alarms
- **What:** Watch a metric, take action
- **States:** OK, ALARM, INSUFFICIENT_DATA
- **Actions:** SNS, Auto Scaling, EC2 actions

```
Metric: CPUUtilization
Threshold: > 80% for 5 minutes
Action: Send SNS notification
```

### Dashboards
- Visualize metrics in graphs/widgets
- Share with team

### Log Insights
- Query logs with SQL-like syntax
```
filter @message like /ERROR/
| stats count() by bin(1h)
```

---

# 🌍 Route 53

## What It Is
DNS service (domain name → IP address)

## Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | Domain → IPv4 | example.com → 1.2.3.4 |
| **AAAA** | Domain → IPv6 | example.com → 2001:... |
| **CNAME** | Domain → Domain | www.example.com → example.com |
| **Alias** | Domain → AWS resource | example.com → ALB |

## Routing Policies

| Policy | What It Does |
|--------|--------------|
| **Simple** | Single resource (no health checks) |
| **Weighted** | Split traffic by percentage (A/B testing) |
| **Latency** | Route to lowest latency region |
| **Failover** | Primary/Secondary (DR) |
| **Geolocation** | Route by user location |
| **Multi-value** | Return multiple healthy IPs |

## Health Checks
- Monitor endpoint health
- Remove unhealthy endpoints from DNS
- Types: HTTP, HTTPS, TCP

---

# ⚖️ Load Balancers

## Types

| Type | Layer | Protocol | Use Case |
|------|-------|----------|----------|
| **ALB** | 7 | HTTP/HTTPS | Web apps, microservices |
| **NLB** | 4 | TCP/UDP | Gaming, IoT, extreme performance |
| **CLB** | 4/7 | Both | Legacy (avoid for new) |

## ALB Features
- Path-based routing (`/api` → backend, `/` → frontend)
- Host-based routing (`api.example.com` → API)
- WebSocket support
- HTTP/2 support
- Sticky sessions

## Target Groups
- **What:** Group of targets (EC2, IP, Lambda)
- **Health checks:** ALB checks targets periodically
- **Unhealthy:** Removed from rotation

## Cross-Zone Load Balancing
- Distribute traffic evenly across all AZs
- ALB: Enabled by default
- NLB: Disabled by default

---

# 🔄 Auto Scaling

## Components

### Launch Template
- **What:** Instance configuration (AMI, type, key, SG)
- **Use:** Defines WHAT to launch

### Auto Scaling Group (ASG)
- **What:** Collection of EC2 instances
- **Defines:** Min, max, desired capacity
- **Use:** Defines HOW MANY to launch

### Scaling Policies

| Type | How It Works |
|------|--------------|
| **Target Tracking** | Maintain metric at target (e.g., 50% CPU) |
| **Step Scaling** | Scale by thresholds (>70% add 2, >90% add 4) |
| **Scheduled** | Scale at specific times (9 AM scale up) |
| **Predictive** | ML-based forecasting |

## Lifecycle Hooks
- Pause instance before InService or Terminate
- Run scripts, drain connections

---

*Master these services and you'll handle ANY infrastructure interview!* 💪
