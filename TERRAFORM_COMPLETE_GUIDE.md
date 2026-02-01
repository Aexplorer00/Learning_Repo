# Terraform Complete Guide for SRE
## Infrastructure as Code (IaC)

---

## 🎯 What is Terraform?

**Terraform = Infrastructure as Code**

```
Write Code → terraform apply → AWS/GCP/Azure creates resources
```

**Key Points:**
- Declarative (describe WHAT, not HOW)
- Multi-cloud (AWS, GCP, Azure, etc.)
- State management
- Written in HCL (HashiCorp Configuration Language)

---

## 📦 Core Concepts

### 1. Providers
**Connect to cloud platforms**

```hcl
provider "aws" {
  region = "ap-south-1"
}
```

### 2. Resources
**What you want to create**

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
  }
}
```

### 3. Variables
**Make code reusable**

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

resource "aws_instance" "web" {
  instance_type = var.instance_type
}
```

### 4. Outputs
**Show results after apply**

```hcl
output "public_ip" {
  value = aws_instance.web.public_ip
}
```

### 5. State
**Terraform tracks what exists**

```
terraform.tfstate → Tracks all resources
                    NEVER edit manually!
                    Store in S3 for teams
```

---

## 🔧 Essential Commands

```bash
terraform init      # Download providers, initialize
terraform plan      # Preview changes (dry run)
terraform apply     # Create/update resources
terraform destroy   # Delete all resources
terraform fmt       # Format code
terraform validate  # Check syntax
terraform state     # Manage state file
```

---

## 📝 Basic Project Structure

```
my-project/
├── main.tf           # Main resources
├── variables.tf      # Variable definitions
├── outputs.tf        # Output values
├── terraform.tfvars  # Variable values (don't commit secrets!)
└── providers.tf      # Provider configuration
```

---

## 🏗️ Complete Example: EC2 + VPC

```hcl
# providers.tf
provider "aws" {
  region = "ap-south-1"
}

# variables.tf
variable "environment" {
  default = "dev"
}

# main.tf
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "${var.environment}-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "${var.environment}-public"
  }
}

resource "aws_instance" "web" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  
  tags = {
    Name = "${var.environment}-webserver"
  }
}

# outputs.tf
output "instance_id" {
  value = aws_instance.web.id
}
```

---

## 📦 Modules

**Reusable components**

```hcl
# Using a module
module "vpc" {
  source = "./modules/vpc"
  
  environment = "prod"
  cidr_block  = "10.0.0.0/16"
}

module "ec2" {
  source = "./modules/ec2"
  
  subnet_id = module.vpc.subnet_id
}
```

**Module structure:**
```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── ec2/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## 🔒 State Management

### Local State (Default)
```
terraform.tfstate → Stored locally
Problem: Team can't collaborate
```

### Remote State (Best Practice)
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-south-1"
    
    # Locking with DynamoDB
    dynamodb_table = "terraform-locks"
  }
}
```

---

## 🎤 Interview Questions

### Q1: What is Terraform state?
> State file tracks all resources Terraform manages.
> Maps config to real infrastructure.
> Must be stored securely (S3 + DynamoDB lock).

### Q2: What's the difference between `terraform plan` and `apply`?
> `plan`: Preview changes without making them (dry run)
> `apply`: Actually creates/modifies resources

### Q3: How do you manage secrets in Terraform?
> 1. Use environment variables
> 2. Use AWS Secrets Manager/SSM
> 3. Use terraform.tfvars (gitignore it!)
> 4. Use Vault for sensitive data

### Q4: What are modules?
> Reusable, self-contained Terraform code packages.
> Like functions in programming.
> Promote DRY (Don't Repeat Yourself).

### Q5: How do you handle state conflicts in teams?
> 1. Use remote backend (S3)
> 2. Enable state locking (DynamoDB)
> 3. Run terraform apply in CI/CD only

### Q6: What is `terraform import`?
> Imports existing infrastructure into Terraform state.
> For resources created manually or by other tools.

---

## 🔥 Best Practices

1. **Always use remote state** (S3 + DynamoDB)
2. **Use modules** for reusability
3. **Use workspaces** for environments (dev/staging/prod)
4. **Never hardcode secrets**
5. **Use `terraform fmt`** for consistent formatting
6. **Run `terraform plan`** before every apply
7. **Version control** your Terraform code
8. **Use CI/CD** for terraform apply

---

*Created for: DEVOPS/SRE 60-Day Journey (Day 7 Extra)*
