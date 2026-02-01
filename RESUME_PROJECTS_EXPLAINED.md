# 📄 Resume Projects - Detailed Explanations
## For Interview Preparation

---

# Project 1: Kubernetes 3-Tier Application with GitOps

## What You Built
Production-ready web application with 3 separate layers:

```
User → Nginx (Frontend) → Flask (Backend API) → Redis (Cache/DB)
        Port 80            Port 5000           Port 6379
        2 replicas         2 replicas          1 replica
```

## Why 3-Tier?
- **Separation of concerns** - Each layer does one thing well
- **Independent scaling** - High traffic? Scale frontend only
- **Easier updates** - Update backend without touching frontend

## Key Components

| Component | What It Does |
|-----------|--------------|
| **Nginx** | Serves static HTML/CSS, proxies `/api/*` to backend |
| **Flask** | Python REST API, handles business logic |
| **Redis** | Stores data (visit counter) |
| **ArgoCD** | Watches GitHub, auto-deploys changes to K8s |
| **HPA** | Auto-scales pods based on CPU usage |

## GitOps Flow
```
You push to GitHub → ArgoCD detects change → Syncs to Kubernetes → App updated!
```

## Interview Answer
> "I built this to learn production K8s patterns. The app uses 3 tiers for separation of concerns. ArgoCD provides GitOps - any change to my GitHub repo automatically deploys to the cluster. I used multi-stage Docker builds to reduce image sizes by 60%."

---

# Project 2: Blue-Green Deployment Pipeline

## What You Built
CI/CD pipeline with **zero downtime** using blue-green strategy.

## How Blue-Green Works
```
Blue (Current) ←── ALB currently points here
Green (New)    ←── Deploy new version here

After testing Green:
ALB switches ──► Green becomes live
Blue becomes backup (rollback ready)
```

## Pipeline Flow
```
Code Push → GitHub Actions:
  1. Run tests
  2. Build Docker image
  3. Push to registry
  4. Deploy to Green environment
  5. Run health checks
  6. Switch ALB to Green
```

## Key Metrics
- **10+ deployments/week** - Frequent, safe releases
- **<5 minutes** - Deployment time
- **2 minutes** - Rollback time

## Interview Answer
> "This pipeline enables zero-downtime deployments. We deploy to the idle environment, run health checks, then switch the ALB. If something goes wrong, we switch back in 2 minutes. No customer ever sees a bad deployment."

---

# Project 3: Kubernetes Monitoring Stack

## What You Built
Complete observability solution using Prometheus + Grafana.

## Architecture
```
Apps expose /metrics → ServiceMonitor discovers →
Prometheus scrapes → stores time-series data →
Grafana queries → shows dashboards
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **Prometheus** | Scrapes metrics from pods every 30s |
| **ServiceMonitor** | CRD that auto-discovers pods to monitor |
| **Grafana** | Visualizes metrics in dashboards |
| **AlertManager** | Sends alerts when thresholds exceeded |

## Why ServiceMonitor?
New service deployed? Auto-discovered! No config change needed.

## Interview Answer
> "I deployed the kube-prometheus-stack using Helm. The key is ServiceMonitor - it's a CRD that tells Prometheus what to scrape based on labels. When we deploy a new service, Prometheus auto-discovers it. Grafana has pre-built K8s dashboards with 7-day retention."

---

# Project 4: Serverless Certificate Monitor

## What You Built
Lambda function monitoring SSL certificates, alerting before expiry.

## Architecture
```
EventBridge (daily) → Lambda → Check 50+ certs → SNS alert if expiring
```

## Why Serverless?
- **$0 cost** - Lambda free tier
- **No servers** - AWS handles everything
- **Reliable** - EventBridge triggers guaranteed

## Interview Answer
> "I built this because we had near-expiry incidents. It's a Python Lambda triggered daily by EventBridge. It connects to each domain via socket, extracts certificate info, and calculates days until expiry. If below thresholds (30/15/7 days), it sends SNS notification. Zero expiry incidents since deployment."

---

# Project 5: Terraform Infrastructure Modules

## What You Built
Reusable Terraform modules for AWS infrastructure.

## Modules Created
```
modules/
├── vpc/           # VPC with public/private subnets
├── ec2/           # EC2 instances
├── security-groups/
├── iam/
└── s3/
```

## Remote State
```hcl
backend "s3" {
  bucket         = "my-tf-state"
  dynamodb_table = "tf-locks"  # Prevents concurrent applies
}
```

## Interview Answer
> "I created reusable Terraform modules following AWS Well-Architected patterns. I use S3 for remote state with DynamoDB locking for team collaboration. Provisioning a new environment went from days to 30 minutes."

---

# Quick Summary

| Project | One-Liner |
|---------|-----------|
| **K8s 3-Tier** | GitOps with ArgoCD auto-deploying from Git |
| **Blue-Green** | Zero-downtime, 2-min rollback via ALB |
| **K8s Monitoring** | Prometheus + Grafana, auto-discovery |
| **Cert Monitor** | $0 serverless Lambda, 50+ certs |
| **Terraform** | Reusable modules, 30-min provisioning |

---

*Read before interview! Good luck! 💪*
