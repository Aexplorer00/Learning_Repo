# 🎯 AWS Adrian Cantrill - Jan End Sprint Plan
## Focus: Interview-Critical Topics for SRE/DevOps (Jan 17-31)

---

## 🚀 **WEEK 1: Core Infrastructure (Jan 17-19)**

### Friday, Jan 17 (2 hours)
**IAM Deep Dive**
- [ ] IAM Identity Policies (15 min)
- [ ] IAM Users and ARNs (13 min)
- [ ] IAM Roles - The Tech (8 min)
- [ ] When to use IAM Roles (15 min)
- [ ] AWS Organizations (12 min)
- [ ] Service Control Policies (12 min)
- **Practice**: Create IAM role for EC2 → S3 access

### Saturday, Jan 18 (3 hours)  
**CloudFormation Foundations**
- [ ] Physical & Logical Resources (7 min)
- [ ] Template & Pseudo Parameters (6 min)
- [ ] Intrinsic Functions (14 min)
- [ ] Mappings (4 min) + Outputs (3 min)
- [ ] DEMO: Template v2 Portable (13 min)
- [ ] Nested Stacks (13 min)
- [ ] Cross-Stack References (10 min)
- **Practice**: Deploy VPC stack with reusable templates

### Sunday, Jan 19 (2 hours)
**Route53 & DNS**
- [ ] Route53 Fundamentals (6 min)
- [ ] DNS Record Types (13 min)
- [ ] Public Hosted Zones (6 min)
- [ ] CNAME vs Alias (5 min)
- [ ] Health Checks (12 min)
- [ ] Failover Routing (1 min)
- [ ] DEMO: Route53 + Failover Routing (16 + 6 min)
- **Practice**: Set up failover between two regions

---

## 🐳 **WEEK 2: Serverless & Containers (Jan 20-23)**

### Monday, Jan 20 (Evening - 1.5 hours)
**Lambda Essentials**
- [ ] AWS Lambda PART 1-3 (11 + 13 + 17 min)
- [ ] Lambda Versions (4 min) + Aliases (4 min)
- [ ] Environment Variables (7 min)
- [ ] Monitoring & Logging Lambda (13 min)
- **Practice**: Create Lambda for S3 event processing

### Tuesday, Jan 21 (Evening - 1.5 hours)
**Containers & ECS**
- [ ] Introduction to Containers (17 min)
- [ ] ECS Concepts (10 min)
- [ ] ECS Cluster Mode (13 min)
- [ ] Kubernetes 101 (11 min)
- [ ] EKS 101 (6 min)
- **Practice**: Deploy container to ECS Fargate (already done in your project! ✅)

### Wednesday, Jan 22 (Evening - 1.5 hours)
**API Gateway & EventBridge**
- [ ] API Gateway 101 (16 min)
- [ ] Methods and Resources (4 min)
- [ ] Integrations (14 min)
- [ ] CloudWatch Events & EventBridge (6 min)
- [ ] Step Functions (16 min)
- **Practice**: API Gateway → Lambda integration

### Thursday, Jan 23 (Evening - 1.5 hours)
**Messaging & Queues**
- [ ] Simple Notification Service (7 min)
- [ ] Simple Queue Service (15 min)
- [ ] SQS Standard vs FIFO (3 min)
- [ ] SQS Dead-Letter Queues (4 min)
- **Mini-Project**: Start Pet-Cuddle-o-Tron (Part 1-2)

---

## 🔄 **WEEK 3: CI/CD & Monitoring (Jan 24-26)**

### Friday, Jan 24 (Evening - 2 hours)
**CI/CD Pipeline**
- [ ] CICD in AWS (14 min)
- [ ] CodePipeline 101 (4 min)
- [ ] CodeBuild 101 (6 min)
- [ ] CodeDeploy 101 (10 min)
- [ ] Elastic Container Registry (4 min)
- **Practice**: Set up basic CodePipeline (build → test)

### Saturday, Jan 25 (3 hours)
**Monitoring Deep Dive**
- [ ] CloudWatch PART 1-2 (9 + 9 min)
- [ ] CloudWatch Logs (13 min)
- [ ] DEMO: CloudWatch Agent (11 + 8 min)
- [ ] CloudTrail (11 min)
- [ ] Config (6 min)
- **Practice**: Set up centralized logging with CloudWatch Logs

### Sunday, Jan 26 (2 hours)
**Systems Manager**
- [ ] SSM Architecture (7 min)
- [ ] SSM Run Command (4 min)
- [ ] SSM Documents (7 min)
- [ ] SSM Inventory & Patching (11 min)
- [ ] SSM Parameter Store (17 min)
- [ ] Secrets Manager (7 min)
- **Practice**: Use SSM to patch fleet of EC2 instances

---

## 📊 **WEEK 4: HA, DR & Storage (Jan 27-31)**

### Monday-Tuesday, Jan 27-28 (1.5 hours each)
**High Availability & Disaster Recovery**
- [ ] HA vs FT vs DR (17 min)
- [ ] Types of DR (17 min)
- [ ] Launch Templates (4 min)
- [ ] Auto-Scaling Groups (16 min)
- [ ] ASG Scaling Policies (10 min)
- [ ] ELB Architecture PART 1-2 (10 + 12 min)
- [ ] ALB vs NLB (16 min)
- **Practice**: Set up ASG with ALB health checks

### Wednesday-Thursday, Jan 29-30 (1.5 hours each)
**Storage Deep Dive**
- [ ] S3 Security (18 min)
- [ ] S3 Versioning & MFA Delete (7 min)
- [ ] S3 Encryption (23 min)
- [ ] S3 Lifecycle (8 min)
- [ ] S3 Replication (13 min)
- [ ] EBS Architecture (8 min)
- [ ] EBS Volume Types (9 + 6 + 4 min)
- **Practice**: Set up cross-region S3 replication with KMS

### Friday, Jan 31 (2 hours - Final Review)
**Interview Prep Focus**
- [ ] Trusted Advisor (8 min)
- [ ] Inspector (6 min)
- [ ] GuardDuty (4 min)
- [ ] Sample Question Walkthrough 1-2 (8 + 8 min)
- **Activity**: Mock interview with all topics covered
- **Update**: Resume with newly learned services

---

## ✅ **Priority Checklist (Must-Know for Interviews)**

### Compute & Orchestration
- [ ] EC2, ASG, Launch Templates
- [ ] Lambda (versions, aliases, VPC access)
- [ ] ECS/EKS basics

### Networking
- [ ] VPC, Subnets, Route Tables
- [ ] ALB, NLB (differences)
- [ ] Route53 (routing policies)

### Storage
- [ ] S3 (versioning, encryption, lifecycle)
- [ ] EBS (volume types)

### Security
- [ ] IAM (roles, policies, SCPs)
- [ ] KMS, Secrets Manager, Parameter Store

### CI/CD
- [ ] CodePipeline, CodeBuild, CodeDeploy
- [ ] CloudFormation (stacks, nested stacks)

### Monitoring
- [ ] CloudWatch (metrics, logs, alarms)
- [ ] CloudTrail (audit logging)

### Serverless
- [ ] Lambda + API Gateway
- [ ] Step Functions
- [ ] SNS + SQS

---

## 📈 **Daily Study Routine (Weekdays)**

**Evening Slot (7:00 - 8:30 PM):**
- 30 min: Watch 2-3 videos (theory)
- 30 min: Hands-on practice in AWS Console
- 30 min: Document learnings + flashcards

**Weekend Slot (9:00 AM - 12:00 PM):**
- 1 hour: Video lessons
- 1 hour: Hands-on labs
- 1 hour: Mini-projects or demos

---

## 🎯 **Success Metrics (Jan 31)**

By month end, you should be able to:
1. ✅ Explain IAM roles vs users vs groups with real-world examples
2. ✅ Design a 3-tier app architecture with HA/DR (already done!)
3. ✅ Set up a full CI/CD pipeline (CodeCommit → CodeBuild → CodeDeploy)
4. ✅ Configure CloudFormation nested stacks
5. ✅ Implement Lambda + API Gateway + DynamoDB serverless app
6. ✅ Explain ASG scaling policies and ELB health checks
7. ✅ Set up S3 cross-region replication with encryption
8. ✅ Use SSM to manage and patch EC2 fleet

---

## 💡 **Pro Tips**

1. **Skip the "Preview" videos** - Focus on demos and hands-on
2. **Watch at 1.25x-1.5x speed** for theory, normal for demos
3. **Use AWS Free Tier** - Most demos work within free tier limits
4. **Take Screenshots** - Save your AWS Console configs for interview prep
5. **Link to Your Project** - Connect new concepts to your EKS 3-Tier App

---

**Total Study Time Commitment:**
- Weekdays (Jan 17-31): 10 days × 1.5 hrs = 15 hours
- Weekends (Jan 18-19, 25-26): 4 days × 2.5 hrs = 10 hours
- **Grand Total**: ~25 hours (very achievable!)

---

*This plan covers 80% of AWS interview questions while skipping less critical topics like OpsWorks, Advanced Athena, EMR deep dives, etc.*
