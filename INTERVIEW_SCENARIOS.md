# 🎤 Interview Scenarios - Ready-to-Use Responses
## Based on Your TCS Experience (4 Years SRE)

---

## Scenario 1: "Tell me about a critical incident you handled"

### 🚨 The Incident: Production API Outage Due to Expired Certificate

**SITUATION** (Set the scene - 30 seconds)
> "At TCS, I manage reliability for 20+ production applications across AWS and Azure. One Friday evening around 7 PM, while I was on-call, we received a P1 alert—our customer-facing API was returning connection errors. Users couldn't access the application, and the business impact was immediate."

**TASK** (Your responsibility - 15 seconds)
> "As the on-call SRE, my immediate responsibility was to restore service as fast as possible while minimizing customer impact. I also needed to communicate status to stakeholders and document everything for the post-incident review."

**ACTION** (What you did - 2 minutes)
> "I started with quick triage. First, I checked Dynatrace and CloudWatch dashboards to understand the scope—all API endpoints were failing, not just specific ones. That told me it wasn't an application bug but likely infrastructure.

> Next, I checked the ALB health checks in AWS Console—all targets were healthy. So the issue was between the user and the ALB. I ran a quick curl command to the API endpoint and saw 'SSL certificate problem: certificate has expired.'

> I immediately checked AWS ACM—the certificate for our API domain had expired just 30 minutes ago. The auto-renewal had failed silently because the DNS validation CNAME record was accidentally deleted during a DNS migration two weeks earlier.

> For the immediate fix, I:
> 1. Re-added the DNS validation CNAME record in Route53
> 2. Requested a new certificate in ACM (since the old one was expired)
> 3. Validated the new cert (DNS propagated in about 5 minutes)
> 4. Updated the ALB HTTPS listener with the new certificate ARN

> Service was restored in about 25 minutes. Throughout this, I kept the incident Slack channel updated every 5 minutes and escalated to our manager after the 15-minute mark as per our P1 protocol."

**RESULT** (Outcome and improvements - 30 seconds)
> "Service was restored within our 30-minute SLA. In the post-incident review, we identified two improvements:
> 1. I built a Lambda-based certificate monitoring solution that checks all our 38+ certificates daily and alerts 30, 15, and 7 days before expiry
> 2. We added ACM certificate status to our CloudWatch dashboard
> 
> Since implementing that monitor, we've had zero certificate-related incidents—that's been running for 18 months now."

---

### 📝 Follow-up Questions They Might Ask:

**Q: "How did you prioritize during the incident?"**
> "My priority was: 1) Restore service first, 2) Communicate status, 3) Document for RCA. I didn't waste time on root cause during the incident—that came in the post-mortem."

**Q: "What would you do differently?"**
> "I would have caught this proactively if we had certificate monitoring earlier. That's exactly why I built the serverless monitor afterward—to shift from reactive to proactive."

**Q: "How did you communicate during the incident?"**
> "Every 5 minutes, I posted a status update in the incident channel with: current status, what I'm trying, and ETA. At 15 minutes, I escalated to my manager per our P1 protocol. After resolution, I sent a summary email to stakeholders."

---

## Scenario 2: "Walk me through your day-to-day activities"

### 📅 A Typical Day as SRE at TCS

**MORNING (9:00 - 12:00)**
> "My day starts with checking overnight alerts. I review our monitoring dashboards in Dynatrace and Splunk to see if any issues occurred during off-hours. I check:
> - Any P2/P3 incidents from the night shift that need follow-up
> - Application health metrics—error rates, latency, throughput
> - Infrastructure metrics—CPU, memory, disk across our 20+ production apps
> 
> Then I handle the queue. We use ServiceNow for incident tickets. I triage new tickets—some are quick fixes like restarting an app pool or clearing disk space. Others need investigation.
> 
> A typical morning might involve:
> - Investigating why an application's response time increased by 20%
> - Reviewing and approving a change request for a production deployment
> - Joining a quick standup with the 6-member SRE team to sync on priorities"

**AFTERNOON (13:00 - 17:00)**
> "Afternoons are usually for deeper work:
> 
> **Automation work**: I spend time reducing toil. For example, I built Python scripts using Boto3 to automate our monthly compliance reporting—that went from 4 hours of manual work to 15 minutes automated. I also developed Ansible playbooks for common IIS server operations, which reduced those incident tickets by 30%.
> 
> **Monitoring improvements**: I maintain our health monitoring bots that scan 50+ endpoints hourly. If I notice gaps in our observability, I add new alerts or dashboards.
> 
> **Change management**: I review upcoming changes, ensure they have proper rollback plans, and sometimes execute production deployments during change windows.
> 
> **Documentation**: I update runbooks when I learn something new from an incident. I've authored 10+ runbooks that our team uses—things like 'How to troubleshoot memory issues on Windows servers' or 'Steps to renew SSL certificates.'"

**ON-CALL ROTATION**
> "We have a weekly on-call rotation. During my on-call week, I'm the first responder for P1/P2 incidents. I carry a laptop and phone everywhere. Most weeks, I handle 2-3 after-hours pages—usually things like disk space alerts or an application restart needed.
> 
> For critical incidents, I follow our runbooks, escalate if needed, and always write up an RCA within 48 hours."

---

### 📝 Follow-up Questions They Might Ask:

**Q: "How do you balance reactive vs proactive work?"**
> "I aim for 30% reactive (incidents, tickets) and 70% proactive (automation, monitoring improvements). When toil increases, I prioritize building automation to bring it back down. For example, our compliance reporting was eating 4+ hours monthly—now it's automated."

**Q: "What tools do you use daily?"**
> "Dynatrace and CloudWatch for monitoring, Splunk for log analysis, ServiceNow for ticketing, Python/Boto3 for automation, Ansible for configuration management, and Git for version control. I also use kubectl regularly for our Kubernetes workloads."

**Q: "How do you handle multiple priorities?"**
> "P1 incidents always come first—everything else stops. For non-urgent work, I use a simple priority matrix: high-impact automation projects over low-impact. I timebox investigation work—if I can't solve something in 2 hours, I escalate or pair with a teammate."

**Q: "Give an example of automation you built."**
> "Our monthly compliance report required manually checking certificate expiry dates, server patch levels, and backup status across 40+ servers. I built a Python script that:
> 1. Queries AWS and Azure APIs for certificate and resource status
> 2. Connects to servers to check patch compliance
> 3. Generates an Excel report automatically
> This reduced a 4-hour task to 15 minutes—95% reduction in toil."

---

## 🎯 Practice Tips

1. **Time yourself**: Incident story should be 3-4 minutes total
2. **Practice out loud**: Record yourself and listen back
3. **Prepare variations**: Have 2-3 incident stories ready
4. **Be specific**: Use numbers (30 minutes, 38 certificates, 95% reduction)
5. **Show growth**: Always end with what you learned/improved

---

## ✅ Quick Checklist Before Interview

- [ ] Can tell incident story in under 4 minutes
- [ ] Know exact numbers from your resume
- [ ] Can explain each resume project in 2 minutes
- [ ] Have 2-3 questions ready for them
- [ ] Know "Why ThoughtSpot?" answer

---

*Save this file and practice these out loud!* 🎤
