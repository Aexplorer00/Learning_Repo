# Problem: Top K Frequent Elements (LeetCode 347)
# Given an integer array nums and an integer k, return the k most frequent elements.
#
# Example:
# Input: nums = [1,1,1,2,2,3], k = 2
# Output: [1,2] (1 appears 3 times, 2 appears 2 times)
#
# This is VERY relevant for SRE - think about:
# - Top K error codes in logs
# - Most frequent API endpoints
# - Hottest cache keys

import heapq
from collections import Counter

# ============== Solution 1: Using Heap (Min-Heap) ==============
def topKFrequent_heap(nums, k):
    """
    Use a min-heap of size k to keep track of top k elements.
    
    Time: O(N log K) - N elements, heap operations are log K
    Space: O(N) for the counter + O(K) for the heap
    """
    # Count frequencies
    count = Counter(nums)
    
    # Use min-heap with size k
    # heapq in Python is min-heap, so we push (frequency, num)
    # When heap size exceeds k, we pop the smallest frequency
    return heapq.nlargest(k, count.keys(), key=count.get)


# ============== Solution 2: Bucket Sort (Optimal) ==============
def topKFrequent_bucket(nums, k):
    """
    Bucket sort approach - O(N) time!
    Create buckets where index = frequency, value = list of numbers
    
    Time: O(N)
    Space: O(N)
    """
    count = Counter(nums)
    
    # Create buckets: index represents frequency
    # Max frequency possible is len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect top k from highest frequency buckets
    result = []
    for i in range(len(buckets) - 1, 0, -1):  # Start from highest frequency
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result


# ============== Solution 3: Quick Select (Advanced) ==============
# This is O(N) average case but more complex - skip for interviews unless asked


# ============== Test Cases ==============
if __name__ == "__main__":
    # Test 1
    nums1 = [1, 1, 1, 2, 2, 3]
    k1 = 2
    print(f"Test 1 (Heap): {topKFrequent_heap(nums1, k1)}")    # [1, 2]
    print(f"Test 1 (Bucket): {topKFrequent_bucket(nums1, k1)}")  # [1, 2]
    
    # Test 2: Single element
    nums2 = [1]
    k2 = 1
    print(f"Test 2: {topKFrequent_heap(nums2, k2)}")  # [1]
    
    # Test 3: All same frequency
    nums3 = [1, 2, 3, 4]
    k3 = 2
    print(f"Test 3: {topKFrequent_heap(nums3, k3)}")  # Any 2 elements
    
    # SRE Example: Top error codes
    error_codes = [500, 404, 500, 500, 503, 404, 500, 502, 404]
    print(f"Top 2 error codes: {topKFrequent_heap(error_codes, 2)}")  # [500, 404]


# ============== Interview Tips ==============
"""
🎯 HEAP PATTERN:
- "Top K" problems → Think HEAP
- Min-heap of size K for top K largest
- Max-heap (negate values) for top K smallest

🗣️ EXPLAIN YOUR CHOICE:
"I'll use a heap because we need the top K elements efficiently.
A min-heap of size K gives us O(N log K) time, which is better
than sorting O(N log N) when K << N."

⏱️ COMPLEXITY COMPARISON:
| Approach      | Time      | Space |
|---------------|-----------|-------|
| Sorting       | O(N log N)| O(N)  |
| Heap          | O(N log K)| O(N)  |
| Bucket Sort   | O(N)      | O(N)  |

🔗 SRE USE CASES:
- Finding top K slow queries
- Most frequent error codes in logs
- Hottest cache keys
- Most active users/IPs (rate limiting)
"""
