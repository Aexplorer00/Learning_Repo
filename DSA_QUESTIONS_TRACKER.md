# 🎯 DSA Questions Tracker
## All Problems Solved During 60-Day Journey

---

## Week 1 (Jan 7-10)

### Arrays & Big-O
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Log Analyzer | Array traversal | Easy |

### Hash Maps
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Two Sum | HashMap lookup | Easy |
| 2 | Top K Frequent | Counter + Heap | Medium |

### Binary Search
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Classic Binary Search | Standard | Easy |
| 2 | Search Insert Position | Modified | Easy |
| 3 | First/Last Position | Boundary | Medium |
| 4 | Search Rotated Array | Modified | Medium |

### Sliding Window
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Max Sum Subarray | Fixed Window | Easy |
| 2 | Longest Substring K Distinct | Variable Window | Medium |
| 3 | Smallest Subarray with Sum | Variable Window | Medium |

---

## Week 2 (Jan 11-13)

### Two Pointers (Day 5)
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Reverse Array | Opposite ends | Easy |
| 2 | Two Sum Sorted | Opposite ends | Easy |
| 3 | Remove Duplicates | Same direction | Easy |
| 4 | Move Zeros | Same direction | Easy |
| 5 | Container With Most Water | Opposite ends | Medium |

### Frequency Counting (Day 6)
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Valid Anagram | Counter compare | Easy |
| 2 | Find All Duplicates | Counter > 1 | Easy |
| 3 | First Unique Character | Counter == 1 | Easy |
| 4 | Top K Frequent Elements | Counter.most_common | Medium |
| 5 | Group Anagrams | Sorted key grouping | Medium |

### String Problems (Day 7)
| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Valid Palindrome | Two Pointers | Easy |
| 2 | Valid Anagram | Frequency Counting | Easy |
| 3 | Reverse String | Two Pointers | Easy |
| 4 | Longest Common Prefix | Prefix comparison | Easy |
| 5 | Reverse Words | Split/Reverse/Join | Medium |
| 6 | Is Subsequence | Two Pointers | Easy |

---

## 📊 Summary

| Pattern | Problems | Mastery |
|---------|----------|---------|
| Arrays/Big-O | 1 | ✅ |
| Hash Maps | 2 | ✅ |
| Binary Search | 4 | ✅ |
| Sliding Window | 3 | ✅ |
| Two Pointers | 5 | ✅ |
| Frequency Counting | 5 | ✅ |
| String Problems | 6 | ✅ |
| **Total** | **26** | |

---

## 🎯 Key Patterns Learned

### 1. Two Pointers
```python
left, right = 0, len(arr) - 1
while left < right:
    # process and move pointers
```

### 2. Frequency Counting
```python
from collections import Counter
freq = Counter(arr)
```

### 3. Sliding Window
```python
for right in range(len(arr)):
    # expand window
    while condition:
        # shrink from left
```

### 4. Binary Search
```python
while left <= right:
    mid = (left + right) // 2
    if target: return mid
```

---

*Last Updated: Jan 13, 2026*
