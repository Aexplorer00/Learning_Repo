# ============================================================
# BFS/DFS Template - MEMORIZE THIS!
# ============================================================
# These patterns apply to: graphs, trees, matrices, and any
# connected component problems.

from collections import deque, defaultdict

# ============== BFS TEMPLATE (Breadth-First Search) ==============
def bfs_template(graph, start):
    """
    BFS explores level by level using a QUEUE (FIFO).
    
    USE WHEN:
    - Finding SHORTEST PATH (unweighted graph)
    - Level-order traversal
    - Finding nodes at distance K
    
    Time: O(V + E) where V = vertices, E = edges
    Space: O(V) for visited set and queue
    """
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()  # FIFO - First In, First Out
        print(f"Visiting: {node}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited


# ============== DFS TEMPLATE (Depth-First Search) ==============
def dfs_template_recursive(graph, start, visited=None):
    """
    DFS explores as deep as possible before backtracking.
    Uses RECURSION (implicit stack).
    
    USE WHEN:
    - Detecting cycles
    - Topological sorting
    - Finding all paths
    - Connected components
    
    Time: O(V + E)
    Space: O(V) for visited + O(V) for recursion stack
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(f"Visiting: {start}")
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_template_recursive(graph, neighbor, visited)
    
    return visited


def dfs_template_iterative(graph, start):
    """
    DFS using explicit STACK (LIFO).
    Better for very deep graphs (avoids recursion limit).
    """
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()  # LIFO - Last In, First Out
        
        if node not in visited:
            visited.add(node)
            print(f"Visiting: {node}")
            
            # Add neighbors to stack
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited


# ============== MATRIX BFS/DFS ==============
def matrix_bfs(grid, start_row, start_col):
    """
    BFS on a 2D matrix/grid.
    Common for: Number of Islands, Shortest Path in Maze
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    
    # 4 directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        row, col = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds and visited
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                (new_row, new_col) not in visited and
                grid[new_row][new_col] == 1):  # or whatever condition
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
    
    return visited


# ============== SHORTEST PATH BFS ==============
def shortest_path_bfs(graph, start, end):
    """
    Find shortest path between two nodes.
    Returns the path length (-1 if no path exists).
    """
    if start == end:
        return 0
    
    visited = set([start])
    queue = deque([(start, 0)])  # (node, distance)
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found


# ============== Test with Sample Graph ==============
if __name__ == "__main__":
    # Sample graph (adjacency list)
    graph = defaultdict(list)
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 5)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    print("=== BFS from node 1 ===")
    bfs_template(graph, 1)
    
    print("\n=== DFS (Recursive) from node 1 ===")
    dfs_template_recursive(graph, 1)
    
    print("\n=== DFS (Iterative) from node 1 ===")
    dfs_template_iterative(graph, 1)
    
    print(f"\n=== Shortest path 1 -> 5 ===")
    print(f"Distance: {shortest_path_bfs(graph, 1, 5)}")


# ============== CHEAT SHEET ==============
"""
┌─────────────────────────────────────────────────────────────┐
│                    BFS vs DFS Cheat Sheet                   │
├─────────────────┬───────────────────┬───────────────────────┤
│                 │       BFS         │         DFS           │
├─────────────────┼───────────────────┼───────────────────────┤
│ Data Structure  │ Queue (deque)     │ Stack (or recursion)  │
│ Order           │ FIFO              │ LIFO                  │
│ Explores        │ Level by level    │ As deep as possible   │
│ Shortest Path   │ ✅ YES            │ ❌ NO                 │
│ Memory          │ O(width of tree)  │ O(depth of tree)      │
│ Use Cases       │ Shortest path,    │ Cycle detection,      │
│                 │ level order       │ topological sort,     │
│                 │                   │ all paths             │
└─────────────────┴───────────────────┴───────────────────────┘

🎯 DECISION TREE:
Q: Do I need the SHORTEST path?
   → YES: Use BFS
   → NO: Either works, DFS is often simpler

Q: Am I exploring a TREE or GRAPH?
   → TREE: No need for visited set (no cycles)
   → GRAPH: ALWAYS use visited set!

⚠️ COMMON MISTAKES:
1. Forgetting to mark as visited BEFORE adding to queue (BFS)
2. Not checking bounds in matrix problems
3. Modifying the graph while traversing
"""
