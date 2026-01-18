# Problem: Number of Islands (LeetCode 200) - Classic BFS/DFS Problem
# This is THE most common graph traversal interview question!
# 
# Given a 2D grid of '1's (land) and '0's (water), count the number of islands.
# An island is surrounded by water and formed by connecting adjacent lands
# horizontally or vertically.
#
# Example:
# grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# Output: 3

from collections import deque

# ============== DFS Solution (Recursive) ==============
def numIslands_DFS(grid):
    """
    DFS Approach: When we find a '1', we "sink" the entire island
    by marking all connected land as visited.
    
    Time: O(M * N) where M = rows, N = cols
    Space: O(M * N) worst case for recursion stack
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Base case: out of bounds or water
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited (sink the land)
        grid[r][c] = '0'
        
        # Explore all 4 directions
        dfs(r + 1, c)  # down
        dfs(r - 1, c)  # up
        dfs(r, c + 1)  # right
        dfs(r, c - 1)  # left
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)  # Sink the entire island
    
    return count


# ============== BFS Solution (Iterative with Queue) ==============
def numIslands_BFS(grid):
    """
    BFS Approach: Use a queue to explore level by level.
    Better for finding shortest path, but same result here.
    
    Time: O(M * N)
    Space: O(min(M, N)) for the queue
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark as visited
        
        while queue:
            row, col = queue.popleft()
            # Check all 4 directions
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    queue.append((nr, nc))
                    grid[nr][nc] = '0'  # Mark as visited
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                bfs(r, c)
    
    return count


# ============== Test Cases ==============
if __name__ == "__main__":
    # Test 1: Multiple islands
    grid1 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    print(f"Test 1 (DFS): {numIslands_DFS([row[:] for row in grid1])}")  # Expected: 3
    print(f"Test 1 (BFS): {numIslands_BFS([row[:] for row in grid1])}")  # Expected: 3
    
    # Test 2: Single island
    grid2 = [
        ["1","1","1"],
        ["1","1","1"]
    ]
    print(f"Test 2 (DFS): {numIslands_DFS([row[:] for row in grid2])}")  # Expected: 1
    
    # Test 3: No islands
    grid3 = [["0","0"],["0","0"]]
    print(f"Test 3 (DFS): {numIslands_DFS([row[:] for row in grid3])}")  # Expected: 0


# ============== Interview Tips ==============
"""
🎯 WHEN TO USE BFS vs DFS:
- BFS: Finding SHORTEST PATH (level by level)
- DFS: Exploring all paths, detecting cycles, topological sort

🗣️ TALK THROUGH IT:
"I'll iterate through each cell. When I find land ('1'), I increment 
my island count and then use DFS/BFS to mark all connected land as 
visited so I don't count it again."

⏱️ COMPLEXITY ANALYSIS:
- Time: O(M × N) - we visit each cell at most once
- Space: O(M × N) for DFS recursion stack / O(min(M,N)) for BFS queue

🔗 SRE CONNECTION:
This pattern is used for:
- Service dependency graphs
- Network topology analysis
- Finding connected components in distributed systems
"""
