# Python Modules & Libraries for SRE/DevOps
A comprehensive guide to the essential tools in the Python ecosystem for automation, monitoring, and systems engineering.

---

## 📦 1. Built-in Modules (Standard Library)

### `os` – Operating System Interface
**Purpose:** Interact with the underlying OS (files, directories, env variables).
- `os.listdir(path)`: List files in a directory.
- `os.environ.get('VAR')`: Get environment variables.
- `os.path.exists(path)`: Check if a file/folder exists.
- `os.makedirs(path)`: Create nested directories.

```python
import os
print(f"Current Directory: {os.getcwd()}")
if os.path.exists("/var/log"):
    logs = os.listdir("/var/log")
```

---

### `sys` – System-specific Parameters
**Purpose:** Access arguments, exit codes, and interpreter settings.
- `sys.argv`: List of command-line arguments.
- `sys.exit(code)`: Exit the script with a specific status.
- `sys.path`: List of directories the interpreter searches for modules.

```python
import sys
if len(sys.argv) < 2:
    print("Usage: script.py <filename>")
    sys.exit(1)
```

---

### `subprocess` – Command Execution
**Purpose:** Run shell commands and capture their output (**Critical for SRE**).
- `subprocess.run()`: Execute a command and wait for it to finish.
- `subprocess.check_output()`: Run a command and return its output as a string.

```python
import subprocess
result = subprocess.run(["df", "-h"], capture_output=True, text=True)
print(result.stdout)
```

---

### `shutil` – High-level File Operations
**Purpose:** Move, copy, and remove files/directories (disk utilities).
- `shutil.copy(src, dst)`: Copy a file.
- `shutil.move(src, dst)`: Move or rename.
- `shutil.disk_usage("/")`: Get disk statistics.

```python
import shutil
usage = shutil.disk_usage("/")
print(f"Free space: {usage.free // (2**30)} GB")
```

---

### `json` & `csv` – Data Serialization
**Purpose:** Parse and generate common data formats for APIs and reports.

```python
import json
data = {"status": "UP", "nodes": 5}
json_string = json.dumps(data)  # To string
parsed = json.loads(json_string) # From string
```

---

### `datetime` – Time & Date Manipulation
**Purpose:** Log timestamps, calculate intervals, and schedule tasks.
- `datetime.now()`: Current time.
- `timedelta`: For date arithmetic (e.g., "7 days ago").

```python
from datetime import datetime, timedelta
now = datetime.now()
expiry = now + timedelta(days=90) # SSL cert expiry trace
```

---

### `re` – Regular Expressions
**Purpose:** Pattern matching in logs and text processing.

```python
import re
log = "ERROR 2024-01-10: Connection timeout"
if re.search(r"ERROR", log):
    print("Error found!")
```

---

### `collections` – Specialized Containers
**Purpose:** Advanced data structures beyond basic list/dict.
- `Counter`: Count occurrences of items.
- `defaultdict`: Dictionary that provides a default value for missing keys.

```python
from collections import Counter
errors = ["404", "500", "404", "503"]
counts = Counter(errors) # {'404': 2, '500': 1, '503': 1}
```

---

## 🌐 2. External Libraries (via `pip`)

### `requests` – HTTP Library
**Purpose:** Interact with REST APIs, webhooks, and health checks.

```python
import requests
response = requests.get("https://api.github.com/status")
if response.status_code == 200:
    print(response.json())
```

---

### `psutil` – Process and System Utils
**Purpose:** Retrieve info on running processes and system utilization (CPU, memory, disks).

```python
import psutil
print(f"CPU Usage: {psutil.cpu_percent()}%")
print(f"Memory Usage: {psutil.virtual_memory().percent}%")
```

---

### `paramiko` – SSH Protocol Logic
**Purpose:** Automate SSH commands on remote servers.

```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.0.1', username='ubuntu')
stdin, stdout, stderr = ssh.exec_command('ls')
```

---

### `prometheus_client` – Custom Metrics
**Purpose:** Expose Python app metrics to Prometheus.

```python
from prometheus_client import start_http_server, Counter
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')

def process_request():
    REQUEST_COUNT.inc()

start_http_server(8000)
```

---

### `PyYAML` – YAML Parsing
**Purpose:** Handle Kubernetes manifests, Ansible playbooks, and configs.

```python
import yaml
with open('k8s_deploy.yaml') as f:
    config = yaml.safe_load(f)
```

---

## 🛡️ 3. SRE Best Practices for Modules
1. **Try-Except:** Always wrap `subprocess` and `requests` calls in `try...except` blocks.
2. **Context Managers:** Use `with open(...)` or `with requests.Session()` for resource safety.
3. **Environment Variables:** Never hardcode secrets; use `os.environ` or `python-dotenv`.
4. **Logging:** Use the `logging` module instead of `print()` for production scripts.

---
*Created for: DEVOPS/SRE 60-Day Journey (Day 4)*
