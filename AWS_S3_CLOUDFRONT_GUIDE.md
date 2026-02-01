# 📦 AWS S3 & CloudFront Complete Guide

**Deep Dive: Storage + CDN**

---

# Part 1: S3 Fundamentals

## What is S3?
- **Simple Storage Service** - Object storage
- **Unlimited storage** - Pay for what you use
- **Highly durable** - 99.999999999% (11 9's)
- **Highly available** - 99.99%

---

## Key Concepts

### Bucket
- Container for objects
- **Globally unique name** across ALL AWS accounts
- Created in ONE region
- Flat structure (no folders, just prefixes)

### Object
- File + metadata
- **Key** = full path (e.g., `folder/image.png`)
- **Value** = file content
- **Max size** = 5 TB (multipart upload for >5GB)

```
s3://my-company-bucket/images/logo.png
       └── Bucket ──┘└─── Key ────┘
```

---

## S3 URIs vs URLs

| Type | Format | Use |
|------|--------|-----|
| **S3 URI** | `s3://bucket/key` | CLI, SDK |
| **Path URL** | `https://s3.region.amazonaws.com/bucket/key` | Virtual hosting |
| **Virtual URL** | `https://bucket.s3.region.amazonaws.com/key` | Standard |

---

# Part 2: Storage Classes

## Comparison Table

| Class | Retrieval | Min Duration | AZs | Use Case |
|-------|-----------|--------------|-----|----------|
| **Standard** | Instant | None | 3+ | Frequently accessed |
| **Intelligent-Tiering** | Instant | 30 days | 3+ | Unknown patterns |
| **Standard-IA** | Instant | 30 days | 3+ | Infrequent, instant need |
| **One Zone-IA** | Instant | 30 days | 1 | Reproducible data |
| **Glacier Instant** | Instant | 90 days | 3+ | Archive, instant access |
| **Glacier Flexible** | 1-12 hours | 90 days | 3+ | Archive, can wait |
| **Glacier Deep** | 12-48 hours | 180 days | 3+ | Long-term compliance |

## Cost Comparison (approx. per GB/month)
```
Standard:        $0.023
Standard-IA:     $0.0125
One Zone-IA:     $0.010
Glacier Instant: $0.004
Glacier Flexible:$0.0036
Glacier Deep:    $0.00099
```

## Interview Question:
> "How do you optimize S3 storage costs?"
>
> "I use **Lifecycle Rules** to automatically transition objects between storage classes. Frequently accessed data stays in Standard. After 30 days, it moves to Standard-IA. After 90 days, to Glacier. This can reduce storage costs by 70%+."

---

# Part 3: S3 Security

## Block Public Access (Account/Bucket Level)
- **BlockPublicAcls** - Block new public ACLs
- **IgnorePublicAcls** - Ignore existing public ACLs
- **BlockPublicPolicy** - Block public bucket policies
- **RestrictPublicBuckets** - Restrict access via public policies

**Best Practice:** Enable ALL at account level, disable selectively for public buckets.

---

## Bucket Policies (JSON)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

### Common Patterns:

**Allow CloudFront Only (OAC)**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "cloudfront.amazonaws.com"},
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*",
    "Condition": {
      "StringEquals": {
        "AWS:SourceArn": "arn:aws:cloudfront::123456789:distribution/EXXX"
      }
    }
  }]
}
```

**Deny Non-HTTPS**
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": ["arn:aws:s3:::my-bucket/*"],
  "Condition": {"Bool": {"aws:SecureTransport": "false"}}
}
```

---

## Encryption

| Type | Key Managed By | When to Use |
|------|---------------|-------------|
| **SSE-S3** | AWS (AES-256) | Default, simple |
| **SSE-KMS** | AWS KMS | Audit trail, key rotation |
| **SSE-C** | Customer | Full control |
| **Client-side** | You | Encrypt before upload |

### Enable Default Encryption
```bash
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
  }'
```

---

# Part 4: Versioning

## What It Does
- Keeps ALL versions of objects
- Protects against accidental overwrites/deletes
- **Delete Marker** = soft delete

## States
- **Unversioned** (default)
- **Enabled**
- **Suspended** (can't go back to unversioned)

## How Delete Works with Versioning
```
1. Delete object → Creates "Delete Marker"
2. Object appears deleted
3. But all versions still exist!
4. Delete the marker → Object reappears
5. Permanently delete → Specify version ID
```

## CLI Commands
```bash
# Enable versioning
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions --bucket my-bucket

# Delete specific version
aws s3api delete-object --bucket my-bucket --key file.txt --version-id xxx
```

---

# Part 5: Lifecycle Rules

## Automate Storage Management

```yaml
Rules:
  - Transition to Standard-IA after 30 days
  - Transition to Glacier after 90 days
  - Delete after 365 days
  - Delete incomplete multipart uploads after 7 days
```

## CLI Example
```bash
aws s3api put-bucket-lifecycle-configuration --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
```

**lifecycle.json:**
```json
{
  "Rules": [{
    "ID": "ArchiveRule",
    "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transitions": [
      {"Days": 30, "StorageClass": "STANDARD_IA"},
      {"Days": 90, "StorageClass": "GLACIER"}
    ],
    "Expiration": {"Days": 365}
  }]
}
```

---

# Part 6: Static Website Hosting

## Enable Website Hosting
```bash
aws s3 website s3://my-bucket \
  --index-document index.html \
  --error-document error.html
```

## Website Endpoint
```
http://my-bucket.s3-website-ap-south-1.amazonaws.com
```

**Note:** HTTP only! Use CloudFront for HTTPS.

---

# Part 7: Cross-Region Replication (CRR)

## What It Does
- Replicate objects to another region
- Disaster Recovery
- Compliance (data residency)
- Reduce latency

## Requirements
- Versioning enabled on BOTH buckets
- IAM role with replication permissions

---

# Part 8: S3 CLI Commands Reference

```bash
# Bucket operations
aws s3 mb s3://my-bucket                    # Create bucket
aws s3 rb s3://my-bucket                    # Delete (empty) bucket
aws s3 rb s3://my-bucket --force            # Delete bucket + all objects

# Object operations
aws s3 ls                                   # List buckets
aws s3 ls s3://my-bucket/                   # List objects
aws s3 ls s3://my-bucket/ --recursive       # List all (recursive)

aws s3 cp file.txt s3://my-bucket/          # Upload
aws s3 cp s3://my-bucket/file.txt ./        # Download
aws s3 mv s3://my-bucket/old.txt s3://my-bucket/new.txt  # Move/rename

aws s3 rm s3://my-bucket/file.txt           # Delete
aws s3 rm s3://my-bucket/ --recursive       # Delete all objects

aws s3 sync ./folder s3://my-bucket/folder/ # Sync local to S3
aws s3 sync s3://my-bucket/folder/ ./folder # Sync S3 to local

# Presigned URLs (temporary access)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

---

# Part 9: CloudFront (CDN)

## What is CloudFront?
- **Content Delivery Network** (CDN)
- Caches content at **400+ edge locations**
- Reduces latency for global users
- Accelerates both static AND dynamic content

---

## How It Works

```
User Request
    ↓
Edge Location (nearest)
    ↓
[Cache Hit?] → Return cached content
    ↓ (Cache Miss)
Origin (S3, ALB, EC2, Custom)
    ↓
Fetch content → Cache at edge → Return to user
```

---

## Key Components

### Distribution
- CloudFront configuration
- Domain: `d1234abcd.cloudfront.net`
- Can use custom domain with SSL

### Origin
| Type | Use Case |
|------|----------|
| **S3 Bucket** | Static files |
| **S3 Website** | Static website |
| **ALB/ELB** | Dynamic apps |
| **EC2** | Custom servers |
| **Custom Origin** | Any HTTP server |

### Cache Behavior
- **Path Pattern:** `/images/*`, `/api/*`
- **TTL:** How long to cache
- **Allowed Methods:** GET, POST, etc.
- **Headers/Cookies/Query Strings:** Forward to origin?

### Edge Location
- AWS data center close to users
- Caches content
- 400+ worldwide

---

## S3 + CloudFront Best Practice

### Origin Access Control (OAC)
Keep S3 bucket private, only allow CloudFront access.

```
User → CloudFront → S3 (private bucket)
         │
    OAC validates request
```

---

## Cache Invalidation

When you update content, CloudFront may still serve old cached version.

**Force refresh:**
```bash
aws cloudfront create-invalidation \
  --distribution-id E1234567890 \
  --paths "/*"
```

**Cost:** First 1000 paths free/month, then $0.005/path

---

## CloudFront + HTTPS

| Scenario | Certificate Source |
|----------|-------------------|
| cloudfront.net domain | AWS default cert (free) |
| Custom domain | ACM certificate (free, must be in us-east-1) |

---

## Interview Questions

**Q: How do you serve S3 content globally with low latency?**
> "Use CloudFront in front of S3. CloudFront caches at edge locations worldwide. Users get content from nearest edge, not from S3 every time. For security, I use Origin Access Control to keep S3 private."

**Q: Static vs Dynamic content with CloudFront?**
> "Static content (images, CSS, JS) is cached with long TTL. Dynamic content (API responses) either isn't cached or uses short TTL with cache headers. CloudFront can accelerate both."

**Q: What if I update a file but users see old version?**
> "CloudFront caches content based on TTL. To immediately refresh, I create a cache invalidation. For versioned deployments, I use unique filenames (hash in URL) so new content has new cache key."

**Q: How do you secure S3 with CloudFront?**
> "I enable Block Public Access on S3, use Origin Access Control (OAC) to allow only CloudFront, and serve all traffic over HTTPS via CloudFront."

---

# Part 10: Hands-On Practice

## Exercise 1: Create S3 Bucket
```bash
aws s3 mb s3://practice-bucket-<your-name>-2026
```

## Exercise 2: Upload Files
```bash
echo "<h1>Hello from S3</h1>" > index.html
aws s3 cp index.html s3://practice-bucket-xxx/
```

## Exercise 3: Enable Static Website
```bash
aws s3 website s3://practice-bucket-xxx --index-document index.html
```

## Exercise 4: Make Public (for testing)
```bash
aws s3api put-bucket-policy --bucket practice-bucket-xxx \
  --policy '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Principal":"*",
      "Action":"s3:GetObject",
      "Resource":"arn:aws:s3:::practice-bucket-xxx/*"
    }]
  }'
```

## Exercise 5: Create CloudFront Distribution
```bash
aws cloudfront create-distribution \
  --origin-domain-name practice-bucket-xxx.s3.amazonaws.com \
  --default-root-object index.html
```

## Exercise 6: Test Access
- Via S3 website endpoint
- Via CloudFront domain

## Exercise 7: Clean Up
```bash
aws s3 rm s3://practice-bucket-xxx --recursive
aws s3 rb s3://practice-bucket-xxx
aws cloudfront delete-distribution --id EXXX --if-match ETAG
```

---

# Summary: Interview Cheat Sheet

| Topic | Key Points |
|-------|------------|
| **S3 Durability** | 11 9's (99.999999999%) |
| **Storage Classes** | Standard → IA → Glacier (lifecycle rules) |
| **Security** | Block Public Access + Bucket Policies + Encryption |
| **Versioning** | Protects against deletes, keeps all versions |
| **CloudFront** | CDN, 400+ edges, caches content globally |
| **OAC** | Origin Access Control - keep S3 private, CF only |
| **Invalidation** | Force cache refresh when content updated |

---

*Practice creating buckets, uploading files, and setting up CloudFront!*

---

# ✅ Hands-On Practice Completed (Jan 24, 2026)

## Session Summary
**Duration:** ~30 min | **Region:** ap-south-1

---

## Exercises Completed

### 1. Created S3 Bucket
```bash
aws s3 mb s3://practice-lucky-2026
```

### 2. Uploaded Static Website
```bash
echo "<html><body><h1>Hello from S3!</h1></body></html>" > index.html
aws s3 cp index.html s3://practice-lucky-2026/
```

### 3. Enabled Static Website Hosting
```bash
aws s3 website s3://practice-lucky-2026 --index-document index.html
```

### 4. Configured Bucket Policy
```bash
# Disabled Block Public Access
aws s3api put-public-access-block --bucket practice-lucky-2026 \
  --public-access-block-configuration "BlockPublicAcls=false,..."

# Added public read policy via file://policy.json
aws s3api put-bucket-policy --bucket practice-lucky-2026 --policy file://policy.json
```

### 5. Tested S3 Website
```
URL: http://practice-lucky-2026.s3-website.ap-south-1.amazonaws.com
Result: ✅ Working!
```

### 6. Created CloudFront Distribution
```bash
# Created config file cf-config.json
aws cloudfront create-distribution --distribution-config file://cf-config.json

# Distribution: d27kw0rkquyi5u.cloudfront.net
```

### 7. Tested CloudFront CDN
```
URL: https://d27kw0rkquyi5u.cloudfront.net
Result: ✅ Working with HTTPS!
```

### 8. Clean Up
```bash
# Disabled and deleted CloudFront
aws cloudfront delete-distribution --id E2VQFHPBSKTPVU --if-match $ETAG

# Deleted S3 bucket
aws s3 rm s3://practice-lucky-2026 --recursive
aws s3 rb s3://practice-lucky-2026

# Verified cleanup
aws cloudfront list-distributions  # null
aws s3 ls                          # empty
```

---

## Key Learnings

| Skill | Interview Answer |
|-------|------------------|
| **S3 Website** | "Enable static hosting, set index.html, configure bucket policy" |
| **CloudFront** | "CDN in front of S3, caches at 400+ edge locations, provides HTTPS" |
| **Bucket Policy** | "JSON policy to allow public read or restrict to CloudFront only" |
| **Cleanup** | "Delete objects first, then bucket. Disable CloudFront before delete" |

---

## Interview-Ready Topics ✅

- [x] Create S3 bucket
- [x] Upload files to S3
- [x] Configure static website hosting
- [x] Set bucket policies
- [x] Create CloudFront distribution
- [x] Test CDN access with HTTPS
- [x] Clean up resources
