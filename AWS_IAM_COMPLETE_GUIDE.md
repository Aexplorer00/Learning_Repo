# AWS IAM Complete Guide for SRE
## Day 7: Concepts + Security + Interview Questions

---

## 🎯 What is IAM?

**IAM = Identity and Access Management**

```
WHO can do WHAT on WHICH resources
 ↓       ↓         ↓
User   Action   Resource
```

**Key Point:** IAM is **global** (not region-specific)

---

## 📋 IAM Components

### 1. Users
**Individual people or services**

```
User = Username + Credentials (password/access keys)

Best Practice:
- One user per person
- Never share credentials
- Use MFA!
```

### 2. Groups
**Collection of users**

```
Developers Group → Dev User 1, Dev User 2
Admin Group      → Admin User 1
                   ↑
           Assign policies to GROUP, not individual users!
```

### 3. Roles
**Temporary permissions for services/users**

```
EC2 Instance → Assume Role → Gets permissions
Lambda       → Assume Role → Access S3
External User → Assume Role → Cross-account access
```

**Key:** No permanent credentials! Temporary tokens.

### 4. Policies
**JSON documents defining permissions**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

---

## 📝 Policy Types

| Type | Attached To | Use Case |
|------|-------------|----------|
| **Identity-based** | User/Group/Role | Common permissions |
| **Resource-based** | S3/SQS/Lambda | Cross-account access |
| **Permission Boundary** | User/Role | Maximum permissions limit |
| **SCP** | Organization | Account-level restrictions |

---

## 🔒 IAM Best Practices

1. **Root Account**
   - Enable MFA immediately
   - Never use for daily tasks
   - Create admin user instead

2. **Users**
   - One user per person
   - Strong passwords + MFA
   - Rotate access keys regularly

3. **Permissions**
   - **Least Privilege** - Only what's needed
   - Use Groups, not individual policies
   - Use Roles for services (not access keys!)

4. **Monitoring**
   - Enable CloudTrail
   - Review IAM Credential Report
   - Use IAM Access Analyzer

---

## 🎯 Common Scenarios

### Scenario 1: EC2 Needs S3 Access
```
❌ BAD: Store access keys in EC2
✅ GOOD: Create IAM Role, attach to EC2

EC2 → IAM Role (S3 access) → S3
```

### Scenario 2: Cross-Account Access
```
Account A (User) → Assume Role → Account B (Resources)

Steps:
1. Account B creates role with trust policy
2. Account A user assumes the role
3. Gets temporary credentials
```

### Scenario 3: Lambda Needs DynamoDB Access
```
Lambda → Execution Role → DynamoDB

Lambda automatically assumes its execution role
```

---

## 📊 Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3Read",           // Statement ID (optional)
      "Effect": "Allow",               // Allow or Deny
      "Action": [                      // What actions
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [                    // Which resources
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {                   // When (optional)
        "IpAddress": {
          "aws:SourceIp": "10.0.0.0/8"
        }
      }
    }
  ]
}
```

---

## 🔥 Important Concepts

### 1. Explicit Deny > Allow
```
If ANY policy says Deny → Access DENIED
Even if another policy says Allow!
```

### 2. Default Deny
```
No policy = No access
Must explicitly allow
```

### 3. Trust Policy (for Roles)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
**Who can assume this role?** → EC2 service

---

## 🎤 Interview Questions & Answers

### Q1: How do you give EC2 access to S3?
> Create an IAM Role with S3 permissions.
> Attach the role to the EC2 instance.
> Never store access keys on EC2!

### Q2: What's the difference between User and Role?
> **User:** Permanent identity with credentials
> **Role:** Temporary identity, assumed by services/users

### Q3: How does least privilege work?
> Give only the minimum permissions needed.
> Start with no access, add only what's required.
> Review and reduce permissions regularly.

### Q4: What happens if Allow and Deny conflict?
> Deny ALWAYS wins.
> Explicit Deny > Explicit Allow > Default Deny

### Q5: How do you audit IAM?
> 1. IAM Credential Report (all users, keys, MFA status)
> 2. CloudTrail (API call logs)
> 3. IAM Access Analyzer (external access detection)

### Q6: What's a Permission Boundary?
> Maximum permissions a user/role CAN have.
> Even if policy allows more, boundary limits it.
> Used for delegated administration.

### Q7: Cross-account access - how?
> 1. Account B creates role with trust policy
> 2. Trust policy allows Account A
> 3. User in A assumes role in B
> 4. Gets temporary credentials

---

## 🔥 Quick Commands (CLI)

```bash
# List users
aws iam list-users

# List roles
aws iam list-roles

# Get user policy
aws iam list-user-policies --user-name myuser

# Create user
aws iam create-user --user-name newuser

# Attach policy to user
aws iam attach-user-policy --user-name myuser \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create role
aws iam create-role --role-name myrole \
    --assume-role-policy-document file://trust-policy.json

# Assume role (get temp credentials)
aws sts assume-role --role-arn arn:aws:iam::123456:role/myrole \
    --role-session-name mysession
```

---

*Created for: DEVOPS/SRE 60-Day Journey (Day 7)*
