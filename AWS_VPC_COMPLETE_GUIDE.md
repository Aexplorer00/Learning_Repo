# AWS VPC Complete Guide for SRE
## Day 6: Concepts + Architecture + Interview Questions

---

## 🎯 What is VPC?

**VPC = Virtual Private Cloud** = Your own isolated network in AWS

```
┌─────────────────────────────────────────────────────┐
│                     AWS CLOUD                        │
│  ┌───────────────────────────────────────────────┐  │
│  │              YOUR VPC (10.0.0.0/16)           │  │
│  │                                               │  │
│  │   ┌───────────┐         ┌───────────┐        │  │
│  │   │  Public   │         │  Private  │        │  │
│  │   │  Subnet   │         │  Subnet   │        │  │
│  │   │10.0.1.0/24│         │10.0.2.0/24│        │  │
│  │   └───────────┘         └───────────┘        │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## � Complete VPC Concepts Checklist

### Core (Must Know) ⭐
| Concept | What It Is | Priority |
|---------|------------|----------|
| **VPC** | Your isolated network | 🔴 High |
| **CIDR** | IP address range | 🔴 High |
| **Subnets** | Network segments (public/private) | 🔴 High |
| **Internet Gateway** | Door to internet | 🔴 High |
| **NAT Gateway** | Private subnet → internet | 🔴 High |
| **Route Tables** | Traffic directions | 🔴 High |
| **Security Groups** | Instance firewall (stateful) | 🔴 High |
| **NACLs** | Subnet firewall (stateless) | 🔴 High |

### Advanced (Good to Know)
| Concept | What It Is | Priority |
|---------|------------|----------|
| **VPC Peering** | Connect 2 VPCs | 🟡 Medium |
| **Transit Gateway** | Connect multiple VPCs | 🟡 Medium |
| **VPC Endpoints** | Private access to AWS services | 🟡 Medium |
| **VPN** | Encrypted tunnel to on-prem | 🟡 Medium |
| **Direct Connect** | Dedicated link to AWS | 🟡 Medium |
| **VPC Flow Logs** | Network traffic logs | 🟡 Medium |
| **Elastic IP** | Static public IP | 🟡 Medium |
| **Egress-Only IGW** | IPv6 outbound only | 🟢 Low |

### Rarely Asked
- PrivateLink
- AWS Network Firewall
- Traffic Mirroring

---

## �📦 Core VPC Components

### 1. CIDR Block (IP Range)

```
VPC CIDR: 10.0.0.0/16 → 65,536 IPs
          ├── Subnet 1: 10.0.1.0/24 → 256 IPs
          ├── Subnet 2: 10.0.2.0/24 → 256 IPs
          └── Subnet 3: 10.0.3.0/24 → 256 IPs
```

**Quick CIDR Reference:**
| CIDR | # of IPs | Use Case |
|------|----------|----------|
| /16 | 65,536 | VPC |
| /24 | 256 | Subnet |
| /28 | 16 | Small subnet |

### 2. Subnets (Public vs Private)

| Type | Internet Access | Use Case |
|------|----------------|----------|
| **Public** | Direct via IGW | Web servers, bastion |
| **Private** | Via NAT | Databases, app servers |

```
Public Subnet:  Has route to Internet Gateway (IGW)
Private Subnet: Has route to NAT Gateway (not direct internet)
```

### 3. Internet Gateway (IGW)

**IGW = Door to the Internet**

```
Internet ←→ IGW ←→ Public Subnet
```

- One IGW per VPC
- Enables internet access for public subnets
- Free (no hourly charge)

### 4. NAT Gateway

**NAT = Allows private subnets to reach internet (outbound only)**

```
Private Subnet → NAT Gateway → IGW → Internet
                    (in public subnet)

Internet ✗→ Private Subnet (blocked!)
```

- Placed in PUBLIC subnet
- Allows outbound traffic from private subnets
- Blocks inbound from internet
- ~$0.045/hour + data transfer

### 5. Route Tables

**Route Tables = Traffic directions**

```
Public Subnet Route Table:
Destination     Target
10.0.0.0/16     local          (within VPC)
0.0.0.0/0       igw-xxxxx      (internet via IGW)

Private Subnet Route Table:
Destination     Target
10.0.0.0/16     local          (within VPC)
0.0.0.0/0       nat-xxxxx      (internet via NAT)
```

### 6. Security Groups vs NACLs

| Feature | Security Group | NACL |
|---------|---------------|------|
| **Level** | Instance | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow + Deny |
| **Default** | Deny all inbound | Allow all |
| **Evaluation** | All rules | Rules in order |

---

## 🏗️ VPC Architecture Patterns

### Pattern 1: Simple 2-Tier

```
┌───────────────────────────────────────────┐
│                   VPC                      │
│   ┌─────────────┐    ┌─────────────┐      │
│   │   Public    │    │   Private   │      │
│   │   Subnet    │───▶│   Subnet    │      │
│   │  (Web/ALB)  │    │   (DB/App)  │      │
│   └──────┬──────┘    └─────────────┘      │
│          │                                 │
│         IGW                                │
└──────────┼─────────────────────────────────┘
           │
        Internet
```

### Pattern 2: High Availability (Multi-AZ)

```
┌───────────────────────────────────────────────────────┐
│                        VPC                             │
│   ┌─────────────────────┐  ┌─────────────────────┐    │
│   │        AZ-1         │  │        AZ-2         │    │
│   │  ┌───────┐ ┌───────┐│  │  ┌───────┐ ┌───────┐│    │
│   │  │Public │ │Private││  │  │Public │ │Private││    │
│   │  │Subnet │ │Subnet ││  │  │Subnet │ │Subnet ││    │
│   │  └───┬───┘ └───────┘│  │  └───┬───┘ └───────┘│    │
│   │      │    NAT       │  │      │    NAT       │    │
│   └──────┼──────────────┘  └──────┼──────────────┘    │
│          │                        │                    │
│          └───────────┬────────────┘                    │
│                     IGW                                │
└──────────────────────┼─────────────────────────────────┘
                    Internet
```

---

## 🔧 VPC Connectivity (On-Prem, VPC-to-VPC, Services)

### 1️⃣ VPC to On-Premises (Your Datacenter)

#### Site-to-Site VPN
```
Your Datacenter ←─── VPN Tunnel ───→ AWS VPC
                    (encrypted, over internet)
```
- **Speed:** Up to 1.25 Gbps
- **Setup:** Hours
- **Cost:** ~$0.05/hour per tunnel
- **Use:** Quick setup, smaller workloads

#### Direct Connect
```
Your Datacenter ←─── Dedicated Line ───→ AWS VPC
                     (private fiber, not internet)
```
- **Speed:** 1-100 Gbps
- **Setup:** Weeks/Months
- **Cost:** Higher (dedicated hardware)
- **Use:** Large data transfer, low latency

---

### 2️⃣ VPC to VPC

#### VPC Peering
```
VPC A (10.0.0.0/16) ←──peering──→ VPC B (172.16.0.0/16)
```
- One-to-one direct connection
- **No transitive:** A→B, B→C ≠ A→C
- CIDRs cannot overlap
- Works across regions/accounts

#### Transit Gateway
```
        ┌─────────────────┐
        │ Transit Gateway │
        └────────┬────────┘
    ┌────────────┼────────────┐
    │            │            │
 VPC A        VPC B        VPC C
```
- Hub-and-spoke model
- **Transitive:** All VPCs can talk
- Simpler for many VPCs (10+)
- Can also connect VPN/Direct Connect

---

### 3️⃣ VPC to AWS Services (VPC Endpoints)

**Problem:** Private subnet → S3 = must go via NAT → Internet → S3
**Solution:** VPC Endpoint = Private connection (no internet!)

#### Gateway Endpoint (Free!)
```
Private Subnet ─────→ Gateway Endpoint ─────→ S3/DynamoDB
                      (stays within AWS)
```
- Only for **S3 and DynamoDB**
- **FREE!**
- Add route to route table

#### Interface Endpoint (PrivateLink)
```
Private Subnet ─────→ ENI ─────→ Any AWS Service
                     (private IP in your subnet)
```
- For other services (SNS, SQS, Lambda, etc.)
- ~$0.01/hour + data
- Creates ENI in your subnet

---

### 📊 Connectivity Summary Table

| Connection Type | Use Case | Speed | Cost |
|-----------------|----------|-------|------|
| **VPN** | On-prem (quick) | 1.25 Gbps | Low |
| **Direct Connect** | On-prem (big data) | 100 Gbps | High |
| **VPC Peering** | 2-3 VPCs | High | Free |
| **Transit Gateway** | Many VPCs | High | ~$0.05/hr |
| **Gateway Endpoint** | S3/DynamoDB | High | Free |
| **Interface Endpoint** | Other AWS services | High | ~$0.01/hr |

---

## 🎤 Interview Questions & Answers

### Q1: What's the difference between public and private subnet?
> Public subnet has a route to IGW (0.0.0.0/0 → igw).
> Private subnet routes to NAT or has no internet route.

### Q2: How does a private subnet access the internet?
> Via NAT Gateway (or NAT Instance) placed in a public subnet.
> NAT translates private IPs to public for outbound traffic.

### Q3: What's the difference between Security Group and NACL?
> SG: Instance-level, stateful, allow-only rules
> NACL: Subnet-level, stateless, allow+deny rules

### Q4: Can VPCs have overlapping CIDR blocks for peering?
> No! CIDR blocks must be non-overlapping for VPC peering.

### Q5: Why use multiple AZs?
> High availability - if one AZ fails, another takes over.
> AWS best practice for production workloads.

### Q6: What happens if NAT Gateway fails?
> Private instances lose internet access.
> Solution: Deploy NAT Gateway in each AZ.

### Q7: How to connect on-prem datacenter to VPC?
> 1. Site-to-Site VPN (quick, encrypted)
> 2. Direct Connect (dedicated, high bandwidth)
> 3. VPN over Direct Connect (both benefits)

---

## 🔥 Quick Commands (CLI)

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create Subnet
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a

# Create Internet Gateway
aws ec2 create-internet-gateway

# Attach IGW to VPC
aws ec2 attach-internet-gateway --vpc-id vpc-xxx --internet-gateway-id igw-xxx

# Create Route Table
aws ec2 create-route-table --vpc-id vpc-xxx

# Add route to IGW
aws ec2 create-route --route-table-id rtb-xxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxx
```

---

## 🛡️ VPC Best Practices

1. **Use private subnets** for databases and backend
2. **Deploy across multiple AZs** for HA
3. **Use VPC Flow Logs** for network monitoring
4. **Restrict NACL and SG rules** (least privilege)
5. **Use VPC Endpoints** for AWS services (S3, DynamoDB)
6. **Plan CIDR blocks carefully** (avoid future conflicts)

---

*Created for: DEVOPS/SRE 60-Day Journey (Day 6)*
