# 🔧 AWS Hands-On Practice Plan

**Goal:** Build confidence through practical exercises for every AWS skill on your resume.

---

## Week 1: VPC & Networking

### Exercise 1.1: Build VPC from Scratch
```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24  # Public
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.2.0/24  # Private

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id <vpc-id> --internet-gateway-id <igw-id>

# Create route table for public subnet
aws ec2 create-route-table --vpc-id <vpc-id>
aws ec2 create-route --route-table-id <rtb-id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-id>
```

### Exercise 1.2: CIDR Practice
```
/24 = 256 IPs (254 usable - AWS reserves 5)
/25 = 128 IPs
/26 = 64 IPs
/27 = 32 IPs
/28 = 16 IPs
```

### Exercise 1.3: Security Groups vs NACLs
- Create SG allowing SSH (port 22) from your IP
- Create NACL with inbound/outbound rules
- Test connectivity

---

## Week 2: EC2 & EBS Operations

### Exercise 2.1: Launch EC2 with SSH
```bash
# Create key pair
aws ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text > my-key.pem
chmod 400 my-key.pem

# Launch instance
aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro --key-name my-key

# Connect
ssh -i my-key.pem ec2-user@<public-ip>
```

### Exercise 2.2: EBS Volume Operations
```bash
# Create volume
aws ec2 create-volume --size 10 --availability-zone us-east-1a --volume-type gp3

# Attach to instance
aws ec2 attach-volume --volume-id <vol-id> --instance-id <i-id> --device /dev/sdf

# On EC2 - format and mount
sudo mkfs -t ext4 /dev/xvdf
sudo mkdir /data
sudo mount /dev/xvdf /data

# Resize volume (increase to 20GB)
aws ec2 modify-volume --volume-id <vol-id> --size 20

# Extend filesystem (on EC2)
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1
```

### Exercise 2.3: Create Snapshot & Restore
```bash
# Create snapshot
aws ec2 create-snapshot --volume-id <vol-id> --description "Backup"

# Create volume from snapshot
aws ec2 create-volume --snapshot-id <snap-id> --availability-zone us-east-1a
```

---

## Week 3: EKS Deep Dive

### Exercise 3.1: Connect to EKS Cluster
```bash
# Configure kubectl
aws eks update-kubeconfig --name my-cluster --region us-east-1

# Verify connection
kubectl get nodes
kubectl get pods -A

# Check current context
kubectl config current-context
```

### Exercise 3.2: Deploy Application
```bash
# Create deployment
kubectl create deployment nginx --image=nginx

# Expose as service
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Check status
kubectl get svc
kubectl describe pod <pod-name>
```

### Exercise 3.3: Debug Pod Issues
```bash
# Common debugging commands
kubectl get pods -A                    # All pods
kubectl describe pod <pod-name>        # Events and status
kubectl logs <pod-name>                # Application logs
kubectl logs <pod-name> --previous     # Previous container logs
kubectl exec -it <pod-name> -- /bin/sh # Shell into pod
kubectl get events --sort-by='.lastTimestamp'
```

### Exercise 3.4: EKS Add-ons
```bash
# List add-ons
aws eks list-addons --cluster-name my-cluster

# Common add-ons: CoreDNS, kube-proxy, VPC-CNI, EBS-CSI
```

---

## Week 4: RDS & Bastion Host

### Exercise 4.1: Launch RDS in Private Subnet
```bash
# Create DB subnet group (private subnets only)
aws rds create-db-subnet-group --db-subnet-group-name my-db-subnet \
  --subnet-ids subnet-xxx subnet-yyy

# Launch RDS (MySQL)
aws rds create-db-instance --db-instance-identifier mydb \
  --db-instance-class db.t3.micro --engine mysql \
  --master-username admin --master-user-password <password>
```

### Exercise 4.2: Connect via Bastion Host
```bash
# Launch bastion in public subnet
# SSH to bastion
ssh -i key.pem ec2-user@<bastion-public-ip>

# From bastion, connect to RDS
mysql -h mydb.xxxxx.us-east-1.rds.amazonaws.com -u admin -p
```

### Exercise 4.3: Lost PEM Key Recovery
```bash
# 1. Stop instance
aws ec2 stop-instances --instance-ids <i-id>

# 2. Detach root volume
aws ec2 detach-volume --volume-id <vol-id>

# 3. Attach to recovery instance
aws ec2 attach-volume --volume-id <vol-id> --instance-id <recovery-id> --device /dev/sdf

# 4. Mount and add new public key
sudo mount /dev/xvdf1 /mnt
echo "ssh-rsa AAAA..." >> /mnt/home/ec2-user/.ssh/authorized_keys

# 5. Unmount, reattach to original, start
```

---

## Week 5: S3 & CloudFront

### Exercise 5.1: Host Static Website
```bash
# Create bucket
aws s3 mb s3://my-static-site-xxx

# Enable static hosting
aws s3 website s3://my-static-site-xxx --index-document index.html

# Upload files
aws s3 cp index.html s3://my-static-site-xxx/

# Set bucket policy for public read
```

### Exercise 5.2: CloudFront Distribution
```bash
# Create CloudFront distribution with S3 origin
# - Origin: S3 bucket
# - Viewer Protocol: Redirect HTTP to HTTPS
# - Cache Behavior: Cache static assets

# Test: Access via CloudFront URL (d123xxx.cloudfront.net)
```

### Exercise 5.3: S3 Lifecycle Rules
```bash
# Transition to IA after 30 days, Glacier after 90
aws s3api put-bucket-lifecycle-configuration --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
```

---

## Week 6: IAM Deep Dive

### Exercise 6.1: Create Role for EC2
```bash
# Create trust policy
cat > trust.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ec2.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# Create role
aws iam create-role --role-name EC2-S3-Access --assume-role-policy-document file://trust.json

# Attach S3 read policy
aws iam attach-role-policy --role-name EC2-S3-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### Exercise 6.2: Least Privilege Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Connect to EKS | `aws eks update-kubeconfig --name <cluster>` |
| Resize EBS | `aws ec2 modify-volume --volume-id <id> --size <new-size>` |
| Extend FS | `sudo growpart /dev/xvda 1 && sudo resize2fs /dev/xvda1` |
| Create snapshot | `aws ec2 create-snapshot --volume-id <id>` |
| List EKS add-ons | `aws eks list-addons --cluster-name <name>` |

---

*Practice each exercise until you can do it without looking!* 💪
