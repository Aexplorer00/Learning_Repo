# 🔧 Troubleshooting Scenarios for Interview
## STAR Format Stories (Situation, Task, Action, Result)

---

# Scenario 1: API Latency Spike During Peak Hours

## Situation
"During my morning shift, I was reviewing overnight incidents from our onshore team and noticed CloudWatch alarms had triggered for increased API response times. Our payment API latency had spiked from the normal 200ms to over 2 seconds, affecting customer transactions during peak business hours."

## Task
"As the SRE on duty, I needed to quickly identify the root cause, coordinate with stakeholders, and restore normal service levels while minimizing business impact."

## Action
"I followed our incident response process:

1. **Scoped the Impact:**
   - Checked Splunk dashboards to confirm which APIs were affected
   - Verified it was isolated to the payment service, not system-wide
   - Confirmed ~15% of transactions were timing out

2. **Investigated Root Cause:**
   - Opened CloudWatch Log Insights and queried for errors in the payment service
   - Found the database connection pool was exhausted
   - Correlated timing with a scheduled deployment the previous night

3. **Identified the Issue:**
   - The deployment included a new feature that opened DB connections but wasn't releasing them properly
   - Connection pool maxed out at 100 connections, causing new requests to queue

4. **Implemented Fix:**
   - Coordinated with DevOps team to rollback to previous version
   - Executed rollback via our CI/CD pipeline (ArgoCD in our case)
   - Monitored the recovery in real-time via Grafana dashboards

5. **Verified Recovery:**
   - Confirmed latency dropped back to normal 200ms range
   - Verified no stuck transactions in the queue
   - Checked database connection count returned to normal (~30)"

## Result
"We restored normal service within 25 minutes of my initial detection. I documented the incident, created a post-mortem highlighting the need for connection leak testing in our CI pipeline, and worked with the development team to add a connection pool monitoring dashboard. The fix was later re-deployed with proper connection handling."

---

## Key Talking Points

- **Tools used:** CloudWatch, Splunk, Grafana, ArgoCD
- **Skills demonstrated:** Systematic debugging, root cause analysis, cross-team coordination
- **Outcome:** Reduced MTTR, preventive measures implemented

---

# Scenario 2: API Returning Incorrect Data After Enterprise Change

## Situation
"We had a scheduled enterprise change window where the database team performed a schema migration. The next morning, during my routine health checks, I noticed our monitoring showed successful API responses (200 OK) but the business team reported customers were seeing incorrect account information."

## Task
"I needed to investigate why the API was returning incorrect data despite passing all our automated health checks, and coordinate a fix while managing communication with stakeholders."

## Action
"I approached this systematically:

1. **Verified the Issue:**
   - Manually tested the API endpoints through Postman
   - Confirmed the API returned 200 but data was stale/incorrect
   - Our health checks only verified HTTP status, not data correctness

2. **Traced the Data Flow:**
   - Checked application logs in Splunk for any errors
   - Found no errors - the app was functioning 'normally'
   - Reviewed the change records for the overnight enterprise change

3. **Identified Root Cause:**
   - The database migration added new columns but the application's cache (Redis) still held old data format
   - Cache TTL was set to 24 hours, so stale data was being served
   - The change management didn't include cache invalidation step

4. **Implemented Fix:**
   - Connected to Redis cluster and flushed the affected cache keys
   - Verified fresh data was being fetched from database
   - Confirmed with business team that correct data was now showing

5. **Prevented Recurrence:**
   - Updated our change management checklist to include cache considerations
   - Created a validation script to verify data integrity post-deployment
   - Added synthetic monitoring that checks actual data content, not just HTTP status"

## Result
"Issue was resolved within 45 minutes of detection. The incident led to improving our health check strategy - we now have synthetic tests that validate actual response content, not just status codes. I also created documentation for our runbook about cache invalidation procedures for database changes."

---

## Key Talking Points

- **Tools used:** Splunk, Redis, Postman, Change Management system
- **Skills demonstrated:** Deep investigation beyond surface symptoms, process improvement
- **Outcome:** Improved monitoring, updated change procedures

---

# Quick Reference: STAR Format Tips

| Element | What to Include |
|---------|-----------------|
| **S**ituation | Context, scale, urgency |
| **T**ask | Your specific responsibility |
| **A**ction | Step-by-step what YOU did |
| **R**esult | Metrics, improvements, lessons |

## Your Daily Activities to Mention

**When asked "Walk me through your typical day as an SRE":**

> "My day starts with reviewing overnight incidents from our onshore team and checking the handoff notes. I then go through our monitoring dashboards—Grafana for infrastructure metrics, CloudWatch for AWS resources, and Splunk for application logs. 
>
> I perform manual health checks across all our production applications and verify if there are any scheduled deployments for the day. We also monitor **SSIS and Databricks jobs** daily using **Control-M** as our job scheduling and monitoring tool—if any jobs fail overnight, I investigate the logs and coordinate with the data team for fixes.
>
> Throughout the day, I work on assigned automation tasks using Python and Boto3, respond to any alerts from CloudWatch Log Insights, and support enterprise-level changes. Common issues I handle include API latency spikes, connection pool issues, and data pipeline failures. I document incidents and contribute to our runbooks for recurring issues."

---

## Key Tools to Mention

| Category | Tools |
|----------|-------|
| **Monitoring** | Grafana, CloudWatch, Splunk, Dynatrace |
| **Job Scheduling** | Control-M, SSIS, Databricks |
| **Cloud** | AWS (EC2, S3, Lambda, EKS, CloudWatch) |
| **Containers** | Kubernetes, Docker, Helm |
| **CI/CD** | GitHub Actions, ArgoCD |
| **Automation** | Python, Boto3, Ansible |

---

*Practice saying these out loud before the interview!* 🎯
