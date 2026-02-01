# 🔗 Linked List DSA Guide

**Fundamentals + Common Interview Problems**

---

# Part 1: What is a Linked List?

## Concept
A sequence of **nodes** where each node points to the next.

```
Head
  ↓
┌─────┬───┐   ┌─────┬───┐   ┌─────┬───┐
│  1  │ ●─┼──→│  2  │ ●─┼──→│  3  │ / │
└─────┴───┘   └─────┴───┘   └─────┴───┘
  val  next     val  next     val  next(null)
```

---

## Array vs Linked List

| Operation | Array | Linked List |
|-----------|-------|-------------|
| Access by index | O(1) ✅ | O(n) ❌ |
| Insert at beginning | O(n) ❌ | O(1) ✅ |
| Insert at end | O(1)* | O(n) or O(1) with tail |
| Delete | O(n) | O(1) if have reference |
| Memory | Contiguous | Scattered |

**Use Linked List when:** Many insertions/deletions, unknown size

---

## Python Node Definition

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Create: 1 → 2 → 3
node3 = ListNode(3)
node2 = ListNode(2, node3)
head = ListNode(1, node2)
```

---

# Part 2: Basic Operations

## Traverse (Print all values)

```python
def print_list(head):
    current = head
    while current:
        print(current.val, end=" → ")
        current = current.next
    print("None")
```

## Count Length

```python
def length(head):
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count
```

## Search for Value

```python
def search(head, target):
    current = head
    while current:
        if current.val == target:
            return True
        current = current.next
    return False
```

---

# Part 3: Reverse Linked List ⭐ (MUST KNOW!)

## Problem
Reverse a linked list.
```
Input:  1 → 2 → 3 → 4 → 5
Output: 5 → 4 → 3 → 2 → 1
```

## Key Insight
We need 3 pointers: prev, current, next

```
Before:  1 → 2 → 3
After:   1 ← 2 ← 3 (reverse arrows)
```

## Solution

```python
def reverseList(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # Save next
        current.next = prev       # Reverse arrow
        prev = current            # Move prev forward
        current = next_temp       # Move current forward
    
    return prev  # prev is new head
```

## Visual Step-by-Step

```
Initial: prev=None, curr=1
         None  1 → 2 → 3
         prev  curr

Step 1: Reverse 1's pointer
         None ← 1    2 → 3
               prev  curr

Step 2: Reverse 2's pointer
         None ← 1 ← 2    3
                    prev curr

Step 3: Reverse 3's pointer
         None ← 1 ← 2 ← 3    None
                         prev curr

Return prev (which is 3, the new head)
```

---

# Part 4: Detect Cycle (Fast-Slow Pointer)

## Problem
Detect if a linked list has a cycle.

```
1 → 2 → 3 → 4
        ↑   ↓
        └───┘  (cycle at 3-4)
```

## Key Insight: Tortoise and Hare
- **Slow pointer:** moves 1 step
- **Fast pointer:** moves 2 steps
- If there's a cycle, they WILL meet!

## Solution

```python
def hasCycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next       # Move 1 step
        fast = fast.next.next  # Move 2 steps
        
        if slow == fast:
            return True  # They met - cycle exists!
    
    return False  # Fast reached end - no cycle
```

## Why Does This Work?
In a cycle, the fast pointer "catches up" to slow by 1 step each iteration.

---

# Part 5: Find Middle of Linked List

## Problem
Find the middle node.
```
1 → 2 → 3 → 4 → 5
        ↑
      middle
```

## Solution (Fast-Slow Pointer)

```python
def middleNode(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow  # When fast reaches end, slow is at middle
```

## Why It Works
Fast moves 2x speed. When fast finishes, slow is at halfway.

---

# Part 6: Merge Two Sorted Lists

## Problem
Merge two sorted linked lists.
```
List 1: 1 → 2 → 4
List 2: 1 → 3 → 4
Result: 1 → 1 → 2 → 3 → 4 → 4
```

## Solution

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)  # Dummy head
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = list1 if list1 else list2
    
    return dummy.next  # Skip dummy
```

---

# Part 7: Common Patterns

## 1. Dummy Node Pattern
Use a dummy head when building a new list.
```python
dummy = ListNode(0)
current = dummy
# ... build list ...
return dummy.next
```

## 2. Two Pointer Pattern
- **Fast-Slow:** Find middle, detect cycle
- **Two lists:** Merge, compare

## 3. Reverse Pattern
Always need: prev, current, next_temp

---

# Summary: Interview Cheat Sheet

| Problem | Pattern | Time |
|---------|---------|------|
| **Reverse List** | prev, curr, next | O(n) |
| **Detect Cycle** | Fast-slow pointer | O(n) |
| **Find Middle** | Fast-slow pointer | O(n) |
| **Merge Sorted** | Two pointers + dummy | O(n+m) |
| **Remove Nth from End** | Fast ahead by n | O(n) |

---

## SRE Connection

- **Log streams:** Processing sequential data
- **Event queues:** Add/remove from ends
- **Service chains:** Request → Service A → B → C

---

*Next: Practice reversing a list by hand!*
