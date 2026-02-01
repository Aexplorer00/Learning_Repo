# 🔥 BFS & DFS Crash Course

**Learn these in 3 days for your HackerRank assessment!**

---

## What Are They?

Both are ways to **traverse/search** through:
- **Graphs** (nodes connected by edges)
- **Trees** (hierarchical structure)
- **2D Grids** (like a matrix/map)

---

## BFS (Breadth-First Search)

### Concept
- Explore **level by level** (all neighbors first, then their neighbors)
- Uses a **QUEUE** (FIFO - First In, First Out)
- Like ripples in water - spreads outward

### When to Use
- **Shortest path** in unweighted graph
- Level-order traversal
- Finding nearest X

### Template (Python)
```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = set([start])
    
    while queue:
        node = queue.popleft()  # Take from front
        print(node)  # Process node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Add to back
```

### Visual
```
    1
   / \
  2   3
 / \
4   5

BFS Order: 1 → 2 → 3 → 4 → 5 (level by level)
```

---

## DFS (Depth-First Search)

### Concept
- Explore **as deep as possible** before backtracking
- Uses a **STACK** (LIFO - Last In, First Out) OR **Recursion**
- Like going down a maze - go deep, then backtrack

### When to Use
- **Explore all paths**
- Check if path exists
- Cycle detection
- Tree traversals

### Template (Python - Recursive)
```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    print(node)  # Process node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### Template (Python - Iterative with Stack)
```python
def dfs_iterative(graph, start):
    stack = [start]
    visited = set()
    
    while stack:
        node = stack.pop()  # Take from top
        if node not in visited:
            visited.add(node)
            print(node)  # Process node
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
```

### Visual
```
    1
   / \
  2   3
 / \
4   5

DFS Order: 1 → 2 → 4 → 5 → 3 (go deep first)
```

---

## BFS vs DFS Comparison

| Aspect | BFS | DFS |
|--------|-----|-----|
| Data Structure | Queue | Stack/Recursion |
| Order | Level by level | Deep then backtrack |
| Best For | Shortest path | Explore all paths |
| Memory | More (stores all level nodes) | Less (only current path) |

---

## Most Common Problem: Number of Islands

**Problem:** Given a 2D grid of '1's (land) and '0's (water), count the number of islands.

```
Grid:
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Answer: 3 islands
```

### Solution (DFS)
```python
def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Out of bounds or water
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        grid[r][c] = '0'  # Mark as visited
        
        # Check all 4 directions
        dfs(r + 1, c)  # Down
        dfs(r - 1, c)  # Up
        dfs(r, c + 1)  # Right
        dfs(r, c - 1)  # Left
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)  # Sink the entire island
    
    return count
```

---

## Practice Problems (Do These!)

### Day 1 - Basics
1. **Number of Islands** (LeetCode 200) - MUST DO
2. **Flood Fill** (LeetCode 733) - Easy
3. **Max Area of Island** (LeetCode 695)

### Day 2 - BFS
4. **Shortest Path in Binary Matrix** (LeetCode 1091)
5. **Rotting Oranges** (LeetCode 994)
6. **Word Ladder** (LeetCode 127)

### Day 3 - Graph Problems
7. **Clone Graph** (LeetCode 133)
8. **Course Schedule** (LeetCode 207) - Cycle detection
9. **Pacific Atlantic Water Flow** (LeetCode 417)

---

## Key Patterns for HackerRank

### Pattern 1: Grid Traversal
```python
# 4 directions
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

for dr, dc in directions:
    new_r, new_c = r + dr, c + dc
    if 0 <= new_r < rows and 0 <= new_c < cols:
        # valid cell
```

### Pattern 2: Track Visited
```python
visited = set()
# OR modify grid in place: grid[r][c] = '#'
```

### Pattern 3: BFS for Shortest Path
```python
queue = deque([(start, 0)])  # (node, distance)
while queue:
    node, dist = queue.popleft()
    if node == target:
        return dist
```

---

## Time Complexity
- Both BFS and DFS: **O(V + E)** for graph
- For grid (m x n): **O(m × n)**

---

*Complete "Number of Islands" today - it's the #1 BFS/DFS interview question!*
