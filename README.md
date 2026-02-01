# 📚 Learning Path - Quick Access

Welcome to your organized learning hub! All docs for your SRE/DevOps journey are here.

---

## 📊 Trackers

| File | Description |
|------|-------------|
| [MASTER_LEARNING_TRACKER.md](./MASTER_LEARNING_TRACKER.md) | **Main tracker** - 4 tracks, weekly view |
| [DEVOPS_CURRICULUM_TRACKER.csv](./DEVOPS_CURRICULUM_TRACKER.csv) | Detailed daily breakdown (CSV) |

---

## 🐍 Python Guides

| File | Description |
|------|-------------|
| [PYTHON_MODULES_FOR_DEVOPS.md](./PYTHON_MODULES_FOR_DEVOPS.md) | Core Python modules for automation |
| [PYTHON_MODULES_FOR_SRE.md](./PYTHON_MODULES_FOR_SRE.md) | SRE-specific Python + Boto3 |

---

## 🛠️ DevOps Quick References

| File | Description |
|------|-------------|
| [DEVOPS_TOOLS_QUICK_REFERENCE.md](./DEVOPS_TOOLS_QUICK_REFERENCE.md) | Nginx, Helm, ArgoCD, Trivy, Istio |
| [NGINX_COMPLETE_GUIDE.md](./NGINX_COMPLETE_GUIDE.md) | Nginx deep dive + interview Qs |
| [MAVEN_QUICK_REFERENCE.md](./MAVEN_QUICK_REFERENCE.md) | Maven basics for interviews |

---

## 📁 Folder Structure

```
Learning-Path/
├── README.md                         ← You are here
├── MASTER_LEARNING_TRACKER.md        ← Main tracker
├── DEVOPS_CURRICULUM_TRACKER.csv     ← Daily details
├── PYTHON_MODULES_FOR_DEVOPS.md      ← Python guide
├── PYTHON_MODULES_FOR_SRE.md         ← Boto3 guide
├── DEVOPS_TOOLS_QUICK_REFERENCE.md   ← DevOps tools
├── NGINX_COMPLETE_GUIDE.md           ← Nginx guide
└── MAVEN_QUICK_REFERENCE.md          ← Maven guide
```

---

## 🎯 Quick Start

1. Open `MASTER_LEARNING_TRACKER.md` to see today's tasks
2. Mark completed items with ✅
3. Use quick reference files during study

---

*Last Updated: Jan 11, 2026*

---

## 🏆 EC2 Project Ideas

### 1. **3-Tier Web Application** (⭐ Recommended)
```
Route53 → ALB → EC2 (Web) → EC2 (App) → RDS
           ↓
    Auto Scaling Group
```
**Learn:** VPC, Subnets, ALB, Auto Scaling, RDS

### 2. **EC2 Auto Start/Stop Scheduler**
```
CloudWatch Events → Lambda → Start/Stop EC2
```
**Learn:** Lambda, CloudWatch Events, Boto3, Cost saving

### 3. **CI/CD to EC2**
```
GitHub → GitHub Actions → Build → Deploy to EC2
```
**Learn:** CI/CD, SSH deploy, CodeDeploy

### 4. **EC2 Monitoring Dashboard**
```
EC2 → CloudWatch Agent → Custom Metrics → Grafana
```
**Learn:** CloudWatch, Custom metrics, Dashboards

### 5. **Bastion Host Setup**
```
Public EC2 (Bastion) → SSH → Private EC2
```
**Learn:** Security, VPC, SSH tunneling
