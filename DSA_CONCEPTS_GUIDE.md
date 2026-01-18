# 🧠 DSA Concepts Guide - Deep Understanding

> **Goal:** Understand the WHY behind each pattern before memorizing code.

---

# 1️⃣ HASH MAPS (Dictionaries)

## What Is It?
A hash map stores **key-value pairs** with near-instant lookup.

```
┌─────────────────────────────────────────┐
│  Key  │  Hash Function  │  Value        │
├───────┼─────────────────┼───────────────┤
│ "cat" │  → hash → 3    │  stores here  │
│ "dog" │  → hash → 7    │  stores here  │
│ "rat" │  → hash → 3    │  collision!   │
└───────┴─────────────────┴───────────────┘
```

## Why Is It Fast?
Instead of searching through all items (O(n)), the hash function **calculates exactly where** to look (O(1)).

Think of it like a library:
- ❌ **Without hash:** Check every book until you find it
- ✅ **With hash:** Go directly to shelf 7, row 3

## When to Use Hash Maps?

| Situation | Why Hash Map? |
|-----------|---------------|
| "Have I seen this before?" | O(1) lookup |
| Count occurrences | `Counter(list)` |
| Group items by property | `defaultdict(list)` |
| Two Sum / find pairs | Store complement |

## Python Syntax
```python
# Basic dictionary
seen = {}
seen["key"] = "value"       # Insert O(1)
if "key" in seen:           # Lookup O(1)
    print(seen["key"])      # Access O(1)

# Counter - counts frequency automatically
from collections import Counter
counts = Counter([1, 1, 2, 3, 3, 3])
# Result: {3: 3, 1: 2, 2: 1}

# defaultdict - auto-creates missing keys
from collections import defaultdict
graph = defaultdict(list)
graph["A"].append("B")  # No KeyError!
```

## Classic Problem: Two Sum
```
Given: [2, 7, 11, 15], target = 9
Find: Two indices whose values sum to target
Answer: [0, 1] because 2 + 7 = 9
```

**Brute Force O(n²):**
```python
for i in range(n):
    for j in range(i+1, n):
        if nums[i] + nums[j] == target:
            return [i, j]
```

**Hash Map O(n):**
```python
seen = {}
for i, num in enumerate(nums):
    complement = target - num  # What do I need?
    if complement in seen:     # Did I see it before?
        return [seen[complement], i]
    seen[num] = i              # Remember this number
```

**Why it works:** Instead of checking every pair, we store what we've seen and ask "do I have what I need?"

---

# 2️⃣ BFS (Breadth-First Search)

## What Is It?
BFS explores a graph **level by level**, like ripples spreading in water.

```
        1           Level 0
       / \
      2   3         Level 1
     / \   \
    4   5   6       Level 2

BFS visits: 1 → 2 → 3 → 4 → 5 → 6
```

## Core Mechanism: QUEUE (FIFO)
```
Queue: [start]
While queue not empty:
    1. Pop from FRONT (oldest first)
    2. Process this node
    3. Add its neighbors to BACK
```

**Visual Step-by-Step:**
```
Start at node 1:
Queue: [1]

Pop 1, add its neighbors (2, 3):
Queue: [2, 3]

Pop 2, add its neighbors (4, 5):
Queue: [3, 4, 5]

Pop 3, add its neighbor (6):
Queue: [4, 5, 6]

... and so on
```

## Why BFS Finds Shortest Path?
Because it explores **ALL nodes at distance 1** before ANY node at distance 2.

```
Finding path A → F:

BFS: A(0) → B(1) → C(1) → D(2) → E(2) → F(2) ✓
     First time we reach F, we know it's the shortest!

DFS might find: A → B → D → E → F (longer path first)
```

## When to Use BFS?

| Problem | Why BFS? |
|---------|----------|
| Shortest path (unweighted) | Level = distance |
| Level-order traversal | Natural level grouping |
| Find nearest X | First occurrence = nearest |
| Minimum steps/moves | Each level = one step |

## Python Template
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])  # Track visited to avoid cycles
    queue = deque([start])  # FIFO queue
    
    while queue:
        node = queue.popleft()  # Pop from FRONT
        print(f"Visit: {node}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Add to BACK
```

## SRE Connection
- **Service dependency shortest path:** How many hops to reach service X?
- **Network topology:** Broadcasting to all nodes level by level
- **Finding closest healthy instance:** Stop at first healthy node

---

# 3️⃣ DFS (Depth-First Search)

## What Is It?
DFS explores **as deep as possible** before backtracking.

```
        1
       / \
      2   3
     / \
    4   5

DFS visits: 1 → 2 → 4 → (backtrack) → 5 → (backtrack) → 3
```

## Core Mechanism: STACK (LIFO) or Recursion
```
Stack: [start]
While stack not empty:
    1. Pop from TOP (newest first)
    2. Process this node
    3. Push its neighbors to TOP
```

**Recursion is "hidden" stack:**
```python
def dfs(node):
    # Process node
    for neighbor in graph[node]:
        dfs(neighbor)  # This creates a call stack!
```

## Visual: DFS vs BFS Path
```
Graph:
    A---B---D
    |   |
    C---E---F

BFS from A: A → B → C → D → E → F (level order)
DFS from A: A → B → D → E → F → C (deep first)
```

## When to Use DFS?

| Problem | Why DFS? |
|---------|----------|
| Find ALL paths | Explores every possibility |
| Detect cycles | Can track "currently visiting" |
| Connected components | Mark entire region |
| Topological sort | Process dependencies |
| Backtracking problems | Try and undo |

## Python Templates
```python
# Recursive DFS (cleaner, but stack limit)
def dfs_recursive(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Iterative DFS (no stack limit)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()  # Pop from TOP (LIFO)
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                stack.append(neighbor)
```

## Matrix DFS (Number of Islands)
```python
def dfs_matrix(grid, row, col):
    # Out of bounds or water? Stop.
    if (row < 0 or row >= len(grid) or 
        col < 0 or col >= len(grid[0]) or
        grid[row][col] == '0'):
        return
    
    grid[row][col] = '0'  # Mark visited (sink the land)
    
    # Explore 4 directions
    dfs_matrix(grid, row+1, col)  # Down
    dfs_matrix(grid, row-1, col)  # Up
    dfs_matrix(grid, row, col+1)  # Right
    dfs_matrix(grid, row, col-1)  # Left
```

## SRE Connection
- **Detect circular dependencies:** A → B → C → A (cycle!)
- **Find all affected services:** If service A fails, what breaks?
- **Configuration validation:** Traverse all nested configs

---

# 4️⃣ BFS vs DFS Quick Reference

```
┌─────────────────┬────────────────────┬────────────────────┐
│                 │       BFS          │        DFS         │
├─────────────────┼────────────────────┼────────────────────┤
│ Data Structure  │ Queue (deque)      │ Stack (or recurse) │
│ Order           │ FIFO (oldest)      │ LIFO (newest)      │
│ Explores        │ Level by level     │ Deep then backtrack│
│ Shortest path?  │ ✅ YES             │ ❌ NO              │
│ Memory          │ O(width)           │ O(depth)           │
│ When to use     │ Shortest path      │ All paths, cycles  │
└─────────────────┴────────────────────┴────────────────────┘
```

---

# 5️⃣ HEAPS (Priority Queue)

## What Is It?
A heap is a tree where the **smallest (or largest) element is always at the top**.

```
Min-Heap:           Max-Heap:
    1                   9
   / \                 / \
  3   2               7   8
 / \                 / \
7   8               3   4
```

## Why Use a Heap?
When you need to **repeatedly get the minimum/maximum** efficiently.

| Operation | Array | Sorted Array | Heap |
|-----------|-------|--------------|------|
| Insert | O(1) | O(n) | O(log n) |
| Get min/max | O(n) | O(1) | O(1) |
| Remove min/max | O(n) | O(1) | O(log n) |

## When to Use Heaps?

| Problem Pattern | Why Heap? |
|-----------------|-----------|
| "Top K largest/smallest" | Keep heap of size K |
| "Kth largest element" | Min-heap of size K |
| "Merge K sorted lists" | Track smallest from each |
| "Streaming median" | Two heaps technique |

## Python Syntax
```python
import heapq

# Python heapq is a MIN-HEAP by default
nums = [5, 2, 8, 1, 9]
heapq.heapify(nums)        # Convert to heap: [1, 2, 8, 5, 9]

heapq.heappush(nums, 3)    # Insert: O(log n)
smallest = heapq.heappop(nums)  # Remove smallest: O(log n)

# Top K largest (built-in!)
top_3 = heapq.nlargest(3, nums)

# Top K smallest
bottom_3 = heapq.nsmallest(3, nums)

# For MAX-HEAP: negate values
max_heap = []
heapq.heappush(max_heap, -5)  # Push -5 instead of 5
largest = -heapq.heappop(max_heap)  # Negate back
```

## Classic Problem: Top K Frequent Elements
```python
from collections import Counter
import heapq

def topKFrequent(nums, k):
    count = Counter(nums)  # {1: 3, 2: 2, 3: 1}
    # nlargest by frequency
    return heapq.nlargest(k, count.keys(), key=count.get)
```

## SRE Connection
- **Top 10 slowest requests:** Keep min-heap of size 10 by latency
- **Most frequent errors:** Heap by count
- **Resource scheduling:** Always pick lowest-load server

---

# 6️⃣ TWO POINTERS

## What Is It?
Use two indices that move toward each other (or same direction) to solve problems in O(n) instead of O(n²).

```
Array: [1, 3, 5, 7, 9, 11]
        ↑              ↑
       left          right
       
Move pointers based on some condition
```

## Common Patterns

### Pattern 1: Opposite Ends (for sorted arrays)
```
Find pair that sums to target:

[1, 3, 5, 7, 9], target = 10
 ↑           ↑
 L           R

1 + 9 = 10 ✓ Found!

If sum < target: move L right (need bigger)
If sum > target: move R left (need smaller)
```

### Pattern 2: Same Direction (fast/slow)
```
Remove duplicates, detect cycle, find middle:

[1, 1, 2, 2, 3]
 ↑  ↑
slow fast

Fast moves ahead, slow marks "good" position
```

## When to Use Two Pointers?

| Problem | Pattern |
|---------|---------|
| Two Sum (sorted array) | Opposite ends |
| Container with most water | Opposite ends |
| Remove duplicates | Same direction |
| Linked list cycle | Fast/slow |
| Merge sorted arrays | Two pointers, one per array |

## Python Example: Two Sum II (Sorted)
```python
def twoSum(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # Need bigger sum
        else:
            right -= 1  # Need smaller sum
    
    return []  # Not found
```

## Python Example: Container With Most Water
```python
def maxArea(heights):
    left, right = 0, len(heights) - 1
    max_water = 0
    
    while left < right:
        # Area = width × min(height)
        width = right - left
        height = min(heights[left], heights[right])
        max_water = max(max_water, width * height)
        
        # Move the shorter line (bottleneck)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

---

# 7️⃣ COMPLEXITY CHEAT SHEET

```
┌────────────────────┬──────────┬─────────────────────────────┐
│ Pattern            │ Time     │ Space                       │
├────────────────────┼──────────┼─────────────────────────────┤
│ Hash Map lookup    │ O(1)     │ O(n)                        │
│ Single loop        │ O(n)     │ O(1)                        │
│ Nested loops       │ O(n²)    │ O(1)                        │
│ Sorting            │ O(n log n)│ O(n) or O(log n)           │
│ Binary Search      │ O(log n) │ O(1)                        │
│ BFS / DFS          │ O(V + E) │ O(V)                        │
│ Heap insert/remove │ O(log n) │ O(n)                        │
│ Heap nlargest(k)   │ O(n log k)│ O(k)                       │
└────────────────────┴──────────┴─────────────────────────────┘
```

---

# 🎯 Pattern Recognition Cheat Sheet

```
"Find if exists" ────────────→ Hash Map
"Count occurrences" ─────────→ Counter / Hash Map
"Shortest path" ─────────────→ BFS
"All paths / cycles" ────────→ DFS
"Top K / Kth largest" ───────→ Heap
"Sorted array + pair" ───────→ Two Pointers
"Substring / window" ────────→ Sliding Window
"Search in sorted" ──────────→ Binary Search
```

---

Good luck with your prep! 🚀
