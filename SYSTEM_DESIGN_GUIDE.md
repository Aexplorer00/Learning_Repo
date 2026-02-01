# System Design for SRE
## Architecture Patterns + Interview Prep

---

## 🎯 What is System Design?

**Designing scalable, reliable, maintainable systems**

```
User → Load Balancer → Web Servers → Cache → Database
```

**Key Focus Areas:**
- Scalability (handle growth)
- Reliability (uptime)
- Performance (speed)
- Maintainability (easy to change)

---

## 📦 Core Components

### 1. Load Balancer

```
           ┌──→ Server 1
Client → ALB ──→ Server 2
           └──→ Server 3
```

**Types:**
| Type | Layer | Use Case |
|------|-------|----------|
| ALB | Layer 7 (HTTP) | Web apps, path routing |
| NLB | Layer 4 (TCP) | High performance, gaming |
| CLB | Classic | Legacy |

**Algorithms:**
- Round Robin (rotate)
- Least Connections
- IP Hash (sticky sessions)

---

### 2. Caching

```
Client → Cache (Redis) → Database
         ↑ 
    Cache Hit = Fast!
    Cache Miss = Query DB
```

**Types:**
| Cache | Use Case |
|-------|----------|
| **CDN** | Static files (images, CSS) |
| **Redis/Memcached** | Session, frequent queries |
| **Application** | In-memory data |

**Strategies:**
- Cache-Aside: App manages cache
- Write-Through: Write to cache + DB
- Write-Behind: Write to cache, async to DB

---

### 3. Database

**SQL vs NoSQL:**

| Feature | SQL (RDS) | NoSQL (DynamoDB) |
|---------|-----------|------------------|
| Schema | Fixed | Flexible |
| Scaling | Vertical | Horizontal |
| ACID | Yes | Eventual consistency |
| Use Case | Transactions | High scale, flexible |

**Scaling Patterns:**
- **Read Replicas**: Handle read load
- **Sharding**: Split data across DBs
- **Master-Slave**: Write to master, read from slave

---

### 4. Message Queues

```
Producer → Queue (SQS) → Consumer
              ↓
         Decoupling!
```

**When to use:**
- Async processing
- Decouple services
- Handle traffic spikes

**Types:** SQS, RabbitMQ, Kafka

---

### 5. CDN (Content Delivery Network)

```
         ┌─ Edge (Mumbai)
User 1 ──┤
         └─ Edge (Singapore)
                  ↑
            Origin (S3)
```

**Benefits:**
- Low latency
- Reduce server load
- Global distribution

---

## 🏗️ Common Architecture Patterns

### Pattern 1: 3-Tier Architecture

```
┌─────────────────────────────────────────────┐
│                 Internet                     │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│           Load Balancer (ALB)               │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│          Web Tier (EC2 / ECS)               │
│    ┌───────┐  ┌───────┐  ┌───────┐          │
│    │  Web  │  │  Web  │  │  Web  │          │
│    └───────┘  └───────┘  └───────┘          │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│         App Tier (EC2 / Lambda)             │
│    ┌───────┐  ┌───────┐  ┌───────┐          │
│    │  App  │  │  App  │  │  App  │          │
│    └───────┘  └───────┘  └───────┘          │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│          Data Tier (RDS / DynamoDB)         │
│         ┌─────────┐  ┌─────────┐            │
│         │ Primary │─▶│ Replica │            │
│         └─────────┘  └─────────┘            │
└─────────────────────────────────────────────┘
```

---

### Pattern 2: Microservices

```
         ┌────────────────────────────────────┐
         │           API Gateway              │
         └────────────────┬───────────────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
┌─────────┐         ┌─────────┐          ┌─────────┐
│  User   │         │  Order  │          │ Payment │
│ Service │         │ Service │          │ Service │
└────┬────┘         └────┬────┘          └────┬────┘
     │                   │                    │
     ▼                   ▼                    ▼
┌─────────┐         ┌─────────┐          ┌─────────┐
│ User DB │         │Order DB │          │Payment DB│
└─────────┘         └─────────┘          └─────────┘
```

**Communication:**
- Sync: REST, gRPC
- Async: Message queues (SQS, Kafka)

---

### Pattern 3: Event-Driven

```
Event Source → Event Bus → Lambda → Process
     │              ↓
     │          EventBridge
     │              ↓
     └──────→ SQS → Lambda → DynamoDB
```

---

## 📊 Scalability Strategies

### Vertical Scaling
```
Small Server → Bigger Server
Problem: Physical limits, expensive, single point of failure
```

### Horizontal Scaling
```
1 Server → Many Servers (behind Load Balancer)
Better: No limit, fault tolerant
```

### Auto Scaling
```
Low Traffic → 2 instances
High Traffic → 10 instances (auto)
```

---

## 🎤 Interview Questions

### Q1: Design a URL Shortener (like bit.ly)

```
Components:
1. API: Create short URL, Redirect
2. Database: Store URL mappings
3. Cache: Frequent URLs
4. Counter/Hash: Generate short codes

Flow:
POST /shorten → Generate code → Store in DB → Return short URL
GET /abc123 → Cache lookup → DB lookup → 301 Redirect
```

### Q2: Design a Rate Limiter

```
Components:
1. Counter per user/IP
2. Time window (1 min, 1 hr)
3. Redis for fast lookup

Algorithms:
- Token Bucket
- Sliding Window
- Fixed Window
```

### Q3: Design Twitter/Feed

```
Components:
1. User Service
2. Tweet Service
3. Timeline Service (Fan-out)
4. Cache (Redis) for hot users
5. CDN for media

Fan-out approaches:
- Push: Write to all follower feeds (celeb problem)
- Pull: Fetch tweets at read time (slow for big feeds)
- Hybrid: Push for normal, pull for celebs
```

### Q4: Design a File Storage (like S3)

```
Components:
1. Metadata DB (filename, size, owner)
2. Object Storage (actual files)
3. CDN for delivery
4. Replication for durability

Challenges:
- Large files (chunking)
- Consistency
- Deduplication
```

---

## 🔥 Design Interview Framework

### Step 1: Clarify Requirements (2-3 min)
- Functional: What features?
- Non-functional: Scale, latency, consistency?
- Constraints: Budget, timeline?

### Step 2: High-Level Design (5 min)
- Draw main components
- Show data flow
- Identify APIs

### Step 3: Deep Dive (15 min)
- Database schema
- Caching strategy
- Scaling approach
- Failure handling

### Step 4: Trade-offs (5 min)
- Consistency vs Availability
- Cost vs Performance
- Complexity vs Speed

---

## 📦 Numbers to Remember

| Metric | Value |
|--------|-------|
| Read from disk | ~10 ms |
| Read from RAM | ~100 ns |
| Network round trip | ~1 ms |
| 1 million requests/day | ~12 req/sec |
| 1 billion requests/day | ~12,000 req/sec |

---

*Created for: DEVOPS/SRE 60-Day Journey (Day 7 Extra)*
