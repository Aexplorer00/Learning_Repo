# 🎯 ThoughtSpot Cloud Reliability Engineer Interview Prep
## JR1887 | 3-Day Sprint (Jan 29 - Jan 31) → Interview: Monday, Feb 3

---

## 📋 Role Analysis

| Required | Your Experience | Match |
|----------|----------------|-------|
| 2-5 years Cloud Ops/SRE/K8s | 4 years SRE at TCS | ✅ |
| AWS/GCP/Azure production | AWS/Azure, 20+ prod apps | ✅ |
| Kubernetes (EKS/GKE/AKS) | EKS 3-Tier project, monitoring | ✅ |
| Python & Jenkins automation | Python/Boto3, CI/CD pipelines | ✅ |
| ITIL (Incident/Change/Problem) | P1/P2 incident response, on-call | ✅ |
| Terraform/Ansible/IaC | Terraform modules, Ansible | ✅ |
| Prometheus/Grafana observability | K8s monitoring stack project | ✅ |

> [!IMPORTANT]
> **First Round Focus**: Heavy on AWS, Kubernetes, Linux, Docker, and real-time concepts. This is an operational role—expect troubleshooting scenarios!

---

## 📅 3-Day Sprint Schedule

### Day 1 (Today - Thursday, Jan 29): AWS + Networking
**Morning (2 hrs)**
- [ ] VPC Deep Dive: [AWS_VPC_COMPLETE_GUIDE.md](file:///d:/Projects/Learning-Path/AWS_VPC_COMPLETE_GUIDE.md)
  - Subnets (public/private), IGW vs NAT
  - Security Groups vs NACLs (stateful vs stateless)
  - VPC Peering vs Transit Gateway

**Afternoon (2 hrs)**
- [ ] EC2 & Compute: [AWS_EC2_COMPLETE_GUIDE.md](file:///d:/Projects/Learning-Path/AWS_EC2_COMPLETE_GUIDE.md)
  - Instance types, pricing models
  - EBS volumes, snapshots
  - Auto Scaling, ALB/NLB

**Evening (1 hr)**
- [ ] Practice AWS CLI commands
- [ ] Review [AWS_SERVICES_COMPLETE_REFERENCE.md](file:///d:/Projects/Learning-Path/AWS_SERVICES_COMPLETE_REFERENCE.md)

---

### Day 2 (Friday, Jan 30): Kubernetes + Docker
**Morning (2 hrs)**
- [ ] Kubernetes Core Concepts:
  - Pods, Deployments, ReplicaSets
  - Services (ClusterIP, NodePort, LoadBalancer)
  - ConfigMaps, Secrets
  - Namespaces, RBAC

**Afternoon (2 hrs)**
- [ ] K8s Troubleshooting (Critical for SRE!):
  - `kubectl get pods -A` → Status analysis
  - `kubectl describe pod <name>` → Events section
  - `kubectl logs <pod>` → Application logs
  - `kubectl exec -it <pod> -- sh` → Debug shell
  - CrashLoopBackOff, ImagePullBackOff, OOMKilled

**Evening (1 hr)**
- [ ] Docker commands & Dockerfile best practices
- [ ] Review EKS project: [05-INTERVIEW-GUIDE.md](file:///d:/Projects/EKS-3Tier-App/docs/05-INTERVIEW-GUIDE.md)

---

### Day 3 (Saturday, Jan 31): Linux + Incident Response
**Morning (2 hrs)**
- [ ] Linux Core Commands:
  - Process: `ps`, `top`, `htop`, `kill`, `nice`
  - Disk: `df`, `du`, `lsblk`, `mount`
  - Network: `netstat`, `ss`, `iptables`, `tcpdump`, `curl`, `dig`
  - Logs: `journalctl`, `tail -f`, `grep`

**Afternoon (2 hrs)**
- [ ] Incident Response Scenarios:
  - "Pod not starting" → troubleshoot
  - "High CPU on node" → identify & remediate
  - "Application latency spike" → systematic debugging

**Evening (1 hr)**
- [ ] Mock Interview: Practice STAR method for behavioral
- [ ] Review your resume projects & be ready to explain each

---

## 🎬 Prioritized K8s Video Watch List (Piyush Sachdeva CKA Course)

> [!TIP]
> **With only 3 days, watch in this order.** Focus on 🔴 Priority 1 (MUST), then 🟡 Priority 2 if time permits.

### 🔴 Priority 1: MUST WATCH (Interview Critical) — ~6 hours

| # | Video | Duration | Why Critical |
|---|-------|----------|--------------|
| **37** | Application Failure Troubleshooting | 32 min | **#1 for SRE interviews!** |
| **38** | Troubleshooting Control Plane Failure | 29 min | What to do when API server is down |
| **39** | Troubleshooting Worker Node Failures | 15 min | kubelet, node NotReady scenarios |
| **8** | Pods Explained (Imperative vs Declarative) | 33 min | Core concept |
| **9** | Deployments, ReplicaSets | 35 min | Scaling, rollouts |
| **10** | Services (ClusterIP/NodePort/LB) | 46 min | Network connectivity |
| **18** | Health Probes (Liveness/Readiness) | 28 min | Why pods restart |
| **17** | Autoscaling (HPA/VPA) | 25 min | Scaling for production |
| **19** | ConfigMaps & Secrets | 17 min | Configuration management |
| **36** | Logging & Monitoring | 25 min | Observability basics |

### 🟡 Priority 2: HIGHLY RECOMMENDED — ~4 hours

| # | Video | Duration | Why Useful |
|---|-------|----------|------------|
| **5** | What is Kubernetes (Architecture) | 25 min | Explain K8s components |
| **11** | Namespaces | 27 min | Multi-tenancy |
| **12** | Sidecar & Init Containers | 25 min | Common pattern |
| **14** | Taints and Tolerations | 26 min | Scheduling constraints |
| **16** | Requests and Limits | 18 min | Resource management |
| **26** | Network Policies | 45 min | Security between pods |
| **29** | Persistent Volumes | 33 min | Stateful workloads |
| **33** | Ingress Tutorial | 54 min | External traffic routing |

### 🟢 Priority 3: GOOD TO KNOW (Skip if short on time)

| # | Video | Topic |
|---|-------|-------|
| **23-25** | RBAC (3 videos) | Role-based access |
| **35** | ETCD Backup/Restore | Disaster recovery |
| **40** | JSONPath kubectl | Advanced queries |
| **45** | Helm Charts | Package management |

### 📺 Suggested Watch Schedule

| Day | Videos to Watch | Total Time |
|-----|-----------------|------------|
| **Day 2 AM** | #37, #38, #39 (Troubleshooting) | ~1.5 hrs |
| **Day 2 PM** | #8, #9, #10 (Core concepts) | ~2 hrs |
| **Day 2 EVE** | #18, #19, #17 (Probes, Configs, HPA) | ~1 hr |
| **Day 3** | #36 (Monitoring) + Priority 2 as needed | Flexible |

---

## 🔥 High-Priority Topics (70% of interview)

### 1. Kubernetes Troubleshooting (30%)

```bash
# Pod not starting
kubectl get pods -n <namespace>
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous  # If container restarted

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Node issues
kubectl get nodes
kubectl describe node <node-name>
kubectl top nodes  # Resource usage
```

**Common Issues & Solutions:**

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **CrashLoopBackOff** | App error, bad config | Check logs, fix app |
| **ImagePullBackOff** | Wrong image, auth failure | Verify image name, check secrets |
| **OOMKilled** | Memory exceeded | Increase limits or optimize app |
| **Pending** | No node capacity | Scale cluster or reduce requests |
| **ContainerCreating** | Volume/network issue | Check PV, CSI, or CNI |

---

### 2. AWS Core Services (25%)

**VPC Questions:**
- How does traffic flow from internet → EC2 in private subnet?
  > Internet → IGW → ALB (public) → Target Group → EC2 (private)

- How to securely allow EC2 in private subnet to reach S3?
  > VPC Gateway Endpoint (free, within AWS backbone)

**EC2/EKS Questions:**
- EKS node not joining cluster?
  > Check: IAM role, security group (443 to control plane), kubelet logs

- How does EKS node autoscaling work?
  > Cluster Autoscaler watches pending pods → triggers ASG scale-up

---

### 3. Linux System Administration (20%)

```bash
# High CPU - Find culprit
top -c                          # Press 'P' to sort by CPU
ps aux --sort=-%cpu | head -10

# Disk full
df -h                           # Check mount points
du -sh /* 2>/dev/null | sort -hr | head -10  # Largest dirs
find /var/log -type f -size +100M  # Large log files

# Network troubleshooting
ss -tulpn                       # What's listening
netstat -an | grep ESTABLISHED | wc -l  # Connection count
curl -v http://service:port     # Test connectivity
dig +short example.com          # DNS resolution

# Memory pressure
free -m
cat /proc/meminfo
```

---

### 4. Docker Essentials (10%)

```bash
# Container not starting
docker logs <container>
docker inspect <container>
docker exec -it <container> sh

# Dockerfile best practices
FROM python:3.11-slim       # Use slim/alpine (smaller)
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  # Cache layer
COPY . .                    # App code last (changes often)
CMD ["python", "app.py"]
```

**Multi-stage build example:**
```dockerfile
# Build stage
FROM python:3.11 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "app.py"]
```

---

### 5. Incident Management (15%)

**STAR Method for Incident Questions:**

> **Q: Tell me about a critical incident you handled.**

**S** - Situation: "We had a P1 incident where our production API started returning 500 errors..."

**T** - Task: "As the on-call SRE, I needed to restore service immediately..."

**A** - Action: "I checked CloudWatch metrics, identified memory exhaustion, scaled the ASG..."

**R** - Result: "Service restored in 15 minutes. MTTR was well within our 30-min SLA. RCA showed a memory leak we later patched."

---

## 💡 ThoughtSpot-Specific Prep

### About ThoughtSpot
- **Product**: AI-powered analytics platform (search-driven BI)
- **Cloud**: SaaS platform deployed on cloud (likely GCP/AWS)
- **Scale**: Forbes Cloud 100 company, enterprise customers

### Questions to Ask Them
1. "What does a typical on-call shift look like? What percentage is reactive vs proactive?"
2. "What's your current monitoring stack and what improvements are you planning?"
3. "How much autonomy does the Cloud Reliability team have in driving automation initiatives?"
4. "What does success look like in the first 90 days for this role?"

### Why ThoughtSpot? (Prepare Your Answer)
> "I'm excited about the blend of operational excellence and automation in this role. I've spent 4 years at TCS building reliability into distributed systems, and I'm looking for a product company where I can directly impact customer experience. ThoughtSpot's focus on reducing toil through code aligns perfectly with my approach—I've already automated certificate monitoring, health checks, and compliance reporting. I want to bring that mindset to a fast-paced SaaS environment."

---

## 📚 Quick Reference Links

| Topic | Resource |
|-------|----------|
| VPC | [AWS_VPC_COMPLETE_GUIDE.md](file:///d:/Projects/Learning-Path/AWS_VPC_COMPLETE_GUIDE.md) |
| EC2 | [AWS_EC2_COMPLETE_GUIDE.md](file:///d:/Projects/Learning-Path/AWS_EC2_COMPLETE_GUIDE.md) |
| All AWS Services | [AWS_SERVICES_COMPLETE_REFERENCE.md](file:///d:/Projects/Learning-Path/AWS_SERVICES_COMPLETE_REFERENCE.md) |
| Kubernetes Project | [EKS 3-Tier Interview Guide](file:///d:/Projects/EKS-3Tier-App/docs/05-INTERVIEW-GUIDE.md) |
| K8s Monitoring | [K8s-Monitoring Interview Guide](file:///d:/Projects/K8s-Monitoring/INTERVIEW-GUIDE.md) |
| Python for SRE | [PYTHON_MODULES_FOR_SRE.md](file:///d:/Projects/Learning-Path/PYTHON_MODULES_FOR_SRE.md) |
| DevOps Tools | [DEVOPS_TOOLS_QUICK_REFERENCE.md](file:///d:/Projects/Learning-Path/DEVOPS_TOOLS_QUICK_REFERENCE.md) |

---

## ✅ Pre-Interview Checklist (Sunday Night)

- [ ] Resume printed/ready
- [ ] Laptop charged, headphones tested
- [ ] Quiet room, good lighting
- [ ] Water bottle nearby
- [ ] Review this prep guide one more time
- [ ] Get good sleep!

---

*Good luck! You've got this. Your 4 years of SRE experience and hands-on projects are a perfect match for this role.* 🚀
