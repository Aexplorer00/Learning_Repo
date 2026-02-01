# GitHub Actions Complete Guide for SRE
## Day 7: CI/CD Basics + Workflow Syntax

---

## 🎯 What is GitHub Actions?

**GitHub Actions = CI/CD built into GitHub**

```
Push Code → GitHub Actions → Build → Test → Deploy
```

**Key Point:** Runs in GitHub's cloud, triggered by events (push, PR, schedule)

---

## 📦 Core Concepts

### 1. Workflow
**A YAML file defining automation**

Location: `.github/workflows/my-workflow.yml`

### 2. Event
**What triggers the workflow**

```yaml
on:
  push:                    # On any push
  pull_request:            # On PR
  schedule:                # Cron schedule
    - cron: '0 9 * * *'
  workflow_dispatch:       # Manual trigger
```

### 3. Job
**A set of steps that run on same runner**

```yaml
jobs:
  build:                   # Job name
    runs-on: ubuntu-latest # Runner OS
    steps:
      - ...
```

### 4. Step
**Individual task in a job**

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4     # Pre-built action
    
  - name: Run tests
    run: npm test                  # Shell command
```

### 5. Runner
**Machine that runs the job**

| Runner | Use Case |
|--------|----------|
| `ubuntu-latest` | Most common |
| `windows-latest` | Windows builds |
| `macos-latest` | iOS/Mac builds |
| Self-hosted | Custom environment |

---

## 📝 Basic Workflow Structure

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

---

## 🔧 Common Patterns

### Pattern 1: Python CI

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

### Pattern 2: Docker Build & Push

```yaml
name: Docker CI

on:
  push:
    branches: [main]

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myuser/myapp:latest
```

### Pattern 3: Deploy to AWS

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to S3
        run: aws s3 sync ./dist s3://my-bucket
```

---

## 🔐 Secrets & Variables

### Secrets (Sensitive data)
```yaml
# Access via: ${{ secrets.SECRET_NAME }}

env:
  API_KEY: ${{ secrets.API_KEY }}
```

**Set in:** Repo Settings → Secrets and variables → Actions

### Variables (Non-sensitive)
```yaml
# Access via: ${{ vars.VARIABLE_NAME }}

env:
  ENVIRONMENT: ${{ vars.ENVIRONMENT }}
```

---

## 📊 Workflow Control

### Conditionals
```yaml
steps:
  - name: Deploy to prod
    if: github.ref == 'refs/heads/main'
    run: ./deploy.sh prod
    
  - name: Deploy to staging
    if: github.ref == 'refs/heads/develop'
    run: ./deploy.sh staging
```

### Matrix (Multiple versions)
```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### Job Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: ...
  
  test:
    needs: build          # Wait for build
    runs-on: ubuntu-latest
    steps: ...
  
  deploy:
    needs: [build, test]  # Wait for both
    runs-on: ubuntu-latest
    steps: ...
```

---

## 🎤 Interview Questions

### Q1: What triggers a GitHub Actions workflow?
> Events: push, pull_request, schedule, workflow_dispatch, release, etc.

### Q2: How do you store sensitive data?
> GitHub Secrets (Settings → Secrets)
> Access via ${{ secrets.NAME }}

### Q3: How do you run jobs in parallel vs sequence?
> **Parallel:** Default (no `needs`)
> **Sequence:** Use `needs: previous-job`

### Q4: What's the difference between `uses` and `run`?
> `uses`: Pre-built action (actions/checkout)
> `run`: Shell command (npm install)

### Q5: How to run on multiple Node versions?
> Use matrix strategy with node-version array

---

## 🔥 Quick Commands

```yaml
# Checkout code
- uses: actions/checkout@v4

# Setup Node
- uses: actions/setup-node@v4
  with:
    node-version: '18'

# Setup Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'

# Cache dependencies
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

# Upload artifact
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: ./dist
```

---

*Created for: DEVOPS/SRE 60-Day Journey (Day 7)*
