# 🎯 ThoughtSpot Interview Q&A - Complete Reference
## Prepared: Saturday, Jan 31, 2026

---

## 📊 Topics Covered Summary

| Category | Questions | Status |
|----------|-----------|--------|
| AWS Scenarios | 5 | ✅ |
| Terraform | 6 | ✅ |
| CI/CD | 3 | ✅ |
| Docker | 6 | ✅ |
| EC2 Console | 7 | ✅ |
| EKS Project | 7+ | ✅ |

---

# ☁️ AWS Scenarios

## 1. S3 + CloudFront (Static Website)
**Q:** How would you host a static website with high performance globally?

**A:** S3 for static hosting + CloudFront CDN. CloudFront uses 400+ edge locations for low latency. Add OAC (Origin Access Control) to keep S3 private, ACM for HTTPS, Route53 for custom domain.

---

## 2. Lambda Timeout Troubleshooting
**Q:** Lambda works locally but times out in production. How do you troubleshoot?

**A:** Check:
- VPC networking (NAT Gateway or VPC Endpoint for S3)
- Timeout setting (default 3s, increase for file processing)
- Memory allocation (more memory = more CPU)
- IAM permissions (s3:GetObject)
- CloudWatch Logs for errors
- Cold starts (use Provisioned Concurrency)

---

## 3. EKS + ALB 504 Errors
**Q:** Users report intermittent 504 Gateway Timeout. Pods look healthy.

**A:** 504 = backend didn't respond in time. Check:
- ALB idle timeout (default 60s)
- Target Group health
- Readiness probe configuration
- Security Groups (ALB → Node port allowed)
- Application response time (slow DB queries?)

---

## 4. IAM Access Denied
**Q:** Developer can't access S3 even with admin permissions.

**A:** IAM follows: Explicit Deny > Explicit Allow > Implicit Deny
- Bucket policy explicit deny
- Block Public Access setting
- Cross-account (need both IAM + bucket policy)
- SCP (org-level restriction)
- VPC Endpoint policy

---

## 5. CloudWatch Investigation
**Q:** Error rate spiked from 0.1% to 5%. How to investigate?

**A:** Systematic approach:
1. SCOPE: Understand the spike
2. CORRELATE: Traffic, deployments, time-based?
3. LOGS: CloudWatch Logs Insights query
4. DEPENDENCIES: DB, APIs, Lambda limits
5. ROOT CAUSE: Fix and monitor

```sql
fields @timestamp, @message
| filter @message like /ERROR|Exception/
| stats count() by bin(5m)
```

---

# 🔧 Terraform

## 1. State File
**Q:** What is Terraform state?

**A:** JSON file mapping config to real resources. Tracks what exists, stores resource IDs/ARNs, enables plan diff, required for destroy. Best practices: store remotely (S3 + DynamoDB), never edit manually, never commit to Git.

---

## 2. Remote Backend
**Q:** How to manage state in a team?

**A:**
```hcl
backend "s3" {
  bucket         = "my-terraform-state"
  key            = "prod/terraform.tfstate"
  dynamodb_table = "terraform-locks"  # Locking
  encrypt        = true
}
```

---

## 3. Modules
**Q:** What are Terraform modules?

**A:** Reusable infrastructure packages. Write once, use across environments (dev/staging/prod). Keeps code DRY, consistent, and testable.

---

## 4. Plan vs Apply
**Q:** Difference between `terraform plan` and `apply`?

**A:** Plan = dry run (safe), Apply = creates resources. In CI/CD: plan on PRs, apply after merge. Save plan: `terraform plan -out=tfplan`

---

## 5. Failed Apply Recovery
**Q:** Apply failed halfway. What do you do?

**A:** Terraform is idempotent. Check state list, read error, fix issue, run apply again. It skips existing resources, creates remaining. Don't manually delete or edit state.

---

## 6. Sensitive Values
**Q:** How to handle passwords in Terraform?

**A:** AWS Secrets Manager, HashiCorp Vault, environment variables (`TF_VAR_`), or `sensitive = true` flag. Never hardcode or commit to Git.

---

# 🚀 CI/CD

## 1. Pipeline Walkthrough
**A:** CI (automatic): Code push → quality check → security scan → Docker build → push to registry. CD (GitOps): Manual approval → Git manifest update → ArgoCD sync → Helm deploy.

---

## 2. Old Version Still Running
**Q:** Deployment succeeded but users see old version.

**A:** Check: image tag (`latest` caching), ALB target group switch, ImagePullPolicy, ArgoCD sync status, CDN/browser cache.

---

## 3. Rollback Strategies
**Q:** How to rollback quickly?

**A:**
- `kubectl rollout undo deployment/app` (30 sec)
- ArgoCD: revert Git commit
- Blue-Green: switch ALB target group
- Helm: `helm rollback myapp 1`

---

# 🐳 Docker

## 1. Image vs Container
**A:** Image = blueprint (read-only). Container = running instance. One image → many containers.

---

## 2. CMD vs ENTRYPOINT
**A:** CMD = default args (easy to override). ENTRYPOINT = fixed command. Use both: ENTRYPOINT for command, CMD for default args.

---

## 3. Build Optimization
**A:** Order matters for caching:
```dockerfile
COPY requirements.txt .    # Rarely changes
RUN pip install            # Cached!
COPY . .                   # Changes often (last)
```

---

## 4. Networking
**A:** Same network (bridge): containers talk via name (DNS). Different networks: need common network or host mode.

---

## 5. Volumes
**A:** Data persists with volumes. Without volume: container deleted = data gone. Use `-v mydata:/app/data` for persistence.

---

## 6. Multi-stage Builds
**A:** Separate build and runtime stages. Final image contains only runtime files. Result: 90% smaller, faster deploys.

---

# 🖥️ EC2 Console

## 1. AMI
Pre-configured OS template (Amazon Linux, Ubuntu, Windows, Custom)

## 2. Instance Types
`t3.micro` = Family (t=burstable) + Generation (3) + Size (micro)

## 3. Key Pair vs IAM
Key Pair (.pem) = SSH into EC2. IAM Access Key = AWS API/CLI access. Completely different!

## 4. Security Groups vs NACL
SG: Instance level, stateful, allow only. NACL: Subnet level, stateless, allow + deny.

## 5. EBS Volumes
gp3 (general), io2 (databases), st1 (big data), sc1 (cold storage)

## 6. Elastic IP
Static IP that persists across stop/start. Free when attached, ~$3.65/month if idle.

## 7. Auto Scaling
Launch Template → ASG (min/max) → Scaling Policy → CloudWatch triggers scale up/down.

---

# ☸️ EKS Project Q&A

## 1. Why 3-Tier?
Separation of concerns, independent scaling, easy to replace components.

## 2. Why Nginx + Flask?
Nginx: static content, reverse proxy, handles 10K+ connections. Flask: business logic only.

## 3. Service Discovery
CoreDNS resolves service names to ClusterIPs. `backend-service` → `10.96.x.x`

## 4. Why ClusterIP?
Backend/Redis don't need external access. ClusterIP = internal only = secure.

## 5. HPA
Horizontal scaling (more pods, not bigger). Scales 2-10 replicas based on CPU 70%.

## 6. GitOps + ArgoCD
Git = source of truth. ArgoCD monitors repo, syncs changes, self-heals drift.

## 7. Monitoring
Prometheus scrapes /metrics → ServiceMonitor auto-discovers → Grafana visualizes.

---

# 🔀 Ingress Routing

**Path-based:** Same domain, different paths → different services
```yaml
/      → frontend-service
/api/* → backend-service
```

**Host-based:** Different subdomains → different services
```yaml
www.myapp.com  → frontend
api.myapp.com  → backend
```

---

# ✅ Ready for Interview!

**Evening session:** More hands-on + Linux scenarios

*Good luck! 💪*

---

# ☁️ AWS Services - Scenario-Based Questions (For Evening Review)

## From Your Resume: EC2, Lambda, S3, VPC, IAM, CloudWatch, ACM, Route53

---

## 🖥️ EC2 Scenarios

### Q1: Instance won't start
**Scenario:** You try to launch an EC2 instance but it fails immediately.

**Causes:**
- Insufficient capacity in AZ
- Limit reached for instance type
- EBS volume limit exceeded
- Invalid AMI

**Debug:** Check EC2 console "Instance State" → "State Transition Reason"

---

### Q2: Can't SSH to instance
**Scenario:** Instance is running but `ssh: Connection timed out`

**Checklist:**
1. Security Group: Inbound port 22 allowed from your IP?
2. NACL: Port 22 not blocked?
3. Route Table: Public subnet has route to IGW?
4. Key pair: Using correct `.pem` file?
5. Instance has public IP or EIP?

---

### Q3: High CPU but app doesn't need it
**Scenario:** CPU at 100% but your app is idle.

**Check:**
- `top` command to find process
- Could be: crypto mining (compromised), runaway process, CloudWatch agent stuck
- **Action:** Isolate instance, analyze, rebuild from AMI

---

## ⚡ Lambda Scenarios

### Q4: Lambda cold start issues
**Scenario:** First request takes 3-5 seconds, then fast.

**Solutions:**
- Keep Lambda warm (scheduled ping every 5 min)
- Provisioned Concurrency (pre-warm instances)
- Reduce package size (smaller = faster init)
- Use ARM (Graviton2) - faster startup

---

### Q5: Lambda can't access RDS
**Scenario:** Lambda in VPC times out connecting to RDS.

**Check:**
- Lambda subnet has route to RDS subnet?
- Security Groups: Lambda SG → RDS SG on 3306/5432?
- RDS in same VPC or need VPC peering?
- Increase Lambda timeout (default 3s too short)

---

### Q6: Lambda hits concurrency limit
**Scenario:** Requests return 429 TooManyRequests.

**Solutions:**
- Request limit increase (default 1000 concurrent)
- Reserved Concurrency for critical functions
- Use SQS to buffer requests
- Check for Lambda recursion (infinite loop)

---

## 🪣 S3 Scenarios

### Q7: S3 upload slow for large files
**Scenario:** 5GB file upload takes forever.

**Solutions:**
- **Multipart Upload:** Break into 100MB chunks, parallel upload
- **Transfer Acceleration:** Use CloudFront edge locations
- **S3 SDK:** AWS SDK handles multipart automatically for large files

---

### Q8: S3 costs unexpectedly high
**Scenario:** Monthly S3 bill 3x expected.

**Investigate:**
- Storage classes (Standard vs IA vs Glacier)
- Lifecycle policies configured?
- Versioning enabled = multiple copies
- Incomplete multipart uploads
- **Cost Explorer:** Filter by S3, check request costs vs storage

---

### Q9: Objects accessible when they shouldn't be
**Scenario:** Private bucket but objects accessible via URL.

**Check:**
- Block Public Access settings
- Bucket policy has `"Principal": "*"`?
- Object ACLs set to public?
- Pre-signed URLs being shared?

---

## 🔗 VPC Scenarios

### Q10: Private instance can't reach internet
**Scenario:** Private subnet EC2 can't `yum update`.

**Fix:**
1. NAT Gateway in public subnet
2. Private route table: `0.0.0.0/0 → nat-gw-id`
3. NAT Gateway needs Elastic IP
4. Check NACL allows outbound 80/443

---

### Q11: Can't connect to resource in another VPC
**Scenario:** EC2 in VPC-A can't reach RDS in VPC-B.

**Options:**
- **VPC Peering:** Direct connection (no overlapping CIDR)
- **Transit Gateway:** Hub for 10+ VPCs
- Update route tables both sides
- Security Groups allow cross-VPC traffic

---

### Q12: VPC Endpoint vs NAT Gateway
**Q:** When to use each?

| Use Case | Solution |
|----------|----------|
| S3/DynamoDB access | Gateway Endpoint (free!) |
| Other AWS services | Interface Endpoint |
| General internet | NAT Gateway |

**Interview answer:** "For S3, I use VPC Gateway Endpoint—it's free and keeps traffic within AWS network. NAT Gateway is for general internet access from private subnets."

---

## 🔐 IAM Scenarios

### Q13: Least privilege for Lambda
**Q:** Lambda needs S3 read + DynamoDB write. What policy?

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem", "dynamodb:UpdateItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/my-table"
    }
  ]
}
```

**Key:** Specific actions + specific resources, never `*`

---

### Q14: Cross-account access
**Scenario:** Account B needs to read S3 bucket in Account A.

**Solution:**
1. Account A: Bucket policy allows Account B's role
2. Account B: IAM role with AssumeRole to Account A
3. Both policies must allow

---

### Q15: IAM role vs IAM user for EC2
**Q:** Why role, not user?

**Answer:** "Roles provide temporary credentials that auto-rotate. Access keys for users are long-lived and can be leaked. EC2 with IAM role gets temp creds from instance metadata—more secure."

---

## 📊 CloudWatch Scenarios

### Q16: Set up alerting for high CPU
**Steps:**
1. CloudWatch → Alarms → Create
2. Metric: EC2 → CPUUtilization
3. Threshold: > 80% for 5 minutes
4. Action: SNS topic → email/Slack

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

---

### Q17: Custom metrics from application
**Scenario:** Track business metric (orders/minute).

**Solution:**
```python
import boto3
cloudwatch = boto3.client('cloudwatch')
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[{
        'MetricName': 'OrdersPerMinute',
        'Value': 42,
        'Unit': 'Count'
    }]
)
```

---

### Q18: Log retention and cost
**Q:** CloudWatch logs getting expensive.

**Solutions:**
- Set retention period (7, 14, 30 days)
- Export old logs to S3 (cheaper storage)
- Use Log Insights for queries (pay per query)
- Filter what you log (don't log DEBUG in prod)

---

## 🔒 ACM (Certificate Manager) Scenarios

### Q19: Certificate stuck in "Pending Validation"
**Causes:**
1. DNS CNAME not added
2. Wrong CNAME value
3. DNS not propagated yet
4. CNAME in wrong hosted zone

**Debug:**
```bash
dig CNAME _acme-challenge.yourdomain.com
```

---

### Q20: Certificate not auto-renewing
**Check:**
- DNS validation CNAME still exists?
- Certificate actually attached to ALB/CloudFront?
- Email validation but emails going to spam?

**Prevention:** Always use DNS validation, never delete the CNAME.

---

## 🌐 Route53 Scenarios

### Q21: Failover routing
**Scenario:** Primary region fails, switch to DR.

**Setup:**
1. Health check on primary endpoint
2. Failover routing policy
3. Primary record: points to us-east-1
4. Secondary record: points to us-west-2
5. When health check fails → traffic goes to secondary

---

### Q22: Latency-based routing
**Scenario:** Users globally, want lowest latency.

**Setup:**
- Create records for each region
- Select "Latency" routing policy
- Route53 routes user to nearest healthy region

---

### Q23: Private hosted zone
**Q:** Internal DNS for private resources?

**Answer:** "I use Route53 Private Hosted Zone associated with VPC. Internal apps resolve `api.internal.company.com` to private IPs without exposing to internet."

---

## 📬 SNS + SQS Scenarios

### Q24: Decouple microservices
**Scenario:** Order service calls Payment service directly. If Payment is down, orders fail.

**Solution:**
```
Order Service → SQS Queue → Payment Service
```
- Orders don't fail if Payment is down
- Messages queue up, processed when back
- Dead Letter Queue for failed messages

---

### Q25: Fan-out pattern
**Scenario:** One event needs to trigger multiple services.

**Solution:**
```
Event → SNS Topic → SQS Queue 1 → Service A
                  → SQS Queue 2 → Service B
                  → Lambda Function C
```

---

## 📦 DynamoDB Scenarios

### Q26: Hot partition
**Scenario:** DynamoDB throttling despite provisioned capacity.

**Cause:** Bad partition key (e.g., date = today, all writes to one partition)

**Fix:**
- Better partition key (user_id, order_id)
- Add random suffix to spread writes
- Use On-Demand mode for unpredictable traffic

---

### Q27: Query vs Scan
**Q:** When to use each?

| Operation | Use When | Cost |
|-----------|----------|------|
| **Query** | Know partition key | Efficient ✅ |
| **Scan** | Need all items | Expensive ❌ |

**Rule:** Never scan in production. Design schema to always query.

---

## 🚀 EKS Scenarios

### Q28: Pod can't pull image
**Error:** `ImagePullBackOff`

**Check:**
1. Image name/tag correct?
2. Private registry? Add `imagePullSecrets`
3. ECR? Node IAM role has `ecr:GetDownloadUrlForLayer`

---

### Q29: Node joins but shows NotReady
**Check:**
1. Security Group: 443 to control plane, 10250 for kubelet
2. IAM Role: `AmazonEKSWorkerNodePolicy`
3. Kubelet running: `journalctl -u kubelet`
4. CNI plugin installed (aws-vpc-cni)

---

### Q30: ALB Ingress not creating
**Check:**
1. AWS Load Balancer Controller installed?
2. IAM role for service account configured?
3. Subnet tags: `kubernetes.io/role/elb=1`
4. Ingress class annotation correct?

---

## ⏰ Evening Study Plan

1. Read through all scenarios (30 min)
2. Try to answer before looking at solutions
3. Note any concepts still unclear
4. Practice explaining out loud

---

*You've got this! 💪*

---

# 🚀 GitHub Actions - Complete Q&A

## Core Concepts

### Q1: What triggers a pipeline?
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Manual trigger
```

### Q2: How to handle secrets?
- Store in: Settings → Secrets → Actions
- Use as: `${{ secrets.AWS_ACCESS_KEY_ID }}`

### Q3: Docker layer caching?
```yaml
cache-from: type=gha    # Load from GitHub Actions cache
cache-to: type=gha      # Save to cache
```
Result: Builds go from 10 min → 2 min

### Q4: Jobs vs Steps?
| Level | What It Is | Runs On |
|-------|-----------|---------|
| **Job** | Group of steps | Own runner (VM) |
| **Step** | Single action | Same runner |

### Q5: Job dependencies?
```yaml
deploy:
  needs: [build, test]  # Waits for both
```

### Q6: Matrix strategy?
```yaml
matrix:
  node: [14, 16, 18]
  os: [ubuntu, windows]
```
Creates 6 parallel jobs (3 versions × 2 OS)

### Q7: Share files between jobs?
```yaml
- uses: actions/upload-artifact@v4
- uses: actions/download-artifact@v4
```

### Q8: Manual trigger with inputs?
```yaml
workflow_dispatch:
  inputs:
    environment:
      required: true
      default: 'staging'
```

---

# ☸️ K8s Monitoring - Key Concepts

### What is ServiceMonitor?
CRD from Prometheus Operator. Tells Prometheus which services to scrape based on label selectors.

### Why Helm for Prometheus?
`kube-prometheus-stack` includes Prometheus, Grafana, Alertmanager—all pre-configured.

### How Grafana gets data?
Queries Prometheus time-series database using PromQL.

### Monitoring Flow:
```
ServiceMonitor → discovers pods → Prometheus scrapes → Grafana visualizes
```

---

## 📅 Tomorrow (Sunday) - Last Day!

- Morning: Mock interview practice
- Afternoon: Review all notes
- Evening: Rest before Monday

*Good luck! 💪*
