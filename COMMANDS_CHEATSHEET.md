# 🚀 DevOps/SRE Commands Cheat Sheet
## Interview Quick Reference

---

# ☸️ Kubernetes Commands

## Cluster Info
```bash
kubectl cluster-info                    # Cluster details
kubectl get nodes                       # List nodes
kubectl get nodes -o wide               # Nodes with IPs
kubectl top nodes                       # Node resource usage
```

## Pods
```bash
kubectl get pods                        # List pods (default ns)
kubectl get pods -n <namespace>         # Specific namespace
kubectl get pods -A                     # All namespaces
kubectl get pods -o wide                # With node info
kubectl describe pod <pod>              # Pod details + events
kubectl logs <pod>                      # Pod logs
kubectl logs <pod> --previous           # Previous container logs
kubectl logs <pod> -f                   # Follow logs
kubectl exec -it <pod> -- bash          # Shell into pod
kubectl delete pod <pod>                # Delete pod
```

## Deployments
```bash
kubectl get deployments                 # List deployments
kubectl describe deployment <name>      # Deployment details
kubectl scale deployment <name> --replicas=5
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>  # Rollback
kubectl set image deployment/<name> container=image:tag
```

## Services
```bash
kubectl get svc                         # List services
kubectl describe svc <name>             # Service details
kubectl expose deployment <name> --port=80 --type=NodePort
kubectl port-forward svc/<name> 8080:80 # Local access
```

## Debugging
```bash
kubectl get events                      # Cluster events
kubectl get events --sort-by='.lastTimestamp'
kubectl describe <resource> <name>      # Always start here!
kubectl get all -n <namespace>          # All resources
kubectl api-resources                   # Available resources
```

## Config & Context
```bash
kubectl config get-contexts             # List contexts
kubectl config use-context <name>       # Switch context
kubectl config current-context          # Current context
```

---

# 🐳 Docker Commands

## Images
```bash
docker images                           # List images
docker pull <image>:<tag>               # Pull image
docker build -t <name>:<tag> .          # Build image
docker push <image>:<tag>               # Push to registry
docker rmi <image>                      # Remove image
docker image prune                      # Remove unused images
```

## Containers
```bash
docker ps                               # Running containers
docker ps -a                            # All containers
docker run -d -p 8080:80 <image>        # Run detached
docker run -it <image> bash             # Interactive shell
docker exec -it <container> bash        # Shell into running
docker stop <container>                 # Stop container
docker rm <container>                   # Remove container
docker logs <container>                 # View logs
docker logs -f <container>              # Follow logs
```

## Cleanup
```bash
docker system prune                     # Clean everything
docker container prune                  # Remove stopped
docker volume prune                     # Remove unused volumes
docker network prune                    # Remove unused networks
```

## Docker Compose
```bash
docker-compose up -d                    # Start services
docker-compose down                     # Stop and remove
docker-compose logs -f                  # Follow logs
docker-compose ps                       # List services
docker-compose build                    # Build images
```

---

# ☁️ AWS CLI Commands

## EC2
```bash
aws ec2 describe-instances              # List instances
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 describe-security-groups
aws ec2 describe-vpcs
aws ec2 describe-subnets
```

## S3
```bash
aws s3 ls                               # List buckets
aws s3 ls s3://bucket-name              # List objects
aws s3 cp file.txt s3://bucket/         # Upload
aws s3 cp s3://bucket/file.txt .        # Download
aws s3 sync ./folder s3://bucket/       # Sync folder
aws s3 rm s3://bucket/file.txt          # Delete
aws s3 rb s3://bucket --force           # Delete bucket
```

## IAM
```bash
aws iam list-users                      # List users
aws iam list-roles                      # List roles
aws iam get-user                        # Current user
aws sts get-caller-identity             # Who am I?
```

## EKS
```bash
aws eks list-clusters                   # List clusters
aws eks describe-cluster --name <name>
aws eks update-kubeconfig --name <name> # Get kubeconfig
```

## CloudWatch
```bash
aws logs describe-log-groups
aws logs tail /aws/lambda/my-function --follow
aws cloudwatch list-metrics
```

---

# 🔧 Terraform Commands

## Core Workflow
```bash
terraform init                          # Initialize
terraform plan                          # Dry run
terraform apply                         # Create resources
terraform destroy                       # Delete all
terraform validate                      # Check syntax
terraform fmt                           # Format code
```

## State Management
```bash
terraform state list                    # List resources
terraform state show <resource>         # Show resource
terraform state rm <resource>           # Remove from state
terraform import <resource> <id>        # Import existing
terraform refresh                       # Sync state
```

## Workspaces
```bash
terraform workspace list                # List workspaces
terraform workspace new <name>          # Create workspace
terraform workspace select <name>       # Switch workspace
```

## Debugging
```bash
terraform plan -out=tfplan              # Save plan
terraform apply tfplan                  # Apply saved plan
terraform apply -replace=<resource>     # Force recreate
TF_LOG=DEBUG terraform plan             # Debug logging
```

---

# 🐧 Linux Commands

## File Operations
```bash
ls -la                                  # List with details
cat file.txt                            # View file
tail -f /var/log/syslog                 # Follow log
grep "error" file.log                   # Search in file
grep -r "pattern" /path                 # Recursive search
find /path -name "*.log"                # Find files
```

## Process Management
```bash
ps aux                                  # All processes
ps aux | grep nginx                     # Find process
top                                     # Live resource usage
htop                                    # Better top
kill <PID>                              # Graceful kill
kill -9 <PID>                           # Force kill
```

## System Info
```bash
df -h                                   # Disk space
du -sh /path                            # Directory size
free -m                                 # Memory usage
uptime                                  # System uptime
hostnamectl                             # OS info
```

## Network
```bash
netstat -tulpn                          # Open ports
ss -tulpn                               # Modern netstat
curl -I https://example.com             # HTTP headers
ping google.com                         # Test connectivity
dig example.com                         # DNS lookup
traceroute google.com                   # Trace route
```

## Permissions
```bash
chmod 755 file                          # rwxr-xr-x
chmod +x script.sh                      # Make executable
chown user:group file                   # Change owner
```

---

# 🔐 Common Ports

| Service | Port |
|---------|------|
| SSH | 22 |
| HTTP | 80 |
| HTTPS | 443 |
| MySQL | 3306 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| MongoDB | 27017 |
| K8s API | 6443 |
| Kubelet | 10250 |
| etcd | 2379 |

---

# 📝 Git Commands

```bash
git status                              # Check status
git add .                               # Stage all
git commit -m "message"                 # Commit
git push origin main                    # Push
git pull origin main                    # Pull
git log --oneline -10                   # Recent commits
git diff                                # Show changes
git checkout -b feature                 # New branch
git merge feature                       # Merge branch
git stash                               # Stash changes
git stash pop                           # Restore stash
```

---

# ⚡ Quick Reference

## K8s Troubleshooting Flow
```
kubectl describe pod → kubectl logs → kubectl exec
```

## Docker Build Best Practice
```
FROM slim → COPY requirements → RUN install → COPY code
```

## Terraform Workflow
```
init → plan → apply (never skip plan!)
```

---

*Good luck with your interview! 💪*
